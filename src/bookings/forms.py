from django import forms

from vehicles.models import Vehicle
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['washing_date', 'status', 'receptionist', 'cleaner', 'customer', 'vehicle', 'service',]
        widgets = {
            'washing_date': forms.DateTimeInput(attrs={ 'type': 'datetime-local' ,'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'receptionist': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'cleaner': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'customer': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'vehicle': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'service': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.none()

        if 'customer' in self.data:
            try:
                customer_id = int(self.data.get('customer'))
                self.fields['vehicle'].queryset = Vehicle.objects.filter(customer_id=customer_id).order_by('brand', 'model', 'color', 'registrationNumber')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['vehicle'].queryset = self.instance.customer.vehicle_set.order_by('brand', 'model', 'color', 'registrationNumber')
            

class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['receptionist', 'cleaner', 'customer', 'vehicle', 'service',]
        widgets = {
            # 'washing_date': forms.DateTimeInput(attrs={ 'type': 'datetime-local' ,'class': 'form-control'}),
            # 'status': forms.TextInput(attrs={'class': 'form-select', 'required': 'required'}),
            'receptionist': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'cleaner': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'customer': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'vehicle': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'service': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.none()

        if 'customer' in self.data:
            try:
                customer_id = int(self.data.get('customer'))
                self.fields['vehicle'].queryset = Vehicle.objects.filter(customer_id=customer_id).order_by('brand', 'model', 'color', 'registrationNumber')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['vehicle'].queryset = self.instance.customer.vehicle_set.order_by('brand', 'model', 'color', 'registrationNumber')
            
            

class BookingUpdateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['washing_date', 'status', 'receptionist', 'cleaner', 'customer', 'vehicle', 'service',]
        widgets = {
            'washing_date': forms.DateTimeInput(attrs={ 'type': 'datetime-local' ,'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'receptionist': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'cleaner': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'customer': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'vehicle': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'service': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.none()

        if 'customer' in self.data:
            try:
                customer_id = int(self.data.get('customer'))
                self.fields['vehicle'].queryset = Vehicle.objects.filter(customer_id=customer_id).order_by('brand', 'model', 'color', 'registrationNumber')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['vehicle'].queryset = self.instance.customer.vehicle_set.order_by('brand', 'model', 'color', 'registrationNumber')
            
            

# def clean_washing_date(self):
#         washing_date = self.cleaned_data.get('washing_date')
#         created_on = self.instance.created_on  # récupération de la date de création de la réservation existante

#         if washing_date and created_on and washing_date <= created_on:
#             raise forms.ValidationError("La date de lavage doit être postérieure à la date d'enregistrement.")
#         return washing_date
            
            
            
            
            
class ReservationWaitingToConfirmForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['washing_date', 'status', 'receptionist', 'cleaner', 'customer', 'vehicle', 'service',]
        widgets = {
            'washing_date': forms.DateTimeInput(attrs={ 'type': 'datetime-local' ,'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'receptionist': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'cleaner': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'customer': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'vehicle': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'service': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:  # Si c’est une modification
            self.fields['statut'].choices = [
                (0, 'En attente'),
                (1, 'Confirmée')
            ]
