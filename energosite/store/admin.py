from django.contrib import admin

from .models import Category, Product, Attribute, ProductAttrs, Article, WholesalePrice, CompanyInfo, PhoneNumber, Packaging, UnitOfMeasurements
# Register your models here.


class ProductAttrsInline(admin.TabularInline):
    model = ProductAttrs
    extra = 1


class PackagingInline(admin.TabularInline):
    model = Packaging
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductAttrsInline,
        PackagingInline
    ]
    list_filter = [("category", admin.RelatedOnlyFieldListFilter)]
    search_fields = ["name", "category__name"]
    list_display = ["__str__", "category", "price"]
    prepopulated_fields = {"slug": ["name"]}
    save_as = True

    fieldsets = [
        (
            None,
            {
                "fields": ["name", "category", "price", "unit_of_measurement", "packaging", "image", "description", "slug"]

            }
        ),
        (
            "Мета-теги",
            {
                "fields": ["meta_keywords", "meta_description"]
            }
        )
    ]


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

    fieldsets = [
        (
            None,
            {
                "fields": ["name", "parent", "description", "image", "slug"]
            }
        ),
        (
            "Мета-теги",
            {
                "fields": ["meta_keywords", "meta_description"]
            }
        )
    ]


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    save_as = True

    fieldsets = [
        (
            None,
            {
                "fields": ["name", "text", "in_top_navbar", "in_footer", "slug"]

            }
        ),
        (
            "Мета-теги",
            {
                "fields": ["meta_keywords", "meta_description"]
            }
        )
    ]


class PhoneNumberInline(admin.TabularInline):
    model = PhoneNumber
    extra = 1


class WholesalePriceInline(admin.TabularInline):
    model = WholesalePrice
    extra = 2


class CompanyInfoAdmin(admin.ModelAdmin):
    inlines = [PhoneNumberInline,
               WholesalePriceInline]

    fieldsets = [
        (
            None,
            {
                "fields": ["name", "email", "catalog_PDF"]

            }
        ),
        (
            "Мета-теги",
            {
                "fields": ["meta_keywords", "meta_description"]
            }
        )
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Attribute)
admin.site.register(Article, ArticleAdmin)
admin.site.register(CompanyInfo, CompanyInfoAdmin)
admin.site.register(UnitOfMeasurements)
