document.addEventListener('DOMContentLoaded', () => {
    let currentPage = 1;
    const totalPages = 4;

    const homeButton = document.getElementById('homeButton');
    const backButton = document.getElementById('backButton');
    const nextButton = document.getElementById('nextButton');
    const pages = document.querySelectorAll('.page');

    // Function to show the current page
    function showPage(pageNumber) {
        pages.forEach((page) => {
            page.classList.remove('active');
        });
        document.getElementById(`page${pageNumber}`).classList.add('active');
        backButton.style.display = (pageNumber === 1) ? 'none' : 'inline-block';
        nextButton.style.display = (pageNumber === totalPages) ? 'none' : 'inline-block';
    }

    homeButton.addEventListener('click', () => {
        currentPage = 1;
        showPage(currentPage);
    });

    backButton.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            showPage(currentPage);
        }
    });

    nextButton.addEventListener('click', () => {
        if (currentPage < totalPages) {
            currentPage++;
            showPage(currentPage);
        }
    });

    showPage(currentPage);
});

function showAlert(message, type) {
    const alertBox = document.getElementById('alert-message');
    alertBox.textContent = message;
    alertBox.className = `alert ${type}`; // Example: 'success', 'error'
    alertBox.style.display = 'block';

    // Automatically hide the alert after 5 seconds
    setTimeout(() => {
        alertBox.style.display = 'none';
    }, 5000);
}

function validatePassword() {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;

    if (password !== confirmPassword) {
        showAlert("Passwords do not match!", "error");
        return false; // Prevent form submission
    }
    return true; // Allow form submission
}

// Add this function to check passwords on input and clear the error message if they match
function checkPasswordsMatch() {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;

    if (password === confirmPassword) {
        clearErrorMessage();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const birthdateInput = document.getElementById('birthdate');

    birthdateInput.addEventListener('input', () => {
        const value = birthdateInput.value.replace(/\D/g, ''); // Remove non-digit characters
        let formattedValue = value;

        if (value.length > 4) {
            formattedValue = `${value.slice(0, 2)}/${value.slice(2, 4)}/${value.slice(4, 8)}`;
        } else if (value.length > 2) {
            formattedValue = `${value.slice(0, 2)}/${value.slice(2, 4)}`;
        } else if (value.length > 0) {
            formattedValue = `${value.slice(0, 2)}`;
        }

        birthdateInput.value = formattedValue;
    });

    // Add event listeners to password fields to check if they match on input
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');

    passwordInput.addEventListener('input', checkPasswordsMatch);
    confirmPasswordInput.addEventListener('input', checkPasswordsMatch);
});

function clearErrorMessage() {
    const alertBox = document.getElementById('alert-message');
    if (alertBox) {
        alertBox.style.display = 'none';
    }

    const alertMessages = document.getElementById('alert-messages');
    if (alertMessages) {
        alertMessages.style.display = 'none';
    }
}
