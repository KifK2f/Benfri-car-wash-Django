from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from vehicles.models import Car, Motorcycle, Vehicle
from vehicles.forms import CarForm, MotorcycleForm
from customers.models import Customer
# from django.contrib import messages
# from django.shortcuts import redirect


# Create your views here.
# Les ListView
@method_decorator(login_required, name='dispatch')
class VehicleHome(ListView):
    model = Vehicle
    context_object_name = "vehicles"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = Car.objects.filter(customer=self.request.user.customer)
        # context['cars'] = Car.objects.all()
        context['motorcycles'] = Motorcycle.objects.filter(customer=self.request.user.customer)
        # context['motorcycles'] = Motorcycle.objects.all()
        return context

    def get_queryset(self):
        try:
            return Vehicle.objects.filter(customer=self.request.user.customer) #Filterer la sortie pour ne prendre que les customer ayant un user = user actuellement connecté    
        except:
            return Vehicle.objects.none()
        
        # return Vehicle.objects.filter(customer=self.request.user.customer) #Filterer la sortie pour ne prendre que les customer ayant un user = user actuellement connecté


    
    
@method_decorator(login_required, name='dispatch')
class CarHome(ListView):
    model = Car
    context_object_name = "cars"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['user'] = self.request.user.username
        context['customers'] = Customer.objects.all()
        return context
    def get_queryset(self):
        try:
            return Car.objects.filter(customer=self.request.user.customer) #Filterer la sortie pour ne prendre que les customer ayant un user = user actuellement connecté    
        except:
            return Car.objects.none()

@method_decorator(login_required, name='dispatch')
class MotorcycleHome(ListView):
    model = Motorcycle
    context_object_name = "motorcycles"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['user'] = self.request.user.username
        return context
    
    
    def get_queryset(self):
        try:
            return Motorcycle.objects.filter(customer=self.request.user.customer) #Filterer la sortie pour ne prendre que les customer ayant un user = user actuellement connecté    
        except:
            return Motorcycle.objects.none()

    
# Les DetailView    
@method_decorator(login_required, name='dispatch')
class CarDetail(DetailView):
    model = Car
    context_object_name = "car"
    
@method_decorator(login_required, name='dispatch')
class MotorcycleDetail(DetailView):
    model = Motorcycle
    context_object_name = "motorcycle"    


# # Les CreateView
# # Pour vehicule
@method_decorator(login_required, name='dispatch')
class VehicleCreate(CreateView):
    model = Vehicle
    template_name = "vehicles/vehicle_create.html"
    fields = ['brand', 'model', 'color', 'registrationNumber', 'registration_certificate', ]
    def form_valid(self, form):
        # form.instance.customer = self.request.user  # Associe l'utilisateur connecté
        form.instance.customer = Customer.objects.get(user=self.request.user)
        return super().form_valid(form)
    
    
    
# # Pour la voiture
@method_decorator(login_required, name='dispatch')
class CarCreate(CreateView):
    model = Car
    form_class = CarForm
    template_name = "vehicles/car_create.html"
    # fields = ['brand', 'model', 'color', 'registrationNumber', 'registration_certificate', 'nb_places', 'nb_doors',]
    def form_valid(self, form):
        form.instance.customer = self.request.user.customer  # Associe l'utilisateur connecté
        return super().form_valid(form)
    # def dispatch(self, request, *args, **kwargs):
    #         if not Customer.objects.filter(user=request.user).exists():
    #             messages.error(request, "Veuillez créer un compte client avant d'ajouter un véhicule.")
    #             return redirect('create-customer')  # Redirige vers la page de création de client
    #         return super().dispatch(request, *args, **kwargs)

    # def form_valid(self, form):
    #     form.instance.customer = Customer.objects.get(user=self.request.user)
    #     return super().form_valid(form)

    
# Pour la moto
@method_decorator(login_required, name='dispatch')
class MotorcycleCreate(CreateView):
    model = Motorcycle
    form_class = MotorcycleForm
    template_name = "vehicles/motorcycle_create.html"
    # fields = ['brand','model',  'color', 'registrationNumber', 'registration_certificate', 'capacity',]
    def form_valid(self, form):
        form.instance.customer = self.request.user.customer  # Associe l'utilisateur connecté
        return super().form_valid(form)
    # def dispatch(self, request, *args, **kwargs):
    #     if not Customer.objects.filter(user=request.user).exists():
    #         messages.error(request, "Veuillez créer un compte client avant d'ajouter une moto.")
    #         return redirect('create-customer')
    #     return super().dispatch(request, *args, **kwargs)

    # def form_valid(self, form):
    #     form.instance.customer = Customer.objects.get(user=self.request.user)
    #     return super().form_valid(form)
    
    
# Les UpdateView et DeleteView
# Modifier et suppprimer pour une voiture
@method_decorator(login_required, name='dispatch')
class CarUpdate(UpdateView):
    model = Car
    template_name = "vehicles/car_edit.html"
    # fields = ['brand', 'model', 'color', 'registrationNumber', 'registration_certificate', 'nb_places', 'nb_doors', ]
    form_class = CarForm


@method_decorator(login_required, name='dispatch')
class CarDelete(DeleteView):
    model = Car
    # Url où dirigé une fois qu'on a effectué la suppresion
    success_url = reverse_lazy("home-vehicle")
    # reverse_lazy car au moment où la classe sera mise en memoire Django n'aura pas resolu les chemins
    # En conclusion on utilise reverse_lazy quand on est dans le conexte de l'attribu d'une classe
    context_object_name = "car"
    
    
# Modifier et suppprimer pour une moto
@method_decorator(login_required, name='dispatch')
class MotorcycleUpdate(UpdateView):
    model = Motorcycle
    template_name = "vehicles/motorcycle_edit.html"
    # fields = ['brand', 'model', 'color', 'registrationNumber', 'registration_certificate', 'capacity',]
    form_class = MotorcycleForm



@method_decorator(login_required, name='dispatch')
class MotorcycleDelete(DeleteView):
    model = Motorcycle
    # Url où dirigé une fois qu'on a effectué la suppresion
    success_url = reverse_lazy("home-vehicle")
    # reverse_lazy car au moment où la classe sera mise en memoire Django n'aura pas resolu les chemins
    # En conclusion on utilise reverse_lazy quand on est dans le conexte de l'attribu d'une classe
    context_object_name = "motorcycle"