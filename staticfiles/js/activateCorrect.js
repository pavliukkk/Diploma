document.getElementById('loginForm').addEventListener('submit', function(event) {
    const emailField = document.getElementById('emailField');
    const errorMessage = document.getElementById('no_login');

    if (!emailField.value.trim()) {
        event.preventDefault(); // Блокує надсилання форми
        errorMessage.style.display = 'block'; // Показує повідомлення про помилку
    } else {
        errorMessage.style.display = 'none'; // Приховує повідомлення про помилку
    }
});