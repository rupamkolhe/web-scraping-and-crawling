

from bs4 import BeautifulSoup
import requests
import json
import re

session = requests.Session()

with open('crawlerData.json','r') as crawlerFile :
    metaData = json.load(crawlerFile)
    crawlerFile.close()

def getIndustry(ind):
    if re.search('\.\.\.',ind):
        return re.sub('/[\sA-Za-z]{1,100}\.\.\.\s{1,5}jobs$','',ind)
    else:
        return re.sub('\s{1,5}jobs$','',ind)
    
def scraperData(data, scrapeInd): # scrapeInd -> list of industries to scrape 
    try :
        try :
            file = open('scraperData.json','r+')
            skillData = json.load(file)
        except :
            file = open('scraperData.json','w+')
            skillData = {'ind':{}}
            print('file created !')
        if scrapeInd:
            for ind in scrapeInd:# industriesToScrape:
                newInd = getIndustry(ind)
                if newInd not in skillData['ind'].keys():
                    # here you start scraping
                    skillData['ind'][newInd] = {'func':{}}
                    for jf in data[ind].keys():
                        if jf != 'link':
                            skillData['ind'][newInd]['func'][jf] = {'spec':{}}
                            for js in data[ind][jf].keys():
                                if js != 'link':
                                    url = data[ind][jf][js]['link']
                                    page = session.get(url).text
                                    soup = BeautifulSoup(page,'lxml')
                                    jobs = soup.find_all('li',{'class':'clearfix job-bx wht-shd-bx'})
                                    skillHolder = []
                                    for job in jobs:
                                        skill = job.find('span',{'class':'srp-skills'}).text
                                        s = [re.sub('[\'\"]','',x.strip().lower()) for x in skill.strip().split(',')]
                                        skillHolder.append(s)
                                                                            
                                    # assign it skillHolder list
                                    skillData['ind'][newInd]['func'][jf]['spec'][js] = skillHolder
                else:
                    print(f'[{newInd}] already present in scraperData file')

            # moving cursor to 0 position
            print(file.closed)
            file.seek(0)
            json.dump(skillData,file)
            print('-')
            print('successfully uploaded data to scraperData file')
            file.close()
        else :
            print('Industries not specified !')
    except Exception as error:
        file.close()
        print(error)


scrapeInd = ['Retailing jobs']

scraperData(metaData,scrapeInd)

session.close()








































