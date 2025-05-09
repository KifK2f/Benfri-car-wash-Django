from django.contrib import admin
from .models import Employee

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("user", "last_name", "first_name","sex", "role", "email", "birth_date", "phone_number", "address", "profile_picture", "last_updated", "created_on",)

admin.site.register(Employee, EmployeeAdmin)
