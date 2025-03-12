function closeModal(modalType) {
    document.getElementById(modalType).style.display = "none";
}

function loadTable() {
        fetch('/api/admin?fetch=allData')
        .then(response => response.json())
        .then(data => {
            const expertsData = data.experts;
            const expertsBody = document.querySelector("#registrationTable tbody");
            expertsBody.innerHTML = '';

            expertsData.forEach(expert => {
                const row = document.createElement('tr');
                if (expert.status === 'NIEUW') {
                    row.innerHTML = `
                        <td> ${expert.voornaam} ${expert.achternaam}</td>
                        <td>
                            <button tabindex="0" class="btn" onclick="openDetailsModal(${expert.deskundige_id}, 'expert')">Details</button>
                        </td>
                        `;
                    expertsBody.appendChild(row)
                }
            });

            const enlistmentData = data.enlistments;
            const enlistmentBody = document.querySelector('#enlistmentTable tbody');
            enlistmentBody.innerHTML = '';

            enlistmentData.forEach(enlistment => {
                const row = document.createElement('tr');
                if (enlistment.status === 'NIEUW') {
                    row.innerHTML = `
                        <td>${enlistment.naam}</td>
                        <td>
                            <button tabindex="0" class="btn" onclick="openDetailsModal(${enlistment.inschrijving_id}, 'enlistment')">Details</button>
                        </td>
                        `;
                    enlistmentBody.appendChild(row);
                }
            });

            const researchData = data.researches;
            const researchesBody = document.querySelector('#researchesTable tbody');
            researchesBody.innerHTML = '';

            researchData.forEach(research => {
                const row = document.createElement('tr');
                if (research.status === 'NIEUW') {
                    row.innerHTML = `
                        <td>${research.titel}</td>
                        <td>
                            <button tabindex="0" class="btn" onclick="openDetailsModal(${research.onderzoek_id}, 'research')">Details</button>
                        </td>
                        `;
                    researchesBody.appendChild(row);
                }
            });

        })
}

function openDetailsModal(dataID, dataType) {
    fetch('/api/admin?fetch=allData')
        .then(response => response.json())
        .then(responseData => {
            const openedModal = document.getElementById("detailsModal");
            if (openedModal) {
                openedModal.remove();
            }

            let modalContent;

            if (dataType === 'expert') {
                console.log('Expert function');
                expertData = responseData.experts[dataID - 1]; // Index key offset

                // Moet nog aan gewerkt worden
                modalContent = `
                        <h1>Expert Details</h1>
                        
                        <h2>Volledige naam</h2>
                        <p>${expertData['voornaam']} ${expertData['achternaam']}</p>
                        
                        <h2>Contactgegevens</h2>
                        <p>${expertData['email']}</p>
                        <p>${expertData['telefoonnummer']}</p>
                        
                        <p>${expertData['postcode']}</p>                        
                        <p>${expertData['geboortedatum']}</p>
                        
                            <form method="POST" id="detailsModal">
                                <input class="modal-btn" type="submit" name="submit" value="Accepteren">
                                <input class="modal-btn" type="submit" name="submit" value="Weigeren">
                            </form>
                `;
            } else if (dataType === 'enlistment') {
                console.log('Enlistment function')
                // Moet nog aan gewerkt worden
                modalContent = `
                        <h1>Inschrijving Details</h1>
                            <form method="POST" id="detailsModal">
        
                                <input class="modal-btn" type="submit" name="submit" value="Accepteren">
                                <input class="modal-btn" type="submit" name="submit" value="Weigeren">
                            </form>
                `;
            } else if (dataType === 'research') {
                console.log('Research function')
                const research = responseData.researches[dataID - 1];
                // Moet nog aan gewerkt worden
                modalContent = `
                        <h1>Onderzoek Details</h1>
                        <h2>Onderzoek</h2>
                        <p>titel: ${research.titel}</p>
                        <p>beschrijving: ${research.beschrijving}</p>
                        <p>datum: ${research.datum_vanaf} tot ${research.datum_tot}</p>
                        <p>type: ${research.onderzoek_type.toLowerCase()}</p>
                        
                        <!-- If OP LOCATIE-->
                        <p>locatie: ${research.locatie}</p>
                        <!--If statement for beloning-->
                        <p>${research.beloning}</p>
                        <p>${research.leeftijd_vanaf} tot ${research.leeftijd_tot} jaar</p>
                        <p>${research.titel}</p>
                        
                        <h3>Beperkingen</h3>
                        <!--todo-->
                        
                        <h3>Organisatie</h3>
                        <p>${research.naam}</p>
                        
                            <form method="POST" id="detailsModal">
                                <input class="modal-btn" type="submit" name="submit" value="Accepteren">
                                <input class="modal-btn" type="submit" name="submit" value="Weigeren">
                            </form>
                `;
            }

            const modal = document.createElement("div");
            modal.id = "detailsModal";
            modal.className = "modal";
            modal.innerHTML = `
                    <div class="modalForm">
                        <button class="close-btn" onclick="closeModal('detailsModal')">x</button>
                       ${modalContent}
                    </div>   
                `;
            document.body.appendChild(modal);
            modal.style.display = "flex";

            document.getElementById("detailsModal").addEventListener('submit', function (event) {
                event.preventDefault();

                const adminId = responseData.admin_id;
                if (event.submitter.value === "Accepteren") {
                    status = 'GOEDGEKEURD'
                } else if (event.submitter.value === "Weigeren") {
                    status = 'AFGEKEURD'
                }
                fetch('/api/admin', {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({status: status, data_type: dataType, data_id: dataID, admin_id : adminId})
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            console.log('Aanvraag geaccepteerd!');
                            loadTable();
                        } else {
                            console.log('Error!');
                            loadTable();
                        }
                    })
                closeModal('detailsModal');
            })
        })
}

window.addEventListener('load', function() {
    setInterval(loadTable, 5000);
})

loadTable()
