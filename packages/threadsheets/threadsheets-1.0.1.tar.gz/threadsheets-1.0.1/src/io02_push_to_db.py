import pandas as pd
import numpy as np
from pymongo import MongoClient

def push_to_db(pl, combined_fpath):
    combined_fpath = pl.combined_pkl_fpath
    print(combined_fpath)
    # Load DB credentials
    with open(".mdbpass", "r", encoding="utf-8") as f:
        mdbpass = f.read()
    # Set up DB connection
    client = MongoClient(f"mongodb+srv://admin:{mdbpass}@cluster0-cg6nz.mongodb.net/test?retryWrites=true&w=majority")
    db = client.test
    # Load the combined data
    df = pd.read_pickle(combined_fpath)
    # Something like mongo.add(df.to_dict('records'))
    print(df.to_dict('records')[:20])