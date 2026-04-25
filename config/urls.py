from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Главная страница - это наша CRM (админка)
    path('admin/', admin.site.urls),
    # Маршрут для бота ВКонтакте (webhook)
    path('bot/', include('crm.urls')),
]

# Раздача статики и медиа файлов в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
