from decimal import Decimal
from django.conf import settings
from store.models import Product

ID_DELIMITER = '|'


def get_id(product, mult):
    return str(product.id) + ID_DELIMITER + str(mult) + ID_DELIMITER + product.unit_of_measurement.unit


def get_id_components(item_id):
    id_parts = item_id.split(ID_DELIMITER)
    return id_parts[0], id_parts[1], id_parts[2]


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, price, quantity=1, update_quantity=False, mult=1):
        product_id = get_id(product, mult)
        price_per_pack = price * mult
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity, 'price': str(price_per_pack)}
        elif update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product, mult):
        product_id = get_id(product, mult)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        for item_id in self.cart:
            p_id, pack, unit = get_id_components(item_id)
            product = Product.objects.get(pk=p_id)

            item = self.cart[item_id]

            item['product'] = product
            item['packaging'] = pack
            item['unit'] = unit
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']

            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price'])*item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
