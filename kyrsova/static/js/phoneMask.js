document.addEventListener("DOMContentLoaded", function() {
    var element = document.getElementById('phone_number');
    var maskOptions = {
        mask: '+380 (99) 999-99-99',
        lazy: false
    };
    var mask = new IMask(element, maskOptions);

    // Додамо обробник події input для поля введення номеру телефону
    element.addEventListener('input', function() {
        var phoneNumber = element.value;

        // Перевіряємо, чи введений номер відповідає масці
        var isMaskFilled = phoneNumber.indexOf('_') === -1;

        // Отримуємо елемент, де відображається помилка-підказка
        var errorElement = document.getElementById('phone_number_error');

        // Якщо номер відповідає масці, ховаємо помилку-підказку
        if (isMaskFilled) {
            errorElement.style.display = 'none';
        } else {
            // Якщо номер не відповідає масці, показуємо помилку-підказку
            errorElement.style.display = 'block';
        }
    });

    // Отримуємо форму
    var signUpForm = document.querySelector('.register_form');

    // Додамо обробник події submit для форми
    signUpForm.addEventListener('submit', function(event) {
        // Отримуємо значення номеру телефону
        var phoneNumber = element.value;

        // Перевіряємо, чи поле номеру телефону не пусте
        if (!phoneNumber.trim()) {
            // Якщо поле номеру телефону пусте, забороняємо відправку форми
            event.preventDefault();

            // Отримуємо елемент, де відображається помилка-підказка
            var errorElement = document.getElementById('phone_number_error');

            // Показуємо помилку-підказку
            errorElement.style.display = 'block';
        }
    });
});
