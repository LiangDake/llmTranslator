from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField, MultipleFileField, HiddenField

"""
Forms for login, registration, create folder and upload file
Some basic validation and message feedback
"""

class CreateFolderForm(FlaskForm):
    folder_name = StringField("Folder name", render_kw={"placeholder": "输入文件夹名"})
    folder_path = StringField("Folder path", render_kw={"readonly": True, "hidden": True})
    create_btn = SubmitField("创建文件夹")

class UploadFileForm(FlaskForm):
    upload_file_name = MultipleFileField("File name")
    folder_path = StringField("Folder path", render_kw={"readonly": True, "hidden": True})
    upload_btn = SubmitField("上传所有文件")
