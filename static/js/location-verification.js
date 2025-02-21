document.addEventListener("DOMContentLoaded", function() {
    let challengeLoc = document.getElementById('challenge-location')
    let challengeLat = parseFloat(challengeLoc.getAttribute("data-lat"));  // Challenge latitude
    let challengeLng = parseFloat(challengeLoc.getAttribute("data-lng"));  // Challenge longitude
    console.log("Challenge Lat" + challengeLat);
    console.log("Challenge Long" + challengeLng);

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                let userLat = position.coords.latitude;
                let userLng = position.coords.longitude;
                console.log("User Lat" + userLat);
                console.log("User Long" + userLng);

                // Compare distances
                let distance = getDistance(userLat, userLng, challengeLat, challengeLng);
                let resultText = (distance < 0.1) ?
                    "✅ You are close to the challenge location!" :
                    "❌ You are too far from the challenge location.";

                document.getElementById("result").innerText = resultText;
            },
            function(error) {
                console.error("Error getting location:", error.message);
            },
            {
                enableHighAccuracy: true,  // Request high accuracy
                timeout: 5000,             // Timeout after 5 seconds
                maximumAge: 0              // Don't use cached position
            }
        );
    } else {
        console.error("Geolocation is not supported by this browser.");
    }

    // Haversine formula to calculate distance between two coordinates in km
    function getDistance(lat1, lon1, lat2, lon2) {
        const R = 6371; // Radius of Earth in km
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLon = (lon2 - lon1) * Math.PI / 180;
        const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                  Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                  Math.sin(dLon / 2) * Math.sin(dLon / 2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c; // Distance in km
    }
});
