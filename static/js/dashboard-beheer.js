function closeModal(modalType) {
  document.getElementById(modalType).style.display = "none"
}

function loadTable() {
  fetch("/api/admin", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${sessionStorage.getItem("accessToken")}`,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data["error"] === "token_expired") {
        refreshAccessToken(loadTable)
        return
      }
      const expertsData = data.experts
      const expertsBody = document.querySelector("#registrationTable tbody")
      expertsBody.innerHTML = ""

      expertsData.forEach((expert) => {
        const row = document.createElement("tr")
        if (expert.status === "NIEUW") {
          row.innerHTML = `
                        <th scope="row"> ${expert.voornaam} ${expert.achternaam}</th>
                        <td>
                            <button tabindex="0" class="btn" onclick="openDetailsModal(${expert.deskundige_id}, 'expert')">Details</button>
                        </td>
                        `
          expertsBody.appendChild(row)
        }
      })

      const enlistmentData = data.enlistments
      const enlistmentBody = document.querySelector("#enlistmentTable tbody")
      enlistmentBody.innerHTML = ""

      enlistmentData.forEach((enlistment) => {
        const row = document.createElement("tr")
        if (enlistment.status === "NIEUW") {
          row.innerHTML = `
                        <th scope="row">${enlistment.voornaam} ${enlistment.achternaam}</th>
                        <td>${enlistment.titel}</td>
                        <td>
                            <button tabindex="0" class="btn" onclick="openDetailsModal(${enlistment.inschrijving_id}, 'enlistment')">Details</button>
                        </td>
                        `
          enlistmentBody.appendChild(row)
        }
      })

      const researchData = data.researches
      const researchesBody = document.querySelector("#researchesTable tbody")
      researchesBody.innerHTML = ""

      researchData.forEach((research) => {
        const row = document.createElement("tr")
        if (research.status === "NIEUW") {
          row.innerHTML = `
                        <th scope="row">${research.titel}</th>
                        <td>
                            <button tabindex="0" class="btn" onclick="openDetailsModal(${research.onderzoek_id}, 'research')">Details</button>
                        </td>
                        `
          researchesBody.appendChild(row)
        }
      })
    })
}

function openDetailsModal(dataID, dataType) {
  fetch("/api/admin", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${sessionStorage.getItem("accessToken")}`,
    },
  })
    .then((response) => response.json())
    .then((responseData) => {
      if (responseData["error"] === "token_expired") {
        refreshAccessToken(openDetailsModal, [dataID, dataType])
        return
      }
      const openedModal = document.getElementById("detailsModal")
      if (openedModal) {
        openedModal.remove()
      }

      let modalContent

      if (dataType === "expert") {
        const expertData = responseData.experts[dataID - 1] // Index key offset

      let guardianContent = "";
      if (expertData['toezichthouder'] === 1) {
          guardianContent = `
            <div>
            <h2>Gegevens Voogd</h2>
            <p>Naam: ${expertData['toezichthouder_naam']}</p>
            <p>Email: ${expertData['toezichthouder_email']}</p>
            <p>Telefoonnummer: ${expertData['toezichthouder_telefoonnummer']}</p>
            </div>
      `;
      }

        // Moet nog aan gewerkt worden
        modalContent = `
                        <h1>Expert Details</h1>
                        <div class="modal-container">
                            <div>
                                <h2>Persoonlijke gegevens</h2>
                                <p>Naam: ${expertData["voornaam"]} ${expertData["achternaam"]}</p>
                                <p>Geboortedatum: ${expertData["geboortedatum"]}</p>
                                <p>Introductie: ${expertData["introductie"]}</p>
                            </div>

                            <div>
                                <h2>Contactgegevens</h2>
                                <p>Email: ${expertData["email"]}</p>
                                <p>Telefoonnummer: ${expertData["telefoonnummer"]}</p>
                            </div>

                            <div>
                                <h2>Overige gegevens</h2>
                                <p>Hulpmiddelen: ${expertData["hulpmiddelen"] || 'Geen'}</p>
                                <p>Bijzonderheden: ${expertData["bijzonderheden"] || 'Geen'}</p>
                                <p>Bijzonderheden beschikbaarheid: ${expertData["bijzonderheden_beschikbaarheid"] || 'Geen'}</p>
                                <p>Voorkeur onderzoeken: ${expertData["type_onderzoeken"].toLowerCase()}</p>     
                            </div>    
                            ${guardianContent}                    
                        </div>
                            <form method="POST" id="detailsModal">
                                <input class="modal-btn" type="submit" name="submit" value="Accepteren">
                                <input class="modal-btn" type="submit" name="submit" value="Weigeren">
                            </form>
                `
      } else if (dataType === "enlistment") {
        const enlistmentData = responseData.enlistments[dataID - 1] // Index key offset
        // Moet nog aan gewerkt worden
        modalContent = `
                        <h1>Inschrijving Details</h1>
                            <div class="modal-container">
                                <div>
                                    <h2>Details inschrijvende:</h2>
                                    <p>Naam: ${enlistmentData["voornaam"]} ${enlistmentData["achternaam"]}</p>
                                    <p>Geboortedatum: ${enlistmentData["geboortedatum"]}</p>
                                    <p>Email: ${enlistmentData["email"]}</p>
                                    <p>Telefoonnummer: ${enlistmentData["telefoonnummer"]}</p>
                                    <p>Hulpmiddelen: ${enlistmentData["hulpmiddelen"] || 'Geen'}</p>
                                    <p>Bijzonderheden: ${enlistmentData["bijzonderheden"] || 'Geen'}</p>
                                    <p>Bijzonderheden beschikbaarheid: ${enlistmentData["bijzonderheden_beschikbaarheid"] || 'Geen'}</p>
                                    <p>Voorkeur onderzoeken: ${enlistmentData["type_onderzoeken"].toLowerCase()}</p>     
                                </div>
                                <div>
                                    <h2>Details onderzoek:</h2>
                                    <p>Titel: ${enlistmentData["titel"]}</p>
                                    <p>Beschrijving: ${enlistmentData["beschrijving"]}</p>
                                    <p>Startdatum: ${enlistmentData["datum_vanaf"]}</p>
                                    <p>Einddatum: ${enlistmentData["datum_tot"]}</p>
                                    <p>Onderzoek-type: ${enlistmentData["onderzoek_type"].toLowerCase()}</p>
                                    ${
                                        enlistmentData.locatie
                                        ? `<p>locatie: ${enlistmentData.locatie}</p>`
                                        : ''
                                    }
                                    
                                    
                                    ${
                                        enlistmentData.beloning 
                                        ? `<p>Beloning: ${enlistmentData.beloning}</p>
                                            <p>${enlistmentData.leeftijd_vanaf} tot ${enlistmentData.leeftijd_tot} jaar</p>
                                            <p>${enlistmentData.titel}</p>`
                                        : ''
                                    }
                                    <p>Vanaf leeftijd: ${enlistmentData["leeftijd_vanaf"]}</p>
                                    <p>Tot leeftijd: ${enlistmentData["leeftijd_tot"]}</p>
                                <div>
                                
                            </div>
                            <form method="POST" id="detailsModal">
                                <input class="modal-btn" type="submit" name="submit" value="Accepteren">
                                <input class="modal-btn" type="submit" name="submit" value="Weigeren">
                            </form>
                `
      } else if (dataType === "research") {
        const research = responseData.researches[dataID - 1]
        // Moet nog aan gewerkt worden
        modalContent = `
        <div>
            <div class="modal-container">
                <div>
                    <h1>Onderzoek Details</h1>
                    <h2>Onderzoek</h2>
                    <p>titel: ${research.titel}</p>
                    <p>beschrijving: ${research.beschrijving}</p>
                    <p>datum: ${research.datum_vanaf} tot ${research.datum_tot}</p>
                    <p>type: ${research.onderzoek_type.toLowerCase()}</p>
                    
                    
                    ${
                        research.locatie
                        ? `<p>locatie: ${research.locatie}</p>`
                        : ''
                    }
                    
                    
                    ${
                        research.beloning 
                        ? `<p>Beloning: ${research.beloning}</p>
                            <p>${research.leeftijd_vanaf} tot ${research.leeftijd_tot} jaar</p>
                            <p>${research.titel}</p>`
                        : ''
                    }
                    
                </div>
                <div>
                    <h3>Organisatie</h3>
                    <p>${research.naam}</p>
                </div>
            </div>
            <form method="POST" id="detailsModal">
                <input class="modal-btn" type="submit" name="submit" value="Accepteren">
                <input class="modal-btn" type="submit" name="submit" value="Weigeren">
            </form>
        </div>
        `
      }

      const modal = document.createElement("div")
      modal.id = "detailsModal"
      modal.className = "modal"
      modal.innerHTML = `
                    <div class="modalForm">
                        <button class="close-btn" onclick="closeModal('detailsModal')">x</button>
                       ${modalContent}
                    </div>   
                `
      document.body.appendChild(modal)

      document
        .getElementById("detailsModal")
        .addEventListener("submit", function (event) {
          event.preventDefault()
          let status
          if (event.submitter.value === "Accepteren") {
            status = "GOEDGEKEURD"
          } else if (event.submitter.value === "Weigeren") {
            status = "AFGEKEURD"
          }

          editRequest(status, dataType, dataID)

          closeModal("detailsModal")
        })
    })
}

function editRequest(status, dataType, dataID) {
  fetch("/api/admin", {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${sessionStorage.getItem("accessToken")}`,
    },
    body: JSON.stringify({
      status: status,
      data_type: dataType,
      data_id: dataID,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data["error"] === "token_expired") {
        refreshAccessToken(editRequest, [status, dataType, dataID])
        return
      }
      if (data.success) {
        showSnackbar(data["message"], "success")
        loadTable()
      } else {
        showSnackbar(data["message"])
        loadTable()
      }
    })
}

window.addEventListener("load", function () {
  setInterval(loadTable, 5000)
})

loadTable()
