import pandas as pd
import os


def concatenate_csv(path, nom_championnat):
    full_path = os.path.join(path, nom_championnat)
    all_files = os.listdir(full_path)
    all_df = []

    for f in all_files:
        df = pd.read_csv(os.path.join(full_path, f), sep=',')
        df = df.dropna(axis=0, how='any')
        df['file'] = f
        all_df.append(df)

    merged_df = pd.concat(all_df, ignore_index=True)
    merged_df.to_csv(os.path.join(path, '{}_complet.csv'.format(nom_championnat)), index=False)


path = 'ML/data/'
nom_championnat = 'France'
concatenate_csv(path, nom_championnat)
