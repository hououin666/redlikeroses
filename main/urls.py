from django.contrib import admin
from django.urls import path

from main.views import index, product_detail, products_list

app_name = 'main'

urlpatterns = [

    path('', index, name='index'),
    path('products/catalog', products_list, name='products_list'),
    path('products/catalog/<int:product_type_id>', products_list, name='category_list'),
    path('products/<int:product_id>', product_detail, name='product_detail'),


]



