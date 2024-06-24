document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const errorMessages = document.querySelectorAll('.error-msg');
    const dateInput = form.querySelector('input[type="date"]');
    const timeInput = form.querySelector('input[type="time"]');
    const saturdayError = document.getElementById('saturday_error');
    
    let currentDate = new Date().toISOString().split('T')[0];
    const currentDateToday = new Date().toISOString().split('T')[0];
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

    if (currentTime >= "19:30") {
        timeInput.setAttribute('min', "11:00");
        timeInput.value = "11:00";
    } else {
        timeInput.setAttribute('min', currentTime);
        timeInput.value = currentTime < "11:00" ? "11:00" : currentTime;
        setTimeToValidRange(); // Check and set time to valid range if necessary
    }

    // Event listener for date input to check if Saturday is selected
    dateInput.addEventListener('change', function (event) {
        let selectedDate = new Date(dateInput.value);
        let isSaturday = selectedDate.getDay() === 6; // 6 represents Saturday

        if (isSaturday) {
            // If Saturday is selected, show the error message
            saturdayError.style.display = 'block';
        } else {
            // If not Saturday, hide the error message
            saturdayError.style.display = 'none';
        }

        // Reset the time input based on the selected date
        if (dateInput.value === currentDate) {
            timeInput.setAttribute('min', currentTime);
            setTimeToValidRange();
        } else {
            timeInput.setAttribute('min', "11:00");
            timeInput.value = "11:00";
        }
    });

    // Event listener for time input to enforce valid range
    timeInput.addEventListener('change', function (event) {
        setTimeToValidRange();
    });

    // Event listener for form submission attempt
    form.addEventListener('submit', function (event) {
        let dateSelected = !!dateInput.value;
        let timeSelected = !!timeInput.value;
        let selectedDate = new Date(dateInput.value);
        
        // Check if Saturday is selected
        let isSaturday = selectedDate.getDay() === 6; // 6 represents Saturday

        // If there's an error, prevent form submission
        if (!dateSelected || !timeSelected || isSaturday) {
            event.preventDefault();
            // Show error messages for date and time
            if (!dateSelected) {
                errorMessages[0].style.display = 'block';
            } else {
                errorMessages[0].style.display = 'none';
            }
            if (!timeSelected) {
                errorMessages[1].style.display = 'block';
            } else {
                errorMessages[1].style.display = 'none';
            }
            // Show error message for Saturday if selected
            if (isSaturday) {
                saturdayError.style.display = 'block';
            } else {
                saturdayError.style.display = 'none';
            }
        }
    });
});
