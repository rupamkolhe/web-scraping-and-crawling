
from bs4 import BeautifulSoup
import requests
import json
import re 


session = requests.Session()


def crawlerData():
    baseURL = 'https://www.timesjobs.com/candidate/job-search.html?utm_source=index&utm_medium=icon&utm_campaign=alljobslogo'
    prefixURL = 'https://www.timesjobs.com/candidate'
    # industry scraping
    page_ind = session.get(baseURL).text
    soup = BeautifulSoup(page_ind,'lxml')
    data_ind = soup.find('ul',{'id':'showIndustry',
                           'class':'browse-ind'})
    metaData = {}
    ######   add COUNT
    countJI = 0
    try :
        for ind in data_ind:
            industry = ind.find('a')
            if (industry != None) and (industry != -1):
                title = industry.get('title') 
                link = 'https://www.timesjobs.com'+industry.get('href')+'/&luceneResultSize=1'
                # [industry , link]
                # dump in metaData 
                metaData[title] = {'link':link}
                # job function scraping 
                page_jobfunc = session.get(link).text
                soup = BeautifulSoup(page_jobfunc,'lxml')
                jobFunc = soup.find('div',{'id':'fa_show'})
                ######   add COUNT
                countJF = 0
                for func in jobFunc:
                    titleJF = func.find('span')
                    linkJF = func.find('input')
                    if (titleJF != -1) and (titleJF != None):
                        titleJF = titleJF.get('title')
                        linkJF = prefixURL+re.findall('getSRPResultByDwr\(\'(.*?)\'\);',
                                                    linkJF.get('onclick'))[0]
                        linkJF = re.sub('&luceneResultSize=[0-9]{1,3}&','&luceneResultSize=1&',linkJF)
                        # [job function , link]
                        # dump in metaData
                        metaData[title][titleJF] = {'link': linkJF}
                        # job specialization scraping
                        page_jobfunc = session.get(linkJF).text
                        soup = BeautifulSoup(page_jobfunc,'lxml')
                        jobSpec = soup.find('div',{'id':'_0_group',
                                                   'class':'specialization-cluster clearfix'})
                        ###### add COUNT
                        countJS = 0
                        for spec in jobSpec:
                            titleJS = spec.find('span')
                            linkJS = spec.find('input')
                            if (linkJS != -1) and (linkJS != None):
                                titleJS = titleJS.get('title')
                                linkJS = linkJS.get('onclick')
                                linkJS = prefixURL+re.findall('getSRPResultByDwr\(\'(.*?)\'\);',
                                                            linkJS)[0]
                                # setting luceneResultSize=100 job posts 
                                linkJS = re.sub('&luceneResultSize=[0-9]{1,3}&','&luceneResultSize=100&',linkJS)
                                # [job specialization , link]
                                # dump in metaData
                                metaData[title][titleJF][titleJS] = {'link':linkJS}
                # counting JI
                countJI += 1
        meta = json.dumps(metaData)
        print('you did it ',countJI)
        with open(jsonFile+'.json','w') as file:
            file.write(meta)
            file.close()
    except Exception:
        print('got stopped ',countJI)
        meta = json.dumps(metaData)
        with open(jsonFile+'.json','w') as file:
            file.write(meta)
            file.close()
        
jsonFile_ = '_'
            
crawlerData(jsonFile)                          
session.close()



























