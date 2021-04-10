import os
import pandas as pd

from flask import make_response, Response
from lxml import html
from betai_flask import app
from pathlib import Path


def list_files_path(country_name, league_name):
    root_path = Path(f'./input/datacouk/all_files/{country_name}')
    list_path = []
    for file in root_path:
        if '.csv' in file and league_name in file:
            list_path.append(os.path.join(root_path, country_name, file))
    return list_path


def gather_unique_file(country_name, season_name):
    output_file = open('file.csv', 'w')
    output_file = pd.concat([pd.read_csv(file) for file in list_files_path(country_name, season_name)]).drop([0], axis = 0)

    output_file.to_csv('./datacoukinput/gathered_file.csv')


"""         try:
            with open(file, 'r') as csvfile:
                lines = csvfile.readlines()
                #records = [[value for value in line.split(",")] for line in lines]
                print(lines)
                print('---')
        except:
            print(f'{file} not loaded') """


@app.route('/datacouk/gather_all_files')
def gather_files(country_name, season_name):
    league_file = gather_unique_file('France', season_name)

