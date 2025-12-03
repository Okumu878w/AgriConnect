from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
   path('marketplace',views.home,name='home'),
   path('sellerdash',views.sellers,name='seller'),
   path('advisory',views.advises,name='advise'),
   path('login', auth_views.LoginView.as_view(template_name='app1/loggy.html'), name='login'),
    

    path('signup', views.signup_view, name='signup'),
    path('logout', auth_views.LogoutView.as_view(next_page='loggy.html'), name='logout'),
]