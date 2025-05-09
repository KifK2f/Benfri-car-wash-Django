from django import forms

from employees.models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['last_name', 'first_name', 'sex', 'role','email', 'birth_date', 'phone_number', 'address', 'profile_picture',]
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'sex': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'role': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': 'required'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'JJ-MM-AAAA' , 'class': 'form-control', 'required': 'required'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
