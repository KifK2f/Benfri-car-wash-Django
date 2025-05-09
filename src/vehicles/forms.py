from django import forms
from .models import Car, Motorcycle

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'color', 'registrationNumber', 'registration_certificate', 'nb_places', 'nb_doors',]
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'registrationNumber': forms.TextInput(attrs={'class': 'form-control'}),
            'registration_certificate': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'nb_places': forms.NumberInput(attrs={'class': 'form-control'}),
            'nb_doors': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class MotorcycleForm(forms.ModelForm):
    class Meta:
        model = Motorcycle
        fields = ['brand','model',  'color', 'registrationNumber', 'registration_certificate', 'capacity',]
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'registrationNumber': forms.TextInput(attrs={'class': 'form-control'}),
            'registration_certificate': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
        }
