from datetime import date

from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    RegexValidator,
)
from django.db import models
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.translation import gettext as _
from model_utils import FieldTracker
from model_utils.models import TimeStampedModel
from sortedm2m.fields import SortedManyToManyField
from taggit.managers import TaggableManager

from .choices import IdentifierTypes, TypeChoices
from .managers import AuthorManager
from .utils import pdf_file_renamer


class LiteratureAuthor(models.Model):
    """An intermediate table for the Work-Author m2m relationship.
    `SortedManyToManyField` automatically creates this table, however, there is no access via querysets. Defining here instead allows us to have access to the intermediate table in order to query author position.
    """

    literature = models.ForeignKey("literature.Literature", on_delete=models.CASCADE)
    author = models.ForeignKey("literature.Author", related_name="position", on_delete=models.CASCADE)
    position = models.IntegerField()

    _sort_field_name = "position"

    def __str__(self):
        return str(self.position)


class Author(TimeStampedModel):
    objects = AuthorManager()

    given = models.CharField(_("given name"), max_length=255, blank=True, null=True)
    family = models.CharField(_("family name"), max_length=255, blank=True)
    ORCID = models.CharField(
        "ORCID",
        max_length=64,
        validators=[RegexValidator("^(?:\\d{4}-){3}\\d{3}[\\d,x]")],
        blank=True,
        null=True,
    )

    # literature = SortedManyToManyField(
    #     to="literature.Literature",
    #     verbose_name=_("literature"),
    #     related_name="authors",
    #     through=LiteratureAuthor,
    #     sort_value_field_name="position",
    #     blank=True,
    # )

    class Meta:
        verbose_name = _("author")
        verbose_name_plural = _("authors")
        ordering = ["family"]

    def __str__(self):
        return self.given_family()

    def get_absolute_url(self):
        return reverse("literature:author_detail", kwargs={"pk": self.pk})

    @staticmethod
    def autocomplete_search_fields():
        return (
            "family__icontains",
            "given__icontains",
        )

    def given_family(self):
        """Returns "John Smith" """
        return f"{self.given} {self.family}"

    def family_given(self):
        """Returns "Smith, John" """
        return f"{self.family}, {self.given}"

    def g_family(self):
        """Returns "J. Smith" """
        return f"{self.given[0]}. {self.family}"

    def family_g(self):
        """Returns "Smith, J." """
        return f"{self.family}, {self.given[0]}."


class Identifier(TimeStampedModel):
    ID = models.CharField(max_length=512, verbose_name=_("Permanent Identifier"), primary_key=True)
    literature = models.ForeignKey("literature.Literature", verbose_name=_("literature"), on_delete=models.CASCADE)
    type = models.IntegerField(choices=IdentifierTypes.choices)  # noqa: A003

    class Meta:
        verbose_name = _("ID")
        verbose_name_plural = _("IDs")
        # ordering = ["citation_key"]
        default_related_name = "identifiers"
        unique_together = ["ID", "literature"]

    def __str__(self):
        return f"{self.get_type_display()} <{self.ID}>"


class Literature(TimeStampedModel):
    """Model for storing literature data"""

    # ARTICLE TYPE
    type = models.CharField(_("type"), choices=TypeChoices.choices, max_length=255)  # noqa: A003

    # THE FOLLOWING FIELDS ARE DEFINED HERE AS THEY MAY BENEFIT FROM INDEXING
    abstract = models.TextField(_("abstract"), blank=True, null=True)
    container_title = models.CharField(
        _("container title"),
        help_text=_(
            "Title of the container holding the item (e.g. the book title for a book chapter, the journal title for a"
            " journal article; the album title for a recording; the session title for multi-part presentation at a"
            " conference)."
        ),
        max_length=512,
        null=True,
        blank=True,
    )
    keyword = TaggableManager(
        verbose_name=_("key words"),
        help_text=_("Keyword(s) or tag(s) attached to the item."),
        blank=True,
    )
    citation_key = models.CharField(
        _("citation key"),
        help_text=_("A human readable identifier of the literature item (analogous to a BibTeX entrykey)."),
        max_length=255,
        blank=True,
        null=True,
        unique=True,
    )
    language = models.CharField(_("language"), max_length=2, blank=True, null=True)
    title = models.TextField(
        _("title"),
        help_text=_("Primary title of the item."),
        blank=True,
        null=True,
    )

    # DJANGO LITERATURE SPECIFIC FIELDS
    authors = SortedManyToManyField(
        to="literature.Author",
        verbose_name=_("authors"),
        related_name="literature",
        through=LiteratureAuthor,
        sort_value_field_name="number",
        blank=True,
    )
    collections = models.ManyToManyField(
        to="literature.collection",
        verbose_name=_("collection"),
        help_text=_("Add the entry to a collection."),
        blank=True,
    )
    pdf = models.FileField(
        "PDF",
        upload_to=pdf_file_renamer,
        validators=[FileExtensionValidator(["pdf"])],
        null=True,
        blank=True,
    )
    published = models.DateField(
        _("date published"),
        max_length=255,
        blank=True,
        null=True,
        validators=[MaxValueValidator(date.today)],
    )
    comment = models.TextField(
        _("comment"),
        help_text=_("General comments regarding the entry."),
        blank=True,
        null=True,
    )

    # RAW CSL DATA FIELD
    CSL = models.JSONField(_("Citation Style Language"), blank=True)

    # tracks whether changes have been made to any fields since the last save
    tracker = FieldTracker()

    class Meta:
        verbose_name = _("literature")
        verbose_name_plural = _("literature")
        ordering = ["citation_key"]
        default_related_name = "literature"

    def __str__(self):
        return force_str(self.citation_key)

    def save(self, *args, **kwargs):
        if self.tracker.has_changed("CSL"):
            self.parse_csl()

        # if self.tracker.has_changed("year"):
        # self.published = date(year=self.year, month=self.month or 1, day=1)

        super().save(*args, **kwargs)
        # if self.tracker.has_changed("CSL"):
        self.update_identifiers()
        return self

    def parse_csl(self):
        CSL = {k.replace("-", "_"): v for k, v in self.CSL.items()}
        for field in [f.name for f in self._meta.fields]:
            if field == "id":
                continue
            if CSL.get(field):
                setattr(self, field, CSL[field])

    def update_identifiers(self):
        # update identifier fields
        for field in IdentifierTypes.labels:
            if self.CSL.get(field):
                obj, new = Identifier.objects.get_or_create(
                    ID=self.CSL.get(field), type=getattr(IdentifierTypes, field), literature=self
                )
                if new:
                    print(f"Creating new {field}")
                    obj.save()

    @staticmethod
    def autocomplete_search_fields():
        return (
            "title__icontains",
            "authors__family__icontains",
            "citation_key__icontains",
        )

    # def to_internal_value(self, data):
    # data['container_title'] = data['container-title']
    # data.pop('container-title', None)
    # return data


class Collection(TimeStampedModel):
    """
    Model representing a collection of publications.
    """

    class Meta:
        ordering = ("name",)
        verbose_name = _("collection")
        verbose_name_plural = _("collections")

    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"))

    def __str__(self):
        return force_str(self.name)


class SupplementaryMaterial(TimeStampedModel):
    literature = models.ForeignKey(
        to="literature.Literature",
        verbose_name=_("literature"),
        related_name="supplementary",
        on_delete=models.CASCADE,
    )
    file = models.FileField(_("file"))

    class Meta:
        verbose_name = _("supplementary material")
        verbose_name_plural = _("supplementary material")
