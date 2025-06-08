from django.shortcuts import render

from cart.cart import Cart
from main.models import ProductVariation
from orders.forms import OrderCreateForm
from orders.models import OrderItem, Order


# Create your views here.



def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(data=request.POST, request=request)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'],
                                         color=item.get('color_obj') if item['color'] else None,
                                         size=item.get('size_obj') if item['size'] else None,
                                         metal_type=item.get('metal_type_obj' if item['metal_type'] else None),
                                         variation_key=item['variation_key']
                                         )
                product = ProductVariation.objects.filter(product = item['product']).first()
                product.quantity -= item['quantity']
                product.save()
            cart.clear()
            return render(request, 'orders/created_order.html', {'order': order})
    else:
        form = OrderCreateForm(request=request)
        return render(request,'orders/create_order.html', {'form': form})
    