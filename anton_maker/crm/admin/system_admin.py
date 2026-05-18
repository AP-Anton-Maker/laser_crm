from django.contrib import admin
from unfold.admin import ModelAdmin
from crm.models import SystemLog

@admin.register(SystemLog)
class SystemLogAdmin(ModelAdmin):
    list_display = ('level', 'message', 'created_at')
    list_filter = ('level', 'created_at')
    readonly_fields = ('level', 'message', 'created_at')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
