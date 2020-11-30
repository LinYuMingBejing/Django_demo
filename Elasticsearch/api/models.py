from django.db import models

# Create your models here.

class Restaurant(models.Model):
    restaurant_id = models.IntegerField()
    restaurant = models.CharField(max_length=255)
    ratings = models.IntegerField()
    price = models.IntegerField()
    types = models.CharField(max_length=10)
    areas = models.CharField(max_length=10)
    spots = models.CharField(max_length=10)


class Areas(models.Model):
    id = models.IntegerField(primary_key=True)
    place = models.CharField(max_length=255)


class RestaurantTypes(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    subcategory = models.CharField(max_length=255)

