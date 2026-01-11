from social_core.backends.oauth import BaseOAuth2


class NEIROAuth2(BaseOAuth2):
    name = "neir"

    def authorization_url(self):
        return self.setting("AUTHORIZATION_URL")

    def access_token_url(self):
        return self.setting("ACCESS_TOKEN_URL")

    def get_user_id(self, details, response):
        """
        CRITICAL:
        This value becomes UserSocialAuth.uid.
        If it is None/empty, Open edX will never create the social association.
        """
        sub = response.get("sub")
        return str(sub) if sub else None

    def user_data(self, access_token, *args, **kwargs):
        url = self.setting("USERINFO_URL")
        return self.get_json(
            url,
            headers={"Authorization": f"Bearer {access_token}"},
        )
    def get_user_details(self, response):
    """
    Open edX–safe user mapping for NEIR
    """
    email = (response.get("email") or "").strip().lower()
    sub = (response.get("sub") or "").strip()
    name = (response.get("name") or "").strip()

    # REQUIRED: username must NOT be numeric-only
    username = f"neir_{sub}" if sub else ""

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
