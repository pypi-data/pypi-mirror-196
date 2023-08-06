#       _                              
#      | |                             
#    __| |_ __ ___  __ _ _ __ ___  ___ 
#   / _` | '__/ _ \/ _` | '_ ` _ \/ __|
#  | (_| | | |  __/ (_| | | | | | \__ \
#   \__,_|_|  \___|\__,_|_| |_| |_|___/ .
#
# A 'Fog Creek'–inspired demo by Kenneth Reitz™

# Python imports
import os
import sys
import time

# 3rd party imports
import dropbox
from flask import Flask, request, render_template, jsonify
import joblib

# Local imports
import pipeline

# Support for gomix's 'front-end' and 'back-end' UI.
app = Flask(__name__, static_folder='public', template_folder='views')

# Set the app secret key from the secret environment variables.
app.secret = os.environ.get('SECRET')

# Threadsheets-specific globals (set in initialize())
latest_grid = None
latest_info = None
iprint = None
dprint = None

# Dream database. Store dreams in memory for now. 
DREAMS = ['Python. Python, everywhere.']

# This is the js code...
#var fetch = require('isomorphic-fetch');
#  var Dropbox = require('dropbox').Dropbox;
#  new Dropbox({
#    fetch: fetch,
#    accessToken: 'YOUR_ACCESS_TOKEN_HERE'
#  })
#  .filesListFolder({path: '/Translation/data02_CombinePL_Input'})
#  .then(console.log, console.error);

# Python code this time

@app.after_request
def apply_kr_hello(response):
    """Adds some headers to all responses."""
  
    # Made by Kenneth Reitz. 
    if 'MADE_BY' in os.environ:
        response.headers["X-Was-Here"] = os.environ.get('MADE_BY')
    
    # Powered by Flask. 
    response.headers["X-Powered-By"] = os.environ.get('POWERED_BY')
    return response

def list_folder(dbx, folder, subfolder):
    """List a folder.
    Return a dict mapping unicode filenames to
    FileMetadata|FolderMetadata entries.
    """
    path = '/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'))
    while '//' in path:
        path = path.replace('//', '/')
    path = path.rstrip('/')
    try:
        with stopwatch('list_folder'):
            res = dbx.files_list_folder(path)
    except dropbox.exceptions.ApiError as err:
        print('Folder listing failed for', path, '-- assumed empty:', err)
        return {}
    else:
        rv = {}
        for entry in res.entries:
            rv[entry.name] = entry
        return rv

data_path = '/Translation/data02_CombinePL_Input'
def get_data_list():
    with open('.dropboxkey', 'r', encoding='utf-8') as f:
        db_key = f.read().strip()
    dbx = dropbox.Dropbox(db_key)
    file_info_list = dbx.files_list_folder(data_path)
    file_str_list = []
    for cur_entry in file_info_list.entries:
        # Check if file or folder
        if type(cur_entry) == dropbox.files.FolderMetadata:
            file_str_list.append(cur_entry.name)
    return file_str_list

@app.route('/grid/<grid_name>')
def get_grid(grid_name):
    # Later I probably have to implement some session thing here, like
    # session['latest_urls'] or smth, but for now I'm just directly accessing
    # the dict without any users or anything
    return latest_grid[grid_name]

@app.route('/info/<grid_name>')
def get_info(grid_name):
    return latest_info[grid_name]

@app.route('/')
def homepage():
    """Displays the homepage."""
    file_str_list = get_data_list()
    return render_template('index.html', files=file_str_list)

@app.route('/run', methods=['POST'])
def run_pipeline():
    """
    Runs the pipeline, importing the .csvs from dropbox and
    (eventually) exporting to GitHub Gist
    """
    print("run_pipeline()")
    print(request.form, file=sys.stderr, flush=True)
    #print(dir(request.form), file=sys.stderr, flush=True)
    folder_list = list(request.form.listvalues())[0]
    print(folder_list, file=sys.stderr, flush=True)
    _run_pl(folder_list)
    # testing
    time.sleep(1)
    return "Good job"

# Exclude for making the grid less hectic, but include in the final "tally" of
# the number of countries!
temp_exclude = ['Australia','Belgium','Canada','France','Iceland','Italy',
                'Japan','Netherlands','New Zealand','Norway','South Korea',
                'Sweden','UK','USA','West Germany']
# These are different: we do technically care about them for the project, but
# they either got independence hella late (Djibouti like 1979, Malta... 1975?)
# or just have so little data that it clutters the grid with white squares
# [Suriname didn't become independent until 1975]
temp_exclude2 = ['Bahrain','Belize','Cuba','Djibouti','Dominica','Fiji',
                 'French West Indies','Grenada','Jamaica','Maldives','Malta',
                 'Micronesia','Namibia','Oman','Papua New Guinea','Reunion',
                 'United Arab Emirates','Saudi Arabia','Seychelles','Suriname',
                 'Western Sahara','Yemen']

def _run_pl(folder_list):
    """
    Helper function, easier for testing (since it can be called by main() or
    by the server)
    """
    # For now, hard-coded input/output paths
    input_path = os.path.join("..","Translation","data02_CombinePL_Input")
    output_path = os.path.join(".","output")
    #var_grids = folder_list
    student_grid = {'variable':'num_students','unit_of_obs':'country','years':range(1959,1991),
                    # Don't care about continental/regional or overall totals rn
                    'exclude_units':['Latin America','Asia','Africa','Total','TOTAL','Totals',
                                     'TOTALS','Middle East','Other','South Asia',
                                     'Sub-Saharan Africa','North Africa','East Asia',
                                     'Europe',
                                     'Middle East And South Asia'
                                    ] + temp_exclude + temp_exclude2}
    var_grids = [student_grid]
    spec_fpath = "dissertation_data.conf"
    public_path = os.path.join(".","public_grids")
    #var_paths = [os.path.join(input_path, f) for f in folder_list]
    pl = pipeline.Pipeline(input_path, output_path, var_grids, spec_fpath)
    steps = [
        "import_local",
        "parse_files",
        "combine_files",
        ("create_grids", {'grid_spec_list':var_grids}),
        #("copy_to_dir", {"path": public_path})
        "push_to_git"
    ]
    pl.run(steps)

@app.route('/dreams', methods=['GET', 'POST'])
def dreams():
    """Simple API endpoint for dreams. 
    In memory, ephemeral, like real dreams.
    """
  
    # Add a dream to the in-memory database, if given. 
    if 'dreams' in request.args:
        DREAMS.append(request.args['dreams'])
    
    # Return the list of remembered dreams. 
    return jsonify(DREAMS)

def initialize():
    """
    Initialize the dicts and stuff, to avoid NullPointerExceptions
    """
    global latest_grid, latest_info, iprint, dprint
    # First things first, iprint() and dprint() for INFO and DEBUG printing
    iprint = lambda x: print(f"[INFO] {x}", file=sys.stderr, flush=True)
    dprint = lambda x: print(f"[DEBUG] {x}", file=sys.stderr, flush=True)
    latest_grid = {}
    if os.path.isfile("latest_grid.pkl"):
        latest_grid = joblib.load("latest_grid.pkl")
    latest_info = {}
    if os.path.isfile("latest_info.pkl"):
        latest_info = joblib.load("latest_info.pkl")

def main():
    initialize()
    #start_server()
    test_pipeline()

def start_server():
    app.run(debug=True)

def test_pipeline():
    _run_pl(["Students"])

if __name__ == '__main__':
    main()