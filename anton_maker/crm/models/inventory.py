from django.db import models

class Material(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название материала")
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу")
    in_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="В наличии")
    min_stock_level = models.DecimalField(max_digits=10, decimal_places=2, default=10, verbose_name="Мин. остаток")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"
        ordering = ['name']

    def __str__(self):
        return self.name

class QuickReply(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    text = models.TextField(verbose_name="Текст ответа")

    class Meta:
        verbose_name = "Быстрый ответ"
        verbose_name_plural = "Быстрые ответы"

    def __str__(self):
        return self.title
