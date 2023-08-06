import glob
import io
import os
import re
from pathlib import Path

import pandas as pd
import numpy as np

import pipeline_util as plu


def apply_index_rules(df, unit_of_obs, index_rules):
    """
    Basically I don't know a better way than just looping through the rules and
    if they match one of the df indices, apply it
    """
    # print(f"apply_index_rules(): {df[unit_of_obs]}")
    # print(f"Before index rules: index col={df[unit_of_obs].values}")
    # print(all_rules)
    # Get the index rules for *this* unit_of_obs
    unit_rules = index_rules[unit_of_obs]
    # Rename rules are easy: just use pandas' rename rule
    rename_rules = [r for r in unit_rules if r.is_rename()]
    rename_dict = {r.unit1: r.unit2 for r in rename_rules}
    df[unit_of_obs] = df[unit_of_obs].apply(lambda x: rename_dict[x] if x in rename_dict else x)
    # Addto rules are a bit harder, need to loop
    addto_rules = [r for r in unit_rules if r.is_addto()]
    addto_dict = {r.unit1: r.unit2 for r in addto_rules}
    df[unit_of_obs] = df[unit_of_obs].apply(lambda x: addto_dict[x] if x in addto_dict else x)
    group_list = [c for c in df.columns if c not in [unit_of_obs, "value"]] + [unit_of_obs]
    new_df = df.groupby(group_list).sum().reset_index()
    return new_df
    # print(f"After index rules: index col={df[unit_of_obs].values}")

def detect_header_rows(csv_fpath, verbose=False):
    """
    Called by process_file() before actually loading the file for parsing, to get
    a list of the header rows. tl;dr the last row with a "\" in the first column
    is the last header row, so that the first row without a "\" in the first column is the start of the data.
    These aren't large files so it's not that bad efficiency-wise to just load twice.
    """
    vprint = print if verbose else lambda x: None
    # Very first step (Step 0): make sure no UnicodeDecodeErrors
    try:
        file_obj = open(csv_fpath, "rb")
        file_bytes = file_obj.read()
        file_text = file_bytes.decode('utf-8')
    except UnicodeDecodeError as e:
        print(file_bytes[:e.start])
    finally:
        file_obj.close()
    # Cool. If we've gotten this far, no UnicodeDecodeErrors.
    # So now we find the header/data split. Long story short the final
    # header row is the last one with a "\"
    temp_df = pd.read_csv(io.StringIO(file_text), header=None)
    #print(f"temp_df first column:\n{temp_df.iloc[:,0]}")
    first_col = temp_df.iloc[:,0]
    #vprint(f"[detect_header_rows()] first_col: {first_col}")
    fc_contains = first_col.str.contains("\\\\")
    # idxmin() gives us the *first* index for which there is *not* a "\"
    data_start = fc_contains.idxmin()
    #vprint(f"[detect_header_rows()] data_start: {data_start}")
    del temp_df
    header_rows = list(range(data_start))
    return header_rows


def extract_cell_entry(pl, item_index, item, header_row_names, row_info):
    # The cell "inherits" the data from the row (which in turn "inherited"
    # the data from the sheet
    cell_dict = row_info.copy()
    # print(val.name)
    # print(item_index)
    # Just create key:value pairs for each header row
    col_info = {header_row_names[i]: item_index[i] for i in range(len(header_row_names))}
    # But if we don't have the unit explicitly given, we assume it's ""
    # (blank string unit = "ones" for numeric vals, or just gets ignored
    # for non-numeric vals)
    if "unit" not in col_info:
        col_info["unit"] = ""
    cell_dict.update(col_info)
    # print(col_info)
    # print(item)
    # And finally, the "value" entry is reserved for the numeric value
    # that this cell contains (basically the only thing in all of this
    # that's not "metadata" in a sense)
    # col_info, from the {hnames[i]: item_index[i]} line above, should
    # now have the variable name for us to look up its spec
    # print(f"Parsing cell: {col_info}")
    var_name = col_info["variable"]
    # Now, if the variable is one we care about (aka is in the var spec)
    # then parse it according to the spec. Otherwise we just store it as
    # a string (in case we want to look at it later on, at which point
    # we can add it to the spec)
    cur_var_spec = pl.get_var_spec(var_name)
    # print(f"var_spec for {var_name}: {cur_var_spec}")
    cur_var_unit = col_info["unit"]
    success, parsed_val, new_unit = parse_value(item, cur_var_unit, cur_var_spec)
    if success:
        cell_dict["value"] = parsed_val
        # And we also need to update the unit
        col_info["unit"] = new_unit
    else:
        if "country" in row_info:
            unit_name = row_info["country"]
        else:
            unit_name = row_info["language"]
        raise Exception(
            f"Error in row #{row_info['row_num']} ({unit_name}), column {col_info}, value '{item}': {parsed_val}")
    return cell_dict


def extract_entries(pl, df):
    """
    TODO: Need to do something with the column metadata (return it with the entries df somehow...)
    """
    all_entries = []
    # print(df.columns)
    hnames = df.columns.names
    source_id_col = plu.get_df_col(df, "source_id")
    # This will store any metadata found in the columns (right now just "Notes")
    column_metadata = {}
    # Just grab the first value, they should all be the same
    source_id = str(source_id_col.iloc[0])
    # This ensures that source_id and the name of the index (country or language)
    # will be included in the info for each row
    sheet_info = {"source_id": source_id, "index_name": df.index.name}
    # print(sheet_info)
    # Loop over rows
    for row_index, row in df.iterrows():
        # First off, if this is a notes row, we just need to move the values
        # into the column metadata (we need the str check because the name could
        # be like 1976)
        if (type(row.name) == str) and (row.name.lower() == "notes"):
            for item_index, item in row.iteritems():
                column_metadata[item_index] = item
            continue
        row_data = extract_row_entries(pl, row_index, row, sheet_info, hnames)
        all_entries.extend(row_data)
    return all_entries

def extract_row_entries(pl, row_index, row, sheet_info, header_row_names):
    # print(f"Parsing row {row.name}: {row}")
    # print(f"row.index={row.index}")
    # Make a copy of the sheet info to initialize the row info dict
    row_info = sheet_info.copy()
    # This looks kinda weird but it's just saying take the name
    # of the index col (e.g., "country") and map it to the actual index
    # *value* for this row (e.g., "Vietnam")
    index_col_name = row_info["index_name"]
    row_info[index_col_name] = row.name
    # Extract row notes if they exist
    row_notes = ""
    notes_cell = plu.get_row_cell(row, "notes")
    # print(f"notes_cell={notes_cell}")
    if notes_cell is not None:
        row_notes = str(notes_cell)
    # But make it a blank string if it came out "nan" or "NaN"
    if (row_notes == "nan" or row_notes == "NaN"):
        row_notes = ""
    row_info["row_notes"] = row_notes
    # And the row number
    rownum_cell = plu.get_row_cell(row, "row_num")
    # This one we need to have (so we can locate the record in the original
    # csv if need be)
    if rownum_cell is None:
        raise Exception("Error: Couldn't find row number for record")
    row_num = int(rownum_cell)
    row_info["row_num"] = row_num
    # And finally, solely as a sanity check, we make sure this row's source_id
    # matches the full sheet's source_id (which we extracted from the first
    # row of the sheet above, before the for loop)
    source_id_cell = plu.get_row_cell(row, "source_id")
    if source_id_cell is None:
        raise Exception(f"Error: Couldn't find source_id for row {row.name}")
    source_id = str(source_id_cell)
    if source_id != sheet_info["source_id"]:
        raise Exception(f"Error: Source id of sheet does not match source id of row {row.name}")
    # print(row_info)
    # Loop over entries in current row
    row_entries = []
    for item_index, item in row.iteritems():
        if (notes_cell is not None) and (item_index == plu.get_row_indexer(row, "notes")):
            continue
        if item_index == plu.get_row_indexer(row, "row_num"):
            continue
        source_id_indexer = plu.get_row_indexer(row, "source_id")
        if item_index == source_id_indexer:
            continue
        cell_dict = extract_cell_entry(pl, item_index, item, header_row_names, row_info)
        # And now we add this cell's dict (with all the sheet+row data it
        # inherited) to all_entries
        row_entries.append(cell_dict)
    return row_entries

def parse_float(val, cur_unit, var_spec):
    desired_unit = var_spec.unit
    # Remove commas like for int, unless rewrite rules already made it non-str
    val = val.replace(",", "")
    # Also, if the field is empty or "N/A", just return np.nan
    if val == "" or val == "N/A":
        return np.nan, desired_unit
    # This gives us an exception if val can't be parsed as float, which we want
    val_float = float(val)
    # But need to check for NaN
    if np.isnan(val_float):
        # NaN values are "auto-converted", in a sense
        return val_float, desired_unit
    # And now that we know we have a non-null numeric value, we can perform the
    # unit conversion
    val_converted, new_unit = plu.correct_unit(val_float, cur_unit, desired_unit)
    # Now we check precision (if it's set) and round
    var_precision = var_spec.get_precision()
    rounded_val = round(val_converted, var_precision)
    # Now, we check if rounding modified the val and warn/error as needed
    # Update: np.isclose(np.nan, np.nan) returns False -____-
    no_rounding = np.isclose(val_converted, rounded_val) or np.isnan(val_converted)
    # If it didn't actually round it anyways, then we can just return
    if no_rounding:
        return (rounded_val, new_unit)
    # Otherwise, we need to check the rounding spec
    rounding_spec = var_spec["rounding"]
    if rounding_spec == "no":
        raise Exception(
            f"Spec does not allow rounding for variable {var_name}, but encountered {val_float} when precision is {precision}")
    if rounding_spec == "warn":
        print_warning(
            f"ROUNDING FLOAT VALUE {val_float} TO LESS PRECISION ({precision}) FOR VARIABLE {var_name}: old={val_float} new={rounded_val}")
    # And now we can return the rounded val
    return (rounded_val, new_unit)
    
def parse_int(val, cur_unit, var_spec):
    # First we remove commas if that setting is True, unless the replace
    # rules already made it numeric (hence the type() check)
    orig_val = val
    desired_unit = var_spec.unit
    # Remove commas from the number (so it can be parsed easily as an int/float)
    val = val.replace(",","")
    # Check if it can be directly parsed as an int
    if plu.represents_int(val):
        # We still need to be careful about returning the value, since we need
        # to make sure the units are correct
        val_int = int(val)
        val_converted, new_unit = plu.correct_unit(val_int, cur_unit, desired_unit)
        return val_converted, new_unit
    # But it could *still* be an int, just in float form like 7.0 or a blank cell
    # representing missing data
    # So first check if blank
    if val == "" or val == "N/A":
        # Remember that pd.NA is how we represent missing int vals (since Pandas
        # allows missing ints as None in int lists)
        return (pd.NA, desired_unit)
    # So check if it can at least be parsed as a float
    try:
        val_float = float(val)
    except ValueError:
        # This just lets me print a little more info on the value that caused the error
        raise Exception(f"Value \"{val}\" (original=\"{orig_val}\") cannot be parsed as numeric")
    # And see if that conversion gave us a NaN (*different* from a ValueError...)
    if np.isnan(val_float):
        return (val_float, desired_unit)
    # If we've gotten here, we have a non-null numeric val, so we can do the var conversion
    val_float_converted, new_unit = plu.correct_unit(val_float, cur_unit, desired_unit)
    # And see if it needs to be rounded (floats have a built-in is_integer() fn)
    if val_float_converted.is_integer():
        # No rounding necessary
        val_int = int(val_float_converted)
        return (val_int, new_unit)
    # Otherwise, we need to round, so make sure the spec allows rounding
    rounded_val = round(val_float_converted)
    if var_spec["rounding"] == "no":
        raise Exception(f"Non-integer value ({val_float_converted}) found for integer variable {var_name}")
    if var_spec["rounding"] == "warn":
        var_name = var_spec["name"]
        print_warning(f"ROUNDING FLOAT VALUE ({val_float_converted}) TO INT FOR VARIABLE {var_name}: old={val_float_converted} {cur_unit} new={rounded_val} {desired_unit}")
    return (rounded_val, new_unit)


def parse_row_value(row, data_spec, verbose=False):
    """
    Sort of a wrapper around parse_value(), which takes in a whole row of a DF
    and then calls parse_value() with the appropriate arguments extracted from
    the row
    """
    vprint = print if verbose else lambda x: None
    row_unit = row["unit"] if "unit" in row.index else ""
    row_var = row['variable'] if 'variable' in row.index else ''
    row_spec = data_spec.get_varspec(row_var) if (row_var != '') else data_spec.get_default_varspec()
    #vprint("row_spec: " + str(row_spec))
    new_val, new_unit = parse_value(row["value"], row_unit, row_spec, verbose=verbose)
    return pd.Series([new_val, new_unit])


def parse_value(val, cur_units, var_spec, verbose=False):
    # Use the variable's specification (loaded from the .conf file when the
    # pipeline launches) to correctly parse the numeric value. It returns a
    # tuple: (success, parsed_value [if success==True]/error_message [if success==False])
    # And also we now remove any whitespace
    vprint = print if verbose else lambda x: None
    val = plu.remove_all_whitespace(val)
    #vprint("var_spec: " + str(var_spec))
    var_datatype = var_spec.get_datatype()
    if var_datatype == "int":
        return parse_int(val, cur_units, var_spec)
    else:  # var_type == "float":
        return parse_float(val, cur_units, var_spec)


def print_warning(msg):
    print("=====[ WARNING ]=====")
    print(msg)

def process_data_file(pl, fpath, verbose=False, debug=True):
    vprint = print if verbose else lambda x: None
    vprint(fpath)
    fname = os.path.basename(fpath)
    fname_elts = os.path.splitext(fname)
    if fname_elts[0].endswith("_entries"):
        vprint(f"process_data_file(): processing already-long dataset {fname}")
        return process_entries_file(fpath, pl.get_index_rules(), verbose=verbose)
    ### Part 1: Detect the headers/data split
    hrows = detect_header_rows(fpath, verbose=verbose)
    num_hrows = len(hrows)
    print(f"process_data_file(): Parsing {fname} with {num_hrows} header rows")
    ### Part 2: Load csv
    # Need the keep_default_na=False option otherwise it stores missing vals as
    # np.nan even with dtype=str -___-
    df = pd.read_csv(fpath, index_col=[0], header=hrows, dtype=str, keep_default_na=False)
    ### Parts 3a/3b: Parse index column (3a)/Parse header rows (3b)
    # Annoying: df.columns.names if multiindex, df.columns.name if single index
    if len(df.columns.names) > 1:
        # Multiple header rows. Pandas will load this as where the first column
        # of the header rows (what we want to be split) will be treated as a list
        # of *column* names
        last_colname = df.columns.names[-1]
        index_name = last_colname.split("\\")[0]
        df.index.name = index_name
        # And now we can remove the index-name part of the column headers
        df.columns.names = [cname.split("\\")[-1] for cname in df.columns.names]
        # Uses strip_unnamed() to ensure blank header vals stay blank (necessary
        # because the headers need to be variable names or years, so "Unnamed: 1"
        # won't work [b/c of the space and the ":" character...])
        df.columns = pd.MultiIndex.from_tuples([plu.strip_unnamed(t) for t in df.columns], names=df.columns.names)
    else:
        # Single header row. In this case, Pandas will treat the upper-right
        # cell as the name of the *index* (and not the name of the column
        # headers, like in the previous case). So instead here we need to give
        # the column headers row a name based on the part of the index name
        # after "\"
        index_name_elts = df.index.name.split("\\")
        real_index_name = index_name_elts[0]
        col_header_row_name = index_name_elts[1]
        df.columns.name = col_header_row_name
        # And now we can remove everything from "\" onwards in the index name
        df.index.name = real_index_name
    ### Part 4: Lowercase any strings in the index and remove "notes" row if it exists
    df.index = pd.Series([plu.clean_index_val(s) if type(s) == str else s for s in df.index], name=df.index.name)
    # errors='ignore' needed since all three most likely will not be in index col
    df.drop(index=["notes","Notes","NOTES"], inplace=True, errors='ignore')
    ### Part 4: Doing magic with the unstack() function
    entry_series = df.unstack()
    entry_series.name = "value"
    df = pd.DataFrame(entry_series).reset_index()
    ### Part 5: Make sure the year column is all-numeric and apply the index
    ### rules to the other axis
    # There could be a "notes" row, so we convert all entries that can be parsed
    # as a year to int (rather than .astype(int) which leads to an exception if
    # there's a "notes" row)
    #df["year"] = df["year"].apply(lambda x: int(x) if (type(x) == int or plu.year_reg.match(x)) else x)
    # Except now we drop any "notes" rows
    df = df[df["year"].apply(str) != "notes"]
    # Now that we're dropping the notes, we can use the much simpler .astype() approach
    #breakpoint()
    df["year"] = df["year"].astype(int)
    unit_of_obs = next(c for c in df.columns if c not in ["unit","variable","year"])
    print(f"unit_of_obs={unit_of_obs}")
    # First we check whether or not this unit_of_obs is part of our study
    if unit_of_obs not in pl.data_spec.get_index_rules():
        # If not, we just jump to the next one
        return None
    # And now we apply the index rules to the unit_of_obs column
    apply_index_rules(df, unit_of_obs, pl.data_spec.get_index_rules())
    # And also that the unit is capitalized (each word) and trimmed of whitespace
    df[unit_of_obs] = df[unit_of_obs].apply(plu.clean_index_val)
    ### Part 6: Add row_num and source_id columns
    # We need to use this special add_df_col() helper function because sometimes
    # the DFs have a single row of col headers but sometimes MultiIndex columns
    df = plu.add_df_col(df, "row_num", np.arange(len(df)))
    # And a column with just the source_id
    df = plu.add_df_col(df, "source_id", fname)
    ### Part 7: Run the parser (turning the strings into ints/floats as desired)
    ### on the value column
    # parse_row_val needs to have the pipeline object, so this partial function
    # lets us pass that while still using it in an apply() call
    df.to_pickle("df_before_parse.pkl")
    if debug:
        # Use a for loop
        results = []
        for row_index, row in df.iterrows():
            row_parsed = parse_row_value(row, pl.data_spec, verbose=verbose)
            results.append(row_parsed)
        df[['value','unit']] = results
    else:
        # Lambda function
        parse_row_partial = lambda x: parse_row_value(x, pl.data_spec)
        df[["value", "unit"]] = df.apply(parse_row_partial, axis=1)
    ### Part 5: Extract entries (i.e., turn into a long-format dataset essentially)
    # Print statements for debugging
    #print(f"process_file(): About to call extract_entries():\n***\ndf.index.name={df.index.name}\n***\ndf.index={df.index}\n***\ndf.columns={df.columns}")
    #df.to_pickle("last_df.pkl")
    # We also need to give it the pipeline (for getting the data specs)
    #all_entries = extract_entries(pl, df)
    ### Part 6: Take this entries list and make it into its own df
    #long_df = pd.DataFrame(all_entries)
    #breakpoint()
    return df

def process_entries_file(fpath, index_rules, verbose=False):
    """
    Process a file already in long format (1 row per country x year). For these,
    we assume that the headers are [unit,year,(1 or more var cols),(0 or 1 notes col)]
    """
    #breakpoint()
    fname = os.path.basename(fpath)
    df = pd.read_csv(fpath, index_col=[0], header=[0])
    unit_of_obs = df.index.name.lower()
    # So now that we got the name we don't need it to be an index anymore, we can
    # convert it to a normal column
    df.reset_index(inplace=True)
    # Find the variable name by finding the col header that's not unit_of_obs
    # and not year
    var_names = [colname for colname in df.columns if colname.lower() not in [unit_of_obs,"year","notes"]]
    if len(var_names) != 1:
        raise Exception("_entries file must have a unique non-year variable")
    var_name = var_names[0]
    df["variable"] = var_name
    # And now we can rename the actual var column "value"
    df.rename(columns={var_name:"value"},inplace=True)
    # Apply remapping rules to the index col
    new_df = apply_index_rules(df, unit_of_obs, index_rules)
    new_df["row_num"] = np.arange(len(new_df))
    new_df["source_id"] = fname
    return new_df

def in_output_folder(fpath, pl):
    path_obj = Path(fpath)
    return path_obj.parent.absolute() == Path(pl.get_output_path()).absolute()

def run(pl, verbose=False):
    """
    The "main" file for the step. Finds all .csv files in `pl.input_path` and
    calls process_file() on each, then saves the new (now long-format) DF 
    """
    vprint = print if verbose else lambda x: None
    vprint(f"Parsing files from input path {pl.input_path}")
    input_fpaths = []
    for cur_varname in pl.get_varnames():
        cur_fpaths = glob.glob(f"{pl.input_path}/{cur_varname}/*.csv")
        input_fpaths.extend(cur_fpaths)
    # We need to remove the trust.csv file, though
    input_fpaths = [f for f in input_fpaths if "trust.csv" not in f]
    # And any .csvs already in the output folder
    input_fpaths = [fp for fp in input_fpaths if not in_output_folder(fp, pl)]
    pkl_output_fpaths = []
    for cur_fpath in input_fpaths:
        vprint(f"parse_files(): Opening {cur_fpath}")
        processed_df = process_data_file(pl, cur_fpath, verbose=verbose)
        if processed_df is None:
            # File does not contain data relevant to our spec, so skip
            vprint(f"Skipping {cur_fpath}")
            continue
        # Save to .csv and .pkl
        ### Part 7: Save long-form df to output folder
        # Now we can use the sheet_id as the filename for the new csv
        source_id = str(processed_df["source_id"].iloc[0])
        csv_output_fname = source_id.replace(".csv","_parsed.csv")
        csv_output_fpath = os.path.join(pl.output_path, csv_output_fname)
        processed_df.to_csv(csv_output_fpath, index=False)
        # Also save a .pkl for later steps
        pkl_output_fpath = csv_output_fpath.replace(".csv",".pkl")
        processed_df.to_pickle(pkl_output_fpath)
        vprint(f"Parsed version saved to {pkl_output_fpath}")
        pkl_output_fpaths.append(pkl_output_fpath)
    # Save the parsed file fpaths to the pl object so later pipeline steps can use them
    pl.parsed_pkl_fpaths = pkl_output_fpaths