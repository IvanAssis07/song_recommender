import pandas as pd
from fpgrowth_py import fpgrowth
import pickle as pickle
import os
import ssl
import time
from datetime import datetime

def rules_generator():
    dataset_url = os.environ["DATASET_URL"]
    df = pd.read_csv(dataset_url)

    item_set_list = df.groupby('pid')['track_name'].apply(list).tolist()

    min_support = 0.06
    min_confidence = 0.08

    freq_itemsets, rules = fpgrowth(item_set_list, minSupRatio=min_support, minConf=min_confidence)

    metadata = {
        "rules": rules,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open('shared/rules.pkl', 'wb') as file:
        pickle.dump(metadata, file)

    while True:
        time.sleep(10)
        print("Model still running")

if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    rules_generator()