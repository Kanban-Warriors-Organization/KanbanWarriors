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
    
    try {
        socket = new WebSocket(`${protocol}//${host}/ws/battle/${roomId}/`);
        
        socket.addEventListener('open', () => {
            logMessage('Connected to battle server!');
            // Request current game state on connect/reconnect
            socket.send(JSON.stringify({ event: 'request_state' }));
        });
        
        socket.addEventListener('message', (event) => {
            try {
                handleMessage(JSON.parse(event.data));
            } catch (e) {
                logMessage('Error processing message: ' + e.message, true);
            }
        });
        
        socket.addEventListener('close', () => {
            logMessage('Disconnected from battle server. Attempting to reconnect...', true);
            setTimeout(connect, 1000);
        });
        
        socket.addEventListener('error', (error) => {
            logMessage('Connection error occurred. Retrying...', true);
            console.error('WebSocket error:', error);
        });
    } catch (e) {
        logMessage('Failed to connect: ' + e.message, true);
        setTimeout(connect, 1000);
    }
}

// Handle incoming messages
function handleMessage(data) {
    switch(data.event) {
        case 'battle_created':
            logMessage('Battle room created. Waiting for opponent...');
            gameState = data.status || "waiting";
            isPlayer1 = true;
            document.getElementById('opponent-name').textContent = 'Waiting for opponent...';
            
            // If status is 'selecting', transition to card selection immediately
            if (data.status === 'selecting') {
                logMessage('Select your cards while waiting for an opponent...');
                transitionToCardSelection();
            }
            break;
            
        case 'battle_joined':
            // Update both players when player 2 joins
            gameState = "selecting";
            
            // Set player role based on data or keep existing
            if (data.is_player1 !== undefined) {
                isPlayer1 = data.is_player1;
            }
            
            // For player 1, the opponent is the joining player (username)
            // For player 2, the opponent is the battle creator (opponent_name)
            const opponentName = isPlayer1 ? data.username : data.opponent_name;
            document.getElementById('opponent-name').textContent = opponentName;
            
            if (isPlayer1) {
                logMessage(`${opponentName} has joined the battle! Select your cards.`);
            } else {
                logMessage('You joined the battle! Select your cards.');
            }
            
            // Both players transition to card selection
            transitionToCardSelection();
            break;
            
        case 'battle_state':
            // Handle reconnection or state updates
            isPlayer1 = data.is_player1;
            gameState = data.status;
            document.getElementById('opponent-name').textContent = 
                data.opponent_name || 'Waiting for opponent...';
            
            if (data.status === 'selecting') {
                gameState = "selecting";
                logMessage('Select your cards for battle!');
                transitionToCardSelection();
            } else if (data.status === 'in_progress') {
                gameState = "playing";
                transitionToBattle(data.current_turn);
            }
            break;
            
        case 'cards_selected':
            logMessage(`${data.username} has selected their cards`);
            break;
            
        case 'player_ready':
            const readyMessage = data.username === username ? 
                'You are ready!' : 
                `${data.username} is ready!`;
            logMessage(readyMessage);
            
            if (data.both_ready && data.battle_status === 'in_progress') {
                logMessage('Both players ready! Battle begins!');
                transitionToBattle(data.first_turn);
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
    if (gameState !== "selecting") {
        logMessage(`Cannot transition to card selection in game state: ${gameState}`, true);
        return;
    }
    
    logMessage('Loading your cards for selection...');
    document.getElementById('card-selection').style.display = 'block';
    document.getElementById('battle-area').style.display = 'none';
    
    // Clear any existing selections
    selectedCards = [];
    document.getElementById('selected-count').textContent = '0';
    document.getElementById('confirm-selection').disabled = true;
    
    fetch('/get-battle-cards/')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            
            const grid = document.getElementById('card-selection-grid');
            grid.innerHTML = '';
            
            if (!data.cards || data.cards.length === 0) {
                logMessage('No cards available for selection. Please collect some cards first!', true);
                return;
            }
            
            logMessage(`${data.cards.length} cards available for selection`);
            data.cards.forEach(card => {
                const cardElement = createCardElement(card);
                cardElement.addEventListener('click', () => toggleCardSelection(cardElement, card));
                grid.appendChild(cardElement);
            });
        })
        .catch(error => {
            logMessage('Error loading cards: ' + error.message, true);
            console.error('Card loading error:', error);
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