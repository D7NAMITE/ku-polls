from django.apps import AppConfig


class PollsConfig(AppConfig):
    """
    PollsConfig class will do the configuration of the polls app
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "polls"
