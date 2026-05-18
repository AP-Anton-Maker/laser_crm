from django.db import models

class SystemLog(models.Model):
    LEVEL_CHOICES = [
        ('INFO', 'Инфо'),
        ('WARNING', 'Предупреждение'),
        ('ERROR', 'Ошибка'),
    ]
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='INFO')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Лог системы"
        verbose_name_plural = "Логи системы"
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.level}] {self.message[:50]}"
