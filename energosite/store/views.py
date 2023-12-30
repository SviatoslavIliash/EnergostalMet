from django.http import HttpResponse
from django.shortcuts import render
from .models import Category, Product, ProductAttrs, Article


def index(request):
    category_list = Category.objects.all()
    categories_per_row = 3
    category_chunks = [category_list[x:x + categories_per_row] for x in range(0, len(category_list), categories_per_row)]
    context = {"category_chunks": category_chunks}
    return render(request, "store/index.html", context)

def article(request, article_name):
    current_article = Article.objects.filter(name=article_name)
    context = {"current_article": current_article.first()}
    return render(request, "store/article.html", context)

#def about(request):
#    return render(request, "store/about.html")


def cart(request):
    return render(request, "store/cart.html")


#def contacts(request):
#    return render(request, "store/contacts.html")


def category_detail(request, category_name):
    product_list = Product.objects.filter(category__name=category_name)
    products_per_row = 3
    product_chunks = [product_list[x:x + products_per_row] for x in range(0, len(product_list), products_per_row)]
    context = {"product_chunks": product_chunks, "category_name": category_name}
    return render(request, "store/category.html", context)


def product_detail(request, category_name, product_id):
    product = Product.objects.get(pk=product_id)
    attributes = ProductAttrs.objects.filter(product=product)
    context = {"product": product, "attrs": attributes}
    return render(request, "store/product.html", context)

