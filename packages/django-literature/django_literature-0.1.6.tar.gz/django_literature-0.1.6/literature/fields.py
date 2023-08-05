from django.db import models
from django.utils.translation import gettext_lazy as _


class LiteratureFK(models.ForeignKey):
    """A foreign key field to the `literature.Literature` model"""

    def __init__(self, *args, **kwargs):
        kwargs["to"] = "literature.Literature"
        if not kwargs.get("verbose_name"):
            kwargs["verbose_name"] = _("literature")
        super().__init__(*args, **kwargs)


class LiteratureM2M(models.ManyToManyField):
    """A many-to-many field to the `literature.Literature` model"""

    def __init__(self, *args, **kwargs):
        kwargs["to"] = "literature.Literature"
        if not kwargs.get("verbose_name"):
            kwargs["verbose_name"] = _("literature")
        super().__init__(*args, **kwargs)
