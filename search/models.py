from django.db import models

class Cities(models.Model):
    city = models.CharField(max_length=20L, unique=True)

class Names(models.Model):
    name = models.CharField(max_length=20L, unique=True)

class Terms(models.Model):
    category = models.CharField(max_length=20L)
    term = models.CharField(max_length=100L)

class Units(models.Model):
    unit = models.CharField(max_length=5L)

class Links(models.Model):
    link = models.CharField(max_length=2000L, unique=True)
    title = models.CharField(max_length=2000L)
    sum_words = models.IntegerField()
    sum_unique_words = models.IntegerField()
    sum_terms = models.IntegerField()
    sum_names = models.IntegerField()
    sum_units = models.IntegerField()
    sum_cities = models.IntegerField()
    sum_percent = models.IntegerField()
    add_time = models.IntegerField()
