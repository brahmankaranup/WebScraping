from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import time

#create webdriver and get target website

driver = webdriver.Chrome("C:/Users/brahm/Desktop/Web Scraping/chromedriver.exe")
driver.get("https://www.linkedin.com/uas/login?fromSignIn=true&trk=cold_join_sign_in")

#Sign-in Automation

username = driver.find_element_by_id("username")
username.send_keys("ankurpankur4@gmail.com")
username.send_keys(Keys.RETURN)
password = driver.find_element_by_id("password")
password.send_keys("ankur@pankur")
password.send_keys(Keys.RETURN)

#wait time for page to load

time.sleep(10)

#redirect to target url because linkedin doesn't allow direct access

driver.get("https://www.linkedin.com/in/pratap-sanap-5b620b2b/")
#wait time for page to load
time.sleep(10)

#create a selector for page source

sel = Selector(text = driver.page_source)

#quit automation
driver.quit()

#extract desired elements using x-path selector

name = sel.xpath('//*[starts-with(@class, "text-heading-xlarge inline t-24 v-align-middle break-words")]/text()').extract_first()
print("\nName: ",name.strip())
Designation = sel.xpath('//*[starts-with(@class, "text-body-medium break-words")]/text()').extract_first()
print("Designation: ",Designation.strip())
Company = sel.xpath('//*[starts-with(@aria-label,"Current company")]/text()').extract_first()
print("Company: ",Company.strip())
Location = sel.xpath('//*[starts-with(@class,"text-body-small inline t-black--light break-words")]/text()').extract_first()
print("Location:",Location.strip())