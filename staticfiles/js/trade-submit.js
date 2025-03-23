document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('trade-form');
    const requested_card = document.getElementById('data').getAttribute('data-requested');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        const data = {};

        formData.forEach((value, key) => {
            data[key] = value;
        });

        data['requested_card'] = requested_card;
        console.log(data)
        const jsonData = JSON.stringify(data);
        fetch("http://127.0.0.1:8000/trades/submit", {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
            },
            body: jsonData
        }).then(response => {
            console.log(response);
            window.location.href = "http://127.0.0.1:8000/trades/personal"
        });

    });
});
