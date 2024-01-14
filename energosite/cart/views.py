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
    form = CartAddProductForm(request.POST)
    response = {}
    if form.is_valid():
        cd = form.cleaned_data
        upd = cd["update"]
        quantity, price = cart.add(product=product, quantity=cd['quantity'], update_quantity=upd)
        response["Price"] = price
    response["Total"] = cart.get_total_price()
    return JsonResponse(response)


def cart_remove(request, product_slug):
    cart = Cart(request)
    product = get_object_or_404(Product, slug=product_slug)
    cart.remove(product)
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


