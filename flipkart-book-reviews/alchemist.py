
from bs4 import BeautifulSoup
import pandas as pd 
import requests
import pprint
import re 
import time 

def getUrl(order='NEGATIVE_FIRST',page=1):
	url = f'https://www.flipkart.com/alchemist/product-reviews/itmfc9jxsc7dckfm?pid=9788172234980&lid=LSTBOK9788172234980ZECYGB&aid=overall&certifiedBuyer=false&sortOrder={order}&page={page}'
	return url
# span class
withoutReadMore = '_1H-bmy'
withReadMore = '_1BWGvX'
collectReview = []
pageNum = 100
session = requests.Session()
start = time.time()
for page in range(1,pageNum+1):
	response = session.get(getUrl(page=page))
	soup = BeautifulSoup(response.text,'lxml')
	data = soup.find('div',class_='_1YokD2 _3Mn1Gg col-9-12')
	reviews = data.find_all('div',class_='col _2wzgFH K0kLPL')
	for review in reviews:
		rateClass = ['_3LWZlK _1rdVr6 _1BLPMq','_3LWZlK _32lA32 _1BLPMq','_3LWZlK _1BLPMq']
		for class_ in rateClass:
			rating = review.find('div',class_=class_)
			if rating:
				rating = rating.text
				break
		rev = review.find('div',class_='t-ZTKy')
		readMoreClass = rev.find('span').attrs['class'][0]
		if readMoreClass == withoutReadMore:
			text = rev.text.lower().replace('read more','').split('.')
			final = '.'.join([x for x in text if x != ''])+'.'
		elif readMoreClass == withReadMore:
			text = rev.text.lower().replace('read more','').split('.')
			final = '.'.join(x for x in text[:-1] if x != '')+'.'
		if final : 
			collectReview.append([final,rating])
end = time.time()
session.close()
print('Scraping Time : ',(end-start))

try :
	file = 'alchemist.csv'
	pd.DataFrame(collectReview,columns=['review','rating']).to_csv(file,index=False)
	print(f'created {file} succesfully !')
except Exception as error :
	print(error)



