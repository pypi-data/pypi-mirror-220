import time
from typing import cast

import requests
from django.db import IntegrityError

from sentry.api.invite_helper import ApiInviteHelper
from sentry.auth.exceptions import IdentityNotValid
from sentry.auth.helper import AuthIdentityHandler
from sentry.auth.provider import MigratingIdentityId
from sentry.auth.providers.oauth2 import OAuth2Callback, OAuth2Login, OAuth2Provider
from sentry.models import identity, organization
from sentry.models.authidentity import AuthIdentity
from sentry.models.organizationmember import OrganizationMember
from sentry.models.user import User
from sentry.utils import auth

from .constants import (
    AUTHORIZATION_ENDPOINT,
    CLIENT_ID,
    CLIENT_SECRET,
    DATA_VERSION,
    ISSUER,
    SCOPE,
    TOKEN_ENDPOINT,
    USER_ID,
    USERINFO_ENDPOINT,
)
from .views import FetchUser, OIDCConfigureView


class OIDCLogin(OAuth2Login):
    authorize_url = AUTHORIZATION_ENDPOINT
    client_id = CLIENT_ID
    scope = SCOPE

    def __init__(self, client_id, domains=None):
        self.domains = domains
        super().__init__(client_id=client_id)

    def get_authorize_params(self, state, redirect_uri):
        params = super().get_authorize_params(state, redirect_uri)
        # TODO(dcramer): ideally we could look at the current resulting state
        # when an existing auth happens, and if they're missing a refresh_token
        # we should re-prompt them a second time with ``approval_prompt=force``
        params["approval_prompt"] = "force"
        params["access_type"] = "offline"
        return params


class OIDCProvider(OAuth2Provider):
    name = ISSUER
    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET

    def __init__(self, domain=None, domains=None, version=None, **config):
        if domain:
            if domains:
                domains.append(domain)
            else:
                domains = [domain]
        self.domains = domains
        # if a domain is not configured this is part of the setup pipeline
        # this is a bit complex in Sentry's SSO implementation as we don't
        # provide a great way to get initial state for new setup pipelines
        # vs missing state in case of migrations.
        if domains is None:
            version = DATA_VERSION
        else:
            version = None
        self.version = version
        super().__init__(**config)

    def get_configure_view(self):
        return OIDCConfigureView.as_view()

    def get_auth_pipeline(self):
        return [
            OIDCLogin(self.client_id, domains=self.domains),
            OAuth2Callback(
                access_token_url=TOKEN_ENDPOINT,
                client_id=self.client_id,
                client_secret=self.client_secret,
            ),
            FetchUser(
                domains=self.domains,
                version=self.version,
            ),
        ]

    def get_refresh_token_url(self):
        return TOKEN_ENDPOINT

    def build_config(self, state):
        return {
            "domains": [state["domain"]],
            "version": DATA_VERSION,
        }

    def get_user_info(self, bearer_token):
        endpoint = USERINFO_ENDPOINT
        bearer_auth = "Bearer " + bearer_token
        retry_codes = [429, 500, 502, 503, 504]
        for retry in range(10):
            if 10 < retry:
                return {}
            r = requests.get(
                endpoint + "?schema=openid",
                headers={"Authorization": bearer_auth},
                timeout=2.0,
            )
            if r.status_code in retry_codes:
                wait_time = 2**retry * 0.1
                time.sleep(wait_time)
                continue
            return r.json()

    def build_identity(self, state):
        data = state["data"]
        user_data = state["user"]
        # self.update_identity()

        bearer_token = data["access_token"]
        user_info = self.get_user_info(bearer_token)

        # XXX(epurkhiser): We initially were using the email as the id key.
        # This caused account dupes on domain changes. Migrate to the
        # account-unique sub key.
        user_id = user_data[USER_ID]
        identity = {
            "id": user_id,
            "email": user_info.get("email"),
            "name": user_info.get("name"),
            "data": self.get_oauth_data(data),
            "email_verified": True,
        }
        auth_handler = cast(AuthIdentityHandler, self.pipeline.auth_handler(identity))
        try:
            user = User.objects.get(username=identity["id"])
        except (User.DoesNotExist, ValueError):
            user = None

        if user is None:
            user = User.objects.create(
                username=identity["id"],
                email=identity["email"],
                name=identity["name"],
                is_managed=True,
                # is_superuser=True,
                # is_staff=True,
            )
            unverified = user.get_unverified_emails()
            for email in unverified:
                email.is_verified = True
                email.save()
        unverified = user.get_unverified_emails()
        for email in unverified:
            email.is_verified = True
            email.save()
        # else:
        #    user = auth_handler.user

        # if user.has_unverified_emails():

        # auth_identity = AuthIdentity.objects.get(
        #    auth_provider=auth_handler.auth_provider, user=user.id
        # )
        auth_identity = auth_handler._get_auth_identity(ident=identity["id"])
        # AuthIdentity.objects.all()
        if auth_identity is None:
            allowed = False
            if user.is_superuser:
                allowed = True
            else:
                try:
                    om = OrganizationMember.objects.get(
                        email=identity["email"],
                        organization=self.pipeline.organization
                        # , user=None
                    )
                    allowed = True
                except OrganizationMember.DoesNotExist:
                    if self.pipeline.organization.slug == "public":
                        allowed = True
                    else:
                        raise IdentityNotValid("No access to selected organization " + str(self.pipeline.organization))
            if allowed:
                if not auth_handler.auth_provider is None:
                    auth_identity = AuthIdentity.objects.create(
                        auth_provider=auth_handler.auth_provider,
                        user=user,
                        ident=identity["id"],
                        data=identity["data"],
                    )
        # auth_handler.user.delete()
        # if not auth_handler.user.is_superuser:
        #    auth_handler.user.delete()
        return identity
