from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

from cart.cart import Cart
from .forms import UserInfoForm, DeliveryForm
from .models import Category, Product, ProductAttrs, Article, OrderItem, Order
from cart.forms import CartAddProductForm

import requests

categories_per_row = 3


def index(request):
    super_category_list = Category.objects.filter(parent=None)
    category_rows = [super_category_list[x:x + categories_per_row]
                     for x in range(0, len(super_category_list), categories_per_row)]
    '''block for all products'''
    product_list = Product.objects.all()
    products_per_row = 3
    product_rows = [product_list[x:x + products_per_row] for x in range(0, len(product_list), products_per_row)]
    context = {"category_rows": category_rows, "product_rows": product_rows, "product_list": product_list,
               "categories": super_category_list}

    return render(request, "store/index.html", context)


def article(request, article_slug):
    current_article = get_object_or_404(Article, slug=article_slug)
    context = {"current_article": current_article}
    return render(request, "store/article.html", context)


def category_detail(request, category_slug):
    category_rows = []
    category = get_object_or_404(Category, slug=category_slug)
    categories = [category]
    children = category.children.all()
    if children:
        category_rows = [children[x:x+categories_per_row] for x in range(0, len(children), categories_per_row)]
        categories.extend(category.all_children())

    product_list = []
    for c in categories:
        product_list.extend(Product.objects.filter(category__name=c.name))

    products_per_row = 3
    product_rows = [product_list[x:x + products_per_row] for x in range(0, len(product_list), products_per_row)]
    context = {"product_rows": product_rows, "category": category,
               "category_rows": category_rows}
    return render(request, "store/category.html", context)


def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    attributes = ProductAttrs.objects.filter(product=product)
    cart_product_form = CartAddProductForm()

    if product.price is None:
        product.price = 'під замовлення'
    context = {"product": product, "attrs": attributes, "cart_product_form": cart_product_form}
    return render(request, "store/product.html", context)


def checkout(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'update': True
            })
    discount_total_price, discount = cart.total_price_discount()

    c_form = UserInfoForm()
    d_form = DeliveryForm()

    if request.method == "POST" and 'checkout' in request.POST:
        c_form = UserInfoForm(request.POST)
        d_form = DeliveryForm(request.POST)
        if c_form.is_valid() and d_form.is_valid():
            order = Order()
            order.user = c_form.save()
            order.post_department = d_form.cleaned_data.get("post_department")
            order.city = d_form.cleaned_data.get("city")
            order.comment = d_form.cleaned_data.get("comment")
            order.delivery_method = d_form.cleaned_data.get("delivery_type")
            order.payment_method = d_form.cleaned_data.get("payment_type")

            order.order_sum = cart.get_total_price()
            order.order_discount = discount
            order.order_sum_w_discount = discount_total_price
            order.save()

            for item in cart:
                o_item = OrderItem()
                o_item.order = order
                o_item.product = item['product']
                o_item.price = item['price']
                o_item.quantity = item['quantity']
                o_item.save()

            cart.clear()
            # email(request)
            telegram(f"NEW order {order.pk}")
            # TODO add email sending & maybe telegram message sending
            return redirect('store:success_order', order_number=order.pk)

    context = {'cart': cart, 'discount_total_price': discount_total_price,
               'discount': discount, 'client_info': c_form, 'client_delivery': d_form}
    return render(request, 'store/checkout.html', context)


def success_order(request, order_number):
    context = {'order_number': order_number}
    return render(request, 'store/order_confirm.html', context)


def telegram(message):
    TOKEN = ""
    chatId = ''
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    try:
        response = requests.post(url, json={'chat_id': chatId, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)


def email(request):
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = []
    send_mail(subject, message, email_from, recipient_list)
    return redirect('redirect to a new page')
