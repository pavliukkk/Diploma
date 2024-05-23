document.addEventListener('DOMContentLoaded', function() {
    const deleteReservationModal = document.getElementById('delete_reservation');
    const wrapper = document.getElementById("wrapper");
    const openModalBtns = document.querySelectorAll('.reservation__profile-delete-button');
    const closeModalBtn = document.querySelector('.close');
    const cancelBtn = document.querySelector('.cancel__delete_reservation');

    // Відкриття модального вікна
    function openModal() {
        deleteReservationModal.style.display = 'block';
        wrapper.classList.add("blur");
    }

    // Закриття модального вікна
    function closeModal() {
        deleteReservationModal.style.display = 'none';
        wrapper.classList.remove("blur");
    }

    // Обробник кліку на кнопках, щоб відкрити модальне вікно
    openModalBtns.forEach(function(btn) {
        btn.addEventListener('click', openModal);
    });

    // Закриття модального вікна при кліку на "хрестик"
    closeModalBtn.addEventListener('click', closeModal);

    // Закриття модального вікна при кліку на "Cancel"
    cancelBtn.addEventListener('click', closeModal);

    // Закриття модального вікна при кліку поза ним, за винятком самого модального вікна та його дітей
    document.addEventListener('mousedown', function(event) {
        if (!deleteReservationModal.contains(event.target) && event.target !== deleteReservationModal) {
            closeModal();
        }
    });
});
