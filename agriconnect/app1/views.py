from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm
from django.db.models import Q
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
