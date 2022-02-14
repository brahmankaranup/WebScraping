# Libraries 

import pandas as pd
import numpy as np
import json

# Library used to extract data from saved source code of the profile pages

from bs4 import BeautifulSoup

# Creating DataFrame to then dump into a .csv file

Columns = ['Name','Designation','Company','Location','Connections','Followers','Residue']
Data = pd.DataFrame(columns = Columns)

# Read list of names to iterate through and get names of files saved as profile names
# Eg. : Anup Brahmankar's will be saved as Anup Brahmankar.txt

df = pd.read_csv(r"C:\Users\brahm\Desktop\Web Scraping\Divided Dataset\YASHWANT_test_set.csv")

# Looping Through the list

for i in range(50) :

	# getting names from dataset
	name = df['Name'][i]
	print(name)

    # creating filename with .txt extension
	file_name = name+'.txt.txt'

 	# creating filepath for each file to read file
	file_path = "C:/Users/brahm/Desktop/Web Scraping/Scraping/new1/"+file_name

	# opening file and reading it
	try: 
		f = open(file_path, 'r',encoding = 'utf-8')
	except FileNotFoundError:
		print("FileNotFoundError")
		continue
	except OSError:
		print("OSError")
		continue
	text = f.read()
	f.close()

	# creating soup variable with particular source code with html
	soup = BeautifulSoup(text,'html.parser')
	
	# getting Name
	Name = soup.find('h1',{'class':"text-heading-xlarge inline t-24 v-align-middle break-words"})
	if type(Name) == type(None):continue
	else:Name = Name.get_text()
	
	# getting Designation
	des = soup.find('div',{'class':"text-body-medium break-words"})
	if type(des) != type(None):
		title = des.get_text().strip()
	else:
		#appending an empty string if not available
		title = ""
	Designation = title

	# getting name of the current company
	comp = soup.find('div',{'aria-label':"Current company"})
	if type(comp) != type(None):
		Company_Name = comp.get_text().strip()
	else:
		#appending an empty string if not available
		Company_Name = ""
	Company = Company_Name

	# getting Current Location
	loc = soup.find('span',{'class':"text-body-small inline t-black--light break-words"}).get_text()
	Location = loc

	# getting no. of followers
	followers = soup.find('li',{'class':"text-body-small t-black--light inline-block"})
	if type(followers) != type(None):
		No_followers = followers.get_text()
	else :
		#appending NaN if not available
		No_followers = np.nan

	No_of_Followers = No_followers

	# No. of Connections
	conns = soup.find('span',{'class':"t-bold"})
	if type(conns) != type(None):
		no_conns = conns.get_text()
	else : 
		#appending NaN if not available
		no_conns = np.nan

	No_of_Connections = no_conns

	Residues = {}
	elements = soup.find_all('li',{'class':"artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"})
	for element in elements:
		all_data = element.find_all('span',{'aria-hidden':"true"})
		for data in all_data:
			Residues.append(data.get_text().strip())
	Residue = json.dumps(Residues)


	#creating a list of all elements extracted to match the list "Column" 
	Append_List = [Name, Designation, Company, Location, No_of_Connections, No_of_Followers, Residues]
	
	#appending list to dataframe
	series = pd.DataFrame([Append_List],columns = Data.columns)
	Data = pd.concat([Data,series],ignore_index = True)

	#exit loop

# creating file path, for storing results to a ".csv" file 
result_file_path = "C:/Users/brahm/Desktop/Web Scraping/Results/yash_trial_2.csv"
File = open(result_file_path,"x")
File.close()

# writing data into the ".csv" file
Data.to_csv(result_file_path)
