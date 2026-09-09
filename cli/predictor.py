import colorama
from core.scraper import get_marks
import inquirer
import pprint
import json
import requests
import getpass


##momentalne nemam znamky fetchujeme prefiled json
#user = input('Username: ')

#password = getpass.getpass("Password: ")




#data = get_marks(user, password)

#################################################

with open('core/subjects.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

subjects = []


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

def renderList(marksFromSelectedSubject):
    for subject in data:
        if subject == answerSubject['subject']:
            for mark in data[answerSubject['subject']]:
                marksFromSelectedSubject.append(mark)


    questions = [
        inquirer.List(
            name = "mark",
            message="Znamky",
            choices = marksFromSelectedSubject,
        ),
    ]

    answerMark = inquirer.prompt(questions)
    return(answerMark)

while True:
    answerMark = renderList(marksFromSelectedSubject)
    if answerMark["mark"] != "DONE":


        i: int = 0
        newMark = []
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

        answerMark = renderList(marksFromSelectedSubject)
    else:
        exit()
        print(answerSubject['subject'])
        pprint.pprint(answerMark['mark'])


