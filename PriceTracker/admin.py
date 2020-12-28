from django.contrib import admin
from PriceTracker.models import  Flipkart
from PriceTracker.models import Amazon
from PriceTracker.models import Ebay


# Register your models here.
admin.site.register(Flipkart)
admin.site.register(Amazon)
admin.site.register(Ebay)