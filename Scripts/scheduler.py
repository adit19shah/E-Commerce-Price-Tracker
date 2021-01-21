import schedule
import time
import re
from PriceTracker.models import Flipkart
from PriceTracker.models import Amazon
from PriceTracker.models import Ebay
from selenium import webdriver
from WebScraper import settings
from django.core.mail import send_mail

# def print_my_name():
#     print("Adidev Scrapers")
#
#
# schedule.every().day.at("21:00").do(Check_Prices)
#
# while 1:
#     schedule.run_pending()
#     time.sleep(1)

def Check_Prices():
    FlipkartInfo = Flipkart.objects.all()
    AmazonInfo = Amazon.objects.all()
    EbayInfo = Ebay.objects.all()

    # For Flipkart
    for person in FlipkartInfo:
        link = person.URL
        desired_price = person.Desired_price
        user_email = person.Email


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

        # Send an E-mail with required details if it is under desired prize
        if (product_details[2]):
            subject = "Your desired product is now in your range !"
            msg = body = " Product Name: " + product_details[0] + "\n Current Price: " + product_details[
                1] + "\n Product Link: " + product_details[3]
            to = user_email
            res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
            if (res == 1):
                msg = "Mail Sent"
            else:
                msg = "Mail could not be sent"
            person.delete()  # Delete data of the user whose product has reached desired price

    #For Amazon
    for person in AmazonInfo:
        link = person.URL
        desired_price = person.Desired_price
        user_email = person.Email

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
            msg = body = " Product Name: " + product_details[0] + "\n Current Price: " + product_details[
                1] + "\n Availability: " + str(product_details[2]) + "\n Product Link: " + product_details[4]
            to = user_email
            res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
            if (res == 1):
                msg = "Mail Sent"
            else:
                msg = "Mail could not be sent"
            person.delete()  # Delete data of the user whose product has reached desired price


    #For Ebay
    for person in EbayInfo:
        link = person.URL
        desired_price = person.Desired_price
        user_email = person.Email

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
            msg = body = " Product Name: " + product_details[0] + "\n Current Price: " + product_details[
                1] + "\n Availability: " + str(product_details[2]) + "\n Product Link: " + product_details[4]
            to = user_email
            res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
            if (res == 1):
                msg = "Mail Sent"
            else:
                msg = "Mail could not be sent"
            person.delete()  # Delete data of the user whose product has reached desired price

schedule.every().day.at("23:55").do(Check_Prices)

while 1:
    schedule.run_pending()
    time.sleep(1)
