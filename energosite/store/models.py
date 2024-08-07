from decimal import Decimal

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.templatetags.static import static


# Create your models here.


DEFAULT_IMAGE_PATH = 'store/images/default_image.jpg'


# Move this func to some util file
def get_image_impl(obj):

    if obj.image:
        return obj.image.get_image_or_default()
    else:
        return static(DEFAULT_IMAGE_PATH)


class ImageModel(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Зображення (вибрати)")

    class Meta:
        verbose_name = "Зображення"
        verbose_name_plural = "Зображення"

    def image_tag(self):
        from django.utils.html import escape
        from django.utils.safestring import mark_safe
        return mark_safe(u'<img src="%s" style="width:150px;height:150px;object-fit:contain;"/>'
                         % escape(self.image.url))

    image_tag.short_description = "Зображення"

    def get_image_or_default(self):
        if self.image and self.image.storage.exists(self.image.name):
            return self.image.url
        else:
            return static(DEFAULT_IMAGE_PATH)

    def __str__(self):
        return self.image.name


class SeoFieldsModel(models.Model):
    meta_keywords = models.CharField(max_length=200, verbose_name="Мета-тег Ключові слова", null=True, blank=True)
    meta_description = models.CharField(max_length=300, verbose_name="Мета-тег Опис", null=True, blank=True)

    class Meta:
        abstract = True


class Category(SeoFieldsModel):
    name = models.CharField(max_length=30, unique=True, verbose_name="Назва")
    parent = models.ForeignKey("self", related_name='children', null=True, blank=True, on_delete=models.CASCADE,
                               verbose_name="Батьківська категорія")
    description = models.TextField(default='', blank=True, verbose_name="Опис")
    image = models.ForeignKey(ImageModel, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Зображення")
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

    def all_children(self):
        res = []
        if self.children:
            res.extend(self.children.all())
            for child in self.children.all():
                res.extend(child.all_children())
        return res


class Product(SeoFieldsModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="Назва")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    price = models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True, verbose_name="Ціна")
    unit_of_measurement = models.ForeignKey("UnitOfMeasurements", on_delete=models.CASCADE,
                                            verbose_name="Одиниці вимірювання")
    packaging = models.IntegerField(blank=True, null=True, verbose_name="Пакування")
    attributes = models.ManyToManyField("Attribute", through="ProductAttrs")
    image = models.ForeignKey(ImageModel, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Зображення")
    description = models.TextField(default="", blank=True, verbose_name="Опис")
    slug = models.SlugField(null=False, default="", unique=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукти"

    def get_image(self):
        return get_image_impl(self)

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    first_name = models.CharField(max_length=250, default="", verbose_name="Ім'я")
    last_name = models.CharField(max_length=250, default="", verbose_name="Прізвище")
    email = models.EmailField(max_length=100, default='', blank=True)
    phone_number = models.CharField(max_length=20, default="", verbose_name="Телефон")

    def __str__(self):
        return (str(self.first_name) + '\n'
                + str(self.last_name) + '\n'
                + str(self.email) + '\n'
                + str(self.phone_number)
                )

    class Meta:
        verbose_name = "Клієнт"
        verbose_name_plural = "Клієнти"


class DeliveryMethod(models.Model):
    name = models.CharField(max_length=200, verbose_name="Спосіб доставки")
    enabled = models.BooleanField(default=True, verbose_name="Доступно")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Метод доставки"
        verbose_name_plural = "Методи доставки"


class PaymentMethod(models.Model):
    name = models.CharField(max_length=200, verbose_name="Спосіб оплати")
    enabled = models.BooleanField(default=True, verbose_name="Доступно")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Метод оплати"
        verbose_name_plural = "Методи оплати"


class Order(models.Model):
    order_date = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=200, verbose_name="Коментар", blank=True, default='')
    city = models.CharField(max_length=200, verbose_name="Місто", default='', blank=True)
    post_department = models.CharField(max_length=200, verbose_name="Відділення або адреса", default='', blank=True)
    delivery_method = models.ForeignKey(DeliveryMethod, on_delete=models.SET_NULL, null=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True, verbose_name="Клієнт")
    order_sum = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal(0), verbose_name="Сума")
    order_discount = models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True, verbose_name="Знижка")
    order_sum_w_discount = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal(0), verbose_name="Ціна зі знижкою")

    def __str__(self):
        return " ".join(('#' + str(self.pk) + ' |', str(self.order_date.date())))

    def get_pk(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="product_item", blank=False, default='', on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Кількість", default=0, blank=False)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal(0), verbose_name="Ціна за одиницю")
    packaging = models.CharField(max_length=100, default="", verbose_name="Пакування")

    def __str__(self):
        return str(self.product)

    @admin.display(description="Ціна")
    def get_total_price(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = "Позиція"
        verbose_name_plural = "Позиції"


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
    address = models.CharField(max_length=100, default='', blank=True, verbose_name="Адреса")
    geo_data = models.CharField(max_length=200, default='', blank=True, verbose_name="Гео координати")
    catalog_PDF = models.FileField(upload_to='files/', null=True, blank=True, verbose_name="Прайс")
    client_info = models.CharField(max_length=200, default='', blank=True, verbose_name="Інформація для клієнтів")

    class Meta:
        verbose_name = "Компанія"
        verbose_name_plural = "Компанії"

    def is_catalog(self):
        return self.catalog_PDF and self.catalog_PDF.storage.exists(self.catalog_PDF.name)

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
