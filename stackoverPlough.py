import json
import os
import requests
import datetime

#stackoverPlough v.0
#Created by P.D.M.Dilan
#2020/04/28

os.system('')
#ANSI escape codes for terminal text color
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


banner=(r"""
         __             __                        ____  __                  __  
   _____/ /_____ ______/ /______ _   _____  _____/ __ \/ /___  __  ______ _/ /_ 
  / ___/ __/ __ `/ ___/ //_/ __ \ | / / _ \/ ___/ /_/ / / __ \/ / / / __ `/ __ \
 (__  ) /_/ /_/ / /__/ ,< / /_/ / |/ /  __/ /  / ____/ / /_/ / /_/ / /_/ / / / /
/____/\__/\__,_/\___/_/|_|\____/|___/\___/_/  /_/   /_/\____/\__,_/\__, /_/ /_/ 
                                                                  /____/        
                ~~ Simple stack overflow searching tool ~~
                    ~~ stackoverPlough version 0.0 ~~
                
                """)

print(banner)
print('\n')

try:

    #get input
    keyWordSearch=input('Search on stackoverflow >> ')

    #cleaning input
    keyWordSearchClean=keyWordSearch.translate({ord(c): None for c in '!@#$/\\'})

    #stakexchange api
    #visit https://api.stackexchange.com/
    url='https://api.stackexchange.com/2.2/search/advanced?site=stackoverflow.com&q=%s' % (keyWordSearchClean)
    jData=requests.get(url)

    #if jData.status_code == 200:
        #print(jData.headers)

    data=jData.json()

    #extract data
    result=[]
    for k in data['items']:
        stackOdata={}
        stackOdata['title']=k.get('title')
        stackOdata['question_id']=k.get('question_id')    
        stackOdata['is_answered']=k.get('is_answered')
        stackOdata['answer_count']=k.get('answer_count')
        creation_date=k.get('creation_date')
        #convert date to human readable date from unix epoch time (UTC)
        stackOdata['creation_date']=datetime.datetime.utcfromtimestamp(creation_date).strftime('%Y-%m-%d %H:%M:%S')
        stackOdata['reputation']=k.get('owner').get('reputation')
        stackOdata['display_name']=k.get('owner').get('display_name')
        stackOdata['link']=k.get('link')
        stackOdata['tags']=k.get('tags')
        result.append(stackOdata)

    #print results
    for item in result:
        print(bcolors.OKBLUE+'-----------------------------------------------------------------------------------------------------------'+bcolors.ENDC+ '\n')
        for k,v in item.items():
            if k=='title':
                print('Title : '+bcolors.OKGREEN + v + bcolors.ENDC)
            elif k=='question_id':
                print('Question ID : '+ str(v))
            elif k=='is_answered':
                print('Is question is answered : ' + str(v))
            elif k=='answer_count':
                print('Answer count : '+ str(v))
            elif k=='creation_date':
                print('Created date : '+ v)
            elif k=='display_name':
                    print('User name : '+ v)
            elif k=='reputation':
                print('User reputation : '+ str(v))
            elif k=='link':
                print('Link : '+bcolors.UNDERLINE +v + bcolors.ENDC)
            elif k=='tags':
                print('Tags : ' + str(v))
        print('\n')

except (requests.HTTPError , requests.ConnectionError):
    print('Please check your internet connection !')
    exit()
