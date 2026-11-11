from django.shortcuts import render

from .models import EducationalMaterial

def material_list(request):
    materials = EducationalMaterial.objects.all()
    context = {'materials': materials}
    return render(request, 'index.html', context)
