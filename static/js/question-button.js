document.addEventListener('DOMContentLoaded', function() {
    const ansDiv = document.getElementById('ans');
    const modal = document.getElementById('modal');
    const modalTitle = document.getElementById('modal-title');
    const modalDescription = document.getElementById('modal-description');
    const closeButton = document.querySelector('.close');
    const corrAns = ansDiv.getAttribute('data-ans');
    document.querySelectorAll(".btn").forEach(button => {
        button.addEventListener("click", function() {
            const ans = button.getAttribute('data-ans');
            const id = document.getElementById('challenge-location').getAttribute('data-id');
            if(ans == corrAns) {
               const cardTitle = document.getElementById('challenge-location').getAttribute('data-name');
               fetch(`http://127.0.0.1:8000/add-card/${id}`);
               modalTitle.textContent = "You've Earned a New Card!";
               modalDescription.textContent = cardTitle;
               modal.style.display = 'flex';
            } else {
                modalTitle.textContent = "Ah! Better Luck Next Time!";
                modal.style.display = 'flex';
            }
        });
    });
    closeButton.addEventListener('click', function() {
        window.location.href = "/challenges/";
    });
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
           window.location.href = "/challenges/";
        }
    });
});




