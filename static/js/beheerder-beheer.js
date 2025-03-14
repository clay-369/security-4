function openModal(modalType) {
    document.getElementById(modalType).style.display = "flex";
}

function closeModal(modalType) {
    document.getElementById(modalType).style.display = "none";
}

function openEditModal(adminID) {
    fetch(`/api/admin/beheer/${adminID}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${sessionStorage.getItem('accessToken')}`
        }
    })
        .then(response => response.json())
        .then(admin => {
            if (admin['error'] === 'token_expired') {
                refreshAccessToken(openEditModal, adminID);
                return;
            }
            const openedModal = document.getElementById("editModal");
            if (openedModal) {
                openedModal.remove();
            }

            const modal = document.createElement("div");
            modal.id = "editModal";
            modal.className = "modal";
            modal.innerHTML = `
                <h1>Bewerk gebruiker</h1>
                <div class="modal-content">
                    <div class="form-container">
                        <div class="input-fields">
                            <div class="field-row">
                                <label for="edit_first_name">Voornaam</label>
                                <input class="text-input" type="text" id="edit_first_name" name="edit_first_name" value="${admin.voornaam}" required>
                                 
                                <label for="edit_email">Email / login</label>
                                <input class="text-input" type="email" id="edit_email" name="edit_email" value="${admin.email}" required>
                            </div>
                            <div class="field-row">
                                <label for="edit_last_name">Achternaam</label>
                                <input class="text-input" type="text" id="edit_last_name" name="edit_last_name" value="${admin.achternaam}" required>
                            
                                <label for="edit_password">Wachtwoord</label>
                                <input class="text-input" type="password" id="edit_password" name="edit_password" placeholder="Nieuw wachtwoord (optioneel)">
                            </div>
                        </div>
                        <div class="action-buttons">
                            <input id="editAdmin" class="modal-btn" type="submit" name="submit" value="Opslaan">
                            <input id="deleteAdmin" class="modal-btn" type="submit" name="submit" value="Verwijderen">
                            <button onclick="closeModal('editModal')" class="close-btn">Annuleren</button>
                        </div>
                    </div>
                </div>
            `;
            document.querySelector('main').appendChild(modal);
            modal.style.display = "flex";

           document.getElementById("editAdmin").addEventListener('click', function(event) {
               event.preventDefault();
                const firstName = document.getElementById("edit_first_name").value;
                const lastName = document.getElementById("edit_last_name").value;
                const email = document.getElementById('edit_email').value;
                let password = document.getElementById('edit_password').value;
                if (password === '') {
                    password = null;
                }
                  editAdmin(adminID, firstName, lastName, email, password);
                closeModal('editModal');
               });

           document.getElementById('deleteAdmin')
               .addEventListener('click', () => {
                   deleteAdmin(adminID);

                    closeModal('editModal');
                })
           });
}

function editAdmin(adminID, firstName, lastName, email, password) {
  fetch(`/api/admin/beheer/${adminID}`, {
      method: 'PATCH',
      headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${sessionStorage.getItem('accessToken')}`
      },
      body: JSON.stringify({
          first_name: firstName, last_name: lastName,
          email: email, password: password
      })
  })
      .then(response => response.json())
      .then(data => {
          if (data['error'] === 'token_expired') {
                refreshAccessToken(editAdmin, [adminID, firstName, lastName, email, password]);
                return;
            }
          if (data.success) {
              showSnackbar("Beheerder is succesvol bewerkt.", 'success');
              loadTable();
          } else {
              showSnackbar("Beheerder kon niet bewerkt worden.");
          }
      })
}

function deleteAdmin(adminID) {
   fetch(`/api/admin/beheer/${adminID}`, {
       method: 'DELETE',
       headers: {
           'Content-Type': 'application/json',
           'Authorization': `Bearer ${sessionStorage.getItem('accessToken')}`
       }
   })
       .then(response => response.json())
       .then(data => {
           if (data['error'] === 'token_expired') {
                refreshAccessToken(deleteAdmin, adminID);
                return;
            }
           if (data.success) {
               showSnackbar("Beheerder is succesvol verwijdert.", 'success');
               loadTable();
           } else {
               showSnackbar("Beheerder kon niet verwijdert worden.");
           }
       })
}

function loadTable() {
        fetch('/api/admin/beheer', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${sessionStorage.getItem('accessToken')}`
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data['error'] === 'token_expired') {
                refreshAccessToken(loadTable);
                return;
            }
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

document.getElementById('createAdmin').addEventListener('click', function(event){
    event.preventDefault();

    const firstName = document.getElementById("first_name").value;
    const lastName = document.getElementById("last_name").value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    createAdmin(firstName, lastName, email, password);

    closeModal('createModal');
});

function createAdmin(firstName, lastName, email, password) {
    fetch('/api/admin/beheer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${sessionStorage.getItem('accessToken')}`
        },
        body: JSON.stringify({
            first_name: firstName,
            last_name: lastName,
            email: email,
            password: password
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data['error'] === 'token_expired') {
                refreshAccessToken(createAdmin, [firstName, lastName, email, password]);
                return;
            }
            if (data.success) {
                showSnackbar("Beheerder succesvol aangemaakt.", 'success');
                loadTable();
            } else {
                showSnackbar("Beheerder kon niet aangemaakt worden.");
            }
        })
}

loadTable()