import pandas as pd 
from parsel import Selector
from bs4 import BeautifulSoup

df = pd.read_csv("C:/Users/brahm/Desktop/Web Scraping/linkedIn_Connections_Data_0.1.csv",encoding='latin-1')

name = df['Column1'][0]

file_name = name+'.txt'

file_path = "C:/Users/brahm/Desktop/Web Scraping/Scraping/New folder (2)/"+file_name

f = open(file_path, 'r',encoding = 'utf-8')
text = f.read()
f.close()


sel = Selector(text = text)


name = sel.xpath('//*[starts-with(@class, "text-heading-xlarge inline t-24 v-align-middle break-words")]/text()').extract_first()
print("\nName: ",name.strip())

Designation = sel.xpath('//*[starts-with(@class, "text-body-medium break-words")]/text()').extract_first()
print("Designation: ",Designation.strip())

Company = sel.xpath('//*[starts-with(@aria-label,"Current company")]/text()').extract_first()
print("Company: ",Company.strip())

Location = sel.xpath('//*[starts-with(@class,"text-body-small inline t-black--light break-words")]/text()').extract_first()
print("Location:",Location.strip())

connections = sel.xpath('//*[starts-with(@class, "t-bold")]/text()').extract_first()
print("No. of Connections: ",connections)

soup = BeautifulSoup(text,'html.parser')

About = soup.find('section',{'class': "pv-profile-section pv-about-section artdeco-card p5 mt4 ember-view"}).find('div')
About_text = About.get_text()
print(About_text.strip())

exp_section = soup.find("section", {"id": "experience-section"}).find('ul').find_all('li') 
print(exp_section)


interests = soup.find('section',{'class': "pv-profile-section pv-interests-section artdeco-card mt4 p5 ember-view"}).find('ul')
interests_text = interests.get_text()
print(interests_text.strip())
for i in Exp:
	x = i.find_all('p')
	print(x)
