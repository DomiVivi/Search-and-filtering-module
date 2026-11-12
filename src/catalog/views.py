from django.shortcuts import render

from .models import EducationalMaterial, Author, Type, Year, Tag


def material_list(request):
    materials = EducationalMaterial.objects.filter(is_active=True)

    type_id = request.GET.get("type", "")
    author_id = request.GET.get("author", "")
    year_id = request.GET.get("year", "")
    tag_id = request.GET.get("tag", "")

    if type_id:
        materials = materials.filter(type_id=type_id)
    if author_id:
        materials = materials.filter(author_id=author_id)
    if year_id:
        materials = materials.filter(year_id=year_id)
    if tag_id:
        materials = materials.filter(materialtag__tag_id=tag_id)

    context = {
        "materials": materials,
        "types": Type.objects.all(),
        "authors": Author.objects.all(),
        "years": Year.objects.all(),
        "tags": Tag.objects.all(),
    }
    return render(request, "index.html", context)
