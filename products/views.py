from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render
from products.models import Basket, Product, ProductCategory


# Create your views here.
def index(request):
    context = {
        'title': 'Store'
    }
    return render(request, 'products/home.html', context=context)


def products(request, category_id=None):
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all() 
    context = {
        'title': 'Store - Каталог',
        'categories': ProductCategory.objects.all(),
        'products': products,
    }
    return render(request, 'products/products.html', context=context)


@login_required
# контролер действия
def basket_add(request, product_id):
    product = Product.objects.get(pk=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(pk=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
