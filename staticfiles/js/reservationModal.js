document.addEventListener("DOMContentLoaded", function() {
    const reservationForm = document.getElementById("reservationForm");
    const successModal = document.getElementById("successfull_reservation");
    const wrapper = document.getElementById("wrapper");

    
    // Функція для відкриття модального вікна
    function openModal() {
        successModal.style.display = "block";
        wrapper.classList.add("blur");
    }

    // Функція для закриття модального вікна та надсилання форми, якщо вони введені коректно
    function closeModalAndSubmitForm() {
        successModal.style.display = "none";
        wrapper.classList.remove("blur");
        success_reservation_modal = false;
        table_is_not_available = false;
    }

    openModal();

    reservationForm.addEventListener('submit', function(event) {

        const dateInput = document.querySelector('input[type="date"]');
        const timeInput = document.querySelector('input[type="time"]');
        const selectBothError = document.getElementById("select_both");
        const selectDateError = document.getElementById("select_date");
        const selectTimeError = document.getElementById("select_time");

        // Сховати всі повідомлення про помилки перед перевіркою
        selectBothError.style.display = "none";
        selectDateError.style.display = "none";
        selectTimeError.style.display = "none";

        // Перевірити, чи обидва поля заповнені
        if (!dateInput.value || !timeInput.value) {
            // Вивести повідомлення про помилку
            if (!dateInput.value && !timeInput.value) {
                selectBothError.style.display = "block";
            } else if (!dateInput.value) {
                selectDateError.style.display = "block";
            } else {
                selectTimeError.style.display = "block";
            }
        } else {
            // Якщо поля заповнені, відкрити модальне вікно
            openModal();
        }
    });

    successModal.addEventListener("click", function(event) {
        if (event.target.classList.contains("close")) {
            closeModalAndSubmitForm();
        }
    });

    document.addEventListener("click", function(event) {
        if (!successModal.contains(event.target)) {
            closeModalAndSubmitForm();
        }
    });
});
