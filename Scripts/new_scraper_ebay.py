from selenium import webdriver
import re
import datetime
import csv
import time
import smtplib

wait_for = 60

#use your webdriver's location in the below string
driver = webdriver.Chrome(executable_path=r"C:\Users\Dev Choganwala\Desktop\chromedriver.exe")

def calc_diff():
    now = datetime.datetime.now()
    try:
        with open("data.csv", "r") as datafile:
            csv_reader = csv.reader(datafile)
            for line in csv_reader:
                curr = line[0]
    except:
        print("No data file found")
        driver.quit()
        exit()
    return (now - datetime.datetime.strptime(curr, '%Y-%m-%d %H:%M:%S.%f')).total_seconds()


def get_row():
    try:
        with open("data.csv", "r") as datafile:
            csv_reader = csv.reader(datafile)
            for line in csv_reader:
                data = line
    except:
        print("No data file found")
        driver.quit()
        exit()
    return data

def write_product(link, price):
    with open("data.csv", "w", newline='') as datafile:
        csv_writer = csv.writer(datafile)
        details = checkPrice(link, price)
        send_mail(details)
        csv_writer.writerow(details)
        if details[4]:
            print("Requirements Satisfied, quitting the program")
            driver.quit()
            exit()

def send_mail(details):
    if details[4]:
        with smtplib.SMTP('smtp.gmail.com',587) as stmp:
            stmp.starttls()
            stmp.login('sender-email-address', 'password')
            subject = f"Your product {details[1]} has satisfied your requirements"
            msg = 'Subject: {}\n\n{}'.format(subject, f"Current price: {details[3]}\n link: {details[5]}\n")
            stmp.sendmail('sender-email-address', 'receiver-email-address', msg)

def checkPrice(link,desired_price):
    product_details = []
    driver.get(link)
    Product_Name = driver.find_element_by_class_name("it-ttl").text
    #price will work only for standard products/deals of the day, will have to add other for other on-sale products
    try:
        product_Price = driver.find_element_by_id("prcIsum").text
    except:
        product_Price = "0"
    #removing special chars from price
    basic_price = re.sub("[, ]","",product_Price)
    product_Price = re.sub("[ABCDEFGHIJKLMNOPQRSTUVWXYZ$₹€, ]","",product_Price)
    now = datetime.datetime.now()
    desired = (float(product_Price)<=int(desired_price))
    product_details.extend([now, Product_Name, desired_price, product_Price, desired, link])
    return product_details

def run_loop():
    time_diff = calc_diff()
    abs_diff = wait_for - time_diff
    data = get_row()
    if abs_diff < 0:
        while True:
            print(data[5], data[2])
            write_product(data[5], data[2])
            time.sleep(wait_for)
    else:
        time.sleep(abs_diff)
        while True:
            print(data[5], data[2])
            write_product(data[5], data[2])
            time.sleep(wait_for)


if __name__ == "__main__":
    choice = int(input("1. Enter a new product\n 2.Run the loop\n"))
    if choice == 1:
        link = input("Enter the link of the product\n")
        price = int(input("Enter the preferred price\n"))
        write_product(link, price)
        while True:
            time.sleep(wait_for)
            write_product(link, price)
    else:
        run_loop()

    driver.quit()
