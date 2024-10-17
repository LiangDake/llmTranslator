import os

from flask import Blueprint, request, redirect, flash
from flask_login import login_required
from werkzeug.security import safe_join
from werkzeug.utils import secure_filename

from localbin.translator import file_processing, tools
from localbin.utils.folder_navigation import get_user_upload_folder, redirect_url_to_page_and_path

translator = Blueprint('translator', __name__)


# 翻译函数
def translate(file_path, translated_folder_path, source_lang = 'osd', target_lang="中文"):
    # 获得文件链接
    file_type = file_processing.get_file_type(file_path)
    # 判断是否为支持翻译的文件类型
    if file_type in file_processing.supported_formats:
        # 判断是否为email
        if file_type in (".eml", ".msg"):
            # 调用邮件翻译功能，所有翻译后的文件均保存至processed文件夹
            translated_file_path = tools.QueryFileBase().translate_email(
                file_path,
                translated_folder_path,
                source_lang,
                target_lang
            )
        else:
            # 调用文件翻译功能，所有翻译后的文件均保存至processed文件夹
            translated_file_path = tools.QueryFileBase().translate_file_without_eml(
                file_path,
                translated_folder_path,
                source_lang,
                target_lang)

        return translated_file_path


@translator.route("/translate_file", methods=["POST"])
@login_required
# 文件翻译的接口
def translate_file():
    file_path = request.form.get('file_path')
    source_lang = request.form.get('source_lang')  # 获取源语言缩写
    user_folder = get_user_upload_folder()
    abs_path = safe_join(user_folder, file_path)
    # 获取文件的目录
    upload_directory = os.path.dirname(abs_path)

    # 定义子文件夹的路径
    translated_directory = os.path.join(upload_directory, 'translated')

    # 创建子文件夹（如果不存在的话）
    if not os.path.exists(translated_directory):
        os.makedirs(translated_directory)
    # 调用翻译函数，返回翻译后的文件路径
    translated_file_path = translate(
        file_path=abs_path,
        translated_folder_path=translated_directory,
        source_lang=source_lang
    )
    parent_path = os.path.dirname(file_path)
    flash("文件翻译成功！请刷新网页或点击translated文件夹查看！")
    return redirect_url_to_page_and_path(parent_path)


@translator.route("/translate_folder", methods=["POST"])
@login_required
# 文件翻译的接口
def translate_folder():
    # 获取到文件夹相对路径
    folder_path = request.form.get("folder_path")
    source_lang = request.form.get('source_lang')  # 获取源语言缩写
    # 去掉前面的斜杠
    folder_path = folder_path.lstrip('/')
    # 获取到当前用户文件夹地址 例如：/Users/liangdake/localbin/localbin/users_space/liangke
    user_folder = get_user_upload_folder()
    # 获取到已上传文件夹地址
    abs_path_to_folder = os.path.join(user_folder, folder_path)
    # 定义子文件夹的路径
    translated_directory = os.path.join(abs_path_to_folder, 'translated')
    # 创建子文件夹（如果不存在的话）
    if not os.path.exists(translated_directory):
        os.makedirs(translated_directory)

    # 获得文件夹中所有文件，作为数组
    files = file_processing.get_files_with_absolute_paths(abs_path_to_folder)
    for file_path in files:
        # 获取文件名并构造翻译文件路径
        filename = os.path.basename(file_path)
        translated_file_path = os.path.join(translated_directory, filename.replace('.', '_Translated.'))

        # 跳过已翻译的文件
        if os.path.exists(translated_file_path):
            print(f"Skipping translation for {filename}: already translated.")
            continue
        try:
            # 进行翻译
            translated_file_path = translate(file_path=file_path, translated_folder_path=translated_directory, source_lang=source_lang)
        except (IOError, ValueError) as e:
            print(f"Translation error for {file_path}: {str(e)}")

    flash("文件夹所有文件翻译成功！请刷新网页或点击translated文件夹查看，请仔细检查是否有未翻译的文件！")
    return redirect_url_to_page_and_path(to_path=folder_path)

