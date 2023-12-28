from django.contrib import admin
from .models import Category, Product, Attribute, ProductAttrs, Article
# Register your models here.

class ProductAttrsInline(admin.TabularInline):
    model = ProductAttrs

class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductAttrsInline,
    ]


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Attribute)
admin.site.register(Article)

