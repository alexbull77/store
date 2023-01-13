from django.urls import path
from products.views import products

app_name = 'products'

urlpatterns = [
    path('catalog/', products, name='index'),
]

