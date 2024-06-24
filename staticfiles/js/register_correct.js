document.addEventListener("DOMContentLoaded", function() {
    const passwordField = document.querySelector('input[name="password"]');
    const confirmPasswordField = document.querySelector('input[name="confirm_password"]');
    const differentPasswordsError = document.getElementById('different_passwords');
    const shortPasswordsError = document.getElementById('short_passwords');
    const weakPasswordError = document.getElementById('weak_password');
    const fillError = document.getElementById('fill_error');
    const signUpForm = document.querySelector('.register_form');
    const phoneNumberField = document.querySelector('input[name="phone_number"]');
    const phoneNumberError = document.getElementById('phone_number_error');
    const surnameField = document.querySelector('input[name="surname"]');
    const nameField = document.querySelector('input[name="name"]');
    
    differentPasswordsError.style.display = 'none';
    shortPasswordsError.style.display = 'none';
    weakPasswordError.style.display = 'none';
    fillError.style.display = 'none';
    phoneNumberError.style.display = 'none';

    surnameField.addEventListener('input', function(event) {
        // Використовуємо регулярний вираз для перевірки наявності символів, які не є буквами
        if (/[^a-zA-Zа-яА-ЯіїєґІЇЄҐ]/.test(event.target.value)) {
            // Якщо введено не букву, встановлюємо значення поля на попередній текст
            event.target.value = event.target.value.replace(/[^a-zA-Zа-яА-ЯіїєґІЇЄҐ]/g, '');
        }
    });
    
    nameField.addEventListener('input', function(event) {
        // Використовуємо регулярний вираз для перевірки наявності символів, які не є буквами
        if (/[^a-zA-Zа-яА-ЯіїєґІЇЄҐ]/.test(event.target.value)) {
            // Якщо введено не букву, встановлюємо значення поля на попередній текст
            event.target.value = event.target.value.replace(/[^a-zA-Zа-яА-ЯіїєґІЇЄҐ]/g, '');
        }
    });

    function validatePassword() {
        const password = passwordField.value;
        const confirmPassword = confirmPasswordField.value;
        const containsLetter = /[a-zA-Z]/.test(password);

        if (!containsLetter) {
            weakPasswordError.style.display = 'block';
        } else {
            weakPasswordError.style.display = 'none';
        }

        if (password.length < 8) {
            shortPasswordsError.style.display = 'block';
        } else {
            shortPasswordsError.style.display = 'none';
        }

        if (password !== confirmPassword) {
            differentPasswordsError.style.display = 'block';
        } else {
            differentPasswordsError.style.display = 'none';
        }
    }

    function validatePhoneNumber() {
        const phoneNumber = phoneNumberField.value;
        const containsMaskChar = phoneNumber.indexOf('_') !== -1;

        if (containsMaskChar) {
            phoneNumberError.style.display = 'none';
        } else {
            phoneNumberError.style.display = 'none';
        }

        return !containsMaskChar;
    }

    passwordField.addEventListener('input', function() {
        validatePassword();
    });

    confirmPasswordField.addEventListener('input', function() {
        validatePassword();
    });

    signUpForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const phoneNumberValid = validatePhoneNumber();
        const password = passwordField.value;
        const confirmPassword = confirmPasswordField.value;
        const surname = document.querySelector('input[name="surname"]').value;
        const name = document.querySelector('input[name="name"]').value;
        const email = document.querySelector('input[name="email"]').value;

        if (!surname || !name || !email || !password || !confirmPassword || !phoneNumberValid) {
            fillError.style.display = 'block';
        } else {
            fillError.style.display = 'none';

            validatePassword();

            if (differentPasswordsError.style.display === 'none' &&
                shortPasswordsError.style.display === 'none' &&
                weakPasswordError.style.display === 'none') {
                this.submit();
            }
        }
    });
});
