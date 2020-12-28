from django.db import models
import datetime

# Create your models here.

# Each E-Commerce website will have its own model so that whenever the price checking script is run for
# all users, each website will get its own users only which is required because price checking script for
# each E-commerce website is different.

class Flipkart(models.Model):
    URL  =  models.CharField(max_length=200)
    Desired_price = models.FloatField()
    Email =  models.EmailField()
    time =  models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
         return self.Email

class Amazon(models.Model):
    URL  =  models.CharField(max_length=200)
    Desired_price = models.FloatField()
    Email =  models.EmailField()
    time =  models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
         return self.Email

class Ebay(models.Model):
    URL  =  models.CharField(max_length=200)
    Desired_price = models.FloatField()
    Email =  models.EmailField()
    time =  models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
         return self.Email
