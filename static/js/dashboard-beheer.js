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
                        <td>${enlistment.voornaam} ${enlistment.achternaam}</td>
                        <td>${enlistment.titel}</td>
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
                const expertData = responseData.experts[dataID - 1]; // Index key offset

                // Moet nog aan gewerkt worden
                modalContent = `
                        <h1>Expert Details</h1>
                        
                        <h2>Persoonlijke gegevens</h2>
                        <p>Naam: ${expertData['voornaam']} ${expertData['achternaam']}</p>
                        <p>Geboortedatum: ${expertData['geboortedatum']}</p>
                        <p>Introductie: ${expertData['introductie']}</p>
                        
                        <h2>Contactgegevens</h2>
                        <p>Email: ${expertData['email']}</p>
                        <p>Telefoonnummer: ${expertData['telefoonnummer']}</p>
                        
                        <h2>Overige gegevens</h2>
                        <p>Hulpmiddelen: ${expertData['hulpmiddelen']}</p>
                        <p>Bijzonderheden: ${expertData['bijzonderheden']}</p>
                        <p>Bijzonderheden beschikbaarheid: ${expertData['bijzonderheden_beschikbaarheid']}</p>
                        <p>Type onderzoeken: ${expertData['type_onderzoeken']}</p>     
                        
                        <h2>Toezichthouder Informatie</h2>
                        
                            <form method="POST" id="detailsModal">
                                <input class="modal-btn" type="submit" name="submit" value="Accepteren">
                                <input class="modal-btn" type="submit" name="submit" value="Weigeren">
                            </form>
                `;
            } else if (dataType === 'enlistment') {
                console.log('Enlistment function')
                const enlistmentData = responseData.enlistments[dataID - 1]; // Index key offset
                // Moet nog aan gewerkt worden
                modalContent = `
                        <h1>Inschrijving Details</h1>
                            <form method="POST" id="detailsModal">
                            
                                <h2>Details inschrijvende:</h2>
                                <p>Naam: ${enlistmentData['voornaam']} ${enlistmentData['achternaam']}</p>
                                <p>Geboortedatum: ${enlistmentData['geboortedatum']}</p>
                                <p>Email: ${enlistmentData['email']}</p>
                                <p>Telefoonnummer: ${enlistmentData['telefoonnummer']}</p>
                                <p>Hulpmiddelen: ${enlistmentData['hulpmiddelen']}</p>
                                <p>Bijzonderheden: ${enlistmentData['bijzonderheden']}</p>
                                <p>Bijzonderheden beschikbaarheid: ${enlistmentData['bijzonderheden_beschikbaarheid']}</p>
                                <p>Type onderzoeken: ${enlistmentData['type_onderzoeken']}</p>     
        
                                <h2>Details onderzoek:</h2>
                                <p>Titel: ${enlistmentData['titel']}</p>
                                <p>Beschrijving: ${enlistmentData['beschrijving']}</p>
                                <p>Startdatum: ${enlistmentData['datum_vanaf']}</p>
                                <p>Einddatum: ${enlistmentData['datum_tot']}</p>
                                <p>Onderzoek-type: ${enlistmentData['onderzoek_type']}</p>
                                <p>Locatie: ${enlistmentData['locatie']}</p>
                                <p>Vanaf leeftijd:: ${enlistmentData['leeftijd_vanaf']}</p>
                                <p>Tot leeftijd: ${enlistmentData['leeftijd_tot']}</p>
        
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
