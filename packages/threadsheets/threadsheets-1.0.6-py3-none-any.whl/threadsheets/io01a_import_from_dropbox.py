import datetime
import io
import os
import shutil
import zipfile
import dropbox
import joblib
import pandas as pd
import numpy as np

def ensure_folder_exists(fpath):
    # Make sure that the subfolder of "input" that we need exists,
    # and create it if not
    fpath_elts = os.path.split(fpath)
    containing_dir_path = fpath_elts[0]
    if not os.path.isdir(containing_dir_path):
        os.makedirs(containing_dir_path)

update_times_fpath = "update_times.pkl"
def get_local_last_update_time(file_obj):
    if not os.path.isfile(update_times_fpath):
        # Return -infinity basically
        return datetime.datetime.min
    # Otherwise, load the dict and get the last update time
    last_updated = joblib.load("update_times.pkl")
    return last_updated[file_obj.name]
        
def is_newer(file_obj):
    # This is janky, but I'm just loading+saving to a pickled dict as my "db"
    local_last_update_time = get_local_last_update_time(file_obj)
    if file_obj.server_modified > local_last_update_time:
        return True
    return False
        
def download_file(file_obj, download_fpath):
    print(file_obj)
    print(f"Checking if newer version of {file_obj.name}")
    # Important: we want to use the *server_modified* time (not client_modified)
    # See https://www.dropboxforum.com/t5/Dropbox-API-Support-Feedback/clientModified-amp-serverModified-date/td-p/356896
    if is_newer(file_obj):
        print(f"Downloading {file_obj.name}")
        # We want to just download it to a file with the same name, but in the
        # "input" folder
        ensure_folder_exists(download_fpath)
        dbx.files_download_to_file(download_fpath, file_obj.path_display)
        print(f"Saved to {download_fpath}")
        #print(dir(f))
        #print(f.content)
        #with io.BytesIO(f.content) as input_stream:
        #    df = pd.read_csv(input_stream)
        ## Now we toss the df into our pipeline
        #print(df)
        return download_fpath

def download_folder(folder_obj):
    cat_name = folder_obj.name
    folder_fpaths = []
    # Open the folders
    folder_contents = list(dbx.files_list_folder(folder_obj.path_display).entries)
    for file_obj in folder_contents:
        #if entry.name == "Translation":
        fname = file_obj.name
        download_fpath = os.path.join("input",cat_name,fname)
        downloaded_fpath = download_file(file_obj, download_fpath)
        folder_fpaths.append(cur_fpath)
    return folder_fpaths

def stream_folders():
    folder_objs = list(dbx.files_list_folder('/Translation/data02_PipelineInput').entries)
    for cur_folder_obj in folder_objs:
        yield cur_folder_obj
        
def clear_path(path):
    shutil.rmtree(path)
        
def import_from_dropbox(pl):
    # Load Dropbox key from file
    with open(".dropboxkey", "r", encoding="utf-8") as f:
        dbkey = f.read()
    dbx = dropbox.Dropbox(dbkey)
    # First we clear out the existing imported files
    clear_path(os.path.join(".","imported_data"))
    # But we need to re-make the ones that are needed by the pipeline
    #pl.ensure_paths_exist()
    db_folder_name = os.path.basename(pl.dropbox_path)
    # Dropbox paths require the "/" at the beginning, like unix
    #dropbox_path = "/" + os.path.join("Translation","data02_CombinePL_Input")
    zip_fname = f"{db_folder_name}.zip"
    download_fpath = os.path.join(".","imported_data",zip_fname)
    result = dbx.files_download_zip_to_file(download_fpath, dropbox_path)
    # And unzip it
    extract_dir = "./imported_data"
    with zipfile.ZipFile(download_fpath, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    # And remove the original .zip file now that we've unzipped
    os.remove(download_fpath)
    # Now we have a subfolder in extract_dir containing our files
    extracted_subdir = os.path.join(extract_dir, input_folder_name)
    return extracted_subdir
