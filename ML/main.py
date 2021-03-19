from utils import load_dataframe, select_features, delete_first_day, handle_categorical
import seaborn as sns

df = load_dataframe('betai/ML/input/FRANCE_ligue1.csv')
df = delete_first_day(df)

categorical_features = ['FTR', 'HTR']
df = handle_categorical(df, categorical_features)


features_to_keep = ['journee','cl_hometeam','cl_awayteam', 'points_h', 'gagnes_h', 'nuls_h',\
    'perdus_h', 'buts_h', 'contre_h', 'points_a', 'gagnes_a', 'nuls_a', 'perdus_a', \
        'buts_a', 'contre_a', 'forme_h_win', 'forme_h_draw', 'forme_h_lose', \
            'forme_a_win', 'forme_a_draw', 'forme_a_lose', 'FTHG', 'FTAG', 'FTR', \
                'HTHG', 'HTAG', 'HTR', 'HST', 'AST', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', \
                    'B365H', 'B365D', 'B365A']
#df = select_features(df, features_to_keep)

print(sns.countplot(x='FTR', data=df))

result = 'FTR'
#print(len(df))
