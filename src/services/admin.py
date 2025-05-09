from django.contrib import admin
from services.models import Service

# Register your models here.
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "image", "created_on", "last_updated",)


admin.site.register(Service, ServiceAdmin)