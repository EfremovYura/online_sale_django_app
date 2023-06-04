from django.db import models
from users.models import User


class Seller(models.Model):
    class Meta:
        verbose_name = "Продавец"
        verbose_name_plural = "Продавцы"

    class SellerType(models.IntegerChoices):
        factory = 1, "Завод"
        retailer = 2, "Розничная сеть"
        businessman = 3, "Индивидуальный предприниматель"

    title = models.CharField(verbose_name="Название", max_length=255)
    seller_type = models.PositiveSmallIntegerField(choices=SellerType.choices)
    email = models.EmailField(verbose_name='email')
    country = models.CharField(verbose_name="Страна")
    city = models.CharField(verbose_name='Город')
    street = models.CharField(verbose_name='Улица')
    house_number = models.CharField(verbose_name='Номер дома')

    products = models.ManyToManyField('products.Product', verbose_name='Продукты', blank=True)
    provider = models.ForeignKey('sellers.Seller', on_delete=models.PROTECT, verbose_name="Поставщик", null=True,
                                 blank=True)
    debt = models.FloatField(verbose_name="Задолженность перед поставщиком", default=0.00)
    created = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Время последнего обновления", auto_now=True)

    def __str__(self):
        return f'{self.seller_type} {self.title}'
