from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect, render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from products.models import Basket, Product, ProductCategory


class IndexView(TemplateView):
    template_name = 'products/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Store'
        return context


class ProductsListView(ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Store - Каталог'
        context['categories'] = ProductCategory.objects.all()
        return context

    def get_queryset(self):
        # аналог Product.objects.all()
        queryset = super().get_queryset()
        # в kwargs находятся все переменные из urls
        # используем метод гет, чтобы защитить от ненайденного ключа 
        # (default=None)
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset


# def products(request, category_id=None, page_number=1):
#     products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all() 
#     paginator = Paginator(products, per_page=2)
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'title': 'Store - Каталог',
#         'categories': ProductCategory.objects.all(),
#         'products': page_obj,
#     }
#     return render(request, 'products/products.html', context=context)


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
