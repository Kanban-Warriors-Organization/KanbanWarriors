document.addEventListener("DOMContentLoaded", function() {
    const alertBox = document.getElementById('alert-box');
    const closeButton = document.querySelector('.close');

    closeButton.addEventListener('click', function() {
        alertBox.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target === alertBox) {
            alertBox.style.display = 'none';
        }
    });
});
