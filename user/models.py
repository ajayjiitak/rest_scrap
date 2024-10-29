# user/models.py
from django.db import models

class Product(models.Model):
    platform = models.CharField(max_length=50, default='Mercari')
    product_name = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    photos = models.JSONField()  # Stores list of photo URLs
    url = models.URLField()
    description = models.TextField(blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    condition = models.CharField(max_length=100, blank=True, null=True)
    seller = models.CharField(max_length=100, blank=True, null=True)