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
        features_to_keep =  [
            'saison', 'journee', 'Date', \
            'HomeTeam', 'AwayTeam', \
            'cl_hometeam', 'cl_awayteam', \
            'points_h','gagnes_h','nuls_h','perdus_h','buts_h','contre_h', \
            'points_a','gagnes_a','nuls_a','perdus_a','buts_a','contre_a', \
            'forme_h_win', 'forme_h_draw', 'forme_h_lose' , 'forme_a_win', 'forme_a_draw', 'forme_a_lose', \
            'FTHG','FTAG','FTR','HTHG','HTAG','HTR',\
            'HST','AST','HC','AC','HY','AY','HR','AR',\
            'B365H','B365D','B365A']
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

                home_request = SQLUtil.get_classement_and_forme_sql(ht_sortie[0], row['saison'], int(row['journee'])- 1)
                away_request = SQLUtil.get_classement_and_forme_sql(at_sortie[0], row['saison'], int(row['journee'])- 1)

                cl_ht = home_request[0]
                cl_at = away_request[0]

                forme_h_win = home_request[1]
                forme_h_draw = home_request[2]
                forme_h_lose = home_request[3]
                forme_a_win = away_request[1]
                forme_a_draw = away_request[2]
                forme_a_lose = away_request[3]

                points_h = home_request[4]
                gagnes_h = home_request[5]
                nuls_h = home_request[6]
                perdus_h = home_request[7]
                buts_h = home_request[8]
                contre_h = home_request[9]
                
                points_a = away_request[4]
                gagnes_a = away_request[5]
                nuls_a = away_request[6]
                perdus_a = away_request[7]
                buts_a = away_request[8]
                contre_a =away_request[9]
                
                df_name.loc[index, 'cl_hometeam'] = cl_ht
                df_name.loc[index, 'cl_awayteam'] = cl_at
                df_name.loc[index, 'forme_h_win'] = str(forme_h_win)
                df_name.loc[index, 'forme_h_draw'] = str(forme_h_draw)
                df_name.loc[index, 'forme_h_lose'] = str(forme_h_lose)
                df_name.loc[index, 'forme_a_win'] = str(forme_a_win)
                df_name.loc[index, 'forme_a_draw'] = str(forme_a_draw)
                df_name.loc[index, 'forme_a_lose'] = str(forme_a_lose)
                
                df_name.loc[index, 'points_h'] = points_h
                df_name.loc[index, 'gagnes_h'] = gagnes_h
                df_name.loc[index, 'nuls_h'] = nuls_h
                df_name.loc[index, 'perdus_h'] = perdus_h
                df_name.loc[index, 'buts_h'] = buts_h
                df_name.loc[index, 'contre_h'] = contre_h

                df_name.loc[index, 'points_a'] = points_a
                df_name.loc[index, 'gagnes_a'] = gagnes_a
                df_name.loc[index, 'nuls_a'] = nuls_a
                df_name.loc[index, 'perdus_a'] = perdus_a
                df_name.loc[index, 'buts_a'] = buts_a
                df_name.loc[index, 'contre_a'] = contre_a


            else:
                df_name.loc[index, 'forme_h_win'] = '-1'
                df_name.loc[index, 'forme_h_draw'] = '-1'
                df_name.loc[index, 'forme_h_lose'] = '-1'
                df_name.loc[index, 'forme_a_win'] = '-1'
                df_name.loc[index, 'forme_a_draw'] = '-1'
                df_name.loc[index, 'forme_a_lose'] = '-1'
                df_name.loc[index, 'points_h'] = '-1'
                df_name.loc[index, 'gagnes_h'] = '-1'
                df_name.loc[index, 'nuls_h'] = '-1'
                df_name.loc[index, 'perdus_h'] = '-1'
                df_name.loc[index, 'buts_h'] = '-1'
                df_name.loc[index, 'contre_h'] = '-1'
                df_name.loc[index, 'points_a'] = '-1'
                df_name.loc[index, 'gagnes_a'] = '-1'
                df_name.loc[index, 'nuls_a'] = '-1'
                df_name.loc[index, 'perdus_a'] = '-1'
                df_name.loc[index, 'buts_a'] = '-1'
                df_name.loc[index, 'contre_a'] = '-1'

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
#nom_championnat = 'FRANCE (copie)'
#name = 'FRANCE(copie)_ligue1_complet_filtered.csv'

nom_championnat = 'FRANCE_ligue1'
name = 'FRANCE_ligue1_complet_filtered.csv'

DataPrep(path, nom_championnat) 
#MapClubName(path, name)