from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import AuthFailed
import logging

log = logging.getLogger(__name__)


class NEIROAuth2(BaseOAuth2):
    name = "neir"

    DEFAULT_SCOPE = ["openid", "email", "profile"]
    SCOPE_SEPARATOR = " "

    def authorization_url(self):
        return self.setting("AUTHORIZATION_URL")

    def access_token_url(self):
        return self.setting("ACCESS_TOKEN_URL")

    def get_user_id(self, details, response):
        log.error("NEIR get_user_id response=%s", response)

        sub = response.get("sub")
        if not sub:
            raise AuthFailed(self, "NEIR response missing 'sub'")
        return str(sub)

    def user_data(self, access_token, *args, **kwargs):
        url = self.setting("USERINFO_URL")
        log.error("NEIR userinfo URL=%s", url)

        response = self.get_json(
            url,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            },
        )

        log.error("NEIR userinfo raw response=%s", response)
        return response

    def get_user_details(self, response):
        log.error("NEIR get_user_details response=%s", response)

        email = (response.get("email") or "").strip().lower()
        sub = (response.get("sub") or "").strip()
        name = (response.get("name") or "").strip()

        if not sub:
            raise AuthFailed(self, "NEIR userinfo missing 'sub'")
        if not email:
            raise AuthFailed(self, "NEIR userinfo missing 'email'")

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
