from django.db import models

# Create your models here.


class SharedImage(models.Model):
    title = models.CharField(max_length = 600)
    description = models.CharField(max_length = 600)
    image = models.ImageField(upload_to='images')

class Malaria(models.Model):

    image = models.ImageField(upload_to='assets/images')
