#!/usr/bin/env python

from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager

from Team import Team
import time
import sys
import os

def initDriver():
  driver = webdriver.Chrome(ChromeDriverManager().install())
  return driver

#standings-18594
def getAllTeamsLigue1():
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
    teams = getAllTeamsLigue1()
    for team in teams:
        print (team.getName())
        print('---')
"""     print(teams) """

"""     team = subMenuTeams(teams)
    links = getAllLinksTeam(team.getWebURL())
    getDataByLinks(links) """
  
"""   toQuit = False
  option = 0
  while not toQuit:
    print ("1. Get JSON data entering team URL (e.g. https://www.whoscored.com/Teams/819/Show/Spain-Getafe)")
    print ("2. Select team from LaLiga")
    print ("3. Get JSON data entering single match (e.g. https://www.whoscored.com/Matches/1492131/Live/Spain-LaLiga-2020-2021-Athletic-Bilbao-Getafe)")
    print ("4. Exit")
    print ("Please, choose an option")
    option = askNumber()

    if option == 1:
      url = str(input("URL: "))
      links = getAllLinksTeam(url)
      getDataByLinks(links)
      print("Job finished")
    elif option == 2:
      teams = getAllTeamsLaLiga()
      team = subMenuTeams(teams)
      links = getAllLinksTeam(team.getWebURL())
      getDataByLinks(links)
      print("Job finished")
    elif option == 3:
      url = str(input("URL: "))
      saveDataSingleMatch(url)
      print("Job finished")
    elif option == 4:
      toQuit = True
    else:
      print ("Enter a number between 1 and 4")
  print ("Bye")
  sys.exit() """

menu()