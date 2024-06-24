document.addEventListener("DOMContentLoaded", function () {
    const successModal = document.getElementById('successfull_reservation');
    const reservationForm = document.querySelector('.reservation__form');
    const dateInput = reservationForm.querySelector('input[type="date"]');
    const timeInput = reservationForm.querySelector('input[type="time"]');
    const nameField = reservationForm.querySelector('input[name="first_name"]');
    const surnameField = reservationForm.querySelector('input[name="last_name"]');
    const phoneNumberField = reservationForm.querySelector('input[name="phone_number"]');
    const wrapper = document.getElementById('wrapper');
    const currentPage = window.location.href;
    const errorMessages = document.querySelectorAll('.error-msg');
    const saturdayError = document.getElementById("saturday_error");

    let currentDate = new Date().toISOString().split('T')[0];
    const currentDateToday = new Date().toISOString().split('T')[0];
    let currentTime = new Date().toLocaleTimeString('en-US', { hour12: false }).slice(0, -3);

    surnameField.addEventListener('input', function(event) {
        if (/[^a-zA-Zа-яА-ЯіїєґІЇЄҐ]/.test(event.target.value)) {
            event.target.value = event.target.value.replace(/[^a-zA-Zа-яА-ЯіїєґІЇЄҐ]/g, '');
        }
    });

    nameField.addEventListener('input', function(event) {
        if (/[^a-zA-Zа-яА-ЯіїєґІЇЄҐ]/.test(event.target.value)) {
            event.target.value = event.target.value.replace(/[^a-zA-Zа-яА-ЯіїєґІЇЄҐ]/g, '');
        }
    });

    // Set the minimum date and initial date value
    if (currentTime >= "19:30") {
        let tomorrow = new Date();
        tomorrow.setDate(new Date().getDate() + 1);
        currentDate = tomorrow.toISOString().split('T')[0];
    }
    dateInput.setAttribute('min', currentDate);
    dateInput.value = currentDate;

    // Function to set time to 11:00 if necessary
    function setTimeToValidRange() {
        if (dateInput.value === currentDate) {
            if (timeInput.value > "19:30") {
                timeInput.value = "19:30";
            } else if (timeInput.value < "11:00" && dateInput.value > currentDateToday) {
                timeInput.value = "11:00";
            }  
            else if(timeInput.value < currentTime && dateInput.value === currentDateToday) {
                timeInput.value = currentTime;
            }   
        } else {
            if (timeInput.value < "11:00") {
                timeInput.value = "11:00";
            } else if (timeInput.value > "19:30") {
                timeInput.value = "19:30";
            }
        }
    }

    // Set the initial time value based on conditions
    if (currentTime >= "19:30") {
        timeInput.setAttribute('min', "11:00");
        timeInput.value = "11:00";
    } else {
        timeInput.setAttribute('min', currentTime);
        timeInput.value = currentTime < "11:00" ? "11:00" : currentTime;
        setTimeToValidRange(); // Check and set time to valid range if necessary
    }

    const phoneInput = reservationForm.querySelector('input[name="phone"]');

    phoneInput.addEventListener('input', function (e) {
        const regex = /[^\d]/g;
        phoneInput.value = phoneInput.value.replace(regex, '').substring(0, 12);
    });

    timeInput.addEventListener('input', function (e) {
        setTimeToValidRange();
    });

    dateInput.addEventListener('change', function (event) {
        let selectedDate = new Date(dateInput.value);
        let isSaturday = selectedDate.getDay() === 6;

        if (isSaturday) {
            saturdayError.style.display = 'block';
        } else {
            saturdayError.style.display = 'none';
        }

        if (dateInput.value === currentDate) {
            timeInput.setAttribute('min', currentTime);
        } else {
            timeInput.setAttribute('min', "11:00");
            timeInput.value = "11:00";
        }
        setTimeToValidRange();
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

    function validatePhoneNumber() {
        const phoneNumber = phoneNumberField.value;
        const containsMaskChar = phoneNumber.indexOf('_') !== -1;

        if (containsMaskChar) {
            phoneNumberError.style.display = 'none';
        } else {
            phoneNumberError.style.display = 'none';
        }

        return !containsMaskChar;
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
        const phone = validatePhoneNumber();
        const date = dateInput.value;
        const time = timeInput.value;

        const errorMessage = document.getElementById("error");

        if (!firstName || !lastName || !email || !phone || !date || !time || !currentPage.includes('/contact/')) {
            errorMessage.style.display = "block";
            event.preventDefault();
        } else {
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
