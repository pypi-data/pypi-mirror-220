from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LiteratureConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "literature"
    verbose_name = _("Literature Manager")
