'''
from common.djangoapps.third_party_auth.provider import (
    BaseOAuth2Provider,
    Registry,
)
from openedx.core.djangoapps.third_party_auth.provider import (
    BaseOAuth2ProviderConfig,
)


# REAL PROVIDER (creates login button)
class NEIRProvider(BaseOAuth2Provider):
    id = "oa2-neir"
    name = "NEIR"

    def get_display_name(self, request):
        return "Login with NEIR"

    def get_icon_class(self):
        return "fa-sign-in"


# PROVIDER CONFIG (used by Django admin)
class NEIRProviderConfig(BaseOAuth2ProviderConfig):
    provider_id = "oa2-neir"
    backend_name = "neir"
    verbose_name = "NEIR"
    description = "Login using NEIR SSO"


# CRITICAL: register provider at import time
Registry.register(NEIRProvider)

'''
