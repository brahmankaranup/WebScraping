# Libraries 

import pandas as pd
import numpy as np
import json

# Library used to extract data from saved source code of the profile pages

from bs4 import BeautifulSoup

# Creating DataFrame to then dump into a .csv file

Columns = ['Name','Designation','Company','Location','Connections','Followers','About','Experience','Education','Endorsements','Interests']
Data = pd.DataFrame(columns = Columns)

# Read list of names to iterate through and get names of files saved as profile names
# Eg. : Anup Brahmankar's will be saved as Anup Brahmankar.txt

df = pd.read_csv("C:/Users/brahm/Desktop/Web Scraping/linkedIn_Connections_Data_0.1.csv",encoding='latin-1')

# Looping Through the list

for i in range(51) :

	# getting names from dataset
	name = df['Column1'][i]

    # creating filename with .txt extension
 	file_name = name+'.txt'

 	# creating filepath for each file to read file
	file_path = "C:/Users/brahm/Desktop/Web Scraping/Scraping/New folder (3)/"+file_name

	# opening file and reading it 
	f = open(file_path, 'r',encoding = 'utf-8')
	text = f.read()
	f.close()

	# creating soup variable with particular source code with html
	soup = BeautifulSoup(text,'html.parser')
	
	# getting Name
	Name = soup.find('h1',{'class':"text-heading-xlarge inline t-24 v-align-middle break-words"}).get_text()
	
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

	#getting About description of the user
	Abt = soup.find('section',{'class': "pv-profile-section pv-about-section artdeco-card p5 mt4 ember-view"}).find('div')
	if type(Abt) != type(None):
		Abt_text = Abt.get_text()
	else:
		#appending an empty string if not available
		Abt_text = ""
	About_Desc = Abt_text.strip()

	#getting endorsements if available
	endorsements = soup.find('section',{'class': "pv-profile-section pv-skill-categories-section artdeco-card mt4 p5 ember-view"})
	if type(endorsements) != type(None):
		endorsements = soup.find('section',{'class': "pv-profile-section pv-skill-categories-section artdeco-card mt4 p5 ember-view"}).find('ol').find_all('li')
		endorsements_list = []
		for end in endorsements:
			iterator = end.find_all('span', {'class':"pv-skill-category-entity__name-text t-16 t-black t-bold"})
			for a in iterator:
				endorsements_list.append(a.get_text().strip())
			
			#exit loop

		Endorsements = json.dumps(endorsements_list)
		
		#exit loop
		
	else:
		#appending an empty string if not available
		Endorsements = ""

	#getting interests
	interests = soup.find('section',{'class': "pv-profile-section pv-interests-section artdeco-card mt4 p5 ember-view"}).find('ul').find_all('li')
	interests_text = []
	for interest in interests :
		interests_text.append(interest.find('span',{'class':"pv-entity__summary-title-text"}).get_text().strip())
		#exit loop
	Interests = json.dumps(interests_text)

	#getting expterience section
	exp_section = soup.find("section", {"id": "experience-section"})
	if type(exp_section) != type(None):

		#creating lists for every element in the section
		exp_section = soup.find("section", {"id": "experience-section"}).find('ul').find_all('li') 
		exp_names_list = []
		exp_durations_list = []
		exp_designations_list = []
		exp_locations_list = []
		exp_descriptions_list = []
		for exp in exp_section:

			# getting designation element
			company_designation = exp.find('h3',{'class':"t-16 t-black t-bold"})
			if type(company_designation) != type(None):
				exp_designations_list.append(company_designation.get_text().strip())
			else:
				#appending an empty string if not available
				exp_designations_list.append("")

			# getting company name element
			company_name = exp.find('p',{'class':"pv-entity__secondary-title t-14 t-black t-normal"})
			if type(company_name) != type(None):
				exp_names_list.append(company_name.get_text().strip())
			else:
				#appending an empty string if not available
				exp_names_list.append("")

			# getting duration of experience
			exp_duration = exp.find('h4',{'class':"t-14 t-black--light t-normal"}).find('span',{'class':"pv-entity__bullet-item-v2"}).get_text().strip()
			exp_durations_list.append(exp_duration)

			# getting location of experience
			company_location = exp.find('h4',{'class':"pv-entity__location t-14 t-black--light t-normal block"})
			if type(company_location) != type(None):
				company_location = exp.find('h4',{'class':"pv-entity__location t-14 t-black--light t-normal block"}).find('span').next_element.next_element.next_element
				if type(company_location) != type(None):
					exp_locations_list.append(company_location.get_text().strip())
				else:
					#appending an empty string if not available
					exp_locations_list.append("")
			else:
				#appending an empty string if not available
				exp_locations_list.append("")

			#getting description of experience
			exp_description = exp.find('div',{'class':"pv-entity__extra-details t-14 t-black--light ember-view"})
			if type(exp_description) != type(None):
				exp_description = exp.find('div',{'class':"pv-entity__extra-details t-14 t-black--light ember-view"}).find('div',{'style':"line-height:2rem;max-height:16rem;"})
				if(type(exp_description) != type(None)):
					exp_descriptions_list.append(exp_description.get_text().strip())
				else:
					exp_description = exp.find('div',{'class':"pv-entity__extra-details t-14 t-black--light ember-view"}).find('div',{'style':"line-height:2rem;max-height:8rem;"})
					if type(exp_description) != type(None): 
						exp_descriptions_list.append(exp_description.get_text().strip())
					else:
						#appending an empty string if not available
						exp_descriptions_list.append("")
			else:
				#appending an empty string if not available
				exp_descriptions_list.append("")

			#exit loop

	#creating labels of experience elements for saving it in JSON format
	experience_labels = ['Company Name', 'Duration','Location','Description']
	experience = {}

	# format for exp:-{["Designation" : "designation1"["Company Name": "company name1",
	#											"Duration" : "duration1",
	#											"Location" : "location1",
	#											"Description: description1"]],
	#			["Designation" : "designation2"[..........................
	#											...........................]]}

	#looping through experience elements and adding them to the "dict experience"
	for n in range(len(exp_names_list)):

		e_data = [exp_names_list[n],exp_durations_list[n],exp_locations_list[n],exp_descriptions_list[n]]
		exp_data = dict(zip(experience_labels,e_data))
		experience[exp_designations_list[n]] = exp_data

		#exit loop

	Experience = json.dumps(experience)

	# getting experience section
	edu_section = soup.find('section', {'id': "education-section"})
	if type(edu_section) != type(None):
		edu_section = soup.find('section', {'id': "education-section"}).find('ul').find_all('li') 
		edu_institute_list = []
		edu_degrees_list = []
		edu_fields_list = []
		for edu in edu_section:

			#getting institute name
			institute = edu.find('h3',{'class':"pv-entity__school-name t-16 t-black t-bold"})
			if type(institute) != type(None):
				edu_institute_list.append(institute.get_text().strip())
			else: 
				edu_institute_list.append("")

			# getting degree details
			degree = edu.find('p',{'class':"pv-entity__secondary-title pv-entity__degree-name t-14 t-black t-normal"})
			if type(degree) != type(None):
				degree = edu.find('p',{'class':"pv-entity__secondary-title pv-entity__degree-name t-14 t-black t-normal"}).find('span').next_element.next_element.next_element
				if type(degree) != type(None):
					edu_degrees_list.append(degree.get_text().strip())
				else:
					edu_degrees_list.append("")				
			else:
				edu_degrees_list.append("")

			#getting field of study
			field = edu.find('p',{'class':"pv-entity__secondary-title pv-entity__fos t-14 t-black t-normal"})
			if type(field) != type(None):
				field = edu.find('p',{'class':"pv-entity__secondary-title pv-entity__fos t-14 t-black t-normal"}).find('span',{'class':"pv-entity__comma-item"})
				if type(field) != type(None):
					edu_fields_list.append(field.get_text().strip())
				else:
					edu_fields_list.append("")
			else:
				edu_fields_list.append("")

			#exit loop

	education_labels = ['Degree','Field of Study']
	education = {}
	#same format as experience section

	# looping through experience elements and adding them to the "dict experience"
	for e in range(len(edu_institute_list)):

		edu_data = [edu_degrees_list[e],edu_fields_list[e]]
		education_data = dict(zip(education_labels,edu_data))
		education[edu_institute_list[e]] = education_data

		#exit loop

	Education = json.dumps(education)


	#creating a list of all elements extracted to match the list "Column" 
	Append_List = [Name, Designation, Company, Location, No_of_Connections, No_of_Followers, About_Desc, Experience, Education, Endorsements, Interests]
	
	#appending list to dataframe
	series = pd.Series(Append_List,index = Data.columns)
	Data = Data.append(series,ignore_index = True)

	#exit loop

# creating file path, for storing results to a ".csv" file 
result_file_path = "C:/Users/brahm/Desktop/Web Scraping/Results/Linkedin_Data_0.3.csv"
File = open(result_file_path,"x")
File.close()

# writing data into the ".csv" file
Data.to_csv(result_file_path)