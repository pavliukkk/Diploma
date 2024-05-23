document.addEventListener("DOMContentLoaded", function() {
    const reservationForm = document.getElementById("reservationForm");
    const successModal = document.getElementById("successfull_reservation");
    const wrapper = document.getElementById("wrapper");

    // Функція для відкриття модального вікна
    function openModal() {
        successModal.style.display = "block";
        wrapper.classList.add("blur");
        activate_link_sent = false;
    }
    openModal();
    // Функція для закриття модального вікна та надсилання форми, якщо вони введені коректно
    function closeModal() {
        successModal.style.display = "none";
        wrapper.classList.remove("blur");

    }
    successModal.addEventListener("click", function(event) {
        if (event.target.classList.contains("close")) {
            closeModal();
        }
    });

    document.addEventListener("click", function(event) {
        if (!successModal.contains(event.target)) {
            closeModal();
        }
    });
});