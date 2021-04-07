import pandas as pd


def load_gathered_file_to_df():
    path = './input/gathered_file.csv'
    df = pd.read_csv(path)
    return df


def select_features(df, features_to_keep):
    df = df[features_to_keep]
    return df


def return_bet_favorite(df):
    df = df.copy()
    df['bet_favorite'] = df[['B365H', 'B365D', 'B365A']].idxmin(axis=1)
    df['bet_favorite'] = df['bet_favorite'].replace('B365H', 'H').replace('B365D', 'D').replace('B365A', 'A')
    return df


def compare_bet_favorite_and_result(df):
    df = df.copy()
    df['compare'] = (df['bet_favorite'] == df['FTR'])
    return df


def apply_features(df):
    df = return_bet_favorite(df)
    df = compare_bet_favorite_and_result(df)
    return df


def save_to_file(df):
    df.to_csv('./output/with_selected_features.csv')


features = ['Div', 'HomeTeam', 'AwayTeam', 'FTR', 'B365H', 'B365D', 'B365A']
if __name__ == "__main__":
    input_df = load_gathered_file_to_df()
    df_selected_features = select_features(input_df, features)
    df_apply_features = apply_features(df_selected_features)
    print(df_apply_features)
    save_to_file(df_apply_features)
