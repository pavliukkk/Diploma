document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('profileEditForm');
    const surnameInput = form.querySelector('input[name="surname"]');
    const nameInput = form.querySelector('input[name="name"]');
    const phoneNumberInput = form.querySelector('input[name="phone_number"]');
    const fillError = document.getElementById('fill_error');
    const phoneNumberError = document.getElementById('phone_number_error');

    // Функція для перевірки, чи всі поля заповнені
    function validateForm() {
        let isValid = true;

        if (!surnameInput.value.trim() || !nameInput.value.trim() || !phoneNumberInput.value.trim()) {
            fillError.style.display = 'block';
            isValid = false;
        } else {
            fillError.style.display = 'none';
        }

        // Перевірка на наявність символу "_" в полі phone_number
        if (phoneNumberInput.value.includes('_')) {
            phoneNumberError.style.display = 'block';
            isValid = false;
        } else {
            phoneNumberError.style.display = 'none';
        }

        return isValid;
    }

    // Блокування відправки форми при незаповнених полях або помилках
    form.addEventListener('submit', function(event) {
        // Обрізаємо пробіли з полів перед валідацією
        surnameInput.value = surnameInput.value.trim();
        nameInput.value = nameInput.value.trim();
        phoneNumberInput.value = phoneNumberInput.value.trim();

        if (!validateForm()) {
            event.preventDefault();
        }
    });

    // Функція для перевірки введення тільки букв у полях surname та name
    function allowOnlyLetters(input) {
        let regex = /^[a-zA-Zа-яА-ЯіІїЇєЄґҐ' ]*$/;
        if (!regex.test(input.value)) {
            input.value = input.value.replace(/[^a-zA-Zа-яА-ЯіІїЇєЄґҐ' ]/g, '');
        }
    }

    surnameInput.addEventListener('input', function() {
        allowOnlyLetters(this);
    });

    nameInput.addEventListener('input', function() {
        allowOnlyLetters(this);
    });

    // Перевірка на наявність символу "_" в полі phone_number при введенні
    phoneNumberInput.addEventListener('input', function() {
        if (this.value.includes('_')) {
            phoneNumberError.style.display = 'block';
        } else {
            phoneNumberError.style.display = 'none';
        }
    });

    // Автоматичне видалення пробілів на початку і в кінці при введенні в поля surname та name
    form.querySelectorAll('input').forEach(input => {
        input.addEventListener('input', function() {
            this.value = this.value.trim();
        });
    });

    // Автоматичне видалення пробілів на початку і в кінці при введенні в поле phone_number
    phoneNumberInput.addEventListener('input', function() {
        this.value = this.value.trim();
    });
});
