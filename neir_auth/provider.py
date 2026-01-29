from common.djangoapps.third_party_auth.provider import BaseOAuth2Provider, Registry
from openedx.core.djangoapps.third_party_auth.provider import BaseOAuth2ProviderConfig


class NEIRProvider(BaseOAuth2Provider):
    """
    Provider that creates the login button and describes how auth should flow.
    """
    id = "oa2-neir"
    name = "NEIR"

    def get_display_name(self, request):
        return "Login with NEIR"

    def get_icon_class(self):
        return "fa-sign-in"

    def get_authentication_flow(self, request):
        """
        CRITICAL for Teak + MFEs.
        Without an explicit flow here, Teak can cancel auth early with
        'Authentication process canceled' before the backend runs.
        """
        return {"type": "redirect"}


class NEIRProviderConfig(BaseOAuth2ProviderConfig):
    """
    Provider config for Django Admin (Third-Party Auth).
    """
    provider_id = "oa2-neir"
    backend_name = "neir"
    verbose_name = "NEIR"
    description = "Login using NEIR SSO"


# Register provider at import time
Registry.register(NEIRProvider)
