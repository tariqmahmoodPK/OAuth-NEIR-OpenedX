import requests
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import AuthFailed


class NEIROAuth2(BaseOAuth2):
    """
    Custom OAuth2 backend for NEIR (Authorization Code flow).
    Works with:
      - Authorization URL
      - Token URL
      - UserInfo URL (Bearer token)
    """
    name = "neir"

    # Default scope (can be overridden by SOCIAL_AUTH_NEIR_SCOPE)
    DEFAULT_SCOPE = ["openid", "email", "profile"]
    SCOPE_SEPARATOR = " "

    # Token response fields to store (optional)
    EXTRA_DATA = [
        ("refresh_token", "refresh_token"),
        ("expires_in", "expires_in"),
        ("token_type", "token_type"),
    ]

    def authorization_url(self):
        return self.setting("AUTHORIZATION_URL")

    def access_token_url(self):
        return self.setting("ACCESS_TOKEN_URL")

    def get_userinfo_url(self):
        return self.setting("USERINFO_URL")

    def user_data(self, access_token, *args, **kwargs):
        """
        Fetch user identity from NEIR using Bearer token.
        """
        url = self.get_userinfo_url()
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }
        resp = requests.get(url, headers=headers, timeout=20)
        if resp.status_code != 200:
            raise AuthFailed(self, f"NEIR userinfo failed ({resp.status_code}): {resp.text[:200]}")
        try:
            return resp.json()
        except Exception as e:
            raise AuthFailed(self, f"NEIR userinfo invalid JSON: {e}")

    def get_user_details(self, response):
        """
        Map NEIR claims into Open edX user fields.
        Response expected:
          { "sub": "...", "email": "...", "name": "...", "email_verified": true }
        """
        email = response.get("email")
        sub = response.get("sub")
        name = response.get("name") or ""

        if not sub:
            raise AuthFailed(self, "NEIR userinfo missing 'sub'")
        if not email:
            raise AuthFailed(self, "NEIR userinfo missing 'email'")

        first_name = name
        last_name = ""
        if name and " " in name:
            parts = name.split()
            first_name = parts[0]
            last_name = " ".join(parts[1:])

        return {
            "username": sub,      # we use sub as stable username key
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "fullname": name,
        }

    def get_user_id(self, details, response):
        # stable unique id for linking
        return response.get("sub") or details.get("username")
