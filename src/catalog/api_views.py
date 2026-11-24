from rest_framework import generics
from rest_framework.pagination import CursorPagination
from .models import EducationalMaterial
from .serializers import EducationalMaterialSerializer


class MaterialCursorPagination(CursorPagination):
    page_size = 5
    ordering = "-created_at"
    cursor_query_param = "cursor"


class MaterialListAPIView(generics.ListAPIView):
    queryset = EducationalMaterial.objects.filter(is_active=True)
    serializer_class = EducationalMaterialSerializer
    pagination_class = MaterialCursorPagination
