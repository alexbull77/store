from django.contrib import admin
from products.models import Basket, Product, ProductCategory

admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAmdin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'quantity', 'category']
    fields = ('name', 'description', ('price', 'quantity'), 'category', 'image')
    readonly_fields = ('description',)
    search_fields = ('name', 'id')
    ordering = ['name', 'price', 'quantity']


# можно применять если есть ForeignKey связь
class BasketAdmin(admin.TabularInline):
    model = Basket
    readonly_fields = ('created_timestamp',)
    fields = ['product', 'quantity', 'created_timestamp']
    extra = 0
