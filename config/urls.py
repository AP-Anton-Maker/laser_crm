from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Главная страница - это наша CRM (админка)
    path('', admin.site.urls),
]

# Чтобы мы могли просматривать чеки и макеты через браузер
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
