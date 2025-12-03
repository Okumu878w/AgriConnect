from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# app/models.py


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('grains', 'Grains'),
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
    ]

    # This links the product to the user currently logged in
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.CharField(max_length=50) # e.g., "50 bags"
    phone_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='product_images/') # Requires Pillow installed

    def __str__(self):
        return self.name