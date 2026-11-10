from django.db import models


class Author(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="ФИО автора")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.full_name


class Discipline(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название дисциплины")

    class Meta:
        verbose_name = "Дисципплина"
        verbose_name_plural = "Дисциплины"

    def __str__(self):
        return self.name


class Year(models.Model):
    year = models.IntegerField(verbose_name="Год выпуска")

    class Meta:
        verbose_name = "Год"
        verbose_name_plural = "Года"

    def __str__(self):
        return self.year


class Type(models.Model):
    name = models.CharField(max_length=255, verbose_name="Типа ресура")

    class Meta:
        verbose_name = "Тип ресурса"
        verbose_name_plural = "Типы ресурсов"

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=255, verbose_name="Языка")

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Языки"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name="Тега")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class EducationalMaterial(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название материала")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    link = models.CharField(
        max_length=500, blank=True, null=True, verbose_name="Ссылка"
    )

    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    discipline = models.ForeignKey(
        Discipline, on_delete=models.CASCADE, verbose_name="Дисциплина"
    )
    year = models.ForeignKey(Year, on_delete=models.CASCADE, verbose_name="Год")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name="Тип")
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE, verbose_name="Язык"
    )

    is_acive = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Учебный материал"
        verbose_name_plural = "Учебные материалы"

    def __str__(self):
        return self.name


class MaterialTag(models.Model):
    material = models.ForeignKey(
        EducationalMaterial, on_delete=models.CASCADE, verbose_name="Материал"
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="Тег")

    class Meta:
        verbose_name = "Тег материала"
        verbose_name_plural = "Теги материалов"

    def __str__(self):
        return f"{self.material.name} - {self.tag.name}"


class Cache(models.Model):
    query_hash = models.CharField(
        max_length=255, unique=True, verbose_name="Хэш запроса"
    )
    query_text = models.CharField(max_length=500, verbose_name="Текст запроса")
    results_json = models.TextField(verbose_name="Результаты (JSON)")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата кэширования"
    )

    class Meta:
        verbose_name = "Кэш поиска"
        verbose_name_plural = "Кэш поисковых запросов"

    def __str__(self):
        return self.query_text
