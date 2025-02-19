const cards = document.querySelectorAll('.card');
const modal = document.getElementById('modal');
const modalTitle = document.getElementById('modal-title');
const modalDescription = document.getElementById('modal-description');
const closeButton = document.querySelector('.close');

cards.forEach(card => {
    card.addEventListener('click', function() {
        const cardTitle = card.getAttribute('data-title');
        const cardDescription = card.getAttribute('data-description')

        modalTitle.textContent = cardTitle;
        modalDescription.textContent = cardDescription;

        modal.style.display = 'flex';
    });
});

closeButton.addEventListener('click', function() {
    modal.style.display = 'none';
});

window.addEventListener('click', function(event) {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});
