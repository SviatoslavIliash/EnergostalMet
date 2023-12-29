from django.db import models
from django.templatetags.static import static

# Create your models here.


# Move this func to some util file
def get_image_impl(obj):
    if obj.image:
        return obj.image.url
    else:
        return static('store/images/default_image.jpg')


class Category(models.Model):
    name = models.CharField(max_length=30)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=250, default='', blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def get_image(self):
        return get_image_impl(self)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    attributes = models.ManyToManyField("Attribute", through="ProductAttrs")
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    description = models.CharField(max_length=250, default='', blank=True)

    def get_image(self):
        return get_image_impl(self)

    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class ProductAttrs(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)

    def __str__(self):
        return self.attribute.name + " = " + self.value


class Article(models.Model):
    name = models.CharField(max_length=30)
    text = models.TextField()
    in_top_navbar = models.BooleanField(default=False)
    in_footer = models.BooleanField(default=True)

    def __str__(self):
        return self.name


