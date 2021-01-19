from django.shortcuts import render
from django.core.mail import send_mail
from PriceTracker.models import Flipkart
from PriceTracker.models import Amazon
from PriceTracker.models import Ebay
from WebScraper import settings
from selenium import webdriver
import re
import datetime

from django.http import HttpResponse
import os

# Create your views here.
def home(request):
    return render(request,'index.html')

def flipkart(request):
    if request.method == "POST":
        link=request.POST.get('website')
        desired_price=request.POST.get('desired_price')
        user_email=request.POST.get('user_email')

        t=Flipkart(URL=link,Desired_price=desired_price,Email=user_email,time=datetime.datetime.now())
        t.save()


        # Scraping part starts
        # use your webdriver's location in the below string
        driver = webdriver.Chrome(executable_path=r"C:\Users\91972\Downloads\chromedriver.exe")

        product_details = []
        driver.get(link)
        Product_Name = driver.find_element_by_class_name("B_NuCI").text
        # price will work only for standard products/deals of the day, will have to add other for other on-sale products
        try:
            product_Price = driver.find_element_by_class_name("_30jeq3").text
        except:
            product_Price = "0"
        # removing special chars from price
        basic_price = re.sub("[, ]", "", product_Price)
        product_Price = re.sub("[$₹€, ]", "", product_Price)
        desired = (float(product_Price) <= float(desired_price))
        product_details.extend([Product_Name, basic_price, desired, link])
        driver.quit()

        #Send an E-mail with required details if it is under desired prize
        if(product_details[2]):
            subject = "Your desired product is now in your range !"
            msg = body =" Product Name: " + product_details[0] + "\n Current Price: " + product_details[1] + "\n Product Link: " + product_details[3]
            to = user_email
            res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
            if (res == 1):
                msg = "Mail Sent"
            else:
                msg = "Mail could not be sent"
            t.delete()     #Delete data of the user whose product has reached desired price
        context = {'product_name':product_details[0],'current_price':product_details[1],'desired_price':str(product_details[2]),'product_link':product_details[3]}
        return render(request,'display_output.html',context)
    return render(request, 'flipkart.html')

def amazon(request):
    if request.method == "POST":
        link=request.POST.get('website')
        desired_price=request.POST.get('desired_price')
        user_email=request.POST.get('user_email')

        a=Amazon(URL=link,Desired_price=desired_price,Email=user_email,time=datetime.datetime.now())
        a.save()

        # use your webdriver's location in the below string
        driver = webdriver.Chrome(executable_path=r"C:\Users\91972\Downloads\chromedriver.exe")

        product_details = []
        driver.get(link)
        availability = driver.find_element_by_id("availability").text
        Product_Name = driver.find_element_by_id("productTitle").text
        # price will work only for standard products/deals of the day, will have to add other for other on-sale products
        try:
            product_Price = driver.find_element_by_id("priceblock_ourprice").text
        except:
            try:
                product_Price = driver.find_element_by_id("priceblock_dealprice").text
            except:
                product_Price = "0"

        # removing special chars from price
        basic_price = re.sub("[, ]", "", product_Price)
        product_Price = re.sub("[$₹€, ]", "", product_Price)
        desired = (float(product_Price) <= float(desired_price))
        product_details.extend([Product_Name, basic_price, availability, desired, link])
        driver.quit()

        # Send an E-mail with required details if it is under desired prize
        if (product_details[3]):
            subject = "Your desired product is now in your range !"
            msg = body = " Product Name: " + product_details[0] + "\n Current Price: " + product_details[1] + "\n Availability: " + str(product_details[2]) + "\n Product Link: " + product_details[4]
            to = user_email
            res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
            if (res == 1):
                msg = "Mail Sent"
            else:
                msg = "Mail could not be sent"
            a.delete();         #Delete the data of user whose product has reached the desired price
        context = {'product_name': product_details[0], 'current_price': product_details[1],'availability':product_details[2],'desired_price': str(product_details[3]), 'product_link': product_details[4]}
        return render(request, '../templates/amazon_output.html', context)
    return render(request, '../templates/amazon.html')


def ebay(request):
    if request.method == "POST":
        link=request.POST.get('website')
        desired_price=request.POST.get('desired_price')
        user_email=request.POST.get('user_email')

        e=Ebay(URL=link,Desired_price=desired_price,Email=user_email,time=datetime.datetime.now())
        e.save()

        # use your webdriver's location in the below string
        driver = webdriver.Chrome(executable_path=r"C:\Users\91972\Downloads\chromedriver.exe")

        product_details = []
        driver.get(link)
        Product_Name = driver.find_element_by_class_name("it-ttl").text
        # price will work only for standard products/deals of the day, will have to add other for other on-sale products
        try:
            product_Price = driver.find_element_by_id("prcIsum").text
        except:
            product_Price = "0"
        # removing special chars from price
        basic_price = re.sub("[, ]", "", product_Price)
        product_Price = re.sub("[ABCDEFGHIJKLMNOPQRSTUVWXYZ$₹€/ea, ]", "", product_Price)
        desired = (float(product_Price) <= float(desired_price))
        product_details.extend([Product_Name, basic_price, desired, link])
        driver.quit()

        # Send an E-mail with required details if it is under desired prize
        if (product_details[2]):
            subject = "Your desired product is now in your range !"
            msg = body = " Product Name: " + product_details[0] + "\n Current Price: " + product_details[1] + "\n Product Link: " + product_details[3]
            to = user_email
            res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
            if (res == 1):
                msg = "Mail Sent"
            else:
                msg = "Mail could not be sent"
            e.delete()      #Delete data of the user whose product has reached desired price
        context = {'product_name': product_details[0], 'current_price': product_details[1],'desired_price': str(product_details[2]), 'product_link': product_details[3]}
        return render(request, 'display_output.html', context)
    return render(request, 'ebay.html')

