function openModal() {
    document.getElementById("createModal").style.display = "flex";
}

function closeModal() {
    document.getElementById("createModal").style.display = "none";
}

document.getElementById('createAdmin').addEventListener('submit', function(event){
    event.preventDefault();

    const first_name = document.getElementById("first_name").value;
    const last_name = document.getElementById("last_name").value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    console.log(first_name)

    fetch('/admin/beheer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({first_name: first_name, last_name: last_name, email: email, password: password})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Admin gemaakt!')
            closeModal()
        } else {
            console.log('Error!')
        }
    })
});