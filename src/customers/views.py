from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from customers.models import Customer
from customers.forms import CustomerForm
from vehicles.models import Vehicle
from bookings.models import Booking

# Create your views here.
@method_decorator(login_required, name='dispatch')
class CustomerHome(ListView):
    model = Customer
    context_object_name = "customers"
    template_name = "account-customer.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['vehicles'] = Vehicle.objects.filter(customer=self.request.user.customer)
            context['bookings'] = Booking.objects.filter(customer=self.request.user.customer)
        except:
            context['vehicles'] = Vehicle.objects.none()
            context['bookings'] = Booking.objects.none()

        # context['vehicles'] = Vehicle.objects.filter(customer=self.request.user.customer)
        return context
    
    
    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user) #Filterer la sorti epour ne prendre que les customer ayant un user = user actuellement connecté
    
@method_decorator(login_required, name='dispatch')
class CustomerCreate(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "customers/customer_create.html"
    def form_valid(self, form):
        form.instance.user = self.request.user  # Associe l'utilisateur connecté à l'attribut user de ma classe Customer
        return super().form_valid(form)
    
@method_decorator(login_required, name='dispatch')
class CustomerUpdate(UpdateView):
    model = Customer
    template_name = "customers/customer_edit.html"
    # fields = ['last_name', 'first_name', 'sex', 'email', 'birth_date', 'phone_number', 'address', 'profile_picture',]
    form_class = CustomerForm


@method_decorator(login_required, name='dispatch')
class CustomerDelete(DeleteView):
    model = Customer
    # Url où dirigé une fois qu'on a effectué la suppresion
    success_url = reverse_lazy("account-customer")
    context_object_name = "customer"
 