from django.contrib import admin

from main.models import Product, MetalType, ProductType, Size, ProductVariation, Color

# Register your models here.



admin.site.register(MetalType)
admin.site.register(ProductType)
admin.site.register(Size)
admin.site.register(Color)


class ProductVariationInLine(admin.TabularInline):
    model = ProductVariation
    fields = ['product','size','color','metal_type','quantity','available']
    extra = 4

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_type','name','description','price','available']
    list_filter = ['product_type', 'available']
    inlines = [ProductVariationInLine]

admin.site.register(Product,ProductAdmin)


