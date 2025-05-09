from django.template.defaultfilters import slugify
import uuid
from django.utils import timezone
from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from employees.models import Employee
from customers.models import Customer
from customers.models import Customer
from services.models import Service
from vehicles.models import Motorcycle
from vehicles.models import Vehicle

# Create your models here.
STATUS_CHOICES = [
    ('', 'Choisissez le statut'),
    (0, 'En attente')
    , (1, 'Confirmé')
    , (2, 'En cours')
    , (3, 'Terminé')
    , (4, 'Annulé')
    , (5, 'Payé')
]

class Booking(models.Model):
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    reference = models.CharField(max_length=20, unique=True)

    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure de création" ,blank=True, null=True) #Defiinir qu'une seule fois la date et heure de creation de la reservation    
    washing_date = models.DateTimeField(verbose_name="Date et heure de lavage", blank=True, null=True)  #Defiinir qu'une seule fois laDate et heure de lavage    
    
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, verbose_name="Statut", default=0)
    waiting_date = models.DateTimeField(null=True, blank=True,verbose_name="Date et heure lavage en attente")
    acceptance_date = models.DateTimeField(null=True, blank=True ,verbose_name="Date et heure lavage confirmé")
    ongoing_date = models.DateTimeField(null=True, blank=True, verbose_name="Date et heure lavage en cours")
    finishing_date = models.DateTimeField(null=True, blank=True, verbose_name="Date et heure lavage terminé")
    cancelling_date = models.DateTimeField(null=True, blank=True, verbose_name="Date et heure lavage annulé")
    payment_date = models.DateTimeField(null=True, blank=True, verbose_name="Date et heure lavage payé")
    
    receptionist = models.ForeignKey(Employee, on_delete=models.CASCADE, limit_choices_to={'role': 0}, related_name='reservations_enregistres', verbose_name="Agent d'accueil") # Agent d'accueil
    cleaner = models.ForeignKey(Employee, on_delete=models.CASCADE,  limit_choices_to={'role': 1}, related_name='reservations_realises', verbose_name="Laveur") # Agent de laveur
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Client")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name="Vehicule")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Service")

    price = models.IntegerField(verbose_name="Prix du lavage")
    
    
    def clean(self):
        # Vérifie si le véhicule est une moto
        is_motorcycle = Motorcycle.objects.filter(pk=self.vehicle.pk).exists()

        # Vérifie si le service est différent de "Lavage extérieur"
        if is_motorcycle and self.service.name != 'Lavage extérieur':
            raise ValidationError("Les motos ne peuvent être lavées qu'avec le service 'Lavage extérieur'.")



    def save(self, *args, **kwargs):
        
        # # Appliquer le prix du service
        # self.price = self.service.base_price

        # # Réduction si le véhicule est une moto
        # if isinstance(self.vehicle, Motorcycle):
        #     self.price -= 2000  # réduction de 2000 franc CFA 
        
        now = timezone.now()


        # Enregistrer l'ancien statut pour détecter un changement
        old_status = None
        if self.pk:
            old = Booking.objects.get(pk=self.pk)
            old_status = old.status

        # Date correspondante selon le nouveau statut
  
        is_new = self.pk is None
            
                
        if self.status == 0 and not self.waiting_date:
            self.waiting_date = timezone.now()
        elif self.status == 1 and not self.acceptance_date:
            self.acceptance_date = timezone.now()
        elif self.status == 2 and not self.ongoing_date:
            self.ongoing_date = timezone.now()
        elif self.status == 3 and not self.finishing_date:
            self.finishing_date = timezone.now()
        elif self.status == 4 and not self.cancelling_date:
            self.cancelling_date = timezone.now()
        elif self.status == 5 and not self.payment_date:
            self.payment_date = timezone.now()
            
        if not self.reference:
            self.reference = f"RES-{uuid.uuid4().hex[:4].upper()}"
        
        if not self.slug:
            self.slug = slugify(self.reference + self.customer.user.username )
            
        self.price = self.service.base_price

            # Réduction si le véhicule est une moto
        # if isinstance(self.vehicle, Motorcycle) and self.service.name == 'Lavage extérieur':
        #     self.price -= 2000
        # if Motorcycle.objects.filter(pk=self.vehicle.pk).exists() :
        #     self.price = null
        
        if Motorcycle.objects.filter(pk=self.vehicle.pk).exists() and self.service.name == 'Lavage extérieur':
            self.price -= 2000
            
        is_new = self.pk is None  # Vérifie si la réservation est nouvelle

            
        super().save(*args, **kwargs)

        # Si nouvelle réservation
        if is_new and self.customer:
            self.customer.total_booking += 1
            self.customer.save()

        # Si nouvelle réservation et statut payé ou annulé
        if is_new and self.receptionist and self.status in [4, 5]:
            self.receptionist.total_booking_registered += 1
            self.receptionist.save()

        # Si nouvelle réservation terminée => lavage effectué
        if is_new and self.status == 3:
            # for cleaner in self.cleaner.all():
            #     cleaner.total_vehicle_cleaned += 1
            #     cleaner.save()
            if self.cleaner:
                self.cleaner.total_vehicle_cleaned += 1
                self.cleaner.save()


        # Mise à jour des compteurs de statuts pour le réceptionniste
        if self.receptionist and old_status != self.status:
            if old_status == 0:
                self.receptionist.waiting_booking -= 1
            elif old_status == 1:
                self.receptionist.confirmed_booking -= 1
            elif old_status == 2:
                self.receptionist.ongoing_booking -= 1
            elif old_status == 3:
                self.receptionist.finished_booking -= 1
            elif old_status == 4:
                self.receptionist.cancelled_booking -= 1
            elif old_status == 5:
                self.receptionist.paid_booking -= 1

            if self.status == 0:
                self.receptionist.waiting_booking += 1
            elif self.status == 1:
                self.receptionist.confirmed_booking += 1
            elif self.status == 2:
                self.receptionist.ongoing_booking += 1
            elif self.status == 3:
                self.receptionist.finished_booking += 1
            elif self.status == 4:
                self.receptionist.cancelled_booking += 1
            elif self.status == 5:
                self.receptionist.paid_booking += 1

            self.receptionist.save()            
          

    def status_durations(self):
        durations = []
        transitions = [
            ("En attente", self.waiting_date),
            ("Confirmé", self.acceptance_date),
            ("En cours", self.ongoing_date),
            ("Terminé", self.finishing_date),
            ("Annulé", self.cancelling_date),
            ("Payé", self.payment_date),
        ]

        for i in range(1, len(transitions)):
            prev_label, prev_time = transitions[i - 1]
            curr_label, curr_time = transitions[i]
            if prev_time and curr_time:
                delta = curr_time - prev_time
                hours = delta.total_seconds() // 3600
                minutes = (delta.total_seconds() % 3600) // 60
                durations.append((f"{prev_label} → {curr_label}", f"{int(hours)}h {int(minutes)}min"))

        return durations

    def __str__(self):
        return f"Réservation #{self.id} - {self.customer} - {self.get_status_display()}"
    
    def get_absolute_url(self,user):
        return reverse('home-booking')
    
    def get_absolute_url_for_user(self, user):
        if hasattr(user, 'employee'):
            if user.employee.role == 0:
                return reverse('home-booking-receptionist')
            elif user.employee.role == 1:
                return reverse('home-booking-cleaner')
        return reverse('home-booking')

    
    # def get_absolute_url(self):
    #     if request.user.employee.role == 0:
    #         return reverse('home-a')
    #     elif request.user.employee.role == 1:
    #         return reverse('home-b')
    #     else:
    #         return reverse('home-booking')

    @property
    def time_from_confirmed_to_ongoing(self):
        if self.ongoing_date and self.acceptance_date:
            return self.ongoing_date - self.acceptance_date
        return None