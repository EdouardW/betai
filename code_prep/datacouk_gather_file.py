import os
import pandas as pd
import json
import csv

from flask import make_response, Response
from betai_flask import app
from pathlib import Path

from .utils import create_input_folder

def list_files_path(root_path):
    list_path = []
    for file in root_path.iterdir():
        if '.csv' in file.name:
            list_path.append(file)
    return list_path


def gather_unique_file(all_filles_path, gathered_path):
    list_to_concat= []
    list_error_reading_csv = []
    list_path = list_files_path(all_filles_path)
    #print('LIST PATH', type(list_path[0]))
    for file in list_path:
        try:
            print('En lecture', file.name)
            pd.read_csv(file)
            list_to_concat.append(file)
        except:
            list_error_reading_csv.append(file.name)

    output_file = pd.concat([pd.read_csv(file, index=False) for file in list_to_concat], axis = 0)
    output_file_name = Path(gathered_path, 'France.csv')
    output_file.to_csv(output_file_name)

    return list_to_concat, list_error_reading_csv


@app.route('/datacouk/gather_all_files')
def gather_files():
    all_filles_path: Path = Path('./input/datacouk/all_files/France/') 
    gathered_path: Path = Path('./input/datacouk/gathered/France/') 
    create_input_folder(gathered_path)
    list_to_concat, list_error_reading_csv = gather_unique_file(all_filles_path, gathered_path)
    response = make_response(json.dumps({"Nb de fichiers concatener": len(list_to_concat),
                                         f"{len(list_error_reading_csv)} Fichier(s) non charge(s)": list_error_reading_csv}))

    response.mimetype = 'application/json'
    return response


"""        {"Nb de fichiers concatener": len(list_to_concat),
        "Fichier(s) non charge(s)": list_error_reading_csv})) """