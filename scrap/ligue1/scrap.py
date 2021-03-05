from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import dateparser
import time
import sys
import os
import json
import re
import datetime

import psycopg2
import psycopg2.extras


PG_HOST = 'localhost'
PG_DATABASE = 'betai'
PG_USER = 'postgres'
PG_PASSWORD = 'dodu'
PG_PORT = '5432'


class SQLUtil():

    @classmethod
    def play_sql_classement(cls, liste):
        connection = None
        cursor = None

        try:
            connection = psycopg2.connect(user=PG_USER,
                                          password=PG_PASSWORD,
                                          host=PG_HOST,
                                          port=PG_PORT,
                                          database=PG_DATABASE)

            cursor = connection.cursor()

            cursor.execute("INSERT into public.classement_ligue1(saison, ligue, journee, classement, equipe, points, joues, gagnes, nuls, perdus, buts, contre, diff, forme_draw, forme_win, forme_lose) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [x for x in liste])
            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()

    @classmethod
    def play_sql_journee(cls, liste):
        connection = None
        cursor = None

        try:
            connection = psycopg2.connect(user=PG_USER,
                                          password=PG_PASSWORD,
                                          host=PG_HOST,
                                          port=PG_PORT,
                                          database=PG_DATABASE)

            cursor = connection.cursor()

            cursor.execute("INSERT into public.journee_ligue1(saison, ligue, journee, date, home_team, home_score, away_score, away_team, resultat, date_ajout) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [x for x in liste])
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


def get_suivi_classement(saison):
    driver = initDriver()

    driver.get("https://www.ligue1.fr/classement?seasonId={}&matchDay=1".format(saison))
    time.sleep(2)

    liste_journee = len(driver.find_elements_by_xpath("//*[contains(@id,'selectdays')]/option"))

    print('Scrap saison {}, journee {}'.format(saison, 1))
    get_data_classement(driver, saison)
    #driver.close()

    for journee in range(2, liste_journee +1):
        time.sleep(2)
        print('Scrap saison {}, journee {}'.format(saison, journee))

        driver.get("https://www.ligue1.fr/classement?seasonId={}&matchDay={}".format(saison, journee))
        
        get_data_classement(driver, saison, journee=journee)
    
    driver.close()
    
def get_data_classement(driver, saison, journee = 1):
    blocs_position = driver.find_elements_by_xpath("//div[@class='classement-table-body']/ul/li")

    for bloc in blocs_position:
        liste_donnees = []
        saison = saison
        ligue = 'Ligue 1'
        journee = journee

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

        liste_donnees.extend((saison, ligue, journee, pos, club, points, joues, gagnes, nuls, perdus, buts, contre, diff, forme_draw, forme_win, forme_lose))
        SQLUtil.play_sql_classement(liste_donnees)


def get_suivi_journee(saison):
    driver = initDriver()

    driver.get("https://www.ligue1.fr/calendrier-resultats?seasonId={}&matchDay=1".format(saison))
    time.sleep(2)

    liste_journee = len(driver.find_elements_by_xpath("//*[contains(@id,'SelectDays')]/option"))
    print('liste journee', liste_journee)

    print('Scrap saison {}, journee {}'.format(saison, 4))
    get_data_journee(driver, saison)

    for journee in range(2, liste_journee +1):
        time.sleep(2)
        print('Scrap saison {}, journee {}'.format(saison, journee))

        driver.get("https://www.ligue1.fr/calendrier-resultats?seasonId={}&matchDay={}".format(saison, journee))
        
        get_data_journee(driver, saison, journee=journee)
    
    driver.close()

def get_data_journee(driver, saison, journee = 1):
    
    saison = saison
    ligue = 'Ligue 1'
    
    bloc_calendrier = driver.find_element_by_xpath("//div[@class='calendar-widget-container']")
 
    blocs_journee = bloc_calendrier.find_elements_by_xpath("./div")
    blocs_match = bloc_calendrier.find_elements_by_xpath("./ul")

    for day, match in zip(blocs_journee, blocs_match):
        date = dateparser.parse(day.text).date()

        bloc_detail_match = match.find_elements_by_xpath("./li")
        
        for detail in bloc_detail_match:
            liste_donnees = []

            hometeam = detail.find_element_by_xpath("./div[@class='clubs-container left']/div[@class='club home']").text
            awayteam = detail.find_element_by_xpath("./div[@class='clubs-container left']/div[@class='club away']").text
            
            bloc_result = detail.find_element_by_xpath("./div[@class='clubs-container left']/div[@class='result']/a")
            home_score = bloc_result.find_element_by_xpath("./span[contains(@id,'home')]").text
            away_score = bloc_result.find_element_by_xpath("./span[contains(@id,'away')]").text
            
            if away_score == home_score:
                result = 'N'
            elif away_score > home_score:
                result = '2'
            elif away_score < home_score:
                result = '1'
            
            liste_donnees.extend((saison, ligue, journee, date, hometeam, home_score, away_score, awayteam, result, datetime.datetime.today().strftime('%Y-%m-%d')))
            SQLUtil.play_sql_journee(liste_donnees)

#saison = ['2000-2001','2001-2002', '2002-2003']
#saison = ['2003-2004','2005-2006', '2006-2007', '2007-2008','2008-2009','2009-2010']
#saison = ['2010-2011','2011-2012','2012-2013','2013-2014','2014-2015','2015-2016','2016-2017','2017-2018','2018-2019','2019-2020','2020-2021']
saison = ['2004-2005']

for i in saison:
    #get_suivi_classement(i)
    get_suivi_journee(i)