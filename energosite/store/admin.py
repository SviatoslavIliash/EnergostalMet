from django.contrib import admin

from .models import Category, Product, Attribute, ProductAttrs, Article, WholesalePrice, CompanyInfo, PhoneNumber
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
    prepopulated_fields = {"slug": ["name"]}
    save_as = True


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
    save_as = True
    inlines = [CategoryInline]
    ordering = ["parent"]

    prepopulated_fields = {"slug": ["name"]}


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    save_as = True


class PhoneNumberInline(admin.TabularInline):
    model = PhoneNumber
    extra = 1


class CompanyInfoAdmin(admin.ModelAdmin):
    inlines = [PhoneNumberInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Attribute)
admin.site.register(Article, ArticleAdmin)
admin.site.register(CompanyInfo, CompanyInfoAdmin)
