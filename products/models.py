from django.db import models

from places.models import Place


class Category(models.Model):
    name = models.CharField(max_length=255)
    is_visible = models.BooleanField(null=True, blank=True, default=True)
    place = models.ForeignKey(
        Place, related_name="categories", on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    cover = models.ImageField()
    description = models.TextField()
    price = models.IntegerField()
    old_price = models.CharField(null=True, blank=True, max_length=255)
    is_visible = models.BooleanField(null=True, blank=True, default=True)
    is_available = models.BooleanField(null=True, blank=True, default=True)
