from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
SEX_CHOICES = [
    ('', 'Choisissez votre sexe'),
    (0, 'Masculin')
  , (1, 'Féminin')
]
class Customer(models.Model):
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Utilisateur") #UN user est lié à un client et un client est lie a un user
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    sex = models.PositiveSmallIntegerField(choices=SEX_CHOICES, verbose_name="Sexe", null=True, blank=True)
    email = models.EmailField(unique=True, verbose_name="Email")
    birth_date = models.DateField(verbose_name="Date de naissance")
    phone_number = models.CharField( unique=True, max_length=8,verbose_name="Numéro de téléphone")
    address = models.CharField(max_length=200,verbose_name="Adresse")
    profile_picture = models.FileField(upload_to='photo_profil/', verbose_name="Photo de profil", blank=True, null=True) #Photo de profil
    last_updated = models.DateTimeField(auto_now=True , verbose_name="Dernière mise à jour", blank=True, null=True)     
    created_on = models.DateField(auto_now_add=True, verbose_name="Date de création" ,blank=True, null=True)     

    #Système de fidelite
    # editable = False pour empecher la modification
    loyality_point = models.PositiveIntegerField(default=0 , editable=False, verbose_name="Points de fidelité")
    total_vehicle = models.PositiveIntegerField(default=0 , editable=False, verbose_name="Nombre total de vehicule")
    total_booking = models.PositiveIntegerField(default=0 , editable=False, verbose_name="Nombre total de réservation")
    
    
    class Meta:
        verbose_name = "Client"
        constraints = [
            models.UniqueConstraint(
                fields=["user" ,"last_name", "first_name", "birth_date", "phone_number",], name="unique_customer"
            )
        ]   

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.last_name + self.first_name +self.phone_number )
            
        # Augmenter le nombre de point de fidelite au fur et a mesure que le nombre de reservation augmente    
        if self.pk:  # Si l'objet existe déjà en BDD
            old = Customer.objects.get(pk=self.pk)
            if self.total_booking > old.total_booking:
                self.loyality_point += 1 

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.phone_number}"


        # Recuperer une  url a partir de son nom => fonction reverse
        #Url ou diriger apres ceation de compte client
    def get_absolute_url(self):
        return reverse('account-customer')
    
