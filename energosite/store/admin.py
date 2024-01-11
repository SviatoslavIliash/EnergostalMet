from django.contrib import admin

from .models import Category, Product, Attribute, ProductAttrs, Article, WholesalePrice
# Register your models here.

class ProductAttrsInline(admin.TabularInline):
    model = ProductAttrs
    extra = 1

class WholesalePriceInline(admin.TabularInline):
    model = WholesalePrice
    extra = 2

class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductAttrsInline,
        WholesalePriceInline
    ]
    list_filter = [("category", admin.RelatedOnlyFieldListFilter)]
    search_fields = ["name", "category__name"]
    list_display = ["__str__", "category", "price"]


class CategoryInline(admin.StackedInline):
    model = Category
    show_change_link = True
    verbose_name = "Child category"
    verbose_name_plural = "Children categories"
    extra = 0
    fields = ["name"]
    can_delete = False

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_filter = [("parent", admin.RelatedOnlyFieldListFilter)]
    list_display = ["__str__", "parents_str"]

    inlines = [CategoryInline]
    ordering = ["parent"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Attribute)
admin.site.register(Article)

