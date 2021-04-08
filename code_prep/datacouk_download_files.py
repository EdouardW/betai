import requests
import os
import json

from flask import make_response, Response
from lxml import html
from betai_flask import app
from pathlib import Path


def create_input_folder(path: Path) -> None:
    if path.is_dir() is False:
        path.mkdir(parents=True)


def find_all_href_links(url: str) -> list:
    response = requests.get(url)
    tree = html.fromstring(response.content)
    href_links = tree.xpath('//a/@href')

    return href_links


def list_all_files_to_download(url: str) -> list:
    all_href_links: list = find_all_href_links(url)

    list_file_to_dl: list = []
    for link in all_href_links:
        if '.csv' in link:
            list_file_to_dl.append(os.path.join('https://www.football-data.co.uk/', link))
        elif 'notes.txt' in link:
            list_file_to_dl.append(os.path.join('https://www.football-data.co.uk/', link))

    return list_file_to_dl


def reformat_season(season: str) -> str:
    if season.startswith('9'):
        season = '19' + season[0:2]
    else:
        season = '20' + season[0:2]
    return season


def reformat_league(league: str, country_name: str) -> str:
    if country_name == 'France':
        if '1' in league:
            league = 'Ligue' + league[1]
        if '2' in league:
            league = 'Ligue' + league[1]
    return league


def download_csv_and_notes(country_name: str, url: str, country_path: Path):
    list_files_to_dl: list = list_all_files_to_download(url)

    for dl_url in list_files_to_dl:
        if '.csv' in dl_url:
            season, league = dl_url.split('/')[-2:]
            season: str = reformat_season(season)
            league: str = reformat_league(league, country_name)
            path_filename: Path = Path(country_path, f'{league}_{season}.csv')
            download = requests.get(dl_url)
            if download.status_code == 200:
                with open(path_filename, 'wb') as file:
                    file.write(download.content)

        if 'notes.txt' in dl_url:
            path_note: Path = Path(country_path, 'note.txt')
            download_note = requests.get(dl_url)
            if download_note.status_code == 200:
                with open(path_note, 'wb') as file:
                    for chunk in download_note:
                        file.write(chunk)


@app.route('/datacouk/download_all_files')
def download_all_files():
    root_path: Path = Path('./input/datacouk/')
    
    country_to_load: dict = {
        'France': 'https://www.football-data.co.uk/francem.php'
        }

    for country_name, url in country_to_load.items():
        country_path: Path = Path(root_path / country_name)
        create_input_folder(country_path)
        download_csv_and_notes(country_name, url, country_path)

    response = make_response(json.dumps(
        {"result": "C'est OK"}))
    response.mimetype = 'application/json'
    return response
