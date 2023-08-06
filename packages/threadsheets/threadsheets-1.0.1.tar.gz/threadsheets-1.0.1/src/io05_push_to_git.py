import glob
import os

import dotenv
import github

def create_grid_repo(g):
    result = g.get_user().create_repo("ts-grids", private=True)
    return result

#dir(repo_obj)
def custom_get_contents(repo):
    # A wrapper around repo_obj.get_contents("") that returns [] if no files
    # (instead of throwing an annoying exception)
    try:
        contents = repo.get_contents("")
    except github.GithubException as e:
        return []
    return contents

def custom_get_file(repo, filename):
    # Another wrapper, returns None if file is not already in repo
    repo_contents = custom_get_contents(repo)
    for cur_content in repo_contents:
        if cur_content.path == filename:
            return cur_content
    return None

# Load the csv contents into strings, then into github.InputFileContent objects
def load_csv_contents(fpaths):
    # {filename: str} dict
    str_dict = {}
    # {filename: InputFileContent} dict
    content_dict = {}
    for cur_fpath in fpaths:
        filename = os.path.basename(cur_fpath)
        with open(cur_fpath, 'r', encoding='utf-8') as f:
            csv_content = f.read().strip()
        str_dict[filename] = csv_content
        csv_content_obj = github.InputFileContent(csv_content)
        content_dict[filename] = csv_content_obj
    return content_dict, str_dict

def run(pl, var_list=None):
    # The idea here is: get a list of .csvs in the output_dir, then push the
    # contents of this folder onto GitHub
    # Load the personal access token
    dotenv.load_dotenv(override=True)
    git_token = os.getenv("GH_TOKEN")
    g = github.Github('jpowerj', git_token)
    user = g.get_user()
    # See if the ts-grids repo already exists
    repo_exists = False
    repo_obj = None
    repos = list(user.get_repos())
    for cur_repo in repos:
        if "ts-grids" in cur_repo.full_name:
            repo_exists = True
            repo_obj = cur_repo
            break
    # Now we create the repo if it doesn't exist
    if not repo_exists:
        repo_obj = create_grid_repo(g)
    # Cool. So if we're here then the repo exists, and we can either add new
    # files to it or update the files already in it
    print(repo_obj)
    # The idea here is (1) put all the .csv files we want on Git into the
    # public_grids folder, then (2) push them all into a Gist
    #grid_csv_fpath = "./public_grids/num_students_grid.csv"
    #info_csv_fpath = "./public_grids/num_students_info.csv"
    # But, there may be outputs from other projects in that dir. So, make sure
    # we only export the ones for this project (the options to the Threader
    # constructor
    if var_list is None:
        # Just export all .csvs found
        all_csv_fpaths = glob.glob(os.path.join(pl.output_path, "grid", "*.csv"))
    else:
        # Export the .csvs for this var
        all_csv_fpaths = []
        for cur_varname in var_list:
            var_csv_fpaths = glob.glob(os.path.join(pl.output_path, "grid", f"{cur_varname}*.csv"))
            all_csv_fpaths.extend(var_csv_fpaths)
    input_dict, str_dict = load_csv_contents(all_csv_fpaths)
    file_results = []
    for cur_fname, content_str in str_dict.items():
        var_name = "_".join(cur_fname.split(".")[0].split("_")[:-1])
        # Here's a tricky part, though -- gotta check if the file exists in the 
        # repo already
        file_obj = custom_get_file(repo_obj, cur_fname)
        if file_obj is None:
            # File doesn't already exist, so we create it
            create_result = repo_obj.create_file(cur_fname, var_name, content_str)
            file_results.append(create_result)
        else:
            # File already exists in repo, so we need to update it
            old_sha = file_obj.sha
            update_result = repo_obj.update_file(cur_fname, var_name, content_str, old_sha)
            file_results.append(update_result)
    # Print the download urls
    for cur_file_result in file_results:
        print(cur_file_result['content'].download_url)

def api_example():
    """
    Example from the docs
    """
    with open(".gitpw", "r", encoding='utf-8') as f:
        git_pw = f.read().strip()
    g = Github("jpowerj", git_pw)
    # Then play with your Github objects:
    user = g.get_user()
    print()
    for repo in g.get_user().get_repos():
        print(repo.name)
        
def main():
    push_to_git(None)

if __name__ == "__main__":
    main()