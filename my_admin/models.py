from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import MinValueValidator





class Customer(models.Model):
    mobile_number = models.CharField(max_length=15)
    age = models.IntegerField()
    gender = models.CharField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.age} {self.gender}"



class Product(models.Model):
    product_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    available = models.BooleanField(blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return f"{self.product_name}"