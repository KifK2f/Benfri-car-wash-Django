from django.db import models
# from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify

class Service(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    base_price = models.IntegerField(verbose_name="Prix de base") # Pour afficher je fais -2000 franc CFA sur le prix de la voiture
    image = models.ImageField( blank=True, upload_to='services_lavage/')
    available_place = models.PositiveIntegerField(default=5 ,verbose_name="Nombre de places disponibles") 
    last_updated = models.DateTimeField(auto_now=True , verbose_name="Dernière mise à jour", blank=True, null=True)     
    created_on = models.DateField(auto_now_add=True, verbose_name="Date de création" ,blank=True, null=True)     


    class Meta:
        verbose_name = "Service"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

