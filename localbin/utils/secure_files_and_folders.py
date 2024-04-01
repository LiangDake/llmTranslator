
from localbin import ALLOWED_EXTENSIONS
import hashlib
import re

def sanitize_folder_name(folder_name):
    """
    Sanitize folder name by removing occurences like
    .. / . <> {} [] | : 
    """
    # Remove invalid characters and add spaces
    folder_name = re.sub(r'[\\/:"*?\[\]\.\.{}<>|]', ' ', folder_name)
    
    # Replace spaces with underscores
    folder_name = folder_name.replace(' ', '_')
    
    # If max length is exceeded cut the name from start to max
    max_length = 100
    if len(folder_name) > max_length:
        folder_name = folder_name[:max_length]
    
    return folder_name

def calculate_file_hash(file_path):
    """
    Helper function to calculate file hash using
    :hashlib
    """
    hash = hashlib.md5()
    
    with open(file_path, 'rb') as f:
        while block := f.read(4096):
            hash.update(block)
    return hash.hexdigest()

def allowed_file(filename):
    """
    Allowed extensions
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS