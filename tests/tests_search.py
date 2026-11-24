from django.test import TestCase
from catalog.models import (
    EducationalMaterial,
    Author,
    Type,
    Year,
    Discipline,
    Language,
    Tag,
    MaterialTag,
)


class SearchTests(TestCase):
    def setUp(self):
        self.author1 = Author.objects.create(full_name="Пушкин А.С.")
        self.author2 = Author.objects.create(full_name="Толстой Л.Н.")

        self.type_book = Type.objects.create(name="Книга")
        self.type_article = Type.objects.create(name="Статья")

        self.year_1823 = Year.objects.create(year=1823)
        self.year_2023 = Year.objects.create(year=2023)

        self.disc = Discipline.objects.create(name="Литература")
        self.lang = Language.objects.create(name="Русский")

        self.tag_rom = Tag.objects.create(name="Роман")
        self.tag_poems = Tag.objects.create(name="Стихи")

        self.material1 = EducationalMaterial.objects.create(
            name="Сборник стихов",
            author=self.author1,
            type=self.type_article,
            year=self.year_2023,
            discipline=self.disc,
            language=self.lang,
        )
        MaterialTag.objects.create(material=self.material1, tag=self.tag_poems)

        self.material2 = EducationalMaterial.objects.create(
            name="Война и мир",
            author=self.author2,
            type=self.type_book,
            year=self.year_1823,
            discipline=self.disc,
            language=self.lang,
        )
        MaterialTag.objects.create(material=self.material2, tag=self.tag_rom)

        self.material3 = EducationalMaterial.objects.create(
            name="Евгений Онегин",
            author=self.author1,
            type=self.type_book,
            year=self.year_1823,
            discipline=self.disc,
            language=self.lang,
        )
        MaterialTag.objects.create(material=self.material3, tag=self.tag_rom)

    def test_filter_by_author(self):
        response = self.client.get("/", {"author": self.author1.id})
        materials = response.context["page_obj"].object_list
        self.assertEqual(len(materials), 2)

    def test_filter_by_type(self):
        response = self.client.get("/", {"type": self.type_book.id})
        materials = response.context["page_obj"].object_list
        self.assertEqual(len(materials), 2)

    def test_combined_filters_success(self):
        response = self.client.get(
            "/",
            {
                "type": self.type_article.id,
                "author": self.author1.id,
                "year": self.year_2023.id,
                "tag": self.tag_poems.id,
            },
        )
        materials = response.context["page_obj"].object_list
        self.assertEqual(len(materials), 1)
        self.assertEqual(materials[0].name, "Сборник стихов")

    def test_combined_filters_empty(self):
        response = self.client.get(
            "/",
            {
                "type": self.type_article.id,
                "author": self.author2.id,
            },
        )
        materials = response.context["page_obj"].object_list
        self.assertEqual(len(materials), 0)
