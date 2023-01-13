from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True) # field may be empty

    def __str__(self) -> str:
        return f'{self.name}'

class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    short_description = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(to='ProductCategory', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Product: {self.name} | Category: {self.category.name}'