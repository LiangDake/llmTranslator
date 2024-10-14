import os
import datetime as dt
from pathlib import Path

def convert_file_stat(file, user_path):
    """
    Get each file needed stat using
    :os.stat()
    Then convert it to human readable information using
    :get_readable_byte_size()
    :get_time_stamp()
    And set file or folder icon and type using
    :get_icon_class()
    """
    file_stat = os.stat(file)
    file_bytes = get_readable_byte_size(file_stat.st_size)
    file_time = get_time_stamp(file_stat.st_mtime)
    file_created_time = get_time_stamp(file_stat.st_ctime)
    
    file_icon = "bi bi-folder-fill" if os.path.isdir(file.path) else get_icon_class(file.name)
    file_type = "folder" if os.path.isdir(file.path) else "file"

    return {'name': file.name,
            'size': file_bytes,
            'created_time':file_created_time,
            'modified_time': file_time,
            'file_icon': file_icon,
            'file_link': os.path.relpath(file.path, user_path),
            'file_type': file_type,
            }

def get_readable_byte_size(num, suffix="B"):
    """
    Convert file bytes to human readable data
    """
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

def get_time_stamp(time_seconds):
    """
    Convert `os.stat().st_mtime and os.stat().st_ctime to readable format `
    """
    time_object = dt.datetime.fromtimestamp(time_seconds)
    time_string = dt.datetime.strftime(time_object, '%d-%m-%Y %H:%M:%S')
    return time_string

def get_icon_class(file_name):
    """
    This will set bootstrap icon for file_name type if its in
    :file_types
    """
    file_extension = Path(file_name).suffix
    file_extension = file_extension[1:] if file_extension.startswith(".") else file_extension

    if file_extension in ["zip", "exe"]:
        return "bi bi-file-zip"

    # if file_extension in ["eml", "msg"]:
    #     return "bi bi-envelope"

    file_types = ["csv", "doc", "docx", "jpg", "pdf", "png"]
    
    file_class_name = f"bi bi-filetype-{file_extension}" if file_extension in file_types else "bi bi-file-earmark"
    
    return file_class_name


    