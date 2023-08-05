from datetime import datetime

from django.utils.module_loading import import_string

from literature.conf import settings


def clean_doi(doi):
    """Clean a DOI string to remove any unnecessary characters."""
    return doi.split("doi.org/")[-1].strip("/").lower()


# def simple_autolabeler(obj):
#     """The strategy used to create unique labels for literature items in the
#     database.

#     TODO: This has not been implemented yet

#     Args:
#         obj (literature.models.Literature): A Literature instance.
#     """
#     label = f"{obj.authors.first().family}{obj.year}"
#     # We don't want label clashes so find how many labels already
#     # in the database start with our new label then append the
#     # appropriate letter.
#     letters = "abcdefghijklmopqrstuvwzy"
#     count = obj._meta.model.objects.filter(label__startswith=label).count()

#     if count:
#         label += letters[count]

#     return label


def simple_file_renamer(instance, fname):
    return f"literature/{instance.title[:50].strip()}.pdf"


def pdf_file_renamer(instance, fname=None):
    func = import_string(settings.LITERATURE_PDF_RENAMER)
    return func(instance, fname)


def get_current_year():
    return datetime.now().year
