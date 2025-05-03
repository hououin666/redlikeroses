

from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from cart.cart import Cart
from cart.forms import CartAddProductForm
from main.models import Product


# Create your views here.



@require_POST
def cart_add(request,product_id):
    cart = Cart(request)
    product = Product.objects.filter(id=product_id).first()
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        cart.add(product=product,
                 quantity=cleaned_data['quantity'],
                 update_quantity=cleaned_data['update'])
        return redirect('cart:cart_detail')

def cart_remove(request,product_id):
    cart = Cart(request)
    product = Product.objects.filter(id=product_id).first()
    cart.remove(product)
    return redirect('carts:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for product in cart:
        print(product)

    context = {
        'cart': cart
    }
    return render(request,'cart/cart_detail.html',context)
