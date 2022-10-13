from django.apps import AppConfig


class BitcoinConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bitcoin'

    def ready(self):
        print('Initialising scheduler')
        from .scheduler import updater
        updater.start()