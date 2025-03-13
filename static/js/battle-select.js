document.addEventListener('DOMContentLoaded', () => {
    const createBattleBtn = document.getElementById('create-battle');
    const joinBattleBtn = document.getElementById('join-battle');
    const roomIdInput = document.getElementById('room-id');

    createBattleBtn.addEventListener('click', () => {
        // Redirect to battle page without room ID to create new battle
        window.location.href = '/battle/';
    });

    joinBattleBtn.addEventListener('click', () => {
        const roomId = roomIdInput.value.trim();
        if (roomId) {
            // Redirect to battle page with room ID
            window.location.href = `/battle/${roomId}/`;
        } else {
            alert('Please enter a room ID');
        }
    });

    roomIdInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            joinBattleBtn.click();
        }
    });
});