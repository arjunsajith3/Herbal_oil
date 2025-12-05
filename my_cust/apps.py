from django.apps import AppConfig


class MyCustConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_cust'

    def ready(self):
        import my_cust.signals

