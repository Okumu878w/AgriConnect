from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product

# UserCreationForm automatically handles password confirmation and hashing
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email') 


 # app/forms.py



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'location', 'price', 'quantity', 'phone_number', 'image']       