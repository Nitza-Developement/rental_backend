from django.apps import AppConfig
from django.db.models.signals import post_migrate

def config_app(sender, **kwargs):
    from django.conf import settings

    from .models import User

    if User.objects.all().count() == 0:
        User.objects.create_superuser(
            email=settings.DJANGO_SUPERUSER_EMAIL,
            password=settings.DJANGO_SUPERUSER_PASSWORD,
        )

class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rental"
    def ready(self):
        post_migrate.connect(config_app, sender=self)
