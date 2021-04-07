# S'amuser avec les datas des chammpionnats de footaball francais (Ligue 1 / Ligue 2)

L'objectif est dans un premier temps de collecter les datas issus des sites:
- https://www.football-data.co.uk/ => récupération entres autres des résultats et des côtes sur les sites de paris pour chaque match.
- https://www.ligue1.fr => récupération des classements, résultats et forme des équipes sur le site officiel du championnat francais.

Utilisations identifiées:
- Dataviz (Apache Superset)
- Prédiction avec algos de ML

## Architecture du projet





## 'Scrap' directory 

### 'ligue1' directory 
Scrap with selenium to get all ranking positions by match day and all scores.

### footballData directory 
Merge all files in one csv output files. 

### result output

'saison' \
'journee' \
'Date'\
'HomeTeam'\
'AwayTeam'\
'cl_hometeam'\
'cl_awayteam'\
'forme_h_win'\
'forme_h_draw'\
'forme_h_lose'\
'forme_a_win'\
'forme_a_draw'\
'forme_a_lose'\



## 'ML' directory

TODO
