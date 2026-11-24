from django.test import TestCase
from catalog.models import EducationalMaterial, Author, Type, Year, Discipline, Language


class HTMLPaginationTests(TestCase):
    def setUp(self):
        author = Author.objects.create(full_name="Тестовый Автор")
        type_obj = Type.objects.create(name="Пособие")
        year = Year.objects.create(year=2026)
        disc = Discipline.objects.create(name="МДК 02.02")
        lang = Language.objects.create(name="Русский")

        for i in range(1, 8):
            EducationalMaterial.objects.create(
                name=f"Материал {i}",
                author=author,
                type=type_obj,
                year=year,
                discipline=disc,
                language=lang,
            )

    def test_first_page_pagination(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

        page_obj = response.context["page_obj"]

        self.assertEqual(len(page_obj), 5)

        self.assertEqual(page_obj.paginator.num_pages, 2)

    def test_second_page_pagination(self):
        response = self.client.get("/?page=2")

        page_obj = response.context["page_obj"]

        self.assertEqual(len(page_obj), 2)

        self.assertEqual(page_obj.number, 2)

    def test_invalid_page_fallback(self):
        response = self.client.get("/?page=999")

        page_obj = response.context["page_obj"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(page_obj.number, 2)
