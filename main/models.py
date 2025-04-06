from tkinter.constants import CASCADE

from django.db import models
from django.db.models import PositiveIntegerField

# Create your models here.


class Color(models.Model):
    color = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.color


class Size(models.Model):
    size = models.PositiveIntegerField()

    def __str__(self):
        return str(self.size)


class MetalType(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)
    carat = models.PositiveIntegerField()



    def __str__(self):
        return f"{self.carat}ct {self.color} {self.name}"



class ProductType(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

0
class Product(models.Model):
    image = models.ImageField(upload_to='images', blank=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    available = models.BooleanField(default=True)
    color = models.ManyToManyField(to=Color,through='ProductVariation',blank=True)
    sizes = models.ManyToManyField(to=Size, through='ProductVariation')
    metal_type = models.ManyToManyField(to=MetalType, through='ProductVariation')
    product_type = models.ForeignKey(to=ProductType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7,decimal_places=2,)

    class Meta:
        verbose_name ='product'
        verbose_name_plural = 'products'
        ordering =['name']

    def __str__(self):
        return f"{self.name} | {self.product_type}"



class ProductVariation(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    color = models.ForeignKey(to=Color,on_delete=models.CASCADE, null=True,blank=True)
    size = models.ForeignKey(to=Size, on_delete=models.CASCADE,null=True, blank=True)
    metal_type = models.ForeignKey(to=MetalType,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    available = models.BooleanField(default=True)



    class Meta:
        unique_together = ['product', 'color', 'size', 'metal_type']

    def __str__(self):
        return f"{self.product.product_type.name} --- {self.metal_type.carat}ct {self.metal_type.color} {self.metal_type.name} --- {self.product.name} {self.color} {self.size}"







