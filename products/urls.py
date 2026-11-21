from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.CampusLoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/profile/', views.account, name='account'),
    path('products/new/', views.product_edit, name='product_create'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
]
