import logging

from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import AuthFailed

log = logging.getLogger(__name__)


class NEIROAuth2(BaseOAuth2):
    """
    NEIR OAuth2 / OIDC-ish backend for Open edX (Tutor/Teak).

    Required settings (in LMS settings):
      SOCIAL_AUTH_NEIR_AUTHORIZATION_URL
      SOCIAL_AUTH_NEIR_ACCESS_TOKEN_URL
      SOCIAL_AUTH_NEIR_USERINFO_URL
      SOCIAL_AUTH_NEIR_KEY
      SOCIAL_AUTH_NEIR_SECRET
    """

    name = "neir"

    DEFAULT_SCOPE = ["openid", "email", "profile"]
    SCOPE_SEPARATOR = " "

    # Be explicit for compatibility
    ACCESS_TOKEN_METHOD = "POST"

    # Persist useful fields into social-auth extra_data
    EXTRA_DATA = [
        ("sub", "sub"),
        ("email", "email"),
        ("name", "name"),
    ]

    def request_access_token(self, url, data, headers, *args, **kwargs):
    log.error("NEIR token request URL=%s", url)
    log.error("NEIR token request DATA=%s", data)

    data = data.copy()
    data["client_id"] = self.key
    data["client_secret"] = self.secret

    return self.request(
        url,
        method="POST",
        data=data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
    )
        
    def authorization_url(self):
        return self.setting("AUTHORIZATION_URL")

    def access_token_url(self):
        return self.setting("ACCESS_TOKEN_URL")

    def get_user_id(self, details, response):
        """
        Value becomes UserSocialAuth.uid - must be stable and non-empty.
        """
        log.error("NEIR get_user_id response=%s", response)

        sub = response.get("sub")
        if not sub:
            raise AuthFailed(self, "NEIR response missing 'sub'")
        return str(sub)

    def user_data(self, access_token, *args, **kwargs):
        """
        Fetch user claims from NEIR userinfo endpoint.
        """
        url = self.setting("USERINFO_URL")
        log.error("NEIR userinfo URL=%s", url)

        data = self.get_json(
            url,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            },
        )

        log.error("NEIR userinfo raw response=%s", data)
        return data

    def get_user_details(self, response):
        """
        Map NEIR claims → Open edX user fields.
        """
        log.error("NEIR get_user_details response=%s", response)

        email = (response.get("email") or "").strip().lower()
        sub = (response.get("sub") or "").strip()
        name = (response.get("name") or "").strip()

        if not sub:
            raise AuthFailed(self, "NEIR userinfo missing 'sub'")
        if not email:
            raise AuthFailed(self, "NEIR userinfo missing 'email'")

        # IMPORTANT: username must not be numeric-only
        username = f"neir_{sub}"

        first_name = ""
        last_name = ""
        if name:
            parts = name.split(" ", 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ""

        return {
            "username": username,
            "email": email,
            "fullname": name,
            "first_name": first_name,
            "last_name": last_name,
        }
