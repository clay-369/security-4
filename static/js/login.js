document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({email: email, password: password})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (data.type === 'user') {
                window.location.href = '/user' // Moet verwijzen naar gebruikers dashboard
                console.log('Succes voor user!')
            }
            if (data.type === 'admin') {
                window.location.href = '/admin/beheer'
                console.log('Succes voor admin!')
            }
        } else {
            console.log('Foktop!')
        }
    })

})