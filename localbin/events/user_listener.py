import os

from sqlalchemy.event import listens_for
from localbin.auth.models import User
from localbin.defaults.dummy_data import create_default_files_and_folders


# An event listener after new user registration to create his folder space + some dummy data for testing  
@listens_for(User, "after_insert")
def create_home_dir_after_insert(map, con, user):
    # Create path for new dir
    root_directory =  f"{user.username}"
    parent_dir = "localbin/users_space"
    path = os.path.join(parent_dir, root_directory)
    
    # Create user root folder in users_space
    os.mkdir(path)
    
    # Create home dir
    home = "home"
    dir2 = f"localbin/users_space/{root_directory}"
    path2 = os.path.join(dir2, home)
    os.mkdir(path2)
    
    # Create user folder in home
    user_folder = user.username
    dir3 = f"localbin/users_space/{root_directory}/{home}"
    path3 = os.path.join(dir3, user_folder)
    os.mkdir(path3)
    
    # Create dummy data and folder structure
    create_default_files_and_folders(path, path3)