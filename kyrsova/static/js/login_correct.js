document.addEventListener('DOMContentLoaded', function () {
    const forms = document.querySelectorAll('.form-register__container form');

    forms.forEach(form => {
        const emailInput = form.querySelector('input[name="email"]');
        const passwordInput = form.querySelector('input[name="password"]');
        const errorMessages = form.querySelectorAll('.error-msg');

        // Helper function to trim whitespace from input fields
        function trimWhitespace(event) {
            event.target.value = event.target.value.trim();
        }

        // Attach the trim function to relevant input fields
        emailInput.addEventListener('input', trimWhitespace);

        form.addEventListener('submit', function (event) {
            // Trim whitespace from fields before validation
            emailInput.value = emailInput.value.trim();
            passwordInput.value = passwordInput.value.trim();

            let valid = true;

            if (!emailInput.value) {
                valid = false;
                errorMessages[0].style.display = 'block';
            } else {
                errorMessages[0].style.display = 'none';
            }

            if (!passwordInput.value) {
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
