from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib import messages
# Create your views here.
def home(request):
    return render (request,'app1/marketplace.html')


def advises(request):
    return render (request,'app1/advisory.html')



def sellers(request):
    return render (request,'app1/sellerdashboard.html')



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

