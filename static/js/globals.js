// Show snackbar method
let snackbarTimeoutId;
function showSnackbar(message, type = "error") {
    // Snackbar
    let snackbar = document.getElementById("snackbar")
    snackbar.className = "show"
    snackbar.innerHTML = message
    if (type === "error") {
        snackbar.style.backgroundColor = "#ff4444"
    } else if (type === "success") {
        snackbar.style.backgroundColor = "#3dbb56"
    }

    clearTimeout(snackbarTimeoutId);
    snackbarTimeoutId = setTimeout(function () {
        snackbar.className = snackbar.className.replace("show", "")
    }, 3000);
}

function refreshAccessToken(func = null, params = null) {
    if (sessionStorage.getItem('refreshToken') === null) {
        return;
    }

    fetch('/auth/refresh', {
        method: 'GET',
        headers: {
        'Authorization': `Bearer ${sessionStorage.getItem('refreshToken')}`
    }})
        .then(response => response.json())
        .then(data => {
            const accessToken = data['access_token'];
            sessionStorage.setItem('accessToken', accessToken);

            if (func) {
                func.apply(null, params);
            }
    });
}

refreshAccessToken();

function toggleDarkMode() {
    if (document.body.classList.contains('dark')) {
      document.body.classList.remove('dark');
      document.querySelector('.dark-mode-toggle').innerHTML = 'Donker Thema';
      // Save if dark mode is on
      localStorage.setItem('darkMode', 'off');
    } else {
      document.body.classList.add('dark');
      document.querySelector('.dark-mode-toggle').innerHTML = 'Licht Thema';
      localStorage.setItem('darkMode', 'on');
    }
}

document.querySelector('.dark-mode-toggle')
    .addEventListener('click', () => {
        toggleDarkMode();
    });

// Toggle dark mode if it is on
if (localStorage.getItem('darkMode') === 'on') {
    toggleDarkMode();
}