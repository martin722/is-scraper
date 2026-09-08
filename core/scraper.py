import requests
from bs4 import BeautifulSoup
import json
import getpass
import re
import os
from colorama import init, Fore, Back, Style
from pprint import pprint


BASE = 'https://is.sps-prosek.cz'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'


def get_cookie(username, password):
    temp_session = requests.Session()

    temp_session.headers.update({'User-Agent': USER_AGENT})

    resp = temp_session.get(f'{BASE}/app/login/', allow_redirects=True)

    match = re.search(r'app=([a-f0-9]+)', resp.url) or re.search(r'app=([a-f0-9]{20,})', resp.text)

    if not match:
        return None
    
    app_token = match.group(1)

    temp_session.post(
        f'{BASE}/app/login/?app={app_token}',
        data={'username': username, 'password': password, 'persistent': 'false'},
        allow_redirects=True
    )
    
    return temp_session.cookies.get('BakaAuth')

def get_marks(user, password):

    BakaAuth = get_cookie(user, password)

    cookies = {
        'BakaAuth': BakaAuth
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    response = requests.get(f'{BASE}/app/next/prubzna.aspx', cookies=cookies, headers=headers)



    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
    

        subjects = soup.find_all('h3', class_=False)
        marks = soup.find_all('div', class_='ob')
        subjectsRow = soup.find_all('div', class_='predmet-radek')
        subjectsCount = len(subjectsRow)
        marksText = []

        subject = [subject.get_text() for subject in subjects]
        for mark in marks:
            marksText.append(mark.text.strip())
        a = 0        
        g = 0
        final = {}
        for row in subjectsRow:
            pocet = len(row.find_all("div", class_="ob"))
            radekSubject = row.select_one('div.predmet-radek h3')

            #################
            ## NAZEV PREDMETU

            #####################################################
            #### je to only prep pro json pro beta test uncomment 
        
            # print('')
            # print(Fore.BLUE + Back.BLACK + radekSubject.text + Style.RESET_ALL)
            # print('')
            ###################################################

            ################

            markInSubject = []
            for i in range(pocet):
                div_element = soup.find_all('div', class_="znamka-v")
                data_str = div_element[g]['data-clasif']
                data_dict = json.loads(data_str)
                caption = data_dict.get('caption')
                vaha = data_dict.get('vaha')

                #######################
                ## NAZEV TESTU + ZNAMKA

                ##################################################
                #### je to only prep pro json pro beta test uncomment 
                
                # print(Fore.GREEN + Back.BLACK + caption + '  ' + marksText[a] + '  ' + str(vaha) + Style.RESET_ALL)

                ##################################################

                #######################

                ##########################
                ## PRIPRAVA ARRAY PRO JSON

                if marksText[a].find('-') == True:
                    marksText[a] = re.sub('-','',marksText[a])
                    marksText[a] = int(marksText[a]) + 0.5
            
            
            
                if radekSubject.text not in final:
                    final[radekSubject.text] = []

                #final[radekSubject.text] = {'nazev': str(caption)}
                #final[radekSubject.text]['znamka'] = float(marksText[a])
                #final[radekSubject.text]['vaha'] = str(vaha)

                final.setdefault(radekSubject.text, []).append({"nazev": str(caption), "znamka": float(marksText[a]), "vaha": str(vaha) })

                a = a+1
                g = g+1

            #####################################
            ################
            ## POCET ZNAMEK

            ##################################################
            #### je to only prep pro json pro beta test uncomment 

            # print('')
            # print(Fore.RED + Back.BLACK + "Pocet znamek " + str(pocet) + Style.RESET_ALL)
        
            ##################################################

            ###############

            ###################
            ## ZAPIS DO JSONU
            SubjectMarksCount = []
            SubjectMarksCount = (row.append(f" - {subject[1]}: {pocet} "))
        jsonString = json.dumps(final, ensure_ascii=False, indent=4)

#        with open ("subjects.json", "w", encoding='utf-8') as f:
#            f.write(jsonString)
        return(jsonString)
            ####################

