from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404

from cart.cart import Cart
from .forms import UserInfoForm, DeliveryForm
from .models import Category, Product, ProductAttrs, Article, OrderItem, Order
from cart.forms import CartAddProductForm
from .utils import send_telegram
from .utils import send_email


categories_per_row = 3
SESSION_ORDER = "Order"

def index(request):
    super_category_list = Category.objects.filter(parent=None)
    category_rows = [super_category_list[x:x + categories_per_row]
                     for x in range(0, len(super_category_list), categories_per_row)]
    '''block for all products'''
    product_list = Product.objects.all()
    products_per_row = 3
    product_rows = [product_list[x:x + products_per_row] for x in range(0, len(product_list), products_per_row)]
    '''pagination'''
    paginator = Paginator(product_rows, 7)  # number of rows of products!!!
    page_number = request.GET.get("page")
    try:
        page_obj = paginator.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = paginator.page(paginator.num_pages)

    context = {"category_rows": category_rows, "product_rows": product_rows, "product_list": product_list,
               "categories": super_category_list, "page_obj": page_obj}

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
    if not cart:
        return redirect('store:index')
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

            order_items = []
            for item in cart:
                o_item = OrderItem()
                o_item.order = order
                o_item.product = item['product']
                o_item.price = item['price']
                o_item.total_price = item['total_price']
                o_item.quantity = item['quantity']
                o_item.packaging = item['packaging'] + " " + item['unit']

                o_item.save()
                order_items.append(o_item)

            send_telegram(order, order_items)
            send_email(order, order_items)
            cart.clear()

            request.session[SESSION_ORDER] = order.pk
            return redirect('store:success_order')

    context = {'cart': cart, 'discount_total_price': discount_total_price,
               'discount': discount, 'client_info': c_form, 'client_delivery': d_form}
    return render(request, 'store/checkout.html', context)


def success_order(request):
    order_number = request.session.get(SESSION_ORDER)
    if order_number:
        context = {'order_number': order_number}
        del request.session[SESSION_ORDER]
        request.session.modified = True
        return render(request, 'store/order_confirm.html', context)
    else:
        return redirect('store:index')
