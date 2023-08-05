from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.template.defaultfilters import pluralize
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.translation import gettext as _
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser

from .csl_map import fields as csl_fields
from .drf import DataTableMixin
from .forms import BibFileUploadForm, OnlineSearchForm
from .models import Author, Collection, Identifier, Literature, SupplementaryMaterial


class SupplementaryInline(admin.TabularInline):
    model = SupplementaryMaterial


class AuthorInline(admin.TabularInline):
    model = Author.literature.through


@admin.register(Literature)
class LiteratureAdmin(DataTableMixin, admin.ModelAdmin):
    """Django Admin setup for the `literature.Work` model."""

    change_list_template = "literature/admin/change_list.html"

    inlines = [SupplementaryInline, AuthorInline]
    fieldsets = [
        (
            _("Basic"),
            {
                "fields": [
                    "citation_key",
                    "pdf",
                    "type",
                    "title",
                    "language",
                    "created",
                    "modified",
                ]
            },
        ),
        (
            _("Recommended"),
            {
                "fields": [
                    "container_title",
                    "abstract",
                    "collections",
                    # "keywords",
                ]
            },
        ),
        (
            _("Comment"),
            {
                "fields": [
                    "comment",
                ]
            },
        ),
        # (
        #     _("Administrative"),
        #     {
        #         "fields": [
        #             "language",
        #             "source",
        #             "comment",
        #             "created",
        #             "modified",
        #             "last_synced",
        #         ]
        #     },
        # ),
    ]

    endpoint = {
        "fields": "__all__",
        "include_str": False,
        "page_size": 1000,
        "permission_classes": [IsAdminUser, DjangoModelPermissions],
    }

    def get_dt_fields(self):
        new_dict = {}
        for field, value in sorted(csl_fields.items()):
            new_dict[field] = value | {"title": field.replace("_", " ").replace("-", " ")}

        return new_dict

    def _pdf(self, obj):
        if obj.pdf:
            return obj.pdf.url

    def edit(self, obj):
        return reverse(
            "admin:{app_label}_{model_name}_change".format(
                app_label=obj._meta.app_label, model_name=obj._meta.model_name
            ),
            args=[obj.id],
        )

    def get_urls(self):
        return [
            path("search/", self.admin_site.admin_view(self.search_online), name="search"),
            path("upload/", self.admin_site.admin_view(self.upload), name="upload"),
            *super().get_urls(),
        ]

    def search_online(self, request, *args, **kwargs):
        """Admin view that handles user-uploaded bibtex files

        Returns:
            HttpResponseRedirect: redirects to model admins change_list
        """
        if request.method == "POST":
            form = OnlineSearchForm(request.POST)
            if form.is_valid():
                bibliography = form.cleaned_data["CSL"]

                imported, updated = 0, 0
                for item in bibliography:
                    imported += 1
                    Literature.objects.create(CSL=item)
                self.message_user(
                    request,
                    level=messages.SUCCESS,
                    message=(
                        f"{imported} literature item{pluralize(imported)} {pluralize(imported,'was,were')} succesfully"
                        f" imported and {updated} {pluralize(updated,'has,have')} been updated."
                    ),
                )
                return HttpResponseRedirect("../")

        else:
            form = OnlineSearchForm(request.GET)

        # return TemplateResponse(request, 'admin/change_form.html', {form: form})
        return TemplateResponse(
            request,
            "literature/admin/search.html",
            {
                "form": form,
                "opts": self.opts,
            },
        )

    def upload(self, request, *args, **kwargs):
        """Admin view that handles user-uploaded bibtex files

        Returns:
            HttpResponseRedirect: redirects to model admins change_list
        """
        if request.method == "POST":
            form = BibFileUploadForm(request.POST)
            if form.is_valid():
                bibliography = form.cleaned_data["CSL"]

                imported, updated = 0, 0
                for item in bibliography:
                    imported += 1
                    Literature.objects.create(CSL=item)
                self.message_user(
                    request,
                    level=messages.SUCCESS,
                    message=(
                        f"{imported} literature item{pluralize(imported)} {pluralize(imported,'was,were')} succesfully"
                        f" imported and {updated} {pluralize(updated,'has,have')} been updated."
                    ),
                )
                return HttpResponseRedirect("../")

        else:
            form = BibFileUploadForm(request.GET)

        # return TemplateResponse(request, 'admin/change_form.html', {form: form})
        return TemplateResponse(
            request,
            "literature/admin/search.html",
            {
                "form": form,
                "opts": self.opts,
            },
        )


@admin.register(Identifier)
class IdentifierAdmin(admin.ModelAdmin):
    list_filter = ["type"]
    search_fields = ["ID", "literature__title"]
    # list_display = ['type', 'ID']
    # list_display_links = ['ID']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    pass


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["family", "given", "ORCID", "created", "modified"]
