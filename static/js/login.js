document.getElementById('loginForm')
    .addEventListener('submit', function(event) {
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
                jwtLogin(email, password);
            } else {
                showSnackbar(data['message']);
            }
    })
})

function jwtLogin(email, password) {
    fetch('/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({email, password})
    })
        .then(response => response.json())
        .then(data => {
            const accessToken = data['tokens']['access'];
            const refreshToken = data['tokens']['refresh'];
            sessionStorage.setItem('accessToken', accessToken);
            sessionStorage.setItem('refreshToken', refreshToken);

            // Redirect after completely logging in
            window.location.href = '/';
        });
}
