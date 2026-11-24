from rest_framework import serializers
from .models import EducationalMaterial


class EducationalMaterialSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.full_name", read_only=True)
    discipline_name = serializers.CharField(source="discipline.name", read_only=True)
    type_name = serializers.CharField(source="type.name", read_only=True)
    language_name = serializers.CharField(source="language.name", read_only=True)
    year_value = serializers.IntegerField(source="year.year", read_only=True)

    class Meta:
        model = EducationalMaterial
        fields = [
            "id",
            "name",
            "description",
            "link",
            "author_name",
            "discipline_name",
            "type_name",
            "language_name",
            "year_value",
        ]
