from django.urls import path
from products.views import basket_add, basket_remove, products

app_name = 'products'

urlpatterns = [
    path('catalog/', products, name='index'),
    path('basket/add/<int:product_id>', basket_add, name='basket_add'),
    path('basket/remove/<int:basket_id>', basket_remove, name='basket_remove'),
]

