import json
import pprint

from django import forms
from django.http import HttpResponse, JsonResponse
from django.utils.encoding import force_str
from django.views.generic import DetailView, ListView
from formset.views import FormCollectionView

from literature.models import Author, Literature

# from literature.conf import
from .formset import LiteratureFormCollection


class CitationMixin:
    citation_style = "bootstrap"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["citation_style"] = self.citation_style
        return context


class LiteratureList(CitationMixin, ListView):
    model = Literature

    def get_queryset(self):
        return super().get_queryset().prefetch_related("authors")


class LiteratureDetail(FormCollectionView, CitationMixin):
    # model = SupplementaryMaterial
    # form_class=LiteratureForm
    collection_class = LiteratureFormCollection
    extra_context = None
    template_name = "literature/literature_form.html"

    # def get_object(self, queryset=None):
    # if self.extra_context['add'] is False:
    # return super().get_object(queryset)

    def form_valid(self, form):
        if (extra_data := self.get_extra_data()) and extra_data.get("delete") is True:
            self.object.delete()
            success_url = self.get_success_url()
            response_data = {"success_url": force_str(success_url)} if success_url else {}
            return JsonResponse(response_data)
        return super().form_valid(form)


class AuthorList(ListView):
    model = Author

    def get_queryset(self):
        return super().get_queryset().with_work_counts()


class AuthorDetail(CitationMixin, DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["literature_list"] = context["author"].literature.prefetch_related("authors")
        return context


class LiteratureForm(forms.ModelForm):
    class Meta:
        model = Literature
        exclude = ["published", "year"]

    # def __init__(self, data=None, *args, **kwargs):
    #     # modify the incoming data to ensure that keys with hyphens are replaced with
    #     data = {k.replace('-','_'):v for k,v in data.items()}
    #     super().__init__(data, *args, **kwargs)


def process_csl(request):
    # formset = forms.formset_factory(LiteratureForm)
    print("here")
    if request.method == "POST":
        form_data = json.loads(request.POST["data"])
        for f in form_data:
            # f = {k.replace('-','_'):v for k,v in f.items()}
            # pprint.pprint(f)
            form = LiteratureForm(f)
            if form.is_valid():
                pprint.pprint(form.cleaned_data)
            else:
                print(form.errors)
            # print(form)
        # print(request.POST['data'])
    # Get the posted form
    #   MyLoginForm = LoginForm(request.POST)
    # html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse("Hi")
