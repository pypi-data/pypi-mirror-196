# https://packaging.python.org/en/latest/tutorials/packaging-projects/
import datetime
import os

from dataspec import DataSpec

class Threader:
    def __init__(self, input_path, spec_fpath, var_grids, output_path=None, verbose=False):
        """


        :param input_path:
        :param output_path:
        :param spec_fpath:
        """
        self.verbose = verbose
        self.vprint = print if self.verbose else lambda x: None
        ### 1. Timestamp the pipeline creation
        self.start_time = datetime.datetime.now()
        self.start_timestamp = self.start_time.strftime("%Y-%m-%d_%H%M%S")
        print(f"[{self.start_timestamp}] Pipeline initialized")
        ### 2. Input and output paths
        self.input_path = input_path
        if (output_path is None):
            # Default output path: [input_path]/parsed
            self.output_path = os.path.join(self.input_path, "parsed")
        else:
            self.output_path = output_path
        # And create it if it doesn't exist
        if not os.path.isdir(self.output_path):
            os.mkdir(self.output_path)
        # And it needs separate subfolders for the combined (entries) file
        # and the grid files
        self.combined_output_path = os.path.join(self.output_path, "combined")
        self.grid_output_path = os.path.join(self.output_path, "grid")
        # And this function makes sure they all exist, creates them otherwise
        self.ensure_paths_exist()
        self.parsed_pkl_fpaths = []
        ### 3. The desired output parameters
        self.var_grids = var_grids
        ### 4. Load and process the data specification (the .conf file)
        self.data_spec = DataSpec.from_file(spec_fpath)
        ### This just increments every time progress() is called, for a rough
        ### progress meter
        self.step_counter = 1

    def combine_parsed_files(self):
        import p02_combine_files
        p02_combine_files.run(self)

    def create_grids(self, grid_spec_list):
        import p03_create_grids
        p03_create_grids.run(self, grid_spec_list)

    def _ensure_path_exists(self, path):
        # Make sure that the subfolder we need exists,
        # and create it if not
        if not os.path.isdir(path):
            os.makedirs(path)

    def ensure_paths_exist(self):
        # Just calls ensure_path_exists on all the dirs we need
        self._ensure_path_exists(self.input_path)
        self._ensure_path_exists(self.output_path)
        self._ensure_path_exists(self.combined_output_path)
        self._ensure_path_exists(self.grid_output_path)

    def get_index_rule(self, var_name):
        return self.data_spec.get_index_rule(var_name)

    def get_index_rules(self):
        return self.data_spec.get_index_rules()

    def get_output_path(self):
        return self.output_path

    def get_varnames(self):
        return [cur_grid['variable'] for cur_grid in self.var_grids]

    def get_varspec(self, var_name):
        return self.data_spec.get_varspec(var_name)

    def get_data_spec(self):
        return self.data_spec

    def parse_data_files(self, verbose=False):
        import p01_parse_files
        p01_parse_files.run(self, verbose=verbose)

    # def parse_data_files(self):
    #     """
    #     The "main" file for the step. Finds all .csv files in `input_path` and
    #     calls parse_data_file() on each, then saves the new (now long-format) DF
    #     """
    #     import p01_parse_files
    #     extract_dir = self.input_path
    #     self.vprint(f"Parsing files from input path {self.input_path}")
    #     data_fpaths = glob.glob(f"{self.input_path}/**/*.csv", recursive=True)
    #     # We need to remove the trust.csv file, though
    #     data_fpaths = [f for f in data_fpaths if "trust.csv" not in f]
    #     pkl_output_fpaths = []
    #     for cur_fpath in data_fpaths:
    #         self.vprint(f"parse_data_files(): Opening {cur_fpath}")
    #         processed_df = p01_parse_files.process_data_file(cur_fpath, index_rules=self.get_index_rules(),
    #                                                          verbose=self.verbose)
    #         # Save to .csv and .pkl
    #         ### Part 7: Save long-form df to output folder
    #         # Now we can use the sheet_id as the filename for the new csv
    #         source_id = str(processed_df["source_id"].iloc[0])
    #         csv_output_fname = source_id.replace(".csv", "_parsed.csv")
    #         csv_output_fpath = os.path.join(pl.output_path, csv_output_fname)
    #         processed_df.to_csv(csv_output_fpath, index=False)
    #         # Also save a .pkl for later steps
    #         pkl_output_fpath = csv_output_fpath.replace(".csv", ".pkl")
    #         processed_df.to_pickle(pkl_output_fpath)
    #         vprint(f"Parsed version saved to {pkl_output_fpath}")
    #         # Save the parsed file fpaths to the pl object so later pipeline steps can use them
    #         self.parsed_pkl_fpaths.append(pkl_output_fpath)

    def push_to_git(self, var_list=None):
        import io05_push_to_git
        io05_push_to_git.run(self, var_list=var_list)

    def save_df(self, df, pkl_fpath, include_index):
        df.to_pickle(pkl_fpath)
        csv_fpath = pkl_fpath.replace(".pkl", ".csv")
        df.to_csv(csv_fpath, index=include_index, float_format='%.3f')
        print(f"Saved {csv_fpath}")

    # def run(self, steps):
    #     for cur_step in steps:
    #         # cur_step should either be a string or a (str,dict) tuple. If the
    #         # latter, the dict contains the kwargs to send to the function
    #         if type(cur_step) == str:
    #             fn_name = cur_step
    #             kwargs = {}
    #         elif type(cur_step) == tuple:
    #             # Separate the fn name and the kwargs
    #             fn_name = cur_step[0]
    #             kwargs = cur_step[1]
    #         self.progress(fn_name)
    #         globals()[fn_name](self, **kwargs)
    #     self.progress("Pipeline complete")
