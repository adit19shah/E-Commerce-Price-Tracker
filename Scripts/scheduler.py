import schedule
import time


def print_my_name():
    print("Adidev Scrapers")


schedule.every().day.at("21:00").do(print_my_name)

while 1:
    schedule.run_pending()
    time.sleep(1)
