from utils import load_dataframe, select_features, delete_first_day, handle_categorical
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

df = load_dataframe('betai/ML/input/FRANCE_ligue1.csv')
df = delete_first_day(df)

categorical_features = ['FTR', 'HTR']
df = handle_categorical(df, categorical_features)

df = df.dropna()

features_to_keep = ['journee','cl_hometeam','cl_awayteam', 'points_h', 'gagnes_h', 'nuls_h',\
    'perdus_h', 'buts_h', 'contre_h', 'points_a', 'gagnes_a', 'nuls_a', 'perdus_a', \
        'buts_a', 'contre_a', 'forme_h_win', 'forme_h_draw', 'forme_h_lose', \
            'forme_a_win', 'forme_a_draw', 'forme_a_lose', 'FTHG', 'FTAG', 'FTR', \
                'HTHG', 'HTAG', 'HTR', 'HST', 'AST', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', \
                    'B365H', 'B365D', 'B365A']
#df = select_features(df, features_to_keep)


x = df[['journee','cl_hometeam','cl_awayteam', 'points_h', 'gagnes_h', 'nuls_h',\
    'perdus_h', 'buts_h', 'contre_h', 'points_a', 'gagnes_a', 'nuls_a', 'perdus_a', \
        'buts_a', 'contre_a', 'forme_h_win', 'forme_h_draw', 'forme_h_lose', \
            'forme_a_win', 'forme_a_draw', 'forme_a_lose', 'B365H', 'B365D', 'B365A']]
y = df['FTR']


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
model_SVC = SVC( kernel = 'linear', gamma = 'scale', shrinking = False,)

model_SVC.fit(x_train, y_train)

precision = model_SVC.score(x_test, y_test)
print(precision*100)

#'https://www.cours-gratuit.com/tutoriel-python/tutoriel-python-matriser-la-rgression-logistique-avec-scikit-learn'