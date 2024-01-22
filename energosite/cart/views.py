from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import Product
from .cart import Cart
from .forms import CartAddProductForm


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
    response = {}
    if form.is_valid():
        cd = form.cleaned_data
        upd = cd["update"]
        cart.add(product=product, price=price, quantity=cd['quantity'], update_quantity=upd, mult=mult)
    response["Total"] = cart.get_total_price()
    return JsonResponse(response)


@require_POST
def cart_remove(request, product_slug):
    cart = Cart(request)
    mult = 1
    if "multiplier" in request.POST:
        mult = int(request.POST["multiplier"])
    product = get_object_or_404(Product, slug=product_slug)
    cart.remove(product, mult)
    response = {"Total": cart.get_total_price(), "Deleted": True}
    return JsonResponse(response)


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                                        initial={
                                            'quantity': item['quantity'],
                                            'update': True
                                        })

    return render(request, 'cart/detail.html', {'cart': cart})

