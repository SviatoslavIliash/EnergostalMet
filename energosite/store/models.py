from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.templatetags.static import static


# Create your models here.


# Move this func to some util file
def get_image_impl(obj):
    if obj.image:
        return obj.image.url
    else:
        return static('store/images/default_image.jpg')


'''def default_wholesale_price(price):
    obj = WholesalePrice()
    obj.from_quantity = 0
    obj.price = price
    return obj'''


class SeoFieldsModel(models.Model):
    meta_keywords = models.CharField(max_length=100, verbose_name="Мета-тег Ключові слова", null=True, blank=True)
    meta_description = models.CharField(max_length=250, verbose_name="Мета-тег Опис", null=True, blank=True)

    class Meta:
        abstract = True


class Category(SeoFieldsModel):
    name = models.CharField(max_length=30, unique=True, verbose_name="Назва")
    parent = models.ForeignKey("self", related_name='children', null=True, blank=True, on_delete=models.CASCADE,
                               verbose_name="Батьківська категорія")
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


class Product(SeoFieldsModel):
    name = models.CharField(max_length=30, unique=True, verbose_name="Назва")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    price = models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True, verbose_name="Ціна")
    unit_of_measurement = models.ForeignKey("UnitOfMeasurements", on_delete=models.CASCADE,
                                            verbose_name="Одиниці вимірювання")
    packaging = models.IntegerField(blank=True, null=True, verbose_name="Пакування")
    attributes = models.ManyToManyField("Attribute", through="ProductAttrs")
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Зображення")
    description = models.CharField(max_length=250, default="", blank=True, verbose_name="Опис")
    slug = models.SlugField(null=False, default="", unique=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукти"

    def get_image(self):
        return get_image_impl(self)

    '''def get_price(self, quantity):
        wholesale_prices = WholesalePrice.objects.filter(product=self).order_by('from_quantity')
        res = self.price
        for wp in wholesale_prices:
            if quantity >= wp.from_quantity:
                res = wp.price
            elif quantity < wp.from_quantity:
                break

        return res'''

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


class UnitOfMeasurements(models.Model):
    unit = models.CharField(max_length=10, unique=True, verbose_name="Одиниці вимірювання")

    class Meta:
        verbose_name = "Одиниці вимірювання"
        verbose_name_plural = "Одиниці вимірювання"

    def __str__(self):
        return self.unit


class Packaging(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="alt_packaging", verbose_name="Продукт")
    packaging = models.IntegerField(verbose_name="Пакування")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Ціна")
    pretty_name = models.CharField(max_length=15, blank=True, default="", verbose_name="Назва для користувача")

    class Meta:
        verbose_name = "Пакування"
        verbose_name_plural = "Пакування"

    def __str__(self):
        if self.pretty_name:
            return self.pretty_name
        else:
            return str(self.packaging)


class Article(SeoFieldsModel):
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


class CompanyInfo(SeoFieldsModel):
    name = models.CharField(max_length=30, verbose_name="Назва")
    email = models.EmailField(max_length=50, verbose_name="Email")

    class Meta:
        verbose_name = "Компанія"
        verbose_name_plural = "Компанії"

    def __str__(self):
        return self.name

    # following 2 methods are needed to preserve Singleton behaviour
    def clean(self):
        if not self.pk and CompanyInfo.objects.exists():
            raise ValidationError("Дозволено додавати тільки один об'єкт з інформацією про компанію. "
                                  "Для редагування інформації використовуйте створений раніше об'єкт.")

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class PhoneNumber(models.Model):
    company = models.ForeignKey(CompanyInfo, related_name="phone_numbers", on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^(\+38)?0\d{9}$')
    phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=False,
                                    verbose_name="Телефонний номер")

    class Meta:
        verbose_name = "Телефонний номер"
        verbose_name_plural = "Телефонні номери"

    def __str__(self):
        return ""


class WholesalePrice(models.Model):
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, related_name="wholesale_prices",
                                verbose_name="Компанія")
    from_sum = models.IntegerField(verbose_name="Від (грн):")
    percentage = models.IntegerField(verbose_name="Відсоток (%)",
                                     validators=[
                                         MaxValueValidator(100),
                                         MinValueValidator(1)
                                     ]
                                     )

    class Meta:
        verbose_name = "Оптова ціна"
        verbose_name_plural = "Оптові ціни"

    def __str__(self):
        return "Від " + str(self.from_sum)
