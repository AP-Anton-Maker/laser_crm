from django.db import models

class Material(models.fields.Model):
    name = models.CharField(max_length=100, verbose_name="Название (напр. Фанера 3мм)")
    price_per_meter = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена за метр реза (руб)")
    in_stock = models.BooleanField(default=True, verbose_name="Есть в наличии")

    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "3. Склад и цены"

    def __str__(self):
        return f"{self.name} - {self.price_per_meter} руб/м"
