document.addEventListener("DOMContentLoaded", function() {
    fetchRecentCard();

    function fetchRecentCard() {
        fetch("http://127.0.0.1:8000/recent-card-data")
        .then(response => response.json())
        .then(data => {
            const recentCardBox = document.querySelector(".recent-card");
            let cardName = recentCardBox.querySelector("h2");
            let cardDesc = recentCardBox.querySelector("p");
            let cardImg = recentCardBox.querySelector("img");

            cardName.textContent = data.name;
            cardDesc.textContent = data.description;
            cardImg.src = data.image;
        })
        //Updates every 100 seconds
        setInterval(fetchRecentCard, 100000);
    }

});
