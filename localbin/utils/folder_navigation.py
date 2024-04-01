import os

from flask import session
from flask import redirect
from flask import url_for

from localbin import app
from localbin import basedir

def get_user_upload_folder():
    """
    Gets the current user working directory.
    Returns None if there is no such user / not loged in.
    user.username is stored in
    :session['user']
    """
    if session["user"]:
        user = session['user']
        
        upload_folder = app.config['UPLOAD_FOLDER']
        default_upload_folder = f"{basedir}/{upload_folder}"
        
        path_to_user_root = f"{default_upload_folder}"
        user_folder = os.path.join(path_to_user_root, user)
        
        return user_folder
    
    return None

def get_user_location_path(parent_path, requested_path):
    """
    This function constructs URL path based on parent and requested paths
    """
    if parent_path == '..':
        return url_for('core.index')
    else:
        return url_for('core.index', requested_path=requested_path)
    
def redirect_url_to_page_and_path(to_path="", to_page='core.index'):
    """
    Function to redirect to index url with or without current path position
    For example if user is in /home/username/my_folder it will return the user to their folder eg my_folder
    """
    return redirect(url_for(to_page, requested_path=to_path))