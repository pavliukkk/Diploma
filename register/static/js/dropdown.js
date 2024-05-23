// Знаходимо елементи .reservation__form-input-text та <ul> за їх класами або ідентифікаторами
const inputText = document.querySelector('.reservation__form-input-text');
const dropdownOptions = document.querySelector('.dropdown-options');
const formInput = document.querySelector('input[name="people"]');
const dropdownItems = document.querySelectorAll('.dropdown-options__item');

// Перевіряємо, чи знайдені обидва елементи та поле вводу форми
if (inputText && dropdownOptions && formInput && dropdownItems.length > 0) {
  // Додаємо обробник подій для кліку на .reservation__form-input-text
  inputText.addEventListener('click', function(event) {
    // Запобігаємо спливанню події до документу
    event.stopPropagation();
    
    // Додаємо або видаляємо стиль visually-hidden в <ul> при кліку на .reservation__form-input-text
    if (dropdownOptions.classList.contains('visually-hidden')) {
      dropdownOptions.classList.remove('visually-hidden');
    } else {
      dropdownOptions.classList.add('visually-hidden');
    }
  });

  // Додаємо обробник подій для кожного <li>
  dropdownItems.forEach(function(item) {
    item.addEventListener('click', function() {
      // Видаляємо клас dropdown-options__item--active у всіх <li>
      dropdownItems.forEach(function(otherItem) {
        otherItem.classList.remove('dropdown-options__item--active');
      });

      // Додаємо клас dropdown-options__item--active до обраного <li>
      item.classList.add('dropdown-options__item--active');

      // Отримуємо текстовий контент <li>, який представляє вибране значення
      const selectedValue = item.textContent;

      // Додаємо стиль visually-hidden в <ul> при виборі значення і оновлюємо значення поля вводу форми
      dropdownOptions.classList.add('visually-hidden');
      formInput.value = selectedValue;
    });
  });

  // Додаємо обробник подій для документу для закриття dropdown-options при кліку поза ним
  document.addEventListener('click', function(event) {
    // Перевіряємо, чи клік був не в dropdown-options та чи він не був в .reservation__form-input-text
    if (!dropdownOptions.contains(event.target) && event.target !== inputText) {
      dropdownOptions.classList.add('visually-hidden');
    }
  });
}
