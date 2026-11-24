from django.urls import path
from . import views
from .api_views import MaterialListAPIView

urlpatterns = [
    path("", views.material_list, name="material_list"),
    path("api/materials/", MaterialListAPIView.as_view(), name="api_materials"),
]
