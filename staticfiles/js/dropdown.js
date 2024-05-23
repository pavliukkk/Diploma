const dropdowns = document.querySelectorAll('.dropdown');

dropdowns.forEach(dropdown => {
  const inputText = dropdown.querySelector('.reservation__form-input-text');
  const dropdownOptions = dropdown.querySelector('.dropdown-options');
  const formInput = dropdown.querySelector('.reservation__form-input-text');
  const dropdownItems = dropdown.querySelectorAll('.dropdown-options__item');

  if (inputText && dropdownOptions && formInput && dropdownItems.length > 0) {
    inputText.addEventListener('click', function (event) {
      event.stopPropagation();

      if (dropdownOptions.classList.contains('visually-hidden')) {
        dropdownOptions.classList.remove('visually-hidden');
      } else {
        dropdownOptions.classList.add('visually-hidden');
      }
    });

    dropdownItems.forEach(function (item) {
      item.addEventListener('click', function () {
        dropdownItems.forEach(function (otherItem) {
          otherItem.classList.remove('dropdown-options__item--active');
        });

        item.classList.add('dropdown-options__item--active');

        const selectedValue = item.textContent;

        dropdownOptions.classList.add('visually-hidden');
        formInput.value = selectedValue;
      });
    });

    document.addEventListener('click', function (event) {
      if (!dropdownOptions.contains(event.target) && event.target !== inputText) {
        dropdownOptions.classList.add('visually-hidden');
      }
    });
  }
});
