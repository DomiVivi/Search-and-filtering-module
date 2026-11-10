from django.contrib import admin
from .models import (
    Author,
    Discipline,
    Year,
    Type,
    Language,
    Tag,
    EducationalMaterial,
    MaterialTag,
    Cache,
)


@admin.register(EducationalMaterial)
class EducationalMaterialAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "discipline", "type", "year", "is_active")
    list_filter = ("discipline", "type", "language", "year", "is_active")
    search_fields = ("name", "description", "author__full_name")
    readonly_fields = ("created_at",)


admin.site.register(Author)
admin.site.register(Discipline)
admin.site.register(Year)
admin.site.register(Type)
admin.site.register(Language)
admin.site.register(Tag)
admin.site.register(MaterialTag)
admin.site.register(Cache)
