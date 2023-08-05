"""Common utilities shared by any e-mail related library."""


import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional, Union

import jwt

from RPA.MFA import MFA


lib_mfa = MFA()

OAuthProviderType = Union["OAuthProvider", str]


class NoRecipientsError(ValueError):
    """Raised when email to be sent does not have any recipients, cc or bcc addresses."""  # noqa: E501


class OAuthProvider(Enum):
    """OAuth2 tested providers."""

    GOOGLE = "google"
    MICROSOFT = "microsoft"


@dataclass
class OAuthConfig:
    """OAuth2 Authorization Code Flow provider settings."""

    auth_url: str
    redirect_uri: str
    scope: str
    token_url: str


OAUTH_PROVIDERS = {
    OAuthProvider.GOOGLE: OAuthConfig(
        auth_url="https://accounts.google.com/o/oauth2/auth",
        redirect_uri="https://developers.google.com/oauthplayground",
        scope="https://mail.google.com",
        token_url="https://accounts.google.com/o/oauth2/token",
    ),
    OAuthProvider.MICROSOFT: OAuthConfig(
        auth_url="https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize",
        redirect_uri="https://login.microsoftonline.com/common/oauth2/nativeclient",
        scope="offline_access https://outlook.office365.com/.default",
        token_url="https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token",
    ),
}


class OAuthMixin:
    """Common keywords for the Email libraries, enabling OAuth2 support."""

    TO_PROTECT = ["get_oauth_token", "refresh_oauth_token"]

    def __init__(self, provider: OAuthProviderType, tenant: Optional[str]):
        self._oauth_provider = OAUTH_PROVIDERS[OAuthProvider(provider)]
        if tenant:
            for url_attr in ("auth_url", "redirect_uri", "token_url"):
                formatted = getattr(self._oauth_provider, url_attr).format(
                    tenant=tenant
                )
                setattr(self._oauth_provider, url_attr, formatted)
        # NOTE(cmin764):
        #  https://github.com/requests/requests-oauthlib/issues/387#issuecomment-1325131664
        os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

    def generate_oauth_url(self, client_id: str) -> str:
        """Generates an authorization URL which must be opened by the user to start the
        OAuth2 flow and obtain an authorization code as response.

        :param client_id: Client app ID. (generated by the provider)
        :returns: Authorization URL string not containing any sensitive info in it.

        **Example: Robot Framework**

        .. code-block:: robotframework

            *** Tasks ***
            Start OAuth Flow
                ${auth_url} =    Generate OAuth URL
                ...     client_id=810482312368-19htmcgcj*******googleusercontent.com
                Log     Start OAuth2 flow: ${auth_url}
        """
        return lib_mfa.generate_oauth_url(
            self._oauth_provider.auth_url,
            client_id=client_id,
            redirect_uri=self._oauth_provider.redirect_uri,
            scope=self._oauth_provider.scope,
            access_type="offline",
            prompt="consent",
        )

    def _sync_token_metadata(self, token: dict):
        # Ensures that the issued expiry time in the access token is in sync with the
        #  one we have stored in the token dictionary. So `exchangelib` will know for
        #  sure when to refresh a potentially expired token.
        try:
            access_token = jwt.decode(
                token["access_token"], options={"verify_signature": False}
            )
        except jwt.exceptions.DecodeError:
            # Logger object declared in every derived class.
            self.logger.debug("Couldn't decode access token or token isn't valid JWT")
        else:
            token["expires_at"] = access_token["exp"]

    def get_oauth_token(self, client_secret: str, response_url: str) -> dict:
        """Exchanges the code obtained previously with ``Generate OAuth URL`` for a
        token.

        :param client_secret: Client app secret. (generated by the provider)
        :param response_url: The final URL containing the authorization `code` found in
            the address bar after authenticating and authorizing the Client app
            through the authorization URL.
        :returns: A dictionary containing the access & refresh token, plus metadata.

        **Example: Robot Framework**

        .. code-block:: robotframework

            *** Tasks ***
            Finish OAuth Flow
                ${token} =      Get OAuth Token
                ...     client_secret=GOCSPX-******mqZAW89
                ...     response_url=${resp_url}  # redirect of `Generate OAuth URL`
        """
        token = lib_mfa.get_oauth_token(
            self._oauth_provider.token_url,
            client_secret=client_secret,
            response_url=response_url,
            include_client_id=True,
        )
        self._sync_token_metadata(token)
        return token

    def refresh_oauth_token(
        self, client_id: str, client_secret: str, token: dict
    ) -> dict:
        """Refreshes the token as the access one usually expires after 1h and the
        refresh one never expires. (as long as it doesn't get revoked)

        :param client_id: Client app ID. (generated by the provider)
        :param client_secret: Client app secret. (generated by the provider)
        :param token: Full token dictionary previously obtained with
            ``Get OAuth Token``.
        :returns: A token dictionary containing a new access token and updated
            metadata.

        **Example: Robot Framework**

        .. code-block:: robotframework

            *** Tasks ***
            Refresh OAuth Flow
                ${token} =      Refresh OAuth Token
                ...     client_id=810482312368-19htmcgcj*******googleusercontent.com
                ...     client_secret=GOCSPX-******mqZAW89
                ...     token=${token}  # from `Get OAuth Token`
        """
        token = lib_mfa.refresh_oauth_token(
            self._oauth_provider.token_url,
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=token["refresh_token"],
        )
        self._sync_token_metadata(token)
        return token


def counter_duplicate_path(file_path: Path) -> Path:
    """Returns a unique file path by adding a suffixed counter if already exists."""
    if not file_path.exists():
        return file_path  # unique already

    root_dir = file_path.parent
    duplicates = root_dir.glob(f"{file_path.stem}*{file_path.suffix}")
    suffixes = []
    for dup in duplicates:
        parts = dup.stem.rsplit("-", 1)
        if len(parts) == 2 and parts[1].isdigit():
            suffixes.append(int(parts[1]))
    next_suffix = max(suffixes) + 1 if suffixes else 2

    file_path = root_dir / f"{file_path.stem}-{next_suffix}{file_path.suffix}"
    return file_path
