import requests
import os

from lxml import html
from betai_flask import app

import json
from flask import make_response, Response

def find_all_links(url) -> list:
    response = requests.get(url)
    tree = html.fromstring(response.content)
    href_links = tree.xpath('//a/@href')

    return href_links


def find_all_csv_links(url) -> list:
    all_links = find_all_links(url)

    list_csv_filename = []
    for link in all_links:
        if '.csv' in link:
            list_csv_filename.append(os.path.join('https://www.football-data.co.uk/', link))

    return list_csv_filename


def find_note_link(url) -> str:
    all_links = find_all_links(url)

    for link in all_links:
        if 'notes.txt' in link:
            note_link = os.path.join('https://www.football-data.co.uk/', link)

    return note_link


def create_input_folder(country_name, path):

    if os.path.isdir(path) is False:
        #print(os.getcwd())
        os.mkdir(path)


def reformat_season(string) -> str:
    if string.startswith('9'):
        season = '19' + string[0:2]
    else:
        season = '20' + string[0:2]
    return season


def reformat_league(league, country_name) -> str:
    if country_name == 'France':
        if '1' in league:
            league = 'Ligue' + league[1]
        if '2' in league:
            league = 'Ligue' + league[1]
    return league


def download_csv_and_notes(country_name, link, path):
    csv_links = find_all_csv_links(link)
    note_link = find_note_link(link)

    for dl_url in csv_links:
        season, league = dl_url.split('/')[-2:]
        season = reformat_season(season)
        league = reformat_league(league, country_name)
        path_filename = os.path.join(path, f'{league}_{season}.csv')
        download = requests.get(dl_url)
        if download.status_code == 200:
            with open(path_filename, 'wb') as file:
                #for chunk in download:
                file.write(download.content)

    path_dl_note = os.path.join(path, 'note.txt')
    download_note = requests.get(note_link)
    if download_note.status_code == 200:
        with open(path_dl_note, 'wb') as file:
            for chunk in download_note:
                file.write(chunk)

@app.route('/datacouk/download_files')
def download_files():
    country_to_load = {
        'France': 'https://www.football-data.co.uk/francem.php'
        }
    for country_name, link in country_to_load.items():
        path = f'./code_prep/input/{country_name}'
        create_input_folder(country_name, path)
        download_csv_and_notes(country_name, link, path)

    response = make_response(json.dumps(
        {"result": "C'est OK"}))
    response.mimetype = 'application/json'
    return response


if __name__ == "__main__":
    country_to_load = {
        'France': 'https://www.football-data.co.uk/francem.php'
        }
    for country_name, link in country_to_load.items():
        path = f'./input/{country_name}'
        create_input_folder(country_name, path)
        download_csv_and_notes(country_name, link, path)
