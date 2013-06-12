from django.db import models

class Cities(models.Model):
    id = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=20L, unique=True)
    class Meta:
        db_table = 'cities'

class HtmlTest(models.Model):
    id = models.IntegerField(primary_key=True)
    site = models.CharField(max_length=255L, unique=True)
    html = models.TextField()
    class Meta:
        db_table = 'html_test'

class Names(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20L, unique=True)
    class Meta:
        db_table = 'names'

class Terms(models.Model):
    category = models.CharField(max_length=13L, blank=True)
    id = models.IntegerField(primary_key=True)
    term = models.CharField(max_length=100L)
    class Meta:
        db_table = 'terms'

class Units(models.Model):
    id = models.IntegerField(primary_key=True)
    unit = models.CharField(max_length=5L)
    class Meta:
        db_table = 'units'

class Links(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.CharField(max_length=255L, unique=True)
    sum_words = models.IntegerField()
    sum_unique_words = models.IntegerField()
    sum_terms = models.IntegerField()
    sum_names = models.IntegerField()
    sum_units = models.IntegerField()
    sum_cities = models.IntegerField()
    sum_percent = models.IntegerField()
    add_time = models.IntegerField()
    class Meta:
        db_table = 'links'
