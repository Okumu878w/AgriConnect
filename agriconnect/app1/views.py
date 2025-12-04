from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Product, SavedItem
import json
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient
from .models import  ConsultationRequest

# Create your views here.


def advises(request):
    return render (request,'app1/advisory.html')







def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # By default, form.save() creates a user with is_staff=False
            # 1. Add a success message to show on the login page
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Please log in.')
            
            # 2. Redirect specifically to the 'login' URL name
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'app1/signny.html', {'form': form})

# app/views.py



# 1. VIEW FOR POSTING PRODUCT
@login_required
def post_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  # Assign the logged-in user as seller
            product.save()
            return redirect('home') 
    else:
        form = ProductForm()
    return render(request, 'app1/add.html', {'form': form})

@login_required
def update(request, pk):
    product = get_object_or_404(Product, id=pk)
    if product.seller != request.user:
        return redirect('home') 

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save() 
            return redirect('home') 
    else:
        form = ProductForm(instance=product) 

    return render(request, 'app1/update.html', {'form': form})
def delete(request,pk):
    form=Product.objects.get(id=pk)
    if request.method=="POST":
        form.delete()
        return redirect("home")
    return render(request,'app1/delete.html')

# 2. MARKETPLACE VIEW (Shows ALL products)
def marketplace(request):
    products = Product.objects.all() # Fetch everything
    return render(request, 'app1/marketplace.html', {'products': products})

# 3. SELLER DASHBOARD VIEW (Shows ONLY logged-in user's products)
@login_required
def seller_dashboard(request):
    # Filter products where seller == current user
    user_products = Product.objects.filter(seller=request.user)
    return render(request, 'app1/sellerdashboard.html', {'products': user_products})


def search_products(request):
    # Get the query, default to empty string
    query = request.GET.get('q', '') 
    
    # Start with an empty list
    results = []

    # Only filter if the user actually typed something
    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(category__icontains=query) | 
            Q(location__icontains=query)
        ).distinct()

    
    
    

    return render(request, 'app1/search_results.html', {'products': results, 'query': query})


@login_required
@require_POST
def toggle_save(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        product = Product.objects.get(id=product_id)
        
        # Check if already saved
        saved_item, created = SavedItem.objects.get_or_create(user=request.user, product=product)
        
        if not created:
            # If it already existed, we delete it (toggle off)
            saved_item.delete()
            action = 'removed'
        else:
            action = 'added'

        # Return the new total count of saved items
        count = SavedItem.objects.filter(user=request.user).count()
        
        return JsonResponse({
            'status': 'ok', 
            'action': action, 
            'count': count,
            'product_name': product.name,
            'product_price': str(product.price),
            'product_image': product.image.url if product.image else '' ,
            'product_phone': product.phone_number,
            'product_location': product.location
        })
        
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

#commenting this because am not using it,i wrote it before i changed the idea
'''def payment(request):
    context={}
    cl = MpesaClient()
    account_reference = 'Agriconnect'
    transaction_desc = 'Description'
    callback_url = 'https://api.darajambili.com/express-payment'
    
    if request.method=="POST":
        phoneNumber=request.POST.get('phoneNumber')
        amount=int(request.POST.get('amount'))
        
        response = cl.stk_push(phoneNumber, amount, account_reference, transaction_desc, callback_url)
        context={"response":response}
    return render(request,'app1/mpesapayment.html',context)'''






'''def index(request):
    cl = MpesaClient()
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = '07xxxxxxxx'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https://api.darajambili.com/express-payment'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)'''


# Assuming you use a form class, but we can do it manually for simplicity here

from django_daraja.mpesa.core import MpesaClient 

def advisory_view(request):
    # --- 1. HANDLE FORM SUBMISSION & PAYMENT (POST) ---
    if request.method == 'POST':
        # Get form data
        crop = request.POST.get('crop_name')
        desc = request.POST.get('description')
        phone = request.POST.get('phone')
        image = request.FILES.get('crop_image')
        amount = 50  # Fixed fee
        
        # Save to database (Marked as Unpaid initially)
        consultation = ConsultationRequest.objects.create(
            user=request.user,
            crop_name=crop,
            problem_description=desc,
            phone_number=phone,
            crop_image=image,
            is_paid=False 
        )
        
        # Trigger M-Pesa STK Push
        client = MpesaClient()
        account_reference = 'Agriconnect'
        transaction_desc = f'Consultation for {crop}'
        callback_url = 'https://api.darajambili.com/express-payment' # Use your actual callback URL here
        
        try:
            # Send payment prompt to user's phone
            response = client.stk_push(phone, amount, account_reference, transaction_desc, callback_url)
            print(response) # For debugging
            
            messages.success(request, f"STK Push sent to {phone}. Please enter your PIN to complete the payment of KES {amount}.")
            
        except Exception as e:
            # If payment fails, we still saved the request, but warn the user
            messages.error(request, f"Request saved, but payment failed to start: {str(e)}")
        
        # Redirect to avoid resubmitting form on refresh
        return redirect('advise') 

    # --- 2. FETCH HISTORY & RENDER PAGE (GET) ---
    # This part runs when the page loads normally
    
    # Get all requests made by this user, ordered by newest first
    user_consultations = ConsultationRequest.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'consultations': user_consultations
    }
    
    
    return render(request, 'app1/advisory.html', context)

def consults(request):
    return render(request)