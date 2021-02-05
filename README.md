# E-Commerce Price Tracker

### General Description:

- This web-app scrapes data from three E-commerce sites: Amazon, Flipkart and Ebay.
- The applicatication takes following three things as input: 
   - product link
   - product price desired by user 
   - her E-mail id  
   and in turn displays all the product details(product name, its current price, its availability, its rating, etc. along with specifying whether the product falls within the user’s desired range or not) after scraping the provided link. 
- Moreover, the application also sends an Email to the user whenever the price of the product drops to meet the User's desired range. 
(For this, it stores data entered by all users, so that scraping can be performed at regular intervals(say every 12 hours) on the stored data and whenever, the price falls to the user’s desired range, an E-mail is triggered to that respective user)

### Tech Stack Used:
- Python (Programming language)
- Django (Python based framework)
- Selenium (Library used for scraping)
