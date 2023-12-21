from django.http import HttpResponse
from django.shortcuts import render
from .models import Category, Product


def index(request):
    category_list = Category.objects.all
    context = {"category_list" : category_list}
    return render(request, "store/index.html", context)

def category_detail(request, category_name):
    product_list = Product.objects.filter(category__name=category_name)
    context = {"product_list" : product_list, "category_name" : category_name}
    return render(request, "store/category.html", context)
