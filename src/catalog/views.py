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

    sort_field1 = request.GET.get("sort_field1", "")
    sort_dir1 = request.GET.get("sort_dir1", "asc")
    sort_field2 = request.GET.get("sort_field2", "")
    sort_dir2 = request.GET.get("sort_dir2", "asc")

    order_by_list = []

    if sort_field1:
        prefix1 = "-" if sort_dir1 == "desc" else ""
        if sort_field1 == "name":
            order_by_list.append(f"{prefix1}name")
        elif sort_field1 == "author":
            order_by_list.append(f"{prefix1}author__full_name")
        elif sort_field1 == "year":
            order_by_list.append(f"{prefix1}year__year")
        elif sort_field1 == "discipline":
            order_by_list.append(f"{prefix1}discipline__name")

    if sort_field2:
        prefix2 = "-" if sort_dir2 == "desc" else ""
        if sort_field2 == "name":
            order_by_list.append(f"{prefix2}name")
        elif sort_field2 == "author":
            order_by_list.append(f"{prefix2}author__full_name")
        elif sort_field2 == "year":
            order_by_list.append(f"{prefix2}year__year")
        elif sort_field2 == "discipline":
            order_by_list.append(f"{prefix2}discipline__name")

    if order_by_list:
        materials = materials.order_by(*order_by_list)

    context = {
        "materials": materials,
        "types": Type.objects.all(),
        "authors": Author.objects.all(),
        "years": Year.objects.all(),
        "tags": Tag.objects.all(),
        "current_sort_field1": sort_field1,
        "current_sort_dir1": sort_dir1,
        "current_sort_field2": sort_field2,
        "current_sort_dir2": sort_dir2,
    }
    return render(request, "index.html", context)
