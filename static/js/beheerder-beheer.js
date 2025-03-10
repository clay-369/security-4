function openModal(modalType) {
    document.getElementById(modalType).style.display = "flex";
}

function closeModal(modalType) {
    document.getElementById(modalType).style.display = "none";
}

function openEditModal(adminID) {
    fetch(`/api/admin/beheer?id=${adminID}`)
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
                        <form method="POST" id="editAdmin">
                            <label for="edit_first_name">Voornaam</label>
                            <input class="text-input" type="text" id="edit_first_name" name="edit_first_name" value="${admin.voornaam}" required>

                            <label for="edit_last_name">Achternaam</label>
                            <input class="text-input" type="text" id="edit_last_name" name="edit_last_name" value="${admin.achternaam}" required>

                            <label for="edit_email">Email / login</label>
                            <input class="text-input" type="email" id="edit_email" name="edit_email" value="${admin.email}" required>

                            <label for="edit_password">Wachtwoord</label>
                            <input class="text-input" type="password" id="edit_password" name="edit_password" placeholder="Nieuw wachtwoord (optioneel)">

                            <input class="modal-btn" type="submit" name="submit" value="Opslaan">
                            <input class="modal-btn" type="submit" name="submit" value="Verwijderen">
                        </form>
                </div>
            `;
            document.body.appendChild(modal);
            modal.style.display = "flex";

           document.getElementById("editAdmin").addEventListener('submit', function(event) {
               event.preventDefault();
                if (event.submitter.value === "Opslaan") {

                    const firstName = document.getElementById("edit_first_name").value;
                    const lastName = document.getElementById("edit_last_name").value;
                    const email = document.getElementById('edit_email').value;
                    const password = document.getElementById('edit_password').value;

                       fetch('/api/admin/beheer', {
                            method: 'PATCH',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({first_name: firstName, last_name: lastName,
                                email: email, password: password, admin_id: adminID})
                       })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                console.log('Admin bewerkt!');
                                loadTable();
                            } else {
                                console.log('Error!');
                            }
                        })
                    closeModal('editModal');
               }
                else if (event.submitter.value === "Verwijderen") {

                       fetch('/api/admin/beheer', {
                            method: 'DELETE',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({admin_id: adminID})
                       })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                console.log('Admin verwijderd!');
                                loadTable();
                            } else {
                                console.log('Error!');
                            }
                        })
                    closeModal('editModal');


                }
           });
    });
}

function loadTable() {
        fetch('/api/admin/beheer?fetch=adminData')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector("table tbody");
            tbody.innerHTML = '';

            data.forEach(admin => {
                const row = document.createElement('tr');
                row.innerHTML = `
                <th scope="row"> ${admin.voornaam} ${admin.achternaam}</th>
                <td>${admin.email}</td>
                <td>
                    <button tabindex="0" class="details-btn" onclick="openEditModal(${admin.beheerder_id})">Details</button>
                </td>
                `;
                tbody.appendChild(row)
            });
        })
}

window.addEventListener('load', function() {
    setInterval(loadTable, 5000);
})

document.getElementById('createAdmin').addEventListener('submit', function(event){
    event.preventDefault();

    const request = 'create'
    const firstName = document.getElementById("first_name").value;
    const lastName = document.getElementById("last_name").value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('/api/admin/beheer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({request: request, first_name: firstName, last_name: lastName, email: email, password: password})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Admin gemaakt!');
            loadTable();
        } else {
            console.log('Error!');
        }
    })
    closeModal('createModal');
});

loadTable()