/**
 * Student Management System - Main JavaScript (UI helpers only)
 * -------------------------------------------------------------
 * IMPORTANT:
 * - Login, registration, authentication and authorization are
 *   handled entirely by the Django backend.
 * - This file contains ONLY small UI helpers such as image/file
 *   previews. No auth logic, no redirects, no AJAX.
 */

// ========= Profile Image Preview =========

/**
 * Displays a preview of the selected profile image
 * @param {HTMLInputElement} input - The file input element
 */
function previewProfileImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();

        reader.onload = function (e) {
            // Hide default image and show preview
            const defaultImage = document.getElementById('defaultProfileImage');
            const previewImage = document.getElementById('profileImagePreview');

            if (defaultImage) {
                defaultImage.style.display = 'none';
            }

            if (previewImage) {
                previewImage.src = e.target.result;
                previewImage.style.display = 'block';
            }
        };

        reader.readAsDataURL(input.files[0]);
    }
}

// ========= Document Preview (Upload page) =========

/**
 * Preview selected document file (name and size only).
 * @param {HTMLInputElement} input - file input element
 * @param {string} listId - id of the container where preview should be rendered
 *
 * NOTE: Actual upload and validation are handled by Django backend.
 */
function previewDocument(input, listId) {
    const list = document.getElementById(listId);
    if (!list) return;

    list.innerHTML = '';

    if (input.files && input.files[0]) {
        const file = input.files[0];
        const item = document.createElement('div');
        item.className = 'file-item';
        item.innerHTML =
            '<div class="file-item-info">' +
            '<i class="bi bi-file-earmark-pdf file-icon"></i>' +
            '<div>' +
            '<strong>' + file.name + '</strong>' +
            '<p class="text-muted mb-0">' + (file.size / 1024 / 1024).toFixed(2) + ' MB</p>' +
            '</div>' +
            '</div>';
        list.appendChild(item);
    }
}

// ========= Initialization =========

// Attach image preview handlers on page load
document.addEventListener('DOMContentLoaded', function () {
    // Attach event listener to profile image upload inputs
    const profileUploadInputs = document.querySelectorAll('.profile-upload-input');

    profileUploadInputs.forEach(function (input) {
        input.addEventListener('change', function () {
            previewProfileImage(this);
        });
    });

    // Handle click on profile upload button (opens hidden file input)
    const profileUploadButtons = document.querySelectorAll('.profile-upload-btn');

    profileUploadButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            const input = this.parentElement.querySelector('.profile-upload-input');
            if (input) {
                input.click();
            }
        });
    });
});
