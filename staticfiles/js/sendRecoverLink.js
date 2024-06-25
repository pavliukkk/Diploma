document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('.register_form');
    const emailInput = document.querySelector('input[name="email"]');
    const errorsDiv = document.querySelector('.errors');
    const noEmailError = document.getElementById('no_login');

    // Функція для перевірки, чи заповнене поле електронної пошти
    function emailFilled() {
        return emailInput.value.trim() !== '';
    }

    // Функція для перевірки всіх полів форми перед її відправкою
    function validateForm() {
        if (!emailFilled()) {
            errorsDiv.style.display = 'block'; // Показуємо повідомлення про помилку
            noEmailError.style.display = 'block'; // Показуємо повідомлення про необхідність введення email
            return false; // Блокуємо відправку форми
        }
        return true; // Дозволяємо відправку форми, якщо всі дані коректні
    }

    // Функція для автоматичного видалення пробілів на початку та в кінці тексту
    function trimWhitespace(event) {
        event.target.value = event.target.value.trim();
    }

    // Навішуємо обробник події input на поле email
    emailInput.addEventListener('input', trimWhitespace);

    // Навішуємо обробник події на відправку форми
    form.addEventListener('submit', function (event) {
        // Видаляємо пробіли з email перед перевіркою
        emailInput.value = emailInput.value.trim();

        if (!validateForm()) {
            event.preventDefault(); // Блокуємо стандартну відправку форми
        }
    });
});
