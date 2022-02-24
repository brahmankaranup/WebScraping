import pandas as pd 
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


Columns = ['Name', 'Followers', 'Designation', 'Age of Post', 'Description']
Data = pd.DataFrame(columns = Columns)

#Create Webdriver

browser = webdriver.Chrome("C:/Users/brahm/Desktop/Web Scraping/chromedriver.exe")

#Use login link to start a session on LinkedIn 
#This session shall be used for accessing all other links associated with www.linkedin.com

browser.get("https://www.linkedin.com/uas/login?fromSignIn=true&trk=cold_join_sign_in")

#Sign-in Automation
email = "ankurpankur4@gmail.com"
pwd = "ankur@pankur"
username = browser.find_element(By.ID,"username")
username.send_keys(email)
username.send_keys(Keys.RETURN)

password = browser.find_element(By.ID,"password")
password.send_keys(pwd)
password.send_keys(Keys.RETURN)

browser.get("https://www.linkedin.com/my-items/saved-posts/")

i_scroll = 0
f_scroll = 1000
start = time.time()
count = 0
while True:
  count += 1
  browser.execute_script(f"window.scrollTo({i_scroll}, {f_scroll})")
  i_scroll = f_scroll
  f_scroll += 1000
  time.sleep(1)
  end = time.time()

  if round(end - start) > 20 :
    break

pg_src = browser.page_source
browser.quit()

soup = BeautifulSoup(pg_src,'html.parser')
posts = soup.find_all('li',{'class':"reusable-search__result-container"})

for post in posts:
	Name = post.find('span',{'aria-hidden':"true"}).get_text().strip()

	followers_OR_des = post.find('div',{'class':"entity-result__primary-subtitle t-14 t-black t-normal"}).get_text().strip()
	followers = designation = ""
	if 'followers' in followers_OR_des:
		followers = followers_OR_des
	else:
		designation = followers_OR_des

	age_of_post = post.find('p',{'class':"t-black--light t-12"}).get_text().strip()

	try :
		description = post.find('p',{'class':"relative entity-result__summary entity-result__content-summary--3-lines entity-result--no-ellipsis mb2 t-14 t-black mh4"}).get_text().strip()
	except AttributeError:
		description = '' 
		try :
			description = post.find('p',{'class':"relative entity-result__content-summary entity-result__content-summary--3-lines entity-result--no-ellipsis t-14 mb2"}).get_text().strip()
		except AttributeError:
			description = ''
		except TypeError:
			description = ''
	except TypeError:
		description = ''

	Append_List = [Name, followers, designation, age_of_post, description]
	series = pd.DataFrame([Append_List],columns = Data.columns)
	Data = pd.concat([Data,series],ignore_index = True)



result_file_path = "C:/Users/brahm/Desktop/Web Scraping/Results/Linkedin_Saved_Posts_0.2.csv"
File = open(result_file_path,"x")
File.close()

# writing data into the ".csv" file
Data.to_csv(result_file_path)
