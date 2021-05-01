from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class userInfo(models.Model):
    firstname = models.CharField(max_length=50, null=True, verbose_name="İsim")
    lastname = models.CharField(max_length=50, null=True, verbose_name="Soyisim")
    address = models.TextField(verbose_name="Adres")
    email = models.EmailField(max_length=70, blank=True, null=True, unique=True, verbose_name="Email")
    phone = PhoneNumberField(null=True, blank=False, unique=True, verbose_name="Telefon")

    def __str__(self):
        return self.firstname + " " + self.lastname

    class Meta:
        ordering = ['id']
