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
import re


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
        nom_pays = curseur.get_attribute("title")
        nom_championnat = curseur.get_attribute("text")
        championnatListe.append(Championnat(
                                            nom_pays=nom_pays,
                                            nom_championnat=nom_championnat,
                                            webURL=championnatURL
                                            ))

        i += 1

    driver.close()

    with open(os.path.join(os.path.dirname(__file__), 'output', 'championnats_majeurs.json'), 'w') as outfile:
        json.dump(championnatListe, outfile, default=serializeReportContent)

    return championnatListe


def getChampionnatsComplets():
    driver = initDriver()
    driver.get("https://www.whoscored.com/")
    time.sleep(2)
    WebDriverWait(driver, 10)
    championnat = driver.find_elements_by_xpath("//*[@type='text/javascript']")

    championnatListe = []
    for _ in championnat:
        if 'var allRegions' in _.get_attribute("text"):
            global_bloc_text = _.get_attribute("text").replace('\n', '')
            final_bloc_text = re.findall('var\ allRegions\ \=\ \[(.*?)\]\;', global_bloc_text)
            detail_list = re.split('type\:', final_bloc_text[0])

            for bloc_pays in detail_list[1:]:
                sous_bloc_general = re.findall('id\:(.*?)tournaments\:\ ', bloc_pays)
                sous_bloc_tournoi = re.findall('tournaments\:\ \[(.*?)\]', bloc_pays)

                id_pays = int(re.findall(r'\d+', sous_bloc_general[0])[0])
                nom_pays = re.findall('name\:\ (.*?),', sous_bloc_general[0])[0]

                for bloc in sous_bloc_tournoi:
                    bloc_championnat = re.findall('id:(.*?)\}', bloc)

                    for i in bloc_championnat:
                        id_championnat = int(re.search(r'\d+', i).group())
                        url_championnat = os.path.join("https://www.whoscored.com", re.findall('url\:\'(.*?)\',', i)[0][1:])
                        nom_championnat = re.findall('name\:\'(.*?)\'', i)[0]

                        championnatListe.append(Championnat(id_pays,
                                                            nom_pays,
                                                            id_championnat,
                                                            nom_championnat,
                                                            url_championnat,
                                                            ))

    with open(os.path.join(os.path.dirname(__file__), 'output', 'championnats_complets.json'), 'w') as outfile:
        json.dump(championnatListe, outfile, default=serializeReportContent)


def getClubs(nom_championnat, url):
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
        #teamURL = teamURL.replace("/Show/","/Fixtures/")
        clubListe.append(Club(teamName, teamURL))

        i += 1

    driver.close()

    with open(os.path.join(os.path.dirname(__file__), 'output', '{}_clubs.json'.format(nom_championnat)), 'w') as outfile:
        json.dump(clubListe, outfile, default=serializeReportContent)


def getJoueurs(nom_equipe, url_equipe):
    driver = initDriver()
    driver.get(url_equipe)
    time.sleep(2)

    pass

    # with open(os.path.join(os.path.dirname(__file__), 'output', '{}_effectifs.json'.format(nom_equipe)), 'w') as outfile:
    #    json.dump(clubListe, outfile, default=serializeReportContent)


# getChampionnatsComplets()
# getChampionnatsMajeurs()
# getClubs("Ligue 1", "https://fr.whoscored.com/Regions/74/Tournaments/22/France-Ligue-1")
#getJoueurs("Lens", "https://fr.whoscored.com/Teams/309/Show/France-Lens")
