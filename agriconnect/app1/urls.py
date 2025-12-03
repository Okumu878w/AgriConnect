from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
   path('marketplace',views.marketplace,name='home'),
   path('sellerdash',views.seller_dashboard,name='seller'),
   path('advisory',views.advises,name='advise'),
   path('login', auth_views.LoginView.as_view(template_name='app1/loggy.html'), name='login'),
    path('signup', views.signup_view, name='signup'),
    path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('search/', views.search_products, name='search_results'),
    path('addproduct',views.post_product,name='add'),
    path('update/<str:pk>',views.update,name='update'),
    path('delete/<str:pk>',views.delete,name='delete')



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)