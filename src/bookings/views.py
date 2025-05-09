from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from bookings.models import Booking
from bookings.forms import BookingForm, BookingCreateForm, BookingUpdateForm
from vehicles.models import Vehicle
from django.contrib import messages
from django.views.decorators.http import require_POST

# from django.shortcuts import redirect



# Create your views here.
@method_decorator(login_required, name='dispatch')
class BookingHome(ListView):
    model = Booking
    context_object_name = "bookings"
    template_name = "bookings/booking_list.html"

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['number_bookings_statut_0'] = Booking.objects.filter(status=0,customer=self.request.user.customer).count()
        context['number_bookings_statut_1'] = Booking.objects.filter(status=1,customer=self.request.user.customer).count()
        context['number_bookings_statut_2'] = Booking.objects.filter(status=2,customer=self.request.user.customer).count()
        context['number_bookings_statut_3'] = Booking.objects.filter(status=3,customer=self.request.user.customer).count()
        context['number_bookings_statut_4'] = Booking.objects.filter(status=4,customer=self.request.user.customer).count()
        context['number_bookings_statut_5'] = Booking.objects.filter(status=5,customer=self.request.user.customer).count()
        return context

    def get_queryset(self):
        try:
            return Booking.objects.filter(customer=self.request.user.customer) #Filterer la sortie pour ne prendre que les customer ayant un user = user actuellement connecté    
        except:
            return Booking.objects.none()
        
        
        
@method_decorator(login_required, name='dispatch')
class BookingHomeCleaner(ListView):
    model = Booking
    context_object_name = "bookings"
    template_name = "bookings/cleaner/booking_list.html"

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = self.request.user.employee
        if employee.role == 1:
            context['number_bookings_statut_0'] = Booking.objects.filter(status=0,cleaner=employee).count()
            context['number_bookings_statut_1'] = Booking.objects.filter(status=1,cleaner=employee).count()
            context['number_bookings_statut_2'] = Booking.objects.filter(status=2,cleaner=employee).count()
            context['number_bookings_statut_3'] = Booking.objects.filter(status=3,cleaner=employee).count()
            context['number_bookings_statut_4'] = Booking.objects.filter(status=4,cleaner=employee).count()
            context['number_bookings_statut_5'] = Booking.objects.filter(status=5,cleaner=employee).count()
        return context

    def get_queryset(self):
        try:
            employee = self.request.user.employee
            if employee.role == 1:
                return Booking.objects.filter(cleaner=employee)
            else:
                return Booking.objects.none()
        except:
            return Booking.objects.none()
        
        
        
        
        
@method_decorator(login_required, name='dispatch')
class BookingHomeReceptionist(ListView):
    model = Booking
    context_object_name = "bookings"
    template_name = "bookings/receptionist/booking_list.html"
    
       
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = self.request.user.employee
        if employee.role == 0:
            context['number_bookings_statut_0'] = Booking.objects.filter(status=0,receptionist=employee).count()
            context['number_bookings_statut_1'] = Booking.objects.filter(status=1,receptionist=employee).count()
            context['number_bookings_statut_2'] = Booking.objects.filter(status=2,receptionist=employee).count()
            context['number_bookings_statut_3'] = Booking.objects.filter(status=3,receptionist=employee).count()
            context['number_bookings_statut_4'] = Booking.objects.filter(status=4,receptionist=employee).count()
            context['number_bookings_statut_5'] = Booking.objects.filter(status=5,receptionist=employee).count()

        return context

    def get_queryset(self):
        try:
            employee = self.request.user.employee
            if employee.role == 0:
                return Booking.objects.filter(receptionist=employee)
            else:
                return Booking.objects.none()
        except:
            return Booking.objects.none()
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

    # def get_queryset(self):
    #     try:
    #         return Booking.objects.filter(receptionist=self.request.user.receptionist) #Filterer la sortie pour ne prendre que les customer ayant un user = user actuellement connecté    
    #     except:
    #         return Booking.objects.none()
        
    #     # return Booking.objects.filter(customer=self.request.user.customer) #Filterer la sortie pour ne prendre que les customer ayant un user = user actuellement connecté



# def recent_bookings(request):
#     bookings = Booking.objects.order_by('-created_on')[:5]  # ou [:10]
#     return render(request, 'bookings/recent_bookings.html', {'bookings': bookings})



@method_decorator(login_required, name='dispatch')
class BookingCreate(CreateView):
    model = Booking
    template_name = "bookings/booking_create.html"
    form_class = BookingCreateForm   
    
    def form_valid(self, form):
        booking = form.save()
        return redirect(booking.get_absolute_url_for_user(self.request.user))

    
    # def form_valid(self, form):
    #     # # form.instance.customer = self.request.user  # Associe l'utilisateur connecté
    #     # form.instance.customer = Customer.objects.get(user=self.request.user)
        
    #     # Assigner le receptionist (si l'utilisateur est un employé avec role=0)
    #     if self.request.user.employee.role == 0:  # 0 = rôle réceptionniste
    #         form.instance.receptionist = self.request.user.employee
                
    #     return super().form_valid(form)
    
    # def form_valid(self, form):
    #     if self.request.user.is_authenticated and hasattr(self.request.user, 'employee'):
    #         if self.request.user.employee.role == 0:  # réceptionniste
    #             form.instance.receptionist = self.request.user.employee
    #     return super().form_valid(form)

    
    
# @method_decorator(login_required, name='dispatch')
# class MotorcycleDetail(DetailView):
#     model = Booking
#     template_name = "bookings/booking_detail.html"
#     context_object_name = "motorcycle"   


@method_decorator(login_required, name='dispatch')
class BookingUpdate(UpdateView):
    model = Booking
    template_name = "bookings/booking_edit.html"
    # fields = ['brand', 'model', '', 'registrationNumber', 'registration_certificate', 'capacity',]
    form_class = BookingUpdateForm   



@method_decorator(login_required, name='dispatch')
class BookingDelete(DeleteView):
    model = Booking
    # Url où dirigé une fois qu'on a effectué la suppresion
    success_url = reverse_lazy("home-booking")
    # reverse_lazy car au moment où la classe sera mise en memoire Django n'aura pas resolu les chemins
    # En conclusion on utilise reverse_lazy quand on est dans le conexte de l'attribu d'une classe
    context_object_name = "booking"



def load_vehicles(request):
    customer_id = request.GET.get('customer')
    vehicles = Vehicle.objects.filter(customer_id=customer_id).order_by('brand', 'model', 'color', 'registrationNumber')
    return render(request, 'bookings/vehicle_dropdown_list_options.html', {'vehicles': vehicles})


# @require_POST
# @login_required
# def update_booking_status(request, booking_id):
#     booking = get_object_or_404(Booking, pk=booking_id)
    
#     if booking.status != 0:
#         messages.error(request, "Seules les réservations en attente peuvent être modifiées.")
#         return redirect('booking_detail', booking_id=booking.id)
    
#     new_status = request.POST.get('status')
#     if new_status not in ['1', '4']:
#         messages.error(request, "Statut invalide.")
#         return redirect('booking_detail', booking_id=booking.id)

#     booking.status = int(new_status)
#     booking.save()
#     messages.success(request, "Statut mis à jour avec succès.")
#     return redirect('booking_detail', booking_id=booking.id)