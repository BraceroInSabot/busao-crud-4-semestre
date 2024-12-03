from django.apps import AppConfig


class ApplicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'views.application'

    def ready(self):
        import os
        from django.core.management import call_command

        # Executar apenas em um ambiente limpo (ex.: primeiro deploy)
        if os.environ.get("RUN_INITIAL_SETUP", "False") == "True":
            call_command("load_initial_data")