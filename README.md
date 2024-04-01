# LocalBin

# Readme Structure
- [UI Preview](#ui-Preview)
- [Introduction](#introduction)
- Video Demo <https://www.youtube.com/watch?v=Uc2_M43Wz_w>
- [How To Install](#how-to-install)
- [Web Client](#web-client)
- [File System Interaction](#file-system-interaction)
- [Folder Navigation](#folder-navigation)
- [File Manipulation](#file-manipulation)
- [Security Considerations](#security-considerations)
- [Used Languages and Tools](#used-languages-and-tools)
- [Ways to improve the app](#ways-to-improve-the-app)

#### UI Preview - Use New picture
![File Browser](https://github.com/Acrofil/emerging-talents-2024-at-exercise/blob/main/file_browser_preview.png)

## Introduction
This is simple file browser build with Flask. 
The server interacts with `Linux` filesystems using Python `os` module to perform the tasks.
Each user has their own private root folder on the server where they can perform basic operations such as
- Navigating file system
- Create folders 
- Upload files
- Rename files and folders 
- Delete files and folders.

#### Video Demo: - Use other video


### How To Install
##### Clone the repo and cd into it
```bash
git clone https://github.com/Acrofil/localbin
cd localbin
```

##### Create env and activate it
```bash
python -m venv env
source ./env/bin/activate
```

##### Install from requirements.txt and create db
```bash
pip install -r requirements.txt
python
from file_browser import db
db.create_all()
```

##### Run flask app in debug mode
```bash
flask --app run run --debug
```

#### Web Client
The web client is build with `Python`, `Jinja`, `HTML`, `CSS`, `Bootstrap` and `JavaScript`
There is Login and Registration page. Form validation is handled on server side and users are notified if form validation fails.
Each user has their own personal folder in the server where they can expand further.
`users_space/username` is the location for each user that we have and this is also the root for them at `username`.
The web client consists of simple UI where users can see their current path in their space with properties for files and folders.
Create new folder, rename files and folders, delete files and folders, navigate and upload are the operations users can perform.
The web client and server are developed under Linux and the os commands used are for Linux only. 
No support for now for other OS's.

##### File System Interaction
File system interaction is handled by `Python` and `os` module. File information is displayed with the `os.stat()` and then converted to human readable data.
* Navigate throuh user space by clicking the backward arrow or hitting the folder icon to go back to the root folder.
* Create new folders.
* Upload files. 
* Rename files and folders.
* Delete files and folders (for folders only empty folders can be deleted).

#### Folder Navigation
Each user has his own root folder. In this example their path is `/home/username`
- Users can navigate in their folders in 3 ways
* By clicking on the root folder icon next to the path indicator
* Go in a folder by clicking unto it or clicking the arrow next to the other interaction buttons
* By going back from the arrow icon

#### File Manipulation
Users can perform basic operations which include:
* Create new folders
* Upload files 
* Download files and check hash data for integrity
* Read/view files directly in the client
* Rename files and folders
* Delete files and folders

#### Security Considerations
For the security of the web server are considered the following: 
* Login is requiered to perform any operations
* Users cannot manipulate other users folders and files. This is done by storing the user name/id in the session
* For handling special cases like `..`, `../..` all files and folders are sanitized/secured.
* File upload is possible only for supported formats `[jpg, jpeg, pdf, txt, gif, 'png]` and maximum size of 15mb. 
* Each user input is validated and sanitized
* Renaming of files is possible only for the main text not the suffix after .

##### Used Languages and Tools:
* Flask, flask_login, wtforms, flask_wtf, flask_sqlalchemy, sqlite3, JavaScript, Jinja, HTML, CSS, Bootstrap, Git, Linux, VsCode

##### Ways to improve the app
* Add tooltip information for better UI experience
* Add more confirmation checks for some operations
* Support wider range of files
* Validate files using library like libmagick
* Scan files for malicious code using ClamAV
* Add more features to the database like store files on remote server and only store the cdn related to the user id
* Use different database
* Support other OS's
* Make Docker image
