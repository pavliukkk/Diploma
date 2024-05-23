document.addEventListener("DOMContentLoaded", function () {
    const successModal = document.getElementById('successfull_reservation');
    const reservationForm = document.querySelector('.reservation__form');
    const dateInput = reservationForm.querySelector('input[type="date"]');
    const timeInput = reservationForm.querySelector('input[type="time"]');
    const wrapper = document.getElementById('wrapper'); // Assuming an element with class 'wrapper' exists
    const currentPage = window.location.href;
    const errorMessages = document.querySelectorAll('.error-msg');
    
    let currentDate = new Date().toISOString().split('T')[0];
    let currentTime = new Date().toLocaleTimeString('en-US', { hour12: false }).slice(0, -3); // Видаляємо секунди з поточного часу
  
    // Set the minimum date and initial date value
    if (currentTime >= "19:30") {
        // If the current time is 19:30 or later, set the minimum date to the next day
        let tomorrow = new Date();
        tomorrow.setDate(new Date().getDate() + 1);
        currentDate = tomorrow.toISOString().split('T')[0];
    }
    dateInput.setAttribute('min', currentDate);
    dateInput.value = currentDate;
  
    // Function to set time to 19:30 if current time is after 19:30
    function setTimeTo1930() {
        if (timeInput.value > "19:30" && timeInput.value <= "20:00") {
            timeInput.value = "11:00";
        }
    }
  
    // Set the initial time value based on conditions
    if (currentTime < "11:00") {
        timeInput.value = "11:00";
    } else if (currentTime >= "19:30") {
        timeInput.value = "11:00";
    } else {
        timeInput.value = currentTime;
        setTimeTo1930(); // Check and set time to 19:30 if necessary
    }
  
    const phoneInput = reservationForm.querySelector('input[name="phone"]');
  
    phoneInput.addEventListener('input', function (e) {
        const regex = /[^\d]/g;
        phoneInput.value = phoneInput.value.replace(regex, '').substring(0, 10);
    });
  
    // Event listener for time input to handle automatic replacement
    timeInput.addEventListener('input', function (e) {
        const enteredTime = e.target.value.slice(0, -3);
  
        // Перетворення рядка у числове значення годин
        const enteredHour = parseInt(enteredTime.split(':')[0]);
  
        if (enteredHour < 11 || enteredHour >= 20) {
            timeInput.value = "11:00";
        }
        setTimeTo1930(); // Check and set time to 19:30 if necessary
    });
  
    function closeModal() {
        successModal.style.display = "none";
        wrapper.classList.remove("blur");
    }
  
    function closeOnOutsideClick(event) {
        if (event.target !== successModal && !successModal.contains(event.target)) {
            closeModal();
        }
    }
  
    document.querySelectorAll(".close").forEach(function (closeBtn) {
        closeBtn.addEventListener("click", closeModal);
    });
  
    window.addEventListener("click", closeOnOutsideClick);
  
    reservationForm.addEventListener('submit', function (event) {
  
        currentTime = new Date().toLocaleTimeString('en-US', { hour12: false });
        const firstName = reservationForm.querySelector('input[name="first_name"]').value;
        const lastName = reservationForm.querySelector('input[name="last_name"]').value;
        const email = reservationForm.querySelector('input[name="email"]').value;
        const phone = reservationForm.querySelector('input[name="phone"]').value;
        const date = dateInput.value;
        const time = timeInput.value;
  
        const errorMessage = document.getElementById("error");
        const saturdayError = document.getElementById("saturday_error");
  
        if (!firstName || !lastName || !email || !phone || !date || !time || !currentPage.includes('/contact/')) {
            errorMessage.style.display = "block";
            event.preventDefault();
        } else {
            // Hide error message
            errorMessage.style.display = "none";
  
            const selectedDate = new Date(date);
            const isSaturday = selectedDate.getDay() === 6;
  
            if (isSaturday) {
                saturdayError.style.display = "block";
                event.preventDefault();
            } else {
                saturdayError.style.display = "none";
            }
        }
    });
  });
  
  