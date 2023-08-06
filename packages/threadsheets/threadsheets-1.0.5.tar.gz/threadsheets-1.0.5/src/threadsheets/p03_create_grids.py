"""
Load the combined datapoints file and use it to construct a grid
for a given variable, where
[rows are countries/languages] x [columns are years]
"""
import os
import pandas as pd
import numpy as np

def get_estimate_list(estimate_df):
    """
    Produces estimate list, formatted for Google Sheet, from the provided df

    :param estimate_df:
    :return:
    """
    return [f"{rnum}: {rtuple[1]['value']} ({rtuple[1]['source_id']})" for rnum, rtuple in enumerate(estimate_df.iterrows())]

def compute_cell_value(pl, estimate_df):
    """
    Given a DF of all observations (estimates) for the cell, combine them
    in some way to generate a single value
    For now [the default] just average them all, dropping any N/As, but
    returning np.nan if this results in no entries
    Combine the rows in a df of estimates into one final estimate
    """
    # If we've gotten here, there are non-NA values, so return their mean
    # TODO: incorporate trust.csv (via trust_dict) here
    if len(estimate_df) == 0:
        # No estimates at all
        return np.nan, "0 estimates"
    # Otherwise, we know there's at least one value. Drop the NAs and return
    # the mean
    notnull_df = estimate_df.dropna(subset=["value"])
    if len(notnull_df) == 0:
        # Find out which rows got dropped
        dropped_df = estimate_df[estimate_df["value"].isnull()]
        num_null = len(dropped_df)
        estimate_str = "|".join(get_estimate_list(dropped_df))
        estimate_info = f"0 non-null estimates|---|{num_null} null estimates:|{estimate_str}"
        return np.nan, estimate_info
    # And if we're here, we know there's at least one non-null value
    entry_values = notnull_df["value"].values
    all_agree = all([x == entry_values[0] for x in entry_values])
    if all_agree and len(entry_values) > 1:
        conflict_text = " consistent"
    elif not all_agree and len(entry_values) > 1:
        conflict_text = " conflicting"
    else:
        # Only one entry, so can't have conflicts
        conflict_text = ""
    #print(entry_values)
    final_estimate = entry_values.mean()
    # And now we need to go round the mean if it's an int var
    var_spec = pl.get_varspec(str(estimate_df["variable"].iloc[0]))
    if var_spec.get_datatype() == "int":
        final_estimate = round(final_estimate)
    num_estimates = len(entry_values)
    estimate_lines = get_estimate_list(notnull_df)
    estimate_str = "|".join(estimate_lines)
    estimate_info = f"{num_estimates}{conflict_text} estimates:|{estimate_str}"
    return final_estimate, estimate_info

def create_row(pl, unit_df, years):
    # Create one entry for each year, by aggregating the rows of unit_df in
    # some way determined by compute_cell_value()
    num_vals = []
    info_vals = []
    for cur_year in years:
        # Get the entries for this year
        year_df = unit_df[unit_df["year"] == cur_year]
        cell_val, num_entries = compute_cell_value(pl, year_df)
        num_vals.append(cell_val)
        info_vals.append(num_entries)
    return num_vals, info_vals

def get_trust(source_name, variable):
    pass

trust_dict = {}
def init_trust_dict(trust_df):
    """
    Basically we're just converting the df with columns [source,variable,score]
    into a lookup table {source->{variable->score}}
    """
    # Lol there's literally no smart (non-loop) way to do this... see Scratchpad
    for row_index, row in trust_df.iterrows():
        cur_source = row["source"]
        cur_variable = row["variable"]
        trust_tuple = (cur_source, cur_variable)
        trust_dict[trust_tuple] = row["score"]
        
def print_summary(var_name, val_list, print_all=False):
    """
    Prints just the first two and last two entries, with "..." in between, unless
    print_all is set to True
    """
    print(f"Values for grid axis [{var_name}]:")
    if print_all:
        print(val_list)
        return
    if len(val_list) <= 4:
        print(val_list)
    else:
        print(f"[{val_list[0]}, {val_list[1]},..., {val_list[-2]}, {val_list[-1]}]")

def create_grid(pl, variable, unit_of_obs, years=None, exclude_list=[]):
    if years is None:
        # Don't filter the years at all
        in_year_range = lambda x: True
    else:
        # Sort the years, just in case
        years_sorted = sorted(years)
        in_year_range = lambda x: x in years_sorted
    print(f"=====[ creating grid for [{variable}] x [{unit_of_obs}], years {years_sorted[0]}-{years_sorted[-1]} ]=====")
    entry_df = pd.read_pickle(pl.combined_pkl_fpath)
    # And the source-trustworthiness file
    trust_fpath = os.path.join(pl.input_path, "trust.csv")
    trust_df = pd.read_csv(trust_fpath)
    init_trust_dict(trust_df)
    # Get all the entries for the var we care about
    entry_df = entry_df[entry_df["variable"] == variable].copy()
    # Get the unique years
    #print("Unique years:")
    #print(entry_df["year"].unique())
    all_years = sorted([int(year) for year in entry_df["year"].unique() if in_year_range(int(year))])
    # Print a summary of the years spanned
    print_summary("year", all_years)
    # And langs/countries
    all_units = sorted(entry_df[unit_of_obs].unique())
    # But remove any in exclude_list
    all_units = [u for u in all_units if u not in exclude_list]
    print_summary(unit_of_obs, all_units)
    # Now we can create the grid
    num_df = pd.DataFrame(index=all_units, columns=all_years)
    num_df.index.name = unit_of_obs
    info_df = pd.DataFrame(index=all_units, columns=all_years)
    info_df.index.name = unit_of_obs
    for cur_unit in all_units:
        #print(f"cur_unit={cur_unit}")
        # Get the entries for this unit
        unit_df = entry_df[entry_df[unit_of_obs] == cur_unit].copy()
        num_row, info_row = create_row(pl, unit_df, all_years)
        num_df.at[cur_unit] = num_row
        info_df.at[cur_unit] = info_row
    #print(grid_df)
    # Make sure the columns are "officially" numeric before saving
    num_df = num_df.apply(pd.to_numeric)
    num_fname_prefix = f"{variable}_grid"
    num_pkl_fpath = os.path.join(pl.grid_output_path, f"{num_fname_prefix}.pkl")
    pl.save_df(num_df, num_pkl_fpath, include_index=True)
    info_fname_prefix = f"{variable}_info"
    info_pkl_fpath = os.path.join(pl.grid_output_path, f"{info_fname_prefix}.pkl")
    pl.save_df(info_df, info_pkl_fpath, include_index=True)
    
def run(pl, grid_spec_list):
    # This is basically just a wrapper around create_grid, so that we can
    # generate arbitrarily-many grids
    for grid_spec in grid_spec_list:
        # Parse the grid info dict before calling create_grid
        grid_var = grid_spec['variable']
        grid_unit = grid_spec['unit_of_obs']
        grid_years = grid_spec['years'] if 'years' in grid_spec else None
        grid_exclude = grid_spec['exclude_units'] if 'exclude_units' in grid_spec else []
        create_grid(pl, grid_var, grid_unit, grid_years, grid_exclude)