from django.apps import AppConfig

class NeirAuthConfig(AppConfig):
    name = "neir_auth"
    verbose_name = "NEIR Auth"

    def ready(self):
        # Import provider module so Registry.register(...) executes at startup
        from . import provider  # noqa: F401
