from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import time
import sys
import os
import json
import re

import psycopg2
import psycopg2.extras


PG_HOST = 'localhost'
PG_DATABASE = 'betai'
PG_USER = 'postgres'
PG_PASSWORD = 'dodu'
PG_PORT = '5432'


class SQLUtil():

    @classmethod
    def play_sql(cls, liste):
        connection = None
        cursor = None

        try:
            connection = psycopg2.connect(user=PG_USER,
                                          password=PG_PASSWORD,
                                          host=PG_HOST,
                                          port=PG_PORT,
                                          database=PG_DATABASE)

            cursor = connection.cursor()

            cursor.execute("INSERT into public.classement_ligue1(saison, ligue, journee, classement, equipe, joues, gagnes, nuls, perdus, buts, contre, diff, forme_draw, forme_win, forme_lose) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [x for x in liste])
            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()




def initDriver():
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    return driver


def getChampionnatsComplets(saison):
    driver = initDriver()

    driver.get("https://www.ligue1.fr/classement?seasonId={}&matchDay=1".format(saison))
    time.sleep(2)

    blocs_position = driver.find_elements_by_xpath("//div[@class='classement-table-body']/ul/li")

    for bloc in blocs_position:
        liste_donnees = []
        saison = saison
        ligue = 'Ligue 1'
        journee = 1

        pos = bloc.find_element_by_xpath("./div[contains(@class,'position')]").text
        club = bloc.find_element_by_xpath("./*[contains(@class,'club')]/a[contains(@class,'clubnamelink')]").text
        points = bloc.find_element_by_xpath("./div[contains(@class,'points')]").text
        
        bloc_stats = bloc.find_elements_by_xpath("./div[contains(@class,'RankPage')]")

        joues = bloc_stats[0].text
        gagnes = bloc_stats[1].text
        nuls = bloc_stats[2].text
        perdus = bloc_stats[3].text
        buts = bloc_stats[4].text
        contre = bloc_stats[5].text
        diff = bloc_stats[6].text
        
        forme_draw = len(bloc_stats[7].find_elements_by_xpath("./span[contains(@class,'circle draw')]"))
        forme_win = len(bloc_stats[7].find_elements_by_xpath("./span[contains(@class,'circle win')]"))
        forme_lose = len(bloc_stats[7].find_elements_by_xpath("./span[contains(@class,'circle lose')]"))

        liste_donnees.extend((saison, ligue, journee, pos, club, joues, gagnes, nuls, perdus, buts, contre, diff, forme_draw, forme_win, forme_lose))
        SQLUtil.play_sql(liste_donnees)
        #print([x for x in liste_donnees])
    #liste_journee = len(driver.find_elements_by_xpath("//*[contains(@id,'selectdays')]/option"))
    #for i in range (liste_journee):
    #    driver.get("https://www.ligue1.fr/classement?seasonId={}&matchDay={}".format(saison, i+1))


saison = '1997-1998'
getChampionnatsComplets(saison)