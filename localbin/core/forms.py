from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField

"""
Forms for login, registration, create folder and upload file
Some basic validation and message feedback
"""

class CreateFolderForm(FlaskForm):
    folder_name = StringField("Folder name", render_kw={"placeholder": "New Folder"})
    folder_path = StringField("Folder path", render_kw={"readonly": True, "hidden": True})
    create_btn = SubmitField("Create")
    
class UploadFileForm(FlaskForm):
    upload_file_name = FileField("File name")
    folder_path = StringField("Folder path", render_kw={"readonly": True, "hidden": True})
    upload_btn = SubmitField("Upload")