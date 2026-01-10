from social_core.backends.oauth import BaseOAuth2


class NEIROAuth2(BaseOAuth2):
    name = "neir"

    def authorization_url(self):
        return self.setting("AUTHORIZATION_URL")

    def access_token_url(self):
        return self.setting("ACCESS_TOKEN_URL")

    def user_data(self, access_token, *args, **kwargs):
        url = self.setting("USERINFO_URL")
        return self.get_json(
            url,
            headers={"Authorization": f"Bearer {access_token}"},
        )

    # 🔴 THIS WAS MISSING IN OUR EARLIER BUILD (CRITICAL)......................
    def get_user_id(self, details, response):
        """
        Return a UNIQUE and STABLE user identifier.
        Open edX requires this, otherwise authentication is canceled.
        """
        return response.get("sub")

    def get_user_details(self, response):
        name = (response.get("name") or "").strip()
        parts = name.split(" ", 1) if name else ["", ""]

        sub = response.get("sub")
        email = response.get("email")

        return {
            "email": email or "",
            "fullname": name,
            "first_name": parts[0],
            "last_name": parts[1] if len(parts) > 1 else "",
        }
