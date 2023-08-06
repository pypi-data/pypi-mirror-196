import os
import pandas as pd
import numpy as np

def run(pl):
    # Output: a giant csv file with a row for *every* piece of data we have
    parsed_fpaths = pl.parsed_pkl_fpaths
    all_dfs = []
    for cur_fpath in parsed_fpaths:
        cur_df = pd.read_pickle(cur_fpath)
        all_dfs.append(cur_df)
    # ignore_index here tells it to re-make the index for the combined df (so
    # that combined entries are numbered 1,2,3,...)
    full_df = pd.concat(all_dfs, ignore_index=True)
    csv_output_fpath = os.path.join(pl.combined_output_path, "combined.csv")
    full_df.to_csv(csv_output_fpath, index=False)
    pkl_output_fpath = csv_output_fpath.replace(".csv",".pkl")
    full_df.to_pickle(pkl_output_fpath)
    pl.combined_pkl_fpath = pkl_output_fpath