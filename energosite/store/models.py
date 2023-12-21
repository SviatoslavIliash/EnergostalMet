from django.db import models
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=250, default='', blank=True, null=True)


class Product(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    #attributes = models.
    image = models.ImageField(upload_to='uploads/products/')
    description = models.CharField(max_length=250, default='', blank=True, null=True)
