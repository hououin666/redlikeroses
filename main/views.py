from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from cart.forms import CartAddProductForm
from main.models import ProductVariation, Color, MetalType, Size, Product, ProductType


# Create your views here.




def index(request):

    products = Product.objects.all()

    context = {
        'products': products,
    }
    return render(request, 'index/index.html', context)


def products_list(request,product_type_id=None):
    categories = ProductType.objects.all()
    if product_type_id:
        products_queryset = Product.objects.filter(product_type_id=product_type_id, available=True).order_by('name')
    else:
        products_queryset = Product.objects.filter(available=True).order_by('name')

    paginator = Paginator(products_queryset,8)
    page_number = request.GET.get('page', 1)
    try:
        products = paginator.page(int(page_number))
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'products/products_list.html', context)


def product_detail(request, product_id):
    product = Product.objects.filter(id=product_id).last()
    cart_product_form = CartAddProductForm()
    context = {
        'product': product,
        'cart_product_form': cart_product_form

    }
    return render(request, 'products/product_detail.html', context)



