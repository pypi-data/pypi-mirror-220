from django.forms.widgets import ChoiceWidget, MultiWidget, TextInput
from django.utils import timezone

from .choices import MonthChoices


class DatePartsWidget(MultiWidget):
    def __init__(self, attrs=None, min_year=1900, max_year=None):
        if max_year is None:
            # use timezone to get the users current year
            max_year = timezone.now().year

        year_choices = ((i, i) for i in range(min_year, max_year))

        widgets = [
            ChoiceWidget(choices=year_choices),
            ChoiceWidget(choices=MonthChoices.choices),
            ChoiceWidget(),
        ]
        super().__init__(widgets, attrs)


class OnlineSearchWidget(TextInput):
    template_name = "literature/widgets/identifier.html"


class PreviewWidget(TextInput):
    template_name = "literature/widgets/preview.html"
