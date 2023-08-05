from typing import Any, Dict

from django import forms
from django.utils.translation import gettext as _
from formset.collection import FormCollection
from formset.fieldset import Fieldset
from formset.renderers import bootstrap
from formset.richtext.widgets import RichTextarea
from formset.widgets import (
    Selectize,
)

from .choices import TypeChoices
from .csl_map import CSL_FIELDS, CSL_TYPES


class CSLMixin:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_fields()
        self.update_field_visibility()

    def update_fields(self):
        for field in self.Meta.fields:
            attrs = CSL_FIELDS[field]
            if attrs["type"] == "standard":
                self.fields[field] = forms.CharField(
                    label=attrs["name"],
                    help_text=_(attrs["description"]),
                    required=False,
                    widget=self.Meta.widgets.get(field, None),
                )
                self.fields[field].widget.attrs.update({"show-if": ""})

    def update_field_visibility(self):
        for csl_type, fields in CSL_TYPES.items():
            for field_name in fields:
                if field_name in self.fields:
                    if not self.fields[field_name].widget.attrs["show-if"]:
                        self.fields[field_name].widget.attrs["show-if"] += f"literature.type == '{csl_type}'"
                    else:
                        self.fields[field_name].widget.attrs["show-if"] += f" || literature.type == '{csl_type}'"


class PublisherForm(CSLMixin, Fieldset):
    legend = _("Publishing")
    # help_text = "I'm a form designed to edit a literature object"

    class Meta:
        fields = ["publisher", "publisher-place", "original-publisher", "original-publisher-place"]
        widgets: Dict[str, Any] = {}


class CSLForm(CSLMixin, Fieldset):
    type = forms.ChoiceField(  # noqa: A003
        label=_("type"), choices=TypeChoices.choices, required=True, widget=Selectize
    )

    class Meta:
        fields = ["title", "abstract"]
        widgets = {
            # "pdf": PDFFileInput(),
            "abstract": RichTextarea(),
            # "published": DateInput,
            # "authors": DualSortableSelector,  # or DualSelector
        }


class LiteratureFormCollection(FormCollection):
    # legend = "I'm the literature form"
    # help_text = "I'm a form designed to edit a literature object"

    default_renderer = bootstrap.FormRenderer(field_css_classes="mb-3")

    literature = CSLForm()
    publishing = PublisherForm()
