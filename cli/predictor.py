import colorama
from core.scraper import get_marks
import inquirer
import pprint
import json
import requests
import getpass

def renderList(marksFromSelectedSubject):

    questions = [
        inquirer.List(
            name = "mark",
            message="Znamky",
            choices = marksFromSelectedSubject,
        ),
    ]

    answerMark = inquirer.prompt(questions)
    return(answerMark)


OriginalDiametr = None

def diametrCalculator(marksFromSelectedSubject):

    global OriginalDiametr

    markList = []
    midCount : float = 0
    vahaSum : float = 0
    topFractionMidCount : float = 0
    for item in marksFromSelectedSubject:

        if isinstance(item, dict):
            znamka = float(item['znamka'])
            vaha = int(item['vaha'])
            midCount = znamka * vaha
            topFractionMidCount += midCount
            vahaSum += vaha
            
            markList.append({
                'znamka': znamka,
                'vaha': vaha
            })

    diametr = topFractionMidCount / vahaSum

    if OriginalDiametr is None:
        OriginalDiametr = diametr
    else:
        pprint.pprint("originalni Průměr: " + str(round(OriginalDiametr, 2)))
    pprint.pprint("Průměr: " + str(round(diametr, 2)))

    


OriginalDiametr = None


user = input('Username: ')

password = getpass.getpass("Password: ")




data = get_marks(user, password)

#pprint.pprint(data)

#################################################
"""
with open('core/subjects.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
"""
subjects = []
i: int = 0
for key in data:
    subjects.append(key)

questions = [
    inquirer.List(
        name = "subject",
        message="Jaky predmet?",
        choices = subjects,
    ),
]

answerSubject = inquirer.prompt(questions)

marksFromSelectedSubject = []
marksFromSelectedSubject.append("add new")
marksFromSelectedSubject.append("DONE")

for subject in data:
    if subject == answerSubject['subject']:
        for mark in data[answerSubject['subject']]:
            marksFromSelectedSubject.append(mark)




while True:
    diametrCalculator(marksFromSelectedSubject)
    #pprint.pprint("Originalni průměr: " + str(round(diametr, 2)))
    answerMark = renderList(marksFromSelectedSubject)
    if answerMark["mark"] == "DONE":
        exit()
        # print(answerSubject['subject'])
        # pprint.pprint(answerMark['mark'])


    if answerMark["mark"] == 'add new':
        nazev = f"added{i}"
        i: int = i + 1
        znamka: float = float(input("Znamka: "))
        vaha: int = int(input("Vaha: "))
    
        markList = {
            'nazev': nazev,
            'znamka': znamka,
            'vaha': vaha
        } 

        marksFromSelectedSubject.append(markList)


