import pandas as pd 
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#Create Webdriver

driver = webdriver.Chrome("C:/Users/brahm/Desktop/Web Scraping/chromedriver.exe")

#Use login link to start a session on LinkedIn 
#This session shall be used for accessing all other links associated with www.linkedin.com

driver.get("https://www.linkedin.com/uas/login?fromSignIn=true&trk=cold_join_sign_in")

#Sign-in Automation
email = "ankurpankur4@gmail.com"
pwd = "ankur@pankur"
username = driver.find_element(By.ID,"username")
username.send_keys(email)
username.send_keys(Keys.RETURN)

password = driver.find_element(By.ID,"password")
password.send_keys(pwd)
password.send_keys(Keys.RETURN)

#wait time after page loading

time.sleep(10)

#get dataset file with names and url(s)
#add your test set path here
df = pd.read_csv("C:/Users/brahm/Desktop/Web Scraping/Divided Dataset/YASHWANT_test_set.csv")

#loop for iterating through dataset and extraction of page source
i = 0

while(i <= 50):

	# Get Name and URL from each row

	name = df['Name'][i]
	url = df['URL'][i]
	
	# open given URL

	driver.get(url)

	#code for scrolling down to the end of the page to ensure that the entire page is loaded

	start = time.time()
	i_scroll = 0
	f_scroll = 1000

	while True:

		driver.execute_script(f"window.scrollTo({i_scroll}, {f_scroll})")
		i_scroll = f_scroll
		f_scroll += 1000
		time.sleep(5)
		end = time.time()

		if round(end - start) > 20 :
			break

	pg_src = driver.page_source

	time.sleep(5)

	# get source code of page as text

	

	# create file name and path for text file

	file_name = name+'.txt'
	#add the file path of the output folder
	file_path = "C:/Users/brahm/Desktop/Web Scraping/Scraping/New folder (5)/"+file_name+

	# save source code into text file

	f = open(file_path , "x" , encoding = 'utf-8')
	f.write(pg_src)
	f.close()

	i += 1
driver.quit()