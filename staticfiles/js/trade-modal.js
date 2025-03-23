const cardsLocked = document.querySelectorAll('.card-locked');
const tradeModal = document.getElementById('trade');
const tradeButton = document.querySelector('.trade-btn');
const tradeClose = document.querySelector('.trade-close');

cardsLocked.forEach(card => {
    card.addEventListener('click', function() {
        tradeModal.style.display = 'flex';
        selectedCard = card.getAttribute('data-title');
        console.log(selectedCard);
    });
});

tradeButton.addEventListener('click', function() {
    window.location.href = `http://127.0.0.1:8000/trades/create/${selectedCard}`;
});

window.addEventListener('click', function(event) {
if (event.target === tradeModal) {
    tradeModal.style.display = 'none';
    }
});

tradeClose.addEventListener('click', function() {
    tradeModal.style.display = 'none';
});
