import re

import pandas as pd
import numpy as np

def add_df_col(df, colname, colvals):
    # This needs to be backwards compatible with a non-MultiIndex df, so check
    # that here
    num_hrows = len(df.columns.names)
    if num_hrows == 1:
        # non-MultiIndex, so just add the column like normal
        df[colname] = colvals
        return df
    # Otherwise, we have a MultiIndex. Need to make a tuple with only the last
    # element not blank
    #print(df.columns.names)
    # The protocol: for singleton cols, the headers will all be empty strings
    # except for the last one (the bottom-most one)
    rn_tuple_list = ["" for i in range(num_hrows)]
    rn_tuple_list[-1] = colname
    rn_tuple = tuple(rn_tuple_list)
    df[rn_tuple] = colvals
    return df

special_name_map = {"usa":"USA","ussr":"USSR","uk":"UK",
                    "democratic republic of the congo":"Democratic Republic of the Congo",
                    "republic of the congo":"Republic of the Congo",
                    "trinidad and tobago":"Trinidad and Tobago",
                    "st. kitts and nevis":"St. Kitts and Nevis",
                    "st. vincent and the grenadines":"St. Vincent and the Grenadines",
                    "sao tome and principe":"Sao Tome and Principe"}
def clean_index_val(index_val):
    """
    Cleans the index value: strips whitespace and capitalizes first letter of each
    word, with exceptions for things like "USA", "USSR", "UK"
    """
    new_val = index_val.strip().lower()
    if new_val in special_name_map:
        # Return the mapped value
        return special_name_map[new_val]
    else:
        # Capitalize the first letter of each word before returning
        return new_val.title()

exp_map = {"":0,"tens":1,"hundreds":2,"thousands":3,"millions":6,"billions":9}
def unit_map(x): return (10 ** exp_map[x]) if x in exp_map else x
def correct_unit(val, cur_unit, desired_unit):
    cur_unum = unit_map(cur_unit)
    desired_unum = unit_map(desired_unit)
    conversion_factor = cur_unum / desired_unum
    if conversion_factor != 1:
        converted_val = val * conversion_factor
        #print(f"Conversion: [{val}] -> [{converted_val}]")
        return converted_val, desired_unit
    # Otherwise, it was already the correct unit
    return val, desired_unit

def get_df_col(df, colname):
    # A 1-liner since we have get_df_indexer()
    # ...except we need to check for None
    df_indexer = get_df_indexer(df, colname)
    if df_indexer in df.columns:
        return df[df_indexer]
    else:
        return None

def get_df_indexer(df, colname):
    num_hrows = len(df.columns.names)
    # If num_hrows is 1, then the indexer is just colname itself, so we just
    # return it so the function is "backwards compatible" with non-MultiIndex df
    if num_hrows == 1:
        return colname
    # Otherwise we need to use _get_mi_indexer()
    return get_mi_tuple(num_hrows, colname)

def get_header_row(df, hrow_num):
    return df.columns[hrow_num]

def get_indexer_string(indexer):
    """
    The inverse of get_df_indexer(), it returns the *string* at the end of the
    (arbitrarily-long) indexer
    """
    if type(indexer) == str:
        return indexer
    return indexer[-1]

def get_mi_tuple(num_hrows, colname):
    # A helper function *only* for MultiIndex dfs that constructs a tuple where all entries
    # are blank except the last one which == colname
    indexer_list = ["" for _ in range(num_hrows)]
    # Replace the final element with colname
    indexer_list[-1] = colname
    # And return it in tuple form
    return tuple(indexer_list)

def get_row_cell(row, colname):
    #print(f"get_row_cell(): Getting cell {colname} for row {row.name}")
    # For use inside for loops -- uses the indexer stuff to (try and) get a
    # cell out of the row. The only reason it needs to be a different function
    # is because for rows the MultiIndex headers are stored in .index instead
    # of .columns like in the full-df case
    row_indexer = get_row_indexer(row, colname)
    #print(f"row_indexer={row_indexer}")
    # But this cell might not exist (for example, when we're checking for a
    # "notes" column), so need to check that
    if row_indexer in row.index:
        return row[row_indexer]
    else:
        return None

def get_row_indexer(row, colname):
    num_hrows = len(row.index.names)
    if num_hrows == 1:
        return colname
    # And here we can just re-use our _get_mi_tuple() function
    return get_mi_tuple(num_hrows, colname)

year_reg = re.compile(r'[0-9]{4}')
def header_row_to_numeric(header_row):
    """
    This needs to be its own function, since just using .astype(int) will lead
    to an error when there's a "notes" column :/
    """
    hr_name = header_row.name
    hr_list = list(header_row)
    #print(f"header_row_to_numeric(): {hr_list}")
    new_hr_list = pd.Index([int(e) if year_reg.match(e) else e for e in hr_list], name=hr_name)
    #print(pd.Index(new_hr_list,name=hr_name))
    return new_hr_list

def set_header_row(df, level_num, new_values):
    df.columns = df.columns.set_levels(new_values, level_num)

def print_warning(warning_msg):
    print(f"<!>***** {warning_msg} *****<!>")
    
def remove_all_whitespace(val):
    if type(val) != str:
        return val
    old_val = val
    new_val = "".join(val.split())
    #if old_val != new_val:
    #    print(f"remove_all_whitespace(): [{old_val}] -> [{new_val}]")
    return new_val

# How to check if string is an int or float (or neither)
# https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except
def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def strip_unnamed(col_tuple):
    return tuple(i if "Unnamed" not in i else "" for i in col_tuple)

def update_df_index(df, new_index_vals):
    """
    Lol I hate Pandas sometimes... Need this function because if you just update
    the index like df.index = [...] you lose the index name
    """
    index_name = df.index.name
    df.index = new_index_vals
    df.index.name = index_name