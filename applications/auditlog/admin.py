from django.contrib import admin
#
from .models import AuditLog
# Register your models here.


class AudiLogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'action',
        'ip_address',
    )

admin.site.register(AuditLog, AudiLogAdmin)