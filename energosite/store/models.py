from django.contrib import admin
from django.db import models
from django.templatetags.static import static

# Create your models here.


# Move this func to some util file
def get_image_impl(obj):
    if obj.image:
        return obj.image.url
    else:
        return static('store/images/default_image.jpg')


def default_wholesale_price(price):
    obj = WholesalePrice()
    obj.from_quantity = 0
    obj.price = price
    return obj


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="Назва")
    parent = models.ForeignKey("self", related_name='children', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Батьківська категорія")
    description = models.CharField(max_length=250, default='', blank=True, verbose_name="Опис")
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Зображення")
    slug = models.SlugField(null=False, default="", unique=True)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def get_image(self):
        return get_image_impl(self)

    def __str__(self):
        return self.name

    @admin.display(description="Батьківські категорії")
    def parents_str(self):
        res = ""
        parents = self.parents()
        parents_len = len(parents)
        for index, parent in enumerate(parents):
            res += parent.name
            if index != parents_len - 1:
                res += "->"
        # res += self.name
        return res

    def is_super_category(self):
        return self.parent is None


    def parents(self):
        res = []
        while self.parent:
            res.append(self.parent)
            self = self.parent
        res.reverse()
        return res


class Product(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="Назва")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Ціна")
    attributes = models.ManyToManyField("Attribute", through="ProductAttrs")
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Зображення")
    description = models.CharField(max_length=250, default='', blank=True, verbose_name="Опис")
    slug = models.SlugField(null=False, default="", unique=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукти"


    def get_image(self):
        return get_image_impl(self)

    def get_price(self, quantity):
        wholesale_prices = WholesalePrice.objects.filter(product=self).order_by('from_quantity')
        res = self.price
        for wp in wholesale_prices:
            if quantity >= wp.from_quantity:
                res = wp.price
            elif quantity < wp.from_quantity:
                break

        return res

    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибути"

    def __str__(self):
        return self.name


class ProductAttrs(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибути"

    def __str__(self):
        return self.attribute.name + " = " + self.value


class Article(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="Назва")
    text = models.TextField(verbose_name="Текст")
    in_top_navbar = models.BooleanField(default=False, verbose_name="Показувати в верхній навігації")
    in_footer = models.BooleanField(default=True, verbose_name="Показувати в футері")
    slug = models.SlugField(null=False, default="", unique=True)

    class Meta:
        verbose_name = "Стаття"
        verbose_name_plural = "Статті"

    def __str__(self):
        return self.name


class WholesalePrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    from_quantity = models.IntegerField(verbose_name="Від:", )
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Ціна")

    class Meta:
        verbose_name = "Оптова ціна"
        verbose_name_plural = "Оптові ціни"


