document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('.register_form');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    const errorsDiv = document.querySelector('.errors');
    const errorMessages = errorsDiv.querySelectorAll('.error-msg');

    // Функція для перевірки, чи співпадають паролі
    function passwordsMatch() {
        return passwordInput.value === confirmPasswordInput.value;
    }

    // Функція для перевірки довжини паролів
    function passwordsLengthValid() {
        const minLength = 8; // Мінімальна довжина пароля
        return passwordInput.value.length >= minLength && confirmPasswordInput.value.length >= minLength;
    }

    // Функція для перевірки наявності літер у паролі
    function passwordContainsLetter() {
        const letterRegex = /[a-zA-Z]/;
        return letterRegex.test(passwordInput.value);
    }

    // Функція для перевірки, чи всі поля заповнені
    function allFieldsFilled() {
        return passwordInput.value !== '' && confirmPasswordInput.value !== '';
    }

    // Функція для відображення повідомлень про помилки
    function showErrors() {
        errorMessages.forEach(function (errorMessage) {
            errorMessage.style.display = 'none'; // Початково ховаємо всі повідомлення про помилки
        });

        if (!allFieldsFilled()) {
            document.getElementById('fill_error').style.display = 'block';
        } else if (!passwordsMatch()) {
            document.getElementById('different_passwords').style.display = 'block';
        } else if (!passwordsLengthValid()) {
            document.getElementById('short_passwords').style.display = 'block';
        } else if (!passwordContainsLetter()) {
            document.getElementById('weak_password').style.display = 'block';
        } else {
            return true; // Повертаємо true, якщо всі дані коректні
        }
        return false; // Якщо є помилка, повертаємо false
    }

    // Функція для відправки форми
    function submitForm(event) {
        event.preventDefault(); // Блокуємо стандартну відправку форми
        if (showErrors()) {
            form.submit(); // Якщо дані коректні, відправляємо форму
        }
    }

    // Навішуємо обробники подій на форму
    form.addEventListener('submit', submitForm);
    passwordInput.addEventListener('input', showErrors);
    confirmPasswordInput.addEventListener('input', showErrors);
});