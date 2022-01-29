import pandas as pd
import numpy as np
import json
from parsel import Selector
from bs4 import BeautifulSoup

columns = ['Name','Designation','Company','Location','Connections','Followers','About','Experience','Education','Endorsements','Interests']
Data = pd.DataFrame(columns = columns)

df = pd.read_csv("C:/Users/brahm/Desktop/Web Scraping/linkedIn_Connections_Data_0.1.csv",encoding='latin-1')
for i in range(51) :
	print(i)
	name = df['Column1'][i]

	file_name = name+'.txt'

	file_path = "C:/Users/brahm/Desktop/Web Scraping/Scraping/New folder (3)/"+file_name

	f = open(file_path, 'r',encoding = 'utf-8')
	text = f.read()
	f.close()

	soup = BeautifulSoup(text,'html.parser')
	
	Name = soup.find('h1',{'class':"text-heading-xlarge inline t-24 v-align-middle break-words"}).get_text()
	print("\nName: ",Name.strip())

	Designation = soup.find('div',{'class':"text-body-medium break-words"})
	if type(Designation) != type(None):
		title = Designation.get_text().strip()
	else:
		title = ""
	print("Designation: ",title)
	Company = soup.find('div',{'aria-label':"Current company"})
	if type(Company) != type(None):
		Company_Name = Company.get_text().strip()
	else:
		Company_Name = ""
	print("Company: ",Company_Name)
	Location = soup.find('span',{'class':"text-body-small inline t-black--light break-words"}).get_text()
	print("Location:",Location.strip())

	followers = soup.find('li',{'class':"text-body-small t-black--light inline-block"})
	if type(followers) != type(None):
		Followers = followers.get_text()
	else :
		Followers = np.nan
	print(Followers)

	Connections = soup.find('span',{'class':"t-bold"})
	if type(Connections) != type(None):
		no_connections = "No. of Connections: ",Connections.get_text()
	else : 
		no_connections = np.nan

	About = soup.find('section',{'class': "pv-profile-section pv-about-section artdeco-card p5 mt4 ember-view"}).find('div')
	if type(About) != type(None):
		About_text = About.get_text()
	else:
		About_text = ""
	print(About_text.strip())

	endorsements = soup.find('section',{'class': "pv-profile-section pv-skill-categories-section artdeco-card mt4 p5 ember-view"}).find('ol').find_all('li')
	endorsements_list = []
	for end in endorsements:
		iterator = end.find_all('span', {'class':"pv-skill-category-entity__name-text t-16 t-black t-bold"})
		for a in iterator:
			endorsements_list.append(a.get_text().strip())
	Endorsements = json.dumps(endorsements_list)

	interests = soup.find('section',{'class': "pv-profile-section pv-interests-section artdeco-card mt4 p5 ember-view"}).find('ul').find_all('li')
	interests_text = []
	for interest in interests :
		interests_text.append(interest.find('span',{'class':"pv-entity__summary-title-text"}).get_text().strip())
	print(interests_text)

	exp_section = soup.find("section", {"id": "experience-section"})
	if type(exp_section) != type(None):

		exp_section = soup.find("section", {"id": "experience-section"}).find('ul').find_all('li') 
		exp_names_list = []
		exp_durations_list = []
		exp_designations_list = []
		exp_locations_list = []
		exp_descriptions_list = []
		for exp in exp_section:

			
			company_designation = exp.find('h3',{'class':"t-16 t-black t-bold"})
			if type(company_designation) != type(None):
				exp_designations_list.append(company_designation.get_text().strip())
			else:
				exp_designations_list.append("")

			company_name = exp.find('p',{'class':"pv-entity__secondary-title t-14 t-black t-normal"})
			if type(company_name) != type(None):
				exp_names_list.append(company_name.get_text().strip())
			else:
				exp_names_list.append("")


			exp_duration = exp.find('h4',{'class':"t-14 t-black--light t-normal"}).find('span',{'class':"pv-entity__bullet-item-v2"}).get_text().strip()
			exp_durations_list.append(exp_duration)

			company_location = exp.find('h4',{'class':"pv-entity__location t-14 t-black--light t-normal block"})
			if type(company_location) != type(None):
				company_location = exp.find('h4',{'class':"pv-entity__location t-14 t-black--light t-normal block"}).find('span').next_element.next_element.next_element
				if type(company_location) != type(None):
					exp_locations_list.append(company_location.get_text().strip())
				else:
					exp_locations_list.append("")
			else:
				exp_locations_list.append("")

			exp_description = exp.find('div',{'class':"pv-entity__extra-details t-14 t-black--light ember-view"})
			if type(exp_description) != type(None):
				exp_description = exp.find('div',{'class':"pv-entity__extra-details t-14 t-black--light ember-view"}).find('div',{'style':"line-height:2rem;max-height:16rem;"})
				if(type(exp_description) == type(None)):
					exp_description = exp.find('div',{'class':"pv-entity__extra-details t-14 t-black--light ember-view"}).find('div',{'style':"line-height:2rem;max-height:8rem;"})
				exp_descriptions_list.append(exp_description.get_text().strip())
			else:
				exp_descriptions_list.append("")


	experience_labels = ['Company Name', 'Duration','Location','Description']
	experience = {}
	for n in range(len(exp_names_list)):

		e_data = [exp_names_list[n],exp_durations_list[n],exp_locations_list[n],exp_descriptions_list[n]]
		exp_data = dict(zip(experience_labels,e_data))
		experience[exp_designations_list[n]] = exp_data
	print(json.dumps(experience))

	edu_section = soup.find('section', {'id': "education-section"})
	if type(edu_section) != type(None):
		edu_section = soup.find('section', {'id': "education-section"}).find('ul').find_all('li') 
		edu_institute_list = []
		edu_degrees_list = []
		edu_fields_list = []
		for edu in edu_section:

			institute = edu.find('h3',{'class':"pv-entity__school-name t-16 t-black t-bold"})
			if type(institute) != type(None):
				edu_institute_list.append(institute.get_text().strip())
			else: 
				edu_institute_list.append("")


			degree = edu.find('p',{'class':"pv-entity__secondary-title pv-entity__degree-name t-14 t-black t-normal"})
			if type(degree) != type(None):
				degree = edu.find('p',{'class':"pv-entity__secondary-title pv-entity__degree-name t-14 t-black t-normal"}).find('span').next_element.next_element.next_element
				if type(degree) != type(None):
					edu_degrees_list.append(degree.get_text().strip())
				else:
					edu_degrees_list.append("")				
			else:
				edu_degrees_list.append("")

			field = edu.find('p',{'class':"pv-entity__secondary-title pv-entity__fos t-14 t-black t-normal"})
			if type(field) != type(None):
				field = edu.find('p',{'class':"pv-entity__secondary-title pv-entity__fos t-14 t-black t-normal"}).find('span',{'class':"pv-entity__comma-item"})
				if type(field) != type(None):
					edu_fields_list.append(field.get_text().strip())
				else:
					edu_fields_list.append("")
			else:
				edu_fields_list.append("")

	education_labels = ['Degree','Field of Study']
	education = {}
	for e in range(len(edu_institute_list)):

		edu_data = [edu_degrees_list[e],edu_fields_list[e]]
		education_data = dict(zip(education_labels,edu_data))
		education[edu_institute_list[e]] = education_data
	print(json.dumps(education))
