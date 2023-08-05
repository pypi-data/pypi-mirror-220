from rest_framework import viewsets

from ..models import Literature
from .serialize import LiteratureSerializer


class LiteratureView(viewsets.ModelViewSet):
    """API endpoint that allows literature to be viewed or edited."""

    max_paginate_by = 1000
    pagination_class = None
    serializer_class = LiteratureSerializer
    queryset = Literature.objects.all()
