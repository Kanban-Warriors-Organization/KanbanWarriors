document.addEventListener("DOMContentLoaded", function() {
    fetchLeaderboard();

    function fetchLeaderboard() {
        fetch("http://127.0.0.1:8000/leaderboard-data/")
        .then(response => response.json())
        .then(data => {
            const leaderboardSlots = document.querySelectorAll(".leaderboard-links > div");

            data.forEach((player, index) => {
                if (leaderboardSlots[index]) {
                    let playerName = leaderboardSlots[index].querySelector("a");
                    let playerScore = leaderboardSlots[index].querySelector("p");

                    playerName.textContent = player.username;
                    playerScore.textContent = player.points;
                }
            });
        })
        .catch(error => console.error("Error loading leaderboard:", error));
    }
    setInterval(fetchLeaderboard, 100000);
});
