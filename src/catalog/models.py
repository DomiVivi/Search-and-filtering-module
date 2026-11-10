from django.db import models

class Author(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="ФИО автора")
    
    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self): 
        return self.full_name


class Discipline(models.Model):
    name =  models.CharField(max_length=255, verbose_name="Название дисциплины")

    class Meta:
        verbose_name = "Дисципплина"
        verbose_name_plural = "Дисциплины"

    def __str__(self):
        return  self.name

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
    name =  models.CharField(max_length=255, verbose_name="Тега")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name
