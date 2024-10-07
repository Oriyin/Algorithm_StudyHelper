// Function to toggle the visibility of task descriptions
function toggleDescription(index) {
    const desc = document.getElementById(`desc-${index}`);
    if (desc) {
        if (desc.style.display === "none" || desc.style.display === "") {
            desc.style.display = "block";
        } else {
            desc.style.display = "none";
        }
    }
}

// Function to display the edit form for a task
function editTask(index) {
    // Hide all other edit forms before showing the selected one
    const editForms = document.querySelectorAll('.edit-form');
    editForms.forEach(form => form.style.display = 'none');

    const editForm = document.getElementById(`edit-form-${index}`);
    if (editForm) {
        editForm.style.display = 'block';
    }
}

// Function to cancel the edit and hide the form
function cancelEdit(index) {
    const editForm = document.getElementById(`edit-form-${index}`);
    if (editForm) {
        editForm.style.display = 'none';
    }
}
