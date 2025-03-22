const toggle = document.getElementById('switch');
const dropDown = document.getElementById('user-select');

toggle.addEventListener('change', function() {
    if (dropDown.style.display == 'none') {
        dropDown.style.display = 'block';
    } else {
        dropDown.style.display = 'none';
    }
});


