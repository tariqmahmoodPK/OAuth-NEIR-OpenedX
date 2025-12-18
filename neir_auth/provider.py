from openedx.core.djangoapps.third_party_auth.provider import (
    BaseOAuth2ProviderConfig
)

class NEIRProviderConfig(BaseOAuth2ProviderConfig):
    """
    Third-Party Auth provider configuration for NEIR
    (Google-like: available to all users)
    """

    provider_id = "neir"
    backend_name = "neir"
    verbose_name = "NEIR"
    description = "Login using NEIR SSO"

    def get_icon_class(self):
        return "fa-sign-in"
