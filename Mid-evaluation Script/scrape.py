import requests
from selenium import webdriver
import smtplib
import csv
from email.message import EmailMessage

driver = webdriver.Chrome(executable_path=r"driver-path")

link = "https://summerofcode.withgoogle.com/archive/2020/organizations/"

driver.get(link)
orgs = driver.find_elements_by_class_name("organization-card__name")
orgs = [x.text for x in orgs]
links = driver.find_elements_by_class_name("organization-card__link")
links = [x.get_attribute('href') for x in links]
un = list(zip(orgs, links))
un = [list(x) for x in un]
for item in un:
    driver.get(item[1])
    techstack = driver.find_elements_by_class_name("organization__tag--technology")
    techstack = [x.text for x in techstack]
    item.append(techstack)
techstack = set()
for item in un:
    [techstack.add(x) for x in item[2]]

print(techstack)
msg = "placeholder"
know = list()
while msg!="exit":
    msg = input("Enter What you know from the above tech stack")
    know.append(msg)

with open('data.csv','w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    for item in know:
        for orgs in un:
            if item in orgs[2]:
                csv_writer.writerow(orgs)

msg = EmailMessage()
msg['Subject'] = 'Your GSOC matched orgs'
msg['From'] = 'sender-email'
msg['To'] = 'receiver-email'
msg.set_content('Here are your matched orgs based on the tech stack you entered')

with open('data.csv', 'rb') as f:
    file_data = f.read()
    file_name = f.name

msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login('sender-email', 'password')
    smtp.send_message(msg)
driver.quit()