from django import template

# from django.conf import settings
from django.template.loader import render_to_string

from literature.conf import settings

register = template.Library()


@register.simple_tag
def bibliography(bibliography, style=None):
    """Renders a bibligraphy in the given style"""
    context = {
        "bibliography": bibliography,
        "citation_style": f"literature/citation/{style or settings.DEFAULT_CITATION_STYLE }.html",
    }
    print(context["citation_style"])
    return render_to_string("literature/bibliography.html", context)
