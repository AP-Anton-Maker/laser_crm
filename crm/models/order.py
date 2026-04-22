from django.db import models
from .client import Client
from .inventory import Material

class Order(models.fields.Model):
    STATUS_CHOICES = [
        ('new', 'Новый (Ожидает оценки)'),
        ('awaiting_payment', 'Ожидает оплаты'),
        ('paid', 'Оплачен (В работу)'),
        ('cutting', 'На станке (Режется)'),
        ('ready', 'Готов к выдаче'),
        ('completed', 'Выдан/Завершен'),
        ('canceled', 'Отменен'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders', verbose_name="Клиент")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    
    # Детали заказа
    description = models.TextField(verbose_name="Описание от клиента (ТЗ)", blank=True)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Материал")
    cut_length = models.FloatField(verbose_name="Длина реза (метры)", null=True, blank=True)
    
    # Файлы (Сохраняются в нашу надежную папку data/media)
    layout_file = models.FileField(upload_to='client_files/', blank=True, null=True, verbose_name="Макет (Вектор)")
    receipt_image = models.ImageField(upload_to='receipts/', blank=True, null=True, verbose_name="Чек об оплате")
    
    # Финансы
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Итоговая цена (руб)")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    
    # Технические метки
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    admin_notes = models.TextField(verbose_name="Заметки мастера (не видно клиенту)", blank=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "2. Заказы"
        ordering = ['-created_at'] # Новые заказы всегда сверху

    def __str__(self):
        return f"Заказ #{self.id} - {self.get_status_display()}"
