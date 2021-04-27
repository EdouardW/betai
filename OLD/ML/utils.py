#!/usr/bin/python

import pandas as pd

from sklearn import preprocessing


def load_dataframe(file_path):
    df_input = pd.read_csv(file_path, sep=';')
    return df_input


def delete_first_day(dataframe):
    df = dataframe[dataframe['cl_hometeam'] != -1]
    return df.reset_index()


def select_features(dataframe, features):
    df = dataframe[features]
    return df


def handle_categorical(dataframe, categorical_features):
    le = preprocessing.LabelEncoder()
    le.fit(["H", "D", "A"])
    for feature in categorical_features:
        dataframe[feature] = le.fit_transform(dataframe[feature])

    return dataframe
