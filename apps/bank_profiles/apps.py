from django.apps import AppConfig


class BankProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.bank_profiles'

    def ready(self):
        import apps.bank_profiles.signals
