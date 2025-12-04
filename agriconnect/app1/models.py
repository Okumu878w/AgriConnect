from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# app/models.py


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('grains', 'Grains'),
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('livestock', 'Livestock'),
        ('tubers', 'Tubers'),
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
    


class SavedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product') # Prevents saving the same item twice

    def __str__(self):
        return f"{self.user.username} saved {self.product.name}"   
    







# 2. Paid Feature: Expert Consultation Request

class ConsultationRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crop_name = models.CharField(max_length=100)
    problem_description = models.TextField()
    # Allowing image uploads for diagnosis
    crop_image = models.ImageField(upload_to='consultations/') 
    phone_number = models.CharField(max_length=15)
    
    # Payment tracking
    is_paid = models.BooleanField(default=False)
    payment_reference = models.CharField(max_length=50, blank=True, null=True) # e.g., M-Pesa Code
    
    # Status of the advice
    status = models.CharField(max_length=20, default='Pending', choices=[('Pending', 'Pending'), ('Resolved', 'Resolved')])
    expert_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.crop_name}"   