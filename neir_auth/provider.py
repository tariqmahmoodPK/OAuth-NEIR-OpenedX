from common.djangoapps.third_party_auth.provider import (
    BaseOAuth2Provider,
    Registry,
    BaseOAuth2ProviderConfig,
)


# 1️⃣ REAL PROVIDER (creates login button)
class NEIRProvider(BaseOAuth2Provider):
    id = "oa2-neir"
    name = "NEIR"

    def get_display_name(self, request):
        return "Login with NEIR"

    def get_icon_class(self):
        return "fa-sign-in"


# 2️⃣ PROVIDER CONFIG (used by Django admin)
class NEIRProviderConfig(BaseOAuth2ProviderConfig):
    provider_id = "oa2-neir"
    backend_name = "neir"
    verbose_name = "NEIR"
    description = "Login using NEIR SSO"


# 3️⃣ Register provider at import time (CRITICAL)
Registry.register(NEIRProvider)
