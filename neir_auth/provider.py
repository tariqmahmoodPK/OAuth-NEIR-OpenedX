from third_party_auth.provider import BaseOAuth2Provider, Registry
from openedx.core.djangoapps.third_party_auth.provider import (
    BaseOAuth2ProviderConfig
)


# 1️⃣ REAL PROVIDER (this creates the login button)
class NEIRProvider(BaseOAuth2Provider):
    id = "neir"
    name = "NEIR"

    def get_display_name(self, request):
        return "Login with NEIR"

    def get_icon_class(self):
        return "fa-sign-in"


# 2️⃣ PROVIDER CONFIG (used by Django admin)
class NEIRProviderConfig(BaseOAuth2ProviderConfig):
    provider_id = "neir"
    backend_name = "neir"
    verbose_name = "NEIR"
    description = "Login using NEIR SSO"


# 3️⃣ CRITICAL: register provider at import time
Registry.register(NEIRProvider)
