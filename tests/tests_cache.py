from django.test import TestCase
from catalog.models import (
    EducationalMaterial,
    Author,
    Type,
    Year,
    Discipline,
    Language,
    Cache,
)


class CacheTests(TestCase):
    def setUp(self):
        author = Author.objects.create(full_name="Тестовый Автор")
        type_obj = Type.objects.create(name="Пособие")
        year = Year.objects.create(year=2026)
        disc = Discipline.objects.create(name="МДК 02.02")
        lang = Language.objects.create(name="Русский")

        EducationalMaterial.objects.create(
            name=f"Материал",
            author=author,
            type=type_obj,
            year=year,
            discipline=disc,
            language=lang,
        )

    def test_cache_creation(self):
        self.assertEqual(Cache.objects.count(), 0)

        self.client.get("/", {"type": 1})
        self.assertEqual(Cache.objects.count(), 1)

        cached_item = Cache.objects.first()
        self.assertIn("type=1", cached_item.query_text)

    def test_cache_usage(self):
        self.client.get("/", {"type": 1})
        self.assertEqual(Cache.objects.count(), 1)

        self.client.get("/", {"type": 1})
        self.assertEqual(Cache.objects.count(), 1)
