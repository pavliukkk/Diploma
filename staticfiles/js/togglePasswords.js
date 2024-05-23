function togglePasswordVisibility(inputId, imageId) {
  var passwordInput = document.getElementById(inputId);
  var passwordImage = document.getElementById(imageId);
  
  var type = passwordInput.type === 'password' ? 'text' : 'password';
  passwordInput.type = type;

  // Отримати поточний src зображення
  var currentSrc = passwordImage.src;

  // Отримати шлях до папки
  var folderPath = currentSrc.substring(0, currentSrc.lastIndexOf('/') + 1);

  // Отримати назву файлу
  var fileName = currentSrc.substring(currentSrc.lastIndexOf('/') + 1);

  // Визначити нову іконку залежно від типу пароля
  var newIcon = type === 'password' ? 'show_password.png' : 'hide_password.png';

  // Створити новий шлях до зображення
  var newSrc = folderPath + newIcon;

  // Змінити src зображення
  passwordImage.src = newSrc;
}
