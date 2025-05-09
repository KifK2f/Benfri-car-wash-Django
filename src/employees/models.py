from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
ROLE_CHOICES = [
    ('', 'Choisissez votre rôle'),
    (0, 'Accueil')
  , (1, 'Lavage')
]

SEX_CHOICES = [
    ('', 'Choisissez votre sexe'),
    (0, 'Masculin')
  , (1, 'Féminin')
]
class Employee(models.Model):
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Utilisateur") #UN user est lié à un employé et un employé est lie a un user
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    sex = models.PositiveSmallIntegerField(choices=SEX_CHOICES, verbose_name="Sexe", null=True, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, verbose_name="Rôle", null=True, blank=True)
    email = models.EmailField(unique=True, verbose_name="Email")
    birth_date = models.DateField(verbose_name="Date de naissance")
    phone_number = models.CharField( unique=True, max_length=8,verbose_name="Numéro de téléphone")
    address = models.CharField(max_length=255,verbose_name="Adresse")
    profile_picture = models.FileField(upload_to='photo_profil/', verbose_name="Photo de profil", blank=True, null=True) #Photo de profil
    last_updated = models.DateTimeField(auto_now=True , verbose_name="Dernière mise à jour", blank=True, null=True)     
    created_on = models.DateField(auto_now_add=True, verbose_name="Date de création" ,blank=True, null=True)     

    #Système de fidelite
    # editable = False pour empecher la modification
    performance_point = models.PositiveIntegerField(default=0 , editable=False, verbose_name="Points de performance")
    total_booking_registered = models.PositiveIntegerField(default=0 , editable=False, verbose_name="Nombre total de réservation enregistrée")
    total_vehicle_cleaned = models.PositiveIntegerField(default=0 , editable=False, verbose_name="Nombre total de vehicule lavé")
    
        # Champs supplémentaires pour le suivi par statut
    waiting_booking = models.PositiveIntegerField(default=0, editable=False, verbose_name="Réservations en attente")
    confirmed_booking = models.PositiveIntegerField(default=0, editable=False, verbose_name="Réservations confirmées")
    ongoing_booking = models.PositiveIntegerField(default=0, editable=False, verbose_name="Réservations en cours")
    finished_booking = models.PositiveIntegerField(default=0, editable=False, verbose_name="Réservations terminées")
    cancelled_booking = models.PositiveIntegerField(default=0, editable=False, verbose_name="Réservations annulées")
    paid_booking = models.PositiveIntegerField(default=0, editable=False, verbose_name="Réservations payées")


    
    class Meta:
        verbose_name = "Employé"
        constraints = [
            models.UniqueConstraint(
                fields=["user" ,"last_name", "first_name", "birth_date", "phone_number",], name="unique_employee"
            )
        ]   

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.last_name + self.first_name +self.phone_number)

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.phone_number}"


        # Recuperer une  url a partir de son nom => fonction reverse
        #Url ou diriger apres ceation de compte employee
    def get_absolute_url(self):
        return reverse('account-employee')
    
