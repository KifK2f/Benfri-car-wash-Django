from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from employees.models import Employee
from employees.forms import EmployeeForm

# Create your views here.
@method_decorator(login_required, name='dispatch')
class EmployeeHome(ListView):
    model = Employee
    context_object_name = "employees"
    template_name = "account-employee.html"
    
    def get_queryset(self):
        return Employee.objects.filter(user=self.request.user) #Filterer la sorti epour ne prendre que les Employee ayant un user = user actuellement connecté
    
@method_decorator(login_required, name='dispatch')
class EmployeeCreate(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "employees/employee_create.html"
    def form_valid(self, form):
        form.instance.user = self.request.user  # Associe l'utilisateur connecté à l'attribut user de ma classe Employee
        return super().form_valid(form)
    
@method_decorator(login_required, name='dispatch')
class EmployeeUpdate(UpdateView):
    model = Employee
    template_name = "employees/employee_edit.html"
    # fields = ['last_name', 'first_name', 'sex', 'role', 'email', 'birth_date', 'phone_number', 'address', 'profile_picture',]
    form_class = EmployeeForm


@method_decorator(login_required, name='dispatch')
class EmployeeDelete(DeleteView):
    model = Employee
    # Url où dirigé une fois qu'on a effectué la suppresion
    success_url = reverse_lazy("account-employee")
    context_object_name = "employee"
    