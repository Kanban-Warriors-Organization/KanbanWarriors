let socket;
let selectedCards = [];
let gameState = "waiting";
let isMyTurn = false;
let currentRound = 1;
let isPlayer1 = true;

// Connect to WebSocket
function connect() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    socket = new WebSocket(`${protocol}//${host}/ws/battle/${roomId}/`);
    
    socket.addEventListener('open', () => logMessage('Connected to battle server!'));
    socket.addEventListener('message', (event) => handleMessage(JSON.parse(event.data)));
    socket.addEventListener('close', () => {
        logMessage('Disconnected from battle server.');
        setTimeout(connect, 1000);
    });
}

// Handle incoming messages
function handleMessage(data) {
    switch(data.event) {
        case 'battle_created':
            logMessage('Battle room created. Waiting for opponent...');
            gameState = "waiting";
            isPlayer1 = true;
            break;
            
        case 'battle_joined':
            logMessage('You joined the battle!');
            transitionToCardSelection();
            isPlayer1 = false;
            break;
            
        case 'cards_selected':
            logMessage(`${data.username} has selected their cards`);
            break;
            
        case 'player_ready':
            logMessage(`${data.username} is ready to battle!`);
            if (data.both_ready && data.battle_status === 'in_progress') {
                logMessage('Both players ready! Battle begins!');
                transitionToBattle(data.first_turn || 1);
            }
            break;
            
        case 'round_result':
            displayRoundResult(data);
            break;
            
        case 'battle_completed':
            displayBattleResult(data);
            break;
            
        case 'current_cards':
            renderInitialCards(data);
            break;
    }
}

// Card selection phase
function transitionToCardSelection() {
    gameState = "selecting";
    document.getElementById('card-selection').style.display = 'block';
    document.getElementById('battle-area').style.display = 'none';
    
    fetch('/get-battle-cards/')
        .then(response => response.json())
        .then(data => {
            const grid = document.getElementById('card-selection-grid');
            grid.innerHTML = '';
            data.cards.forEach(card => {
                const cardElement = createCardElement(card);
                cardElement.addEventListener('click', () => toggleCardSelection(cardElement, card));
                grid.appendChild(cardElement);
            });
        });
}

function toggleCardSelection(cardElement, card) {
    if (selectedCards.includes(card.name)) {
        cardElement.classList.remove('selected');
        selectedCards = selectedCards.filter(name => name !== card.name);
    } else if (selectedCards.length < 4) {
        cardElement.classList.add('selected');
        selectedCards.push(card.name);
    }
    
    document.getElementById('selected-count').textContent = selectedCards.length;
    document.getElementById('confirm-selection').disabled = selectedCards.length !== 4;
}

// Battle phase
function transitionToBattle(firstTurn) {
    gameState = "playing";
    document.getElementById('card-selection').style.display = 'none';
    document.getElementById('battle-area').style.display = 'flex';
    
    isMyTurn = (firstTurn === 1 && isPlayer1) || (firstTurn === 2 && !isPlayer1);
    updateTurnIndicator();
    
    socket.send(JSON.stringify({
        event: 'request_current_cards'
    }));
}

function updateTurnIndicator() {
    const playerArea = document.querySelector('.player-area');
    const opponentArea = document.querySelector('.opponent-area');
    
    playerArea.classList.toggle('active-turn', isMyTurn);
    opponentArea.classList.toggle('active-turn', !isMyTurn);
    
    logMessage(isMyTurn ? "Your turn! Select a stat to compare." : "Opponent's turn...");
}

// UI Helpers
function createCardElement(card, showStats = false) {
    const el = document.createElement('div');
    el.className = 'card';
    el.innerHTML = `
        <h3>${card.name}</h3>
        <div class="card-image">
            <img src="${card.image || ''}" alt="${card.name}">
        </div>
        ${showStats ? createStatsHTML(card) : ''}
    `;
    return el;
}

function createStatsHTML(card) {
    return `
        <div class="card-stats">
            <button class="stat-button" data-stat="environmental_friendliness">
                Environment: ${card.environmental_friendliness}
            </button>
            <button class="stat-button" data-stat="beauty">
                Beauty: ${card.beauty}
            </button>
            <button class="stat-button" data-stat="cost">
                Cost: ${card.cost}
            </button>
        </div>
    `;
}

function logMessage(message, isError = false) {
    const log = document.getElementById('battle-log');
    const entry = document.createElement('div');
    entry.className = `log-entry${isError ? ' error' : ''}`;
    entry.textContent = message;
    log.appendChild(entry);
    log.scrollTop = log.scrollHeight;
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    connect();
    
    document.getElementById('confirm-selection').addEventListener('click', () => {
        if (selectedCards.length === 4) {
            socket.send(JSON.stringify({
                event: 'select_cards',
                card_ids: selectedCards
            }));
            socket.send(JSON.stringify({ event: 'ready' }));
            document.getElementById('confirm-selection').disabled = true;
        }
    });
    
    document.getElementById('new-battle').addEventListener('click', () => {
        window.location.href = '/battle/';
    });
});