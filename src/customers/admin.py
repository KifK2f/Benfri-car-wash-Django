from django.contrib import admin
from .models import Customer

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "last_name", "first_name", "sex", "email", "birth_date", "phone_number", "address", "profile_picture", "last_updated", "created_on",)

admin.site.register(Customer, CustomerAdmin)
