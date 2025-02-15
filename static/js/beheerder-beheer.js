function openModal(modalType) {
    document.getElementById(modalType).style.display = "flex";
}

function closeModal(modalType) {
    document.getElementById(modalType).style.display = "none";
}

function openEditModal(adminID) {
    fetch(`/admin/beheer?id=${adminID}`)
        .then(response => response.json())
        .then(admin => {
            const openedModal = document.getElementById("editModal");
            if (openedModal) {
                openedModal.remove();
            }

            const modal = document.createElement("div");
            modal.id = "editModal";
            modal.className = "modal";
            modal.innerHTML = `
                <div class="modalForm">
                    <button class="close-btn" onclick="closeModal('editModal')">x</button>
                    <h1>Bewerk gebruiker</h1>
                        <form method="POST" id="editForm">
                            <label for="voornaam">Voornaam</label>
                            <input class="text-input" type="text" id="voornaam" name="voornaam" value="${admin.voornaam}" required>

                            <label for="achternaam">Achternaam</label>
                            <input class="text-input" type="text" id="achternaam" name="achternaam" value="${admin.achternaam}" required>

                            <label for="login">Email / login</label>
                            <input class="text-input" type="email" id="login" name="login" value="${admin.email}" required>

                            <label for="password">Wachtwoord</label>
                            <input class="text-input" type="password" id="password" name="password" placeholder="Nieuw wachtwoord (optioneel)">

                            <input class="btn" type="submit" name="submit" value="Opslaan">
                            <input class="btn" type="submit" name="submit" value="Verwijderen">
                        </form>
                </div>
            `;

    document.body.appendChild(modal);
    modal.style.display = "flex";
    });
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
                    <button class="btn" onclick="openEditModal(${admin.beheerder_id})">Details</button>
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