import json
import os
from pathlib import Path

from flask import Blueprint
from flask import render_template, flash, session, send_file
from flask_login import login_required
from werkzeug.security import safe_join

from localbin.core.forms import CreateFolderForm, UploadFileForm
from localbin.utils.convert_file_data import convert_file_stat
from localbin.utils.folder_navigation import get_user_location_path, get_user_upload_folder
from localbin.utils.folder_navigation import redirect_url_to_page_and_path

core = Blueprint('core', __name__, template_folder='../templates/core', static_folder='static')

@core.route("/", defaults={"requested_path": ""}, methods=["GET", "POST"])
@core.route("/<path:requested_path>")
@login_required
def index(requested_path):
    
    user = session['user']
    create_folder_form = CreateFolderForm()
    upload_file_form = UploadFileForm()
    
    user_folder = get_user_upload_folder() 
    abs_path = safe_join(user_folder, requested_path)
    
    if user not in abs_path:
        flash("Not allowed!")
        return redirect_url_to_page_and_path()
    
    if os.path.isfile(abs_path):
        try:
            return send_file(abs_path)
        
        except Exception as e:
            print(e)

    #all_files = [convert_file_stat(file, user_folder) for file in os.scandir(abs_path)]
    folders = [convert_file_stat(file, user_folder) for file in os.scandir(abs_path) if os.path.isdir(file.path)]
    files = [convert_file_stat(file, user_folder) for file in os.scandir(abs_path) if os.path.isfile(file.path)]

    parent_path = os.path.relpath(Path(abs_path).parents[0], user_folder)
    path_indicator = get_user_location_path(parent_path, requested_path)

    with open('localbin/translator/language.json', 'r', encoding='utf-8') as f:
        languages = json.load(f)

    return render_template("index.html", 
                           user_folder=user_folder, 
                           folders=folders,
                           files=files,
                           parent_path=parent_path, 
                           path_indicator=path_indicator,
                           create_folder_form=create_folder_form, 
                           upload_file_form=upload_file_form,
                           languages=languages,
                           os=os)


