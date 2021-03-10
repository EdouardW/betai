import pandas as pd
import os
import datetime


from utils import SQLUtil


class DataPrep():

    def __init__(self, path, nom_championnat):
        self.__full_path__ = os.path.join(path, nom_championnat)
        self.__all_files__ = os.listdir(self.__full_path__)
        self.__all_df__ = []

        for f in self.__all_files__:
            print(f)
            df = self.load_files_and_format(f)
            df = self.add_journee(df)
            df['file'] = f
            self.__all_df__.append(df)

        self.df_all_seasons = pd.concat(self.__all_df__, ignore_index=True)
        self.save_clubs(self.df_all_seasons)
        self.df_filtered = self.filtered_df(self.df_all_seasons)

        self.save_pdf(self.df_filtered)

    def load_files_and_format(self, f):
        custom_date_parser = lambda x: datetime.datetime.strptime(x, "%d/%m/%Y")
        df = pd.read_csv(os.path.join(self.__full_path__, f), sep=',', parse_dates=['Date'], date_parser=custom_date_parser)
        
        return df

    def save_clubs(self, df):
        unique_clubs = list(set([x for x in df['HomeTeam']]))

        SQLUtil.play_sql(unique_clubs)

    def filtered_df(self, df):
        features_to_keep =  ['file', 'journee', 'Date', 'HomeTeam', 'AwayTeam']
        df_filtered = df[features_to_keep]

        return df_filtered

    def add_journee(self, df):
        number_of_team = 20 
        step = list(range(0, number_of_team** 2 -number_of_team, int(number_of_team / 2)))

        df_temp = df.sort_values(by="Date").reset_index()

        for j in range(len(step)):
            journee = j + 1
            raw_inf = step[j]
            raw_sup = step[j] + int(number_of_team / 2)
            df_temp.loc[raw_inf:raw_sup-1, 'journee'] = int(j + 1)
        
        return df_temp

    def save_pdf(self, df_name):
        df_name.to_csv(os.path.join(path, '{}_complet_filtered.csv'.format(nom_championnat)), index=False)


path = 'scrap/footballData/data/'
nom_championnat = 'FRANCE_ligue1'
DataPrep(path, nom_championnat) 
