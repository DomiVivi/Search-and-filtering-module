from django.urls import path
from . import views

urlpatterns = [
    path("", views.material_list, name="material_list"),
]
