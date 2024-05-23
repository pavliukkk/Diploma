if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        // Відправка даних на сервер Django
        fetch('/save_location/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCSRFToken() // Отримання CSRF токену для Django
            },
            body: `latitude=${latitude}&longitude=${longitude}`
        })
            .then(response => response.json())
            .then(data => {
                console.log(data.message); // Виведення повідомлення про успішне збереження
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
} else {
    console.log('Geolocation is not supported by this browser.');
}
