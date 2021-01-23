import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from django_apscheduler.jobstores import register_job, register_events
from apscheduler.triggers.cron import CronTrigger


from django.conf import settings

import re
from PriceTracker.models import Flipkart
from PriceTracker.models import Amazon
from PriceTracker.models import Ebay
from selenium import webdriver
from WebScraper import settings
from django.core.mail import send_mail


# Create scheduler to run in a thread inside the application process
scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)

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

def start():
    if settings.DEBUG:
    # Hook into the apscheduler logger
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    # Adding this job here instead of to crons.
    # This will do the following:
    # - Add a scheduled job to the job store on application initialization
    # - The job will execute a model class method at midnight each day
    # - replace_existing in combination with the unique ID prevents duplicate copies of the job
    #scheduler.add_job(Check_Prices, "cron", id="my_class_method",h , replace_existing=True)
    #scheduler.add_job(Check_Prices, 'interval', hours=24, name='clean_accounts', jobstore='default',id="my_class_method",replace_existing=True)
    scheduler.add_job(
        Check_Prices,
        trigger=CronTrigger(hour="*/12"),  # Every 12 hours
        id="my_class_method",  # The `id` assigned to each job MUST be unique
        max_instances=1,
        replace_existing=True,
    )
    # Add the scheduled jobs to the Django admin interface
    register_events(scheduler)

    scheduler.start()