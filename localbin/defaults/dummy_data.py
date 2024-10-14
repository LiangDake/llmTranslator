import os

def create_default_files_and_folders(path, path3):
    """
    Create dummy data with files and folders after new user registration
    """
    
    default_files_root = []
    default_files_home = []
    
    default_folders_home = ['文件', '邮件']
    default_folders_root = []

    # # Creating default files and folders
    # for file in default_files_root:
    #     file_path = os.path.join(path, file)
    #     with open(file_path, 'w') as file:
    #         file.write("This is the file that contains some random data".format(file))
    #
    # for file in default_files_home:
    #     file_path = os.path.join(path3, file)
    #     with open(file_path, 'w') as file:
    #         file.write(f"This is the file that contains some random data".format(file))
    #
    # for folder in default_folders_root:
    #     folder_path = path
    #     directory_path = os.path.join(folder_path, folder)
    #     os.mkdir(directory_path)
    
    for folder in default_folders_home:
        folder_path = path3
        directory_path = os.path.join(folder_path, folder)
        os.mkdir(directory_path)