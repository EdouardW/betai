#!/usr/bin/env python

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from data_model import Club, Championnat
from utils import serializeReportContent
#from data_model import Team
import time
import sys
import os
import json


def initDriver():
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    return driver


def getChampionnatsMajeurs():
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

    with open(os.path.join(os.path.dirname(__file__), 'output', 'championnats.json'), 'w') as outfile:
        json.dump(championnatListe, outfile, default=serializeReportContent)

    return championnatListe


def getChampionnatsComplets():
    driver = initDriver()
    driver.get("https://www.whoscored.com/")
    time.sleep(2)
    WebDriverWait(driver, 10)
    championnat = driver.find_elements_by_xpath("//*[@type='text/javascript']")
    #championnat = driver.find_elements_by_xpath("//*[@class='nav-region']")
    print(championnat)
    #print(championnat[0].text)


def getClubs(name_championnat, url):
    driver = initDriver()
    driver.get(url)
    time.sleep(2)

    clubs = driver.find_elements_by_xpath("//*[contains(@id,'standings')][contains(@id,'content')]/tr[*]/td[*]/a[@class='team-link ']")

    clubListe = []
    i = 0
    while i < len(clubs):
        curseur = clubs[i]
        teamURL = curseur.get_attribute("href")
        teamName = curseur.get_attribute("innerHTML")
        teamURL = teamURL.replace("/Show/","/Fixtures/")
        clubListe.append(Club(teamName, teamURL))

        i += 1

    driver.close()

    with open(os.path.join(os.path.dirname(__file__), 'output', '{}_clubs.json'.format(name_championnat)), 'w') as outfile:
        json.dump(clubListe, outfile, default=serializeReportContent)


championnatListe = getChampionnatsMajeurs()
for _ in championnatListe:
    name = _._getName()
    url = _._getWebURL()
    getClubs(name, url)


# NON FONCTIONNEL getChampionnatsComplets()
# getClubs("https://www.whoscored.com/Regions/252/Tournaments/2/England-Premier-League")


"""     for cham in champ:
        print(cham.getName())
        print(cham.getWebURL())
        print('---')
"""
