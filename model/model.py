import pandas as pd
from fpgrowth_py import fpgrowth
import pickle as pickle
import os
import ssl

def rules_generator():
    dataset_url = os.environ["DATASET_URL"]
    df = pd.read_csv(dataset_url)

    item_set_list = df.groupby('pid')['track_name'].apply(list).tolist()

    min_support = 0.07
    min_confidence = 0.2

    freq_itemsets, rules = fpgrowth(item_set_list, minSupRatio=min_support, minConf=min_confidence)

    with open('rules.pkl', 'wb') as file:
        pickle.dump(rules, file)

if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    rules_generator()