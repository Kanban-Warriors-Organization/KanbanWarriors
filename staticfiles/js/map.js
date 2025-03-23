document.addEventListener('DOMContentLoaded', function() {
    var map = L.map("map").setView([50.7371, -3.5251], 15);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    function updateCardMarkers() {
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
    }

    function updateUserMarker() {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                let userLat = position.coords.latitude;
                let userLng = position.coords.longitude;
                //Custom red marker for the user
                let customIcon = L.icon({
                    iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png`,
                    iconSize: [25, 41],
                    iconAnchor: [12, 41]
                });
                    L.marker([userLat, userLng], {icon: customIcon})
                    .addTo(map)
                    .bindPopup("<b>You are here</b>");
                    map.setView([userLat, userLng], 15);
            },
            function(error) {
                console.error("Error getting location:", error);
            }
        );
    }

    updateCardMarkers();
    updateUserMarker();
    setInterval(updateCardMarkers, 100000);
    setInterval(updateUserMarker, 100000);
});

