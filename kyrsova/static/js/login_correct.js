document.addEventListener('DOMContentLoaded', function () {
    const forms = document.querySelectorAll('.form-register__container form');

    forms.forEach(form => {
        const emailInput = form.querySelector('input[name="email"]');
        const passwordInput = form.querySelector('input[name="password"]');
        const errorMessages = form.querySelectorAll('.error-msg');

        form.addEventListener('submit', function (event) {
            let valid = true;

            if (!emailInput.value.trim()) {
                valid = false;
                errorMessages[0].style.display = 'block';
            } else {
                errorMessages[0].style.display = 'none';
            }

            if (!passwordInput.value.trim()) {
                valid = false;
                errorMessages[1].style.display = 'block';
            } else {
                errorMessages[1].style.display = 'none';
            }

            if (!valid) {
                event.preventDefault();
            }
        });
    });
});
