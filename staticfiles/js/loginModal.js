document.addEventListener("DOMContentLoaded", function() {
    const loginModal = document.getElementById("login");
    const wrapper = document.getElementById("wrapper");

    // Затримка відображення модального вікна через 2 секунди
    setTimeout(function() {
        loginModal.style.display = "block";
        wrapper.classList.add("blur");
    }, 2000);

    function closeModal() {
        loginModal.style.display = "none";
        wrapper.classList.remove("blur");
    }

    function closeOnOutsideClick(event) {
        if (event.target !== loginModal && !loginModal.contains(event.target)) {
            closeModal();
        }
    }

    document.querySelectorAll(".close").forEach(function(closeBtn) {
        closeBtn.addEventListener("click", closeModal);
    });

    window.addEventListener("click", closeOnOutsideClick);
});
