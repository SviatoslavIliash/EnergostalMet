from django.shortcuts import render, redirect, get_object_or_404

from cart.cart import Cart
from .models import Category, Product, ProductAttrs, Article
from cart.forms import CartAddProductForm

categories_per_row = 3


def index(request):
    category_list = Category.objects.all()
    super_category_list = list(filter(lambda c: c.is_super_category(), category_list))
    category_rows = [super_category_list[x:x + categories_per_row]
                     for x in range(0, len(super_category_list), categories_per_row)]
    '''block for all products'''
    product_list = Product.objects.all()
    products_per_row = 3
    product_rows = [product_list[x:x + products_per_row] for x in range(0, len(product_list), products_per_row)]
    context = {"category_rows": category_rows, "product_rows": product_rows, "product_list": product_list}
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



