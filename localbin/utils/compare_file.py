from flask import Flask, render_template, send_file, url_for
import os
import PyPDF2
from email import policy
from email.parser import BytesParser

from langchain_community.document_loaders import UnstructuredEmailLoader, PyPDFLoader, UnstructuredImageLoader

from localbin.translator.file_processing import import_file


def get_translated_file_path(file_link):
    # 获取文件所在的目录路径
    dir_path = os.path.dirname(file_link)

    # 获取文件名和扩展名
    base_name, ext = os.path.splitext(os.path.basename(file_link))

    # 拼接翻译文件路径 (在目录下添加 `translated` 文件夹，并修改文件名)
    translated_dir_path = os.path.join(dir_path, 'translated')
    translated_file_name = f"{base_name}_Translated{ext}"
    translated_file_path = os.path.join(translated_dir_path, translated_file_name)

    return translated_file_path


# 读取PDF文件内容
def read_content(file_path, lang):
    doc = import_file(file_path, lang)
    text = doc[0].page_content
    return text


# 读取EML文件内容
def read_eml_content(file_path: str):
    # 读取 .eml/.msg 文件
    with open(file_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    # 获取邮件头信息并保存到字典中
    email_headers = {
        "From": msg['From'],
        "To": msg['To'],
        "Cc": msg.get('Cc', 'None'),
        "Subject": msg.get('Subject', 'None'),
        # 获取邮件发送时间
        "Date": msg.get('Date', 'None')
    }

    # 生成邮件头信息的字符串格式
    header_info = (f"发件人：{email_headers['From']}\n"
                   f"收件人：{email_headers['To']}\n"
                   f"抄送：{email_headers['Cc']}\n"
                   f"日期：{email_headers['Date']}\n\n"
                   f"正文：")

    # 获取邮件正文信息
    doc = UnstructuredEmailLoader(file_path=file_path, process_attachments=False).load()

    # 将邮件头信息添加到正文内容开头
    text = header_info + doc[0].page_content
    # 返回处理后的 doc 和 email_headers
    return text


# 读取文件内容，根据文件扩展名调用不同的处理方法
def read_file_content(file_path, lang):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.eml':
        return read_eml_content(file_path)
    else:
        return read_content(file_path, lang)

