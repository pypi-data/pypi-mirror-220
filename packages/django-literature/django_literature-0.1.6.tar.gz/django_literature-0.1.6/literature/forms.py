from django import forms
from django.forms.models import ModelForm, construct_instance, model_to_dict
from django.utils.translation import gettext as _
from formset.collection import FormCollection
from formset.fieldset import FieldsetMixin
from formset.renderers import bootstrap
from formset.richtext.widgets import RichTextarea
from formset.widgets import DateInput, DualSortableSelector, UploadedFileInput

from .models import Literature, SupplementaryMaterial
from .widgets import OnlineSearchWidget, PreviewWidget


class CitationJSFormMixin(forms.Form):
    """A mixin that adds a hidden text field for the CSL JSON data and a preview field
    that renders the formatted content.
    """

    CSL = forms.JSONField(widget=forms.HiddenInput())
    preview = forms.CharField(label=_("Preview"), required=False, widget=PreviewWidget)

    class Media:
        js = (
            "vendor/js/citation.js",
            "literature/js/main.js",
        )


class OnlineSearchForm(CitationJSFormMixin, forms.ModelForm):
    """A form that renders a search bar for DOI, PMCID, PMID, Wikidata and previews the
    formatted content below. Data is appended to a hidden text field when submitting.
    """

    identifier = forms.CharField(
        label=_("Identifier"),
        help_text=_(
            "Enter a valid DOI, ISBN, PMCID, PMID, Wikidata QID or GitHub repository URL to gather citation data"
        ),
        widget=OnlineSearchWidget,
        required=False,
    )

    class Meta:
        model = Literature
        fields = ["identifier", "CSL", "preview"]


class BibFileUploadForm(CitationJSFormMixin, forms.ModelForm):
    """A form that accepts a bibliography file, parses and previews it using citation.js,
    then submits CSL-JSON data to the server for validation and saving via a hidden text
    field.
    """

    file = forms.FileField(label=_("Bibliography File"), help_text=_("Upload a bibliography file."), required=False)

    class Meta:
        model = Literature
        fields = ["file", "CSL", "preview"]


class PDFFileInput(UploadedFileInput):
    template_name = "literature/widgets/pdf_viewer.html"


class LiteratureRequired(FieldsetMixin, ModelForm):
    legend = "Required Content"

    class Meta:
        model = Literature
        fields = ["title", "published", "container_title"]
        widgets = {
            "abstract": RichTextarea(),
            "published": DateInput,
            "authors": DualSortableSelector,  # or DualSelector
        }


class LiteratureExtra(FieldsetMixin, ModelForm):
    legend = "Extra Content"
    help_text = "These fields are not required but are highly recommended."

    class Meta:
        model = Literature
        fields = ["pdf"]
        widgets = {
            "pdf": PDFFileInput(),
            "abstract": RichTextarea(),
            "published": DateInput,
            "authors": DualSortableSelector,  # or DualSelector
        }


class SuppMatForm(ModelForm):
    class Meta:
        model = SupplementaryMaterial
        fields = ["file"]
        widgets = {
            "file": UploadedFileInput(),
        }


class SuppMatCollection(FormCollection):
    legend = "Supplementary Material"
    min_siblings = 0
    extra_siblings = 1
    default_renderer = bootstrap.FormRenderer()

    supplementary_material = SuppMatForm()

    def model_to_dict(self, literature):
        opts = self.declared_holders["supps"]._meta
        return [{"supp": model_to_dict(supp, fields=opts.fields)} for supp in literature.supplementary.all()]

    def construct_instance(self, literature, data):
        for d in data:
            try:
                supp_object = literature.supplementary.get(id=d["supplementary"]["id"])
            except (KeyError, SupplementaryMaterial.DoesNotExist):
                supp_object = SupplementaryMaterial(literature=literature)
            form_class = self.declared_holders["supps"].__class__
            form = form_class(data=d["supplementary"], instance=supp_object)
            if form.is_valid():
                if form.marked_for_removal:
                    supp_object.delete()
                else:
                    construct_instance(form, supp_object)
                    form.save()


class LiteratureForm(FormCollection):
    # legend = "I'm the literature form"

    # help_text = "I'm a form designed to edit a literature object"

    default_renderer = bootstrap.FormRenderer()
    required = LiteratureRequired()
    extra = LiteratureExtra()

    # fieldsets = (
    #     ('Required', {
    #         "fields":["DOI", "pdf"]
    #     }
    #      )
    # )


class LiteratureFormWithSupps(FormCollection):
    legend = "I'm the literature form"

    help_text = "I'm a form designed to edit a literature object"

    default_renderer = bootstrap.FormRenderer()
    # literature = LiteratureForm()
    required = LiteratureRequired()
    extra = LiteratureExtra()
    supps = SuppMatCollection()
