import pandas as pd
from fpgrowth_py import fpgrowth
import pickle as pickle

df = pd.read_csv('datasets/2023_spotify_ds1.csv')

item_set_list = df.groupby('pid')['track_name'].apply(list).tolist()

min_support = 0.08
min_confidence = 0.2

freq_itemsets, rules = fpgrowth(item_set_list, minSupRatio=min_support, minConf=min_confidence)

with open('rules.pkl', 'wb') as file:
    pickle.dump(rules, file)