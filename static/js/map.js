var map = L.map("map").setView([50.7371, -3.5251], 15);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

fetch("http://127.0.0.1:8000/locations-data/")
    .then(response => response.json())
    .then(data => {
        data.locations.forEach(location => {
            L.marker([location.latitude, location.longitude])
                .addTo(map)
                .bindPopup(`<b>${location.name}</b>`);
        });
    })
    .catch(error => console.error('Error loading locations:', error));
