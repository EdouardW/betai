import tensorflow as tf
import pandas as pd
import numpy as np
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing


odd_train = pd.read_csv(
    "ML/data/odd.csv", sep=';',
    names=["result", "odds-home", "odds-draw", "odds-away"],
    skiprows=1)

odd_train['odds-home'] = pd.to_numeric(odd_train['odds-home'], errors='coerce')
odd_train['odds-draw'] = pd.to_numeric(odd_train['odds-draw'], errors='coerce')
odd_train['odds-away'] = pd.to_numeric(odd_train['odds-away'], errors='coerce')


##print(odd_train.dtypes)

odd_features = odd_train.copy()
odd_labels = odd_features.pop('result')

odd_features = np.array(odd_features)

print(odd_features)
odd_model = tf.keras.Sequential([
                                    layers.Dense(64),
                                    layers.Dense(1)
                                    ])

odd_model.compile(loss=tf.losses.MeanSquaredError(),
                  optimizer=tf.optimizers.Adam())

odd_model.fit(odd_features, odd_labels, epochs=100)


#print(odd_train.head())


#COLUMN_NAMES = ['odds-home', 'odds-draw', 'odds-away']
#LABEL = ['H', 'D', 'A']