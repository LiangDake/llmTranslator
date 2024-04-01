function confirmDeletion(displayName) {
    let warningText = `You are about to delete ${displayName} Are you sure?`;

    if (confirm(warningText) == true) {
        return true;
      } else {
        return false;
      }
}

// Handle renaming files and folders
document.addEventListener('DOMContentLoaded', function () {

    const csrfTokenMeta = document.querySelector('meta[name="csrf-token"]');
    const csrfToken = csrfTokenMeta ? csrfTokenMeta.content : '';
    
    let editFilaNameBtns = document.querySelectorAll(".edit_file_name");
    let deleteBtns = document.querySelectorAll(".delete_file");

    editFilaNameBtns.forEach(function (button) {
        button.addEventListener('click', function () {

            const parentTr = this.closest('tr');
            let fileNameInput = parentTr.querySelector('.new_file_name');
            let displayName = parentTr.querySelector('.display_name');
            let hideDisplayName = parentTr.querySelector('.hide_display_name');
            let saveButton = parentTr.querySelector('.save_btn');
            let cancelButton = parentTr.querySelector('.cancel_btn');
            let pathToFile = saveButton.value;

            fileNameInput.value = displayName.value;

            let fileNameToSplit = fileNameInput.value; 
            
            // Split the file from the dot
            if (fileNameToSplit.indexOf(".") !== -1) {
                fileNameAndSuffix = fileNameToSplit.split(".");
                fileNameInput.value = fileNameAndSuffix[0];
                fileNameSuffix = fileNameAndSuffix[1];
            } else {
                // Handle filenames without dot
                fileNameInput.value = fileNameToSplit;
                fileNameSuffix = ""; 
            }
            
            // Hide/show and focus rename input 
            hideDisplayName.hidden = true;
            fileNameInput.hidden = false;
            fileNameInput.readOnly= false;
            saveButton.hidden = false;
            cancelButton.hidden = false;
            console.log(fileNameInput.value);
            
            fileNameInput.focus();

            // If save button is clicked
            saveButton.addEventListener('click', () => {
                let oldFileName = displayName.value;
                let newFileName = fileNameInput.value;
                
                fetch('/rename_file', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({
                        old_file_name: oldFileName,
                        new_file_name: newFileName,
                        file_suffix: fileNameSuffix,
                        path_to_file: pathToFile
                    })
                })
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error('Failed to rename file');
                    }
                })
                .then(data => {
                    // Update file name displayed on the page
                    displayName = data.new_file_name;
                    fileNameInput.value = data.new_file_name;
                    // Hide input field and buttons
                    fileNameInput.hidden = true;
                    fileNameInput.readOnly = true;
                    saveButton.hidden = true;
                    cancelButton.hidden = true;
                    location.reload();
                })
                .catch(error => {
                    console.log('Error', error);
                });
            });

            // If cancel button is clicked
            cancelButton.addEventListener('click', () => {
                location.reload();
            });
        });
    });

    // Handle deleting files and folders
    deleteBtns.forEach( function (button_d) {
        button_d.addEventListener('click', function () {
            
            const parentTr = this.closest('tr');
            let displayName = parentTr.querySelector('.display_name');
            let deleteBtn = parentTr.querySelector('.save_btn');
            let pathToDeleteFile = deleteBtn.value;
            console.log(pathToDeleteFile)

            let deleteFileConfirmation = confirmDeletion(displayName.value);

            if (!deleteFileConfirmation) {
                location.reload();
            };
            
            fetch('/delete_file', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    delete_file: displayName.value,
                    path_to_delete_file: pathToDeleteFile
                })
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Failed to delete file');
                }
            })
            .then(data => {
                location.reload();
            })
            .catch(error => {
                console.log('Error deleting file', error);
            })
        });
    });
});
