function openModal(modalType) {
    document.getElementById(modalType).style.display = "flex";
}

function closeModal(modalType) {
    document.getElementById(modalType).style.display = "none";
}

window.addEventListener('load', function() {
    setInterval(function() {
        fetch('/admin/beheer?fetch=adminData')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector("table tbody");
            tbody.innerHTML = '';

            data.forEach(admin => {
                const row = document.createElement('tr');
                row.innerHTML = `
                <td> ${admin.voornaam} ${admin.achternaam}</td>
                <td>${admin.email}</td>
                <td>
                    <button class="btn" id=${admin.beheerder_id}>Details</button>
                </td>
                `;
                tbody.appendChild(row)
            });
        })
    }, 1000)
})

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
            console.log('Admin gemaakt!');
            closeModal('createModal');
        } else {
            console.log('Error!');
        }
    })
});