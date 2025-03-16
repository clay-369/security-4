// Toezichthouder checkbox
document
  .getElementById("toezichthouder")
  .addEventListener("change", function () {
    if (this.checked) {
      document.getElementById("toezichthouder-container").style.display =
        "block"
    } else {
      document.getElementById("toezichthouder-container").style.display = "none"
    }
  })

// Load type of disablities
window.addEventListener("load", function () {
  fetch("/api/disabilities", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        data.disabilities.forEach((disability) => {
          const option = document.createElement("option")
          option.value = disability.beperking_id
          option.textContent = disability.beperking
          document.getElementById("type-beperking").appendChild(option)
        })
      } else {
        console.error(data.message)
      }
    })
    .catch((error) => {
      console.error("Error:", error)
    })


    const addedTypes = new Set();
    ['Op locatie', 'Telefonisch', 'Online'].forEach((researchType) => {
      const option = document.createElement("option")
      option.value = researchType.toUpperCase()
      option.textContent = researchType
      document.getElementById("type-onderzoek").appendChild(option)
      addedTypes.add(researchType)
    })
})

window.addEventListener("load", function () {
    fillPage();
})

function fillPage() {
    fetch("/api/deskundige", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${sessionStorage.getItem('accessToken')}`
        },
    })
        .then((response) => response.json())
        .then((expert) => {
            if (expert['error'] === 'token_expired') {
                refreshAccessToken(fillPage);
                return;
            }
            // Update the title and input fields with the user data
            document.getElementById("naam-title").textContent = `${expert.voornaam} ${expert.achternaam}`;
            document.getElementById("voornaam").value = expert.voornaam
            document.getElementById("achternaam").value = expert.achternaam
            document.getElementById("email").value = expert.email
            document.getElementById("postcode").value = expert.postcode
            document.getElementById("telefoonnummer").value =
                expert.telefoonnummer
            document.getElementById("geboortedatum").value =
                expert.geboortedatum
            document.getElementById("type-beperking").value =
                expert.type_beperking
            document.getElementById("hulpmiddelen").value =
                expert.hulpmiddelen
            document.getElementById("introductie").value =
                expert.introductie
            document.getElementById("bijzonderheden").value =
                expert.bijzonderheden
            document.getElementById("toezichthouder").value =
                expert.toezichthouder
            document.getElementById("toezichthouder-naam").value =
                expert.toezichthouder_naam
            document.getElementById("toezichthouder-email").value =
                expert.toezichthouder_email
            document.getElementById("toezichthouder-telefoonnummer").value =
                expert.toezichthouder_telefoonnummer
            document.getElementById("type-onderzoek").value =
                expert.type_onderzoek
            document.getElementById("bijzonderheden-beschikbaarheid").value =
                expert.bijzonderheden_beschikbaarheid
            if (expert.voorkeur_benadering === "telefoon") {
                document.getElementById("preference-email").checked = false
                document.getElementById("preference-telefoon").checked = true
            } else {
                document.getElementById("preference-email").checked = true
                document.getElementById("preference-telephone").checked = false
            }
        })
        .catch((error) => {
            console.error("Error:", error)
        })
}

document
  .getElementById("updateDeskundige")
  .addEventListener("submit", function (event) {
    event.preventDefault()

    const firstName = document.getElementById("voornaam").value
    const lastName = document.getElementById("achternaam").value
    const email = document.getElementById("email").value
    let password = document.getElementById("wachtwoord").value
    if (password === '') {
        password = null;
    }
    const postcode = document.getElementById("postcode").value
    const telefoonnummer = document.getElementById("telefoonnummer").value
    const geboortedatum = document.getElementById("geboortedatum").value
    const geslacht = document.getElementById("geslacht").value
    const hulpmiddelen = document.getElementById("hulpmiddelen").value
    const introductie = document.getElementById("introductie").value
    const bijzonderheden = document.getElementById("bijzonderheden").value
    const toezichthouder = document.getElementById("toezichthouder").checked
    const toezichthouder_naam = document.getElementById(
      "toezichthouder-naam"
    ).value
    const toezichthouder_email = document.getElementById(
      "toezichthouder-email"
    ).value
    const toezichthouder_telefoonnummer = document.getElementById(
      "toezichthouder-telefoonnummer"
    ).value
    const type_onderzoek = document.getElementById("type-onderzoek").value
    let voorkeur_benadering = ""
    if (document.getElementsByName("voorkeur-benadering")[0].checked) {
      voorkeur_benadering = "Telefoon"
    } else {
      voorkeur_benadering = "E-mail"
    }
    const bijzonderheden_beschikbaarheid = document.getElementById(
      "bijzonderheden-beschikbaarheid"
    ).value

    let deskundige_data = {
      voornaam: firstName,
      achternaam: lastName,
      email: email,
      wachtwoord: password,
      postcode: postcode,
      telefoonnummer: telefoonnummer,
      geboortedatum: geboortedatum,
      geslacht: geslacht,
      hulpmiddelen: hulpmiddelen,
      introductie: introductie,
      bijzonderheden: bijzonderheden,
      toezichthouder: toezichthouder,
      toezichthouder_naam: toezichthouder_naam,
      toezichthouder_email: toezichthouder_email,
      toezichthouder_telefoonnummer: toezichthouder_telefoonnummer,
      type_onderzoek: type_onderzoek,
      voorkeur_benadering: voorkeur_benadering,
      bijzonderheden_beschikbaarheid: bijzonderheden_beschikbaarheid,
    }

    editExpert(deskundige_data);
  })

function editExpert(expertData) {
    fetch("/api/deskundige", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${sessionStorage.getItem('accessToken')}`
        },
        body: JSON.stringify(expertData),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data['error'] === 'token_expired') {
                refreshAccessToken(editExpert, expertData);
                return;
            }
            if (data.success) {
                showSnackbar("Deskundige gewijzigd!", "success")
            } else {
                console.error(data.message)
                showSnackbar(data.message, "error")
            }
        })
        .catch((error) => {
            console.error("Error:", error)
            showSnackbar(
                "Er is een fout opgetreden bij het wijzigen van de deskundige.",
                "error"
            )
        })
}
