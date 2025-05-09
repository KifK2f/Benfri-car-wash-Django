from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from customers.models import Customer

class Vehicle(models.Model):
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    
    brand = models.CharField(max_length=70, verbose_name="Marque") #marque d'une vehicule
    model = models.CharField(max_length=70, verbose_name="Modele") #model d'une vehicule
    color = models.CharField(max_length=70, verbose_name="Couleur") #couleur d'une vehicule
    registrationNumber = models.CharField(max_length=10, verbose_name="Immatriculation",unique=True) #immatriculation
    registration_certificate = models.FileField(upload_to='cartes_grises/') #Carte grise
    last_updated = models.DateTimeField(auto_now=True , verbose_name="Dernière mise à jour", blank=True, null=True)     
    created_on = models.DateField(auto_now_add=True, verbose_name="Date de création" ,blank=True, null=True)     


    # Un client peut avoir 1 ou plusieurs  vehicule(voitures ou moto)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    # customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

        
    class Meta:
        verbose_name="Véhicule"
        constraints = [
            models.UniqueConstraint(
                fields=["brand", "model", "registrationNumber", "color"], name="unique_vehicle"
            )
        ]    

            
    def __str__(self):
        return self.brand + " " + self.model + " " + self.registrationNumber
    
        
        # Recuperer une  url a partir de son nom => fonction reverse
    def get_absolute_url(self):
        return reverse('home-vehicle')
    
    @property
    def customer_or_default(self):
        return self.customer.username if self.customer else "Client inconnu"
    
    
class Car(Vehicle):
    nb_places = models.PositiveIntegerField(default=5, verbose_name="Nombre de places") #Nombre de places conducteur y compris
    nb_doors = models.PositiveIntegerField(default=4,  verbose_name="Nombre de portes") #Nombre de portes
    
    class Meta:
        verbose_name = 'Voiture'
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.brand+ self.model+self.registrationNumber)
            
        is_new = self.pk is None # Verifier si c'est une creation
        super().save(*args, **kwargs)
        if is_new and self.customer:
            self.customer.total_vehicle += 1
            self.customer.save()  # Mise à jour du client   
    
    def __str__(self):
        return super().__str__() + " " + str(self.nb_doors)+ " portes" + " " + str(self.nb_places) + " places"
    
    
class Motorcycle(Vehicle):
    capacity = models.IntegerField(verbose_name= "Capacite du moteur") #capacite du moteur
    
    class Meta:
        verbose_name = 'Moto'
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.brand+ self.model)
            
        is_new = self.pk is None # Verifier si c'est une creation
        super().save(*args, **kwargs)
        if is_new and self.customer:
            self.customer.total_vehicle += 1
            self.customer.save()  # Mise à jour du client   
    
    def __str__(self):
        return super().__str__() + " " + str(self.capacity)

