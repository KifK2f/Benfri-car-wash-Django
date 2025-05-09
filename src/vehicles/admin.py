from django.contrib import admin
from .models import Vehicle, Car, Motorcycle

# Register your models here.
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "color", "registrationNumber", "registration_certificate", "last_updated", "created_on",)

admin.site.register(Vehicle, VehicleAdmin)

class CarAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "color", "registrationNumber", "registration_certificate", "nb_places", "nb_doors", "last_updated", "created_on",)

admin.site.register(Car, CarAdmin)

class MotorcycleAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "color", "registrationNumber", "registration_certificate",  "capacity", "last_updated", "created_on",)

admin.site.register(Motorcycle, MotorcycleAdmin)