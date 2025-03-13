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
    currentRound = 1;
    
    // Update UI elements
    document.getElementById('card-selection').style.display = 'none';
    document.getElementById('battle-area').style.display = 'flex';
    
    // Reset scores display
    document.getElementById('player-score').textContent = '0';
    document.getElementById('opponent-score').textContent = '0';
    
    // Determine if it's the player's turn
    isMyTurn = (firstTurn === 1 && isPlayer1) || (firstTurn === 2 && !isPlayer1);
    
    // Clear previous cards
    document.getElementById('player-cards').innerHTML = '';
    document.getElementById('opponent-cards').innerHTML = '';
    
    updateTurnIndicator();
    
    // Request initial cards
    socket.send(JSON.stringify({
        event: 'request_current_cards'
    }));
    
    logMessage(`Battle begins! ${isMyTurn ? 'Your turn first.' : 'Opponent goes first.'}`);
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
    
    // Use a default image if none provided
    const imageSrc = card.image || '/static/img/card_placeholder.png';
    
    el.innerHTML = `
        <h3>${card.name || 'Unknown Card'}</h3>
        <div class="card-image">
            <img src="${imageSrc}" alt="${card.name || 'Card'}" onerror="this.src='/static/img/card_placeholder.png'">
        </div>
        ${showStats ? createStatsHTML(card) : ''}
    `;
    return el;
}

function createStatsHTML(card) {
    if (!card) return '';
    
    // Default values in case stats are undefined
    const envFriendliness = card.environmental_friendliness !== undefined ? card.environmental_friendliness : '?';
    const beauty = card.beauty !== undefined ? card.beauty : '?';
    const cost = card.cost !== undefined ? card.cost : '?';
    
    return `
        <div class="card-stats">
            <button class="stat-button" data-stat="environmental_friendliness">
                Environment: ${envFriendliness}
            </button>
            <button class="stat-button" data-stat="beauty">
                Beauty: ${beauty}
            </button>
            <button class="stat-button" data-stat="cost">
                Cost: ${cost}
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

function renderInitialCards(data) {
    // Clear existing cards
    document.getElementById('player-cards').innerHTML = '';
    document.getElementById('opponent-cards').innerHTML = '';
    
    // Update scores
    document.getElementById('player-score').textContent = isPlayer1 ? 
        data.player1_score || 0 : data.player2_score || 0;
    document.getElementById('opponent-score').textContent = isPlayer1 ? 
        data.player2_score || 0 : data.player1_score || 0;
    
    // Render player card with stats
    if (data.player_card) {
        const playerCardElement = createCardElement(data.player_card, true);
        document.getElementById('player-cards').appendChild(playerCardElement);
        
        // Add event listeners to stat buttons if it's player's turn
        if (isMyTurn) {
            const statButtons = playerCardElement.querySelectorAll('.stat-button');
            statButtons.forEach(button => {
                button.classList.add('selectable');
                button.addEventListener('click', () => {
                    if (isMyTurn) {
                        selectStat(button.dataset.stat);
                    }
                });
            });
        }
    }
    
    // Render opponent card without stats
    if (data.opponent_card) {
        const opponentCardElement = createCardElement(data.opponent_card, false);
        document.getElementById('opponent-cards').appendChild(opponentCardElement);
    }
    
    logMessage('Cards loaded for battle. ' + (isMyTurn ? 'Your turn!' : 'Waiting for opponent...'));
}

function selectStat(stat) {
    if (!isMyTurn || gameState !== 'playing') {
        return;
    }
    
    logMessage(`You selected ${getStatDisplayName(stat)} to compare`);
    
    socket.send(JSON.stringify({
        event: 'select_stat',
        stat: stat
    }));
    
    // Disable further selections until next turn
    const statButtons = document.querySelectorAll('.stat-button');
    statButtons.forEach(button => {
        button.classList.remove('selectable');
    });
}

function getStatDisplayName(stat) {
    switch(stat) {
        case 'environmental_friendliness': return 'Environmental Friendliness';
        case 'beauty': return 'Beauty';
        case 'cost': return 'Cost';
        default: return stat;
    }
}

function displayRoundResult(data) {
    // Update scores
    document.getElementById('player-score').textContent = isPlayer1 ? 
        data.player1_score : data.player2_score;
    document.getElementById('opponent-score').textContent = isPlayer1 ? 
        data.player2_score : data.player1_score;
    
    // Display round result
    let resultMessage;
    if (data.result === 'tie') {
        resultMessage = `Round ${currentRound}: It's a tie! Both players get 1 point.`;
    } else if (
        (data.result === 'player1' && isPlayer1) || 
        (data.result === 'player2' && !isPlayer1)
    ) {
        resultMessage = `Round ${currentRound}: You win! Your card has better ${getStatDisplayName(data.stat)}.`;
    } else {
        resultMessage = `Round ${currentRound}: Opponent wins! Their card has better ${getStatDisplayName(data.stat)}.`;
    }
    
    logMessage(resultMessage);
    
    // Set up for next round
    currentRound++;
    isMyTurn = (data.next_turn === 1 && isPlayer1) || (data.next_turn === 2 && !isPlayer1);
    
    // Show remaining cards
    logMessage(`${data.cards_remaining} cards remaining`);
    
    // After a short delay, fetch new cards
    setTimeout(() => {
        if (data.cards_remaining > 0) {
            socket.send(JSON.stringify({
                event: 'request_current_cards'
            }));
            updateTurnIndicator();
        }
    }, 2000);
}

function displayBattleResult(data) {
    gameState = 'completed';
    
    // Update final scores
    document.getElementById('player-score').textContent = isPlayer1 ? 
        data.player1_score : data.player2_score;
    document.getElementById('opponent-score').textContent = isPlayer1 ? 
        data.player2_score : data.player1_score;
    
    const playerWon = (isPlayer1 && data.winner === username) || (!isPlayer1 && data.winner !== username);
    
    // Display title and message
    const resultOverlay = document.getElementById('result-overlay');
    const resultTitle = document.getElementById('result-title');
    const resultMessage = document.getElementById('result-message');
    
    resultTitle.textContent = playerWon ? 'Victory!' : 'Defeat!';
    resultMessage.textContent = playerWon ? 
        'You won the battle! +10 points awarded.' : 
        'You lost the battle. +2 points awarded for participating.';
    
    resultTitle.className = `result-title ${playerWon ? 'win' : 'lose'}`;
    
    // Show the overlay
    resultOverlay.classList.add('active');
    
    logMessage(playerWon ? 
        'Battle complete! You are victorious!' : 
        'Battle complete! Better luck next time.');
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