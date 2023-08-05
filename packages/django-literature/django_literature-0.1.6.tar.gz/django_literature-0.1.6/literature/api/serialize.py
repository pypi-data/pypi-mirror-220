from rest_framework import serializers

from ..models import Literature


class LiteratureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Literature
        exclude = ["container_title", "citation_key", "pdf", "authors", "collections", "abstract"]

    def to_representation(self, data):
        data = super().to_representation(data)
        return data.pop("CSL") | data
