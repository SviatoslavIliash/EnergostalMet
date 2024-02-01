from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import Product
from .cart import Cart
from .forms import CartAddProductForm


def response_prices(cart):
    total_price = cart.get_total_price()
    total_price_d, d = cart.total_price_discount(total_price)
    response = {"Total": total_price, "Total_discount": total_price_d,
                "Discount": d}
    return response


@require_POST
def cart_add(request, product_slug):
    cart = Cart(request)
    product = get_object_or_404(Product, slug=product_slug)
    price = product.price
    form = CartAddProductForm(request.POST)
    if "price" in request.POST:
        price = Decimal(request.POST["price"])
    mult = 1
    if "multiplier" in request.POST:
        mult = int(request.POST["multiplier"])

    if form.is_valid():
        cd = form.cleaned_data
        upd = cd["update"]
        quantity = cd['quantity']
    else:
        # default values
        upd = False
        quantity = 1

    cart.add(product=product, price=price, quantity=quantity, update_quantity=upd, mult=mult)

    response = response_prices(cart)
    return JsonResponse(response)


@require_POST
def cart_remove(request, product_slug):
    cart = Cart(request)
    mult = 1
    if "multiplier" in request.POST:
        mult = int(request.POST["multiplier"])
    product = get_object_or_404(Product, slug=product_slug)
    cart.remove(product, mult)
    response = response_prices(cart)
    response["Deleted"] = True
    return JsonResponse(response)


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                                        initial={
                                            'quantity': item['quantity'],
                                            'update': True
                                        })

    discount_total_price, discount = cart.total_price_discount()

    return render(request, 'cart/detail.html',
                  {'cart': cart, 'discount_total_price': discount_total_price, 'discount': discount})
