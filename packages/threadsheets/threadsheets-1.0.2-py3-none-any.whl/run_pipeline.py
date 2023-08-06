import os

from pipeline import Pipeline

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

def main():
    input_path = os.path.join("..","Translation","data02_CombinePL_Input")
    output_path = os.path.join("..","Translation","data03_PipelineOutput")
    spec_fpath = os.path.join(".","dissertation_data.conf")
    books_grid = {'variable':'num_copies', 'unit_of_obs':'language', 'years':range(1945,1991),
                  'exclude_units':['Foreign Languages','Total','TOTAL','Totals','TOTALS',
                                   'Languages of India','Other']}
    student_grid = {'variable':'num_students','unit_of_obs':'country','years':range(1959,1991),
                    # Don't care about continental/regional or overall totals rn
                    'exclude_units':['Latin America','Asia','Africa','Total','TOTAL','Totals','TOTALS',
                                     'Middle East','Other','South Asia','Sub-Saharan Africa',
                                     'North Africa','East Asia','Europe',
                                     'Middle East And South Asia'] + temp_exclude + temp_exclude2}
    var_grids = [books_grid, student_grid,
                 {'variable':'cp_membership','unit_of_obs':'country', 'years':range(1945,1991)}]
    pl = Pipeline(input_path=input_path, output_path=output_path,
                  var_grids=var_grids, spec_fpath=spec_fpath)
    public_path = os.path.join("..","public_html","threadsheets")
    # TODO: make a lil gui where there are checkboxes for enabling/disabling
    # steps, and then a "Run" button
    #steps = [
    #    #"import_from_dropbox",
    #    "parse_files",
    #    "combine_files",
    #    ("create_grids", {'grid_spec_list':var_grids}),
    #    ("copy_to_dir", {"path": public_path})
    #]
    #pl.run(steps)
    pl.parse_files()
    
if __name__ == "__main__":
    main()