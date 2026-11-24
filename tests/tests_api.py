from django.test import TestCase
from catalog.models import EducationalMaterial, Author, Type, Year, Discipline, Language


class APITests(TestCase):
    def setUp(self):
        author = Author.objects.create(full_name="Тестовый Автор")
        type_obj = Type.objects.create(name="Пособие")
        year = Year.objects.create(year=2026)
        disc = Discipline.objects.create(name="МДК 02.02")
        lang = Language.objects.create(name="Русский")

        for i in range(7):
            EducationalMaterial.objects.create(
                name=f"Материал {i}",
                author=author,
                type=type_obj,
                year=year,
                discipline=disc,
                language=lang,
            )

    def test_api_cursor_pagination(self):
        response = self.client.get("/api/materials/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/json")

        data = response.json()

        self.assertEqual(len(data["results"]), 5)

        self.assertIsNotNone(data["next"])
        self.assertIn("cursor=", data["next"])

    def test_api_data_fields(self):
        response = self.client.get("/api/materials/")
        first_material = response.json()["results"][0]

        self.assertIn("name", first_material)
        self.assertIn("author_name", first_material)
        self.assertIn("year_value", first_material)
        self.assertIn("language_name", first_material)
