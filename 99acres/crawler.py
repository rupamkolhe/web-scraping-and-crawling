from bs4 import BeautifulSoup 
import pandas as pd 
import requests 
import json 
import pprint 
import re 

baseURL = 'https://www.99acres.com/'

def getURL(pageNumber=1,pageSize=1):
	url = f'https://www.99acres.com/api-aggregator/discovery/srp/search?locality_array=3246&area_unit=1&localityNameMap=%5Bobject%20Object%5D&platform=DESKTOP&moduleName=GRAILS_SRP&workflow=GRAILS_SRP&page_size={pageSize}&page={pageNumber}&city=274&preference=S&res_com=R&seoUrlType=DEFAULT&recomGroupType=VSP&pageName=SRP&groupByConfigurations=true'
	return url

maxPageSize = 25
maxPageNumber = 80

session = requests.Session()

links = []

size = 0
for pageNum in range(1,maxPageNumber+1):
	r = session.get(getURL(pageNumber=pageNum,
						   pageSize=maxPageSize))
	propData = json.loads(r.text)['properties']
	for prop in propData:
		if 'landingPage' in prop.keys():
			urlKey = 'landingPage'
			links.append(prop[urlKey]['url'])
		elif 'PROP_DETAILS_URL' in prop.keys():
			urlKey = 'PROP_DETAILS_URL'
			links.append(baseURL+prop[urlKey])
		else :
			continue 
		size += 1
		print(size)

pd.DataFrame(links,columns=['URLs']).to_csv('99acresCrawlerData.csv')

session.close()



