from django.db import models
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='images/', default='')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    attributes = models.ManyToManyField("Attribute", through="ProductAttrs")
    image = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=250, default='', blank=True)

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


