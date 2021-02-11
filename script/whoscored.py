#!/usr/bin/env python

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from data_model import Team, Championnat
from utils import serializeReportContent
#from data_model import Team
import time
import sys
import os
import json


def initDriver():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    return driver


def getChampionnat():
    driver = initDriver()
    driver.get("https://www.whoscored.com/")
    time.sleep(2)

    championnat = driver.find_elements_by_xpath("//*[@id='popular-tournaments-list']/li[*]/a")

    championnatListe = []
    i = 0
    while i < len(championnat):
        curseur = championnat[i]
        championnatURL = curseur.get_attribute("href")
        championnatPays = curseur.get_attribute("title")
        championnatNom = curseur.get_attribute("text")
        championnatListe.append(Championnat(championnatPays, championnatNom, championnatURL))

        i += 1

    driver.close()

    with open(os.path.join(os.path.dirname(__file__), 'output', 'championnat.json'), 'w') as outfile:
        json.dump(championnatListe, outfile, default=serializeReportContent)


def getAllTeamsLigue1():
    # standings-18594
    teams = []
    driver = initDriver()
    driver.get("https://www.whoscored.com/Regions/74/Tournaments/22/France-Ligue-1")
    time.sleep(2)
    teamsList = driver.find_elements_by_xpath("//*[@id='standings-18594-content']/tr[*]/td[*]/a[@class='team-link ']")

    i = 0
    while i < len(teamsList):
        anchor = teamsList[i]
        teamURL = anchor.get_attribute("href")
        teamName = anchor.get_attribute("innerHTML")
        teamURL = teamURL.replace("/Show/","/Fixtures/")
        teams.append(Team(teamName, teamURL))

        i += 1
    driver.close()

    return teams


def menu():
    # teams = getAllTeamsLigue1()

    champ = getChampionnat()
    print('---')
    getAllTeamsLigue1()


"""     for cham in champ:
        print(cham.getName())
        print(cham.getWebURL())
        print('---')
"""


menu()
