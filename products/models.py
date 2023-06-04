from django.db import models


class Product(models.Model):
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    title = models.CharField(verbose_name="Название")
    model = models.CharField(verbose_name="Модель", unique=True)
    release_date = models.DateField(verbose_name="Дата выхода продукта на рынок")

    def __str__(self):
        return f'{self.title} {self.model}'
