import pandas as pd
import os
import datetime

import psycopg2
import psycopg2.extras

from utils import SQLUtil


class DataPrep():

    def __init__(self, path, nom_championnat):
        self.__full_path__ = os.path.join(path, nom_championnat)
        self.__all_files__ = os.listdir(self.__full_path__)
        self.__all_df__ = []

        for f in self.__all_files__:
            df = self.load_files_and_format(f)
            df['saison'] = f.split('.')[0]
            print(df['saison'])
            df = self.add_journee(df)
            df = self.update_classement(df)
            
            self.__all_df__.append(df)

        self.df_all_seasons = pd.concat(self.__all_df__, ignore_index=True)
        #self.save_clubs(self.df_all_seasons)
        self.df_filtered = self.filtered_df(self.df_all_seasons)

        self.save_csv(self.df_filtered)

    def load_files_and_format(self, f):
        custom_date_parser = lambda x: datetime.datetime.strptime(x, "%d/%m/%Y")
        df = pd.read_csv(os.path.join(self.__full_path__, f), sep=',', parse_dates=['Date'], date_parser=custom_date_parser)
        
        return df

    def save_clubs(self, df):
        unique_clubs = list(set([x for x in df['HomeTeam']]))

        SQLUtil.play_sql(unique_clubs)

    def filtered_df(self, df):
        features_to_keep =  ['saison', 'journee', 'Date', 'HomeTeam', 'AwayTeam', 'cl_hometeam', 'cl_awayteam', 'forme_h_win', 'forme_h_draw', 'forme_h_lose' , 'forme_a_win', 'forme_a_draw', 'forme_a_lose']
        df_filtered = df[features_to_keep]

        return df_filtered

    def add_journee(self, df):
        number_of_team = 20 
        step = list(range(0, number_of_team** 2 -number_of_team, int(number_of_team / 2)))

        df_temp = df.sort_values(by="Date").reset_index()

        for j in range(len(step)):
            raw_inf = step[j]
            raw_sup = step[j] + int(number_of_team / 2)
            df_temp.loc[raw_inf:raw_sup-1, 'journee'] = str(j + 1)
            if int(j + 1) == 1:
                df_temp.loc[raw_inf:raw_sup-1, 'cl_hometeam'] = '-1'
                df_temp.loc[raw_inf:raw_sup-1, 'cl_awayteam'] = '-1'
            else:
                 df_temp.loc[raw_inf:raw_sup-1, 'cl_hometeam'] = '0'
                 df_temp.loc[raw_inf:raw_sup-1, 'cl_awayteam'] = '0'
        
        return df_temp

    def update_classement(self,df_name):
        print(df_name['saison'])
        for index, row in df_name.iterrows():
            if row['cl_hometeam'] != '-1':
                ht_sortie = SQLUtil.mapping_name_sql(row['HomeTeam'])
                at_sortie = SQLUtil.mapping_name_sql(row['AwayTeam'])

                cl_ht = SQLUtil.get_classement_sql(ht_sortie[0], row['saison'], int(row['journee'])- 1)[0]
                cl_at = SQLUtil.get_classement_sql(at_sortie[0], row['saison'], int(row['journee']) - 1)[0]

                forme_h_win = SQLUtil.get_forme_sql(ht_sortie[0], row['saison'], int(row['journee'])- 1)[0]
                forme_h_draw = SQLUtil.get_forme_sql(ht_sortie[0], row['saison'], int(row['journee']) - 1)[1]
                forme_h_lose = SQLUtil.get_forme_sql(ht_sortie[0], row['saison'], int(row['journee']) - 1)[2]

                forme_a_win = SQLUtil.get_forme_sql(at_sortie[0], row['saison'], int(row['journee'])- 1)[0]
                forme_a_draw = SQLUtil.get_forme_sql(at_sortie[0], row['saison'], int(row['journee']) - 1)[1]
                forme_a_lose = SQLUtil.get_forme_sql(at_sortie[0], row['saison'], int(row['journee']) - 1)[2]
                
                df_name.loc[index, 'cl_hometeam'] = cl_ht
                df_name.loc[index, 'cl_awayteam'] = cl_at

                df_name.loc[index, 'forme_h_win'] = str(forme_h_win)
                df_name.loc[index, 'forme_h_draw'] = str(forme_h_draw)
                df_name.loc[index, 'forme_h_lose'] = str(forme_h_lose)
                df_name.loc[index, 'forme_a_win'] = str(forme_a_win)
                df_name.loc[index, 'forme_a_draw'] = str(forme_a_draw)
                df_name.loc[index, 'forme_a_lose'] = str(forme_a_lose)

        return df_name

    def save_csv(self, df_name):
        df_name.to_csv(os.path.join(path, '{}_complet_filtered.csv'.format(nom_championnat)), index=False)

class MapClubName():

    def __init__(self, path, filename):
        self.list_club_duplicate = []
        self.list_club_unique = []

        list_unique_datacouk = self.get_unique_name_from_file()
        list_unique_lfp = self.request()

        #list_unique_lfp = [x.capitalize() for x in list_unique_lfp]

        list_unique_datacouk = sorted(list(list_unique_datacouk))
        list_unique_lfp = sorted(list_unique_lfp)

        for i in list_unique_lfp:
            print(i)

    def request(self):
        req ='SELECT DISTINCT(equipe) FROM public.classement_ligue1'
        response = SQLUtil.play_sql(req)
        return response

    def get_unique_name_from_file(self):
        df = pd.read_csv(os.path.join(path, name), sep=',')
        
        for club_name_home in df['HomeTeam']:
            self.list_club_duplicate.append(club_name_home)
        for club_name_away in df['AwayTeam']:
            self.list_club_duplicate.append(club_name_away)

        self.list_club_unique = set(self.list_club_duplicate)
        return self.list_club_unique

    
path = 'scrap/footballData/data/'
nom_championnat = 'FRANCE (copie)'
name = 'FRANCE (copie)_ligue1_complet_filtered.csv'

DataPrep(path, nom_championnat) 
#MapClubName(path, name)