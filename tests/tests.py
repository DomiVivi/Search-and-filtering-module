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
        materials = response.context["materials"]
        self.assertEqual(len(materials), 2)

    def test_filter_by_type(self):
        response = self.client.get("/", {"type": self.type_book.id})
        materials = response.context["materials"]
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
        materials = response.context["materials"]
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
        materials = response.context["materials"]
        self.assertEqual(len(materials), 0)


class SortingTests(TestCase):
    def setUp(self):
        self.author1 = Author.objects.create(full_name="Пушкин А.С.")
        self.author2 = Author.objects.create(full_name="Толстой Л.Н.")

        self.type = Type.objects.create(name="Книга")
        self.lang = Language.objects.create(name="Русский")
        self.year_2023 = Year.objects.create(year=2023)
        self.year_2024 = Year.objects.create(year=2024)

        self.disc_lit1 = Discipline.objects.create(name="Литература")
        self.disc_lit2 = Discipline.objects.create(name="Литература Родного Края")

        EducationalMaterial.objects.create(
            name="Евгений Онегин",
            author=self.author1,
            type=self.type,
            year=self.year_2023,
            discipline=self.disc_lit1,
            language=self.lang,
        )

        EducationalMaterial.objects.create(
            name="Война и мир",
            author=self.author2,
            type=self.type,
            year=self.year_2024,
            discipline=self.disc_lit2,
            language=self.lang,
        )

        EducationalMaterial.objects.create(
            name="Воскресенье",
            author=self.author2,
            type=self.type,
            year=self.year_2024,
            discipline=self.disc_lit2,
            language=self.lang,
        )

    def test_sort_by_name_asc(self):
        response = self.client.get("/", {"sort_field1": "name", "sort_dir1": "asc"})
        materials = response.context["materials"]

        self.assertEqual(materials[0].name, "Война и мир")
        self.assertEqual(materials[1].name, "Воскресенье")
        self.assertEqual(materials[2].name, "Евгений Онегин")

    def test_sort_by_author_then_year_desc(self):
        response = self.client.get(
            "/",
            {
                "sort_field1": "author",
                "sort_dir1": "asc",
                "sort_field2": "year",
                "sort_dir2": "desc",
            },
        )
        materials = response.context["materials"]

        self.assertEqual(materials[0].author.full_name, "Пушкин А.С.")
        self.assertEqual(materials[0].name, "Евгений Онегин")

        self.assertEqual(materials[1].author.full_name, "Толстой Л.Н.")
        self.assertEqual(materials[2].author.full_name, "Толстой Л.Н.")

    def test_sort_by_discipline_then_name(self):
        response = self.client.get(
            "/",
            {
                "sort_field1": "discipline",
                "sort_dir1": "asc",
                "sort_field2": "name",
                "sort_dir2": "asc",
            },
        )
        materials = response.context["materials"]

        self.assertEqual(materials[0].discipline.name, "Литература")
        self.assertEqual(materials[0].name, "Евгений Онегин")

        self.assertEqual(materials[1].discipline.name, "Литература Родного Края")
        self.assertEqual(materials[1].name, "Война и мир")

        self.assertEqual(materials[2].discipline.name, "Литература Родного Края")
        self.assertEqual(materials[2].name, "Воскресенье")
