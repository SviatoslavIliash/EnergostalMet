from django.http import HttpResponse
from django.shortcuts import render
from .models import Category, Product, ProductAttrs


def index(request):
    category_list = Category.objects.all
    context = {"category_list" : category_list}
    return render(request, "store/index.html", context)

def category_detail(request, category_name):
    product_list = Product.objects.filter(category__name=category_name)
    context = {"product_list" : product_list, "category_name" : category_name}
    return render(request, "store/category.html", context)

def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    attributes = ProductAttrs.objects.filter(product=product)
    context = {"product": product, "attrs": attributes}
    return render(request, "store/product.html", context)

