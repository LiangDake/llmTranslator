import os
import shutil

from flask_login import login_required

from flask import request, flash, redirect, abort, session, url_for, render_template
from flask import send_file, jsonify
from werkzeug.security import safe_join
from werkzeug.utils import secure_filename

from localbin.translator import file_processing
from localbin.utils.compare_file import read_file_content, get_translated_file_path
from localbin.utils.folder_navigation import redirect_url_to_page_and_path
from localbin.utils.secure_files_and_folders import sanitize_folder_name, calculate_file_hash, allowed_file
from localbin.utils.folder_navigation import get_user_upload_folder
from flask import Blueprint

user = Blueprint('user', __name__, template_folder='templates', static_folder='static', static_url_path='/user/static')

@user.route("/return_to_root>", methods=["GET", "POST"])
@login_required
def return_to_root():
    """
    Route to return to root when clicking on folder icon next to the path indicator
    """
    return redirect_url_to_page_and_path()

# Route for create new folder
@user.route("/create_folder", methods=["GET", "POST"])
@login_required
def create_folder():
    """
    Route for creating new folder
    New folder name is sanitazed with custom function using re
    :sanitize_folder_name
    """  
    if request.method == "POST":
        new_folder_name = request.form.get("folder_name")
        current_path = request.form.get("folder_path")
        
        # Catch if any error occur
        try:
            sanitized_folder_name = sanitize_folder_name(new_folder_name)
        except Exception:
            flash("Name not supported! Try again!")
            return redirect_url_to_page_and_path(current_path)
        
        # Get user folder and current path level structure
        user_folder = get_user_upload_folder()
        folder_level = current_path[1:].split("/")

        # Construct the abs path
        abs_path_to_folder = safe_join(user_folder, *folder_level, sanitized_folder_name)
        
        # Check if new folder exists
        if os.path.exists(abs_path_to_folder):
            flash(f"与 '{sanitized_folder_name}' 同名文件夹已存在，请修改文件夹名称！")
            return redirect_url_to_page_and_path(current_path)
        
        # Create new folder or catch exception
        try:
            os.mkdir(abs_path_to_folder)
            flash(f"Folder {sanitized_folder_name} created!")
            return redirect_url_to_page_and_path(current_path)
        
        # Return error and redirect
        except Exception as error:
            flash("An error occured while creating folder! Please try again!")
            return redirect_url_to_page_and_path()
    
    return redirect_url_to_page_and_path()
     
# Route to download file
@user.route("/download/<path:requested_file>")
@login_required
def download(requested_file):
    
    user = session['user']
    user_folder = get_user_upload_folder()
    abs_path = safe_join(user_folder, requested_file)
    
    if user not in user_folder:
        return abort(404)
    
    # If the path doesnt exists abort
    if not os.path.exists(abs_path):
        flash("File doesnt exists! Redirecting to root!")
        return redirect_url_to_page_and_path()
 
    if os.path.isfile(abs_path):
        try:
            # Send the file to the client
            response = send_file(abs_path, as_attachment=True)

            # Calculate hash of the downloaded file
            file_hash = calculate_file_hash(abs_path)

            # Add file hash to response headers
            response.headers['X-File-Hash'] = file_hash

            return response
        
        except Exception as e:
            print(e)

# Verify file integrity after each request
@user.after_request
def verify_file(response):
    if request.endpoint == "download":
        # Get user path and file name
        user_folder = get_user_upload_folder()
        file_name = request.view_args["requested_file"]
        
        # Build path
        file_path = os.path.join(user_folder, file_name)
        
        # Calculate the original file hash and get the stored hash in the headers
        original_file_hash = calculate_file_hash(file_path)
        downloaded_file_hash = response.headers['X-File-Hash']
        
        # Compare original file hash with downloaded
        if original_file_hash != downloaded_file_hash:
            flash(f"Integrity error! Please try downloading the file: {file_name} again!")
        
        else:
            flash(f"{file_name} 已成功下载!")
        
        return response
    
    return response

# Route for upload file
@user.route("/upload_file", methods=["GET", "POST"])
@login_required
def upload_file():
    """
    This route handles file upload
    file name is secured with 
    :werkzeug.utils secure_filename()
    
    Allowed file extensions for now are 'txt, pdf, jpg, png, jpeg and gif'
    Max size is 15mb
    """
    if request.method == 'POST':
        user_folder = get_user_upload_folder()
        current_path = request.form.get("folder_path")
        
        folder_level = current_path[1:].split("/")

        # check if the post request has the file part
        if 'upload_file_name' not in request.files:
            flash('No file')
            return redirect_url_to_page_and_path()
        
        files = request.files.getlist('upload_file_name')
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        for file in files:
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            if file and allowed_file(file.filename):
                secured_filename = secure_filename(file.filename)
                # Construct the absolute path
                abs_path_for_upload = safe_join(user_folder, *folder_level)
                full_file_path = os.path.join(abs_path_for_upload, secured_filename)
                file.save(full_file_path)

                # Check if the file is a zip and handle accordingly
                if file.filename.endswith('.zip'):
                    try:
                        file_processing.unzip(full_file_path, abs_path_for_upload)
                        # 解压缩成功后删除原始 .zip 文件
                        os.remove(full_file_path)
                        flash(f"{file.filename} 已成功解压缩并上传，请检查文件是否遗漏！")
                    except Exception as e:
                        flash(f"解压缩 {file.filename} 失败: {str(e)}")

                else:
                    flash(f"{file.filename} 已成功上传！")

            else:
                flash(f"{file.filename}的文件格式不支持，请尝试更换文件后缀或重新上传!")

        return redirect_url_to_page_and_path(current_path)

    return redirect_url_to_page_and_path()

# Rename file or folder
@user.route("/rename_file", methods=["POST"])
@login_required
def rename():
    if request.method == "POST":
        old_file_name = request.json.get('old_file_name')
        file_name_suffix = request.json.get('file_suffix')
        new_file_name = request.json.get('new_file_name')
        path_to_file = request.json.get('path_to_file')
        
        # Construct the path
        user_folder = get_user_upload_folder()
        folder_level = path_to_file[1:].split("/")
        full_path_to_file = os.path.join(user_folder, *folder_level, old_file_name)
        
        # Secure file name and add the original extension
        secured_new_file_name = sanitize_folder_name(new_file_name)
        
        # Add suffix if file
        if os.path.isfile(full_path_to_file):    
            secured_new_file_name += f".{file_name_suffix}"
        
        # Construct the full path to the new file
        new_file_abs_path = safe_join(user_folder, *folder_level, secured_new_file_name)
        
        # Check if new file exists
        if os.path.exists(new_file_abs_path):
            flash(f"File with name '{secured_new_file_name}' already exists or name not allowed!")
            return jsonify({'error': 'Method not allowed'}), 400
        
        # Path to file to be renamed and the new path
        new_path_to_file = os.path.join(user_folder, *folder_level, new_file_abs_path)
        
        # Catch any error
        try:
            os.rename(full_path_to_file, new_path_to_file)
        except Exception as e:
            flash("Error while renaming!")
        
        # Return response
        return jsonify({'success': True, 'renamed_file': new_file_name}), 200
    else:
        return jsonify({'error': 'Method not allowed'}), 400

# Route for deleting file
@user.route("/delete_file", methods=["POST"])
@login_required
def delete_file():

    if request.method == "POST":
        user = session['user']
        file_to_delete = request.json.get('delete_file')
        path_to_file = request.json.get('path_to_delete_file')

        # Construct the path
        user_folder = get_user_upload_folder()
        folder_level = path_to_file[1:].split("/")
        full_path_to_file = os.path.join(user_folder, *folder_level, file_to_delete)

        if not user in full_path_to_file:
            flash("Not allowed!")
            return abort(404)

        if not os.path.exists(full_path_to_file):
            flash("Error deleting! No such file")
            return jsonify({'error': 'No such file!'}), 400

        try:
            if os.path.isfile(full_path_to_file):
                os.remove(full_path_to_file)

            elif os.path.isdir(full_path_to_file):

                shutil.rmtree(full_path_to_file)

        except Exception:
            flash("File cannot be deleted! Sorry")
            return jsonify({'error': 'Error!'}), 400

        return jsonify({'success': True}), 200

    return jsonify({'error': 'Method not allowed'}), 400


# 对比文件的路由
@user.route('/compare')
@login_required
def compare_files():
    # 原始文件路径
    file_path = request.args.get('file_link')
    user_folder = get_user_upload_folder()
    abs_path = safe_join(user_folder, file_path)
    translated_file_path = get_translated_file_path(abs_path)
    # 检查文件是否存在
    if not os.path.exists(abs_path):
        return f"原文件 {file_path} 未找到！", 404
    else:
        # 读取原文件和翻译文件内容
        original_content = read_file_content(abs_path)
    if not os.path.exists(translated_file_path):
        translated_content = "文件未翻译或无法找到已翻译文件！"
    else:
        # 读取翻译文件内容
        translated_content = read_file_content(translated_file_path)

    # 渲染模板
    return render_template('core/compare.html',
                           original_filename=os.path.basename(abs_path),
                           translated_filename=os.path.basename(translated_file_path),
                           original_content=original_content,
                           translated_content=translated_content)
