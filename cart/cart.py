from decimal import Decimal

from django.conf import settings

from main.models import Product, Color, Size, MetalType


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False, color=None, size=None, metal_type=None):

        variation_key = f'{product.id}_{color.id if color else 'none'}_{size.id if size else 'none'}_{metal_type.id if metal_type else 'none'}'


        if variation_key not in self.cart:
            self.cart[variation_key] = {
                'product_id': str(product.id),
                'quantity': 0,
                'price': str(product.price),
                'color': str(color.id) if color else None,
                'size': str(size.id) if size else None,
                'metal_type': str(metal_type.id) if metal_type else None,
            }
        if update_quantity:
            self.cart[variation_key]['quantity'] = quantity
        else:
            self.cart[variation_key]['quantity'] +=quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self,product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):

        products_ids = {int(item['product_id'])  for item in self.cart.values()}
        products = Product.objects.in_bulk(products_ids)

        colors_ids = {int(item['color']) for item in self.cart.values() if item['color'] is not None}
        sizes_ids = {int(item['size'])  for item in self.cart.values() if item['size'] is not None}
        metal_types_ids = {int(item['metal_type']) for item in self.cart.values() if item['metal_type'] is not None}

        colors = Color.objects.in_bulk(colors_ids) if colors_ids else {}
        sizes = Size.objects.in_bulk(sizes_ids) if sizes_ids else {}
        metal_types = MetalType.objects.in_bulk(metal_types_ids) if metal_types_ids else {}

        cart = self.cart.copy()

        for variation_key, item in cart.items():
            product_id = int(item['product_id'])
            item['product'] = products.get(product_id)

            if not ['product']:
                continue
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            item['variation_key'] = variation_key

            if item['color']:
                item['color_obj'] = colors.get(int(item['color']))
            if item['size']:
                item['size_obj'] = sizes.get(int(item['size']))
            if item['metal_type']:
                item['metal_type_obj'] = metal_types.get(int(item['metal_type']))

            yield item



    def __len__(self):
        #Размер корзины
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        #Итоговая сумма корзины
        print('aa')
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified=True




