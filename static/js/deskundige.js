document
  .getElementById("createDeskundige")
  .addEventListener("submit", function (event) {
    event.preventDefault()

    const firstName = document.getElementById("voornaam").value
    const lastName = document.getElementById("achternaam").value
    const email = document.getElementById("email").value
    const password = document.getElementById("wachtwoord").value
    const postcode = document.getElementById("postcode").value
    const telefoonnummer = document.getElementById("telefoonnummer").value
    const geboortedatum = document.getElementById("geboortedatum").value
    const geslacht = document.getElementById("geslacht").value
    const type_beperking = document.getElementById("type-beperking").value
    const hulpmiddelen = document.getElementById("hulpmiddelen").value
    const introductie = document.getElementById("introductie").value
    const bijzonderheden = document.getElementById("bijzonderheden").value
    const toezichthouder = document.getElementById("toezichthouder").value
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

    deskundige_data = {
      first_name: firstName,
      last_name: lastName,
      email: email,
      password: password,
      postcode: postcode,
      telefoonnummer: telefoonnummer,
      geboortedatum: geboortedatum,
      geslacht: geslacht,
      type_beperking: type_beperking,
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

    fetch("/api/deskundige", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(deskundige_data),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          console.log("Deskundige gemaakt!")
        } else {
          console.log("Error!")
        }
      })
      .catch((error) => {
        console.error("Error:", error)
      })
  })

window.addEventListener("load", function () {
  fetch("/api/deskundige?id=1", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        console.log("Deskundige gevonden!")
        console.log(data.deskundige)
        document.getElementById("voornaam").value = data.deskundige.voornaam
        document.getElementById("achternaam").value = data.deskundige.achternaam
        document.getElementById("email").value = data.deskundige.email
        document.getElementById("wachtwoord").value = data.deskundige.wachtwoord
        document.getElementById("postcode").value = data.deskundige.postcode
        document.getElementById("telefoonnummer").value =
          data.deskundige.telefoonnummer
        document.getElementById("geboortedatum").value =
          data.deskundige.geboortedatum
        document.getElementById("geslacht").value = data.deskundige.geslacht
        document.getElementById("type-beperking").value =
          data.deskundige.type_beperking
        document.getElementById("hulpmiddelen").value =
          data.deskundige.hulpmiddelen
        document.getElementById("introductie").value =
          data.deskundige.introductie
        document.getElementById("bijzonderheden").value =
          data.deskundige.bijzonderheden
        document.getElementById("toezichthouder").value =
          data.deskundige.toezichthouder
        document.getElementById("toezichthouder-naam").value =
          data.deskundige.toezichthouder_naam
        document.getElementById("toezichthouder-email").value =
          data.deskundige.toezichthouder_email
        document.getElementById("toezichthouder-telefoonnummer").value =
          data.deskundige.toezichthouder_telefoonnummer
        document.getElementById("type-onderzoek").value =
          data.deskundige.type_onderzoek
        document.getElementById("voorkeur-benadering").value =
          data.deskundige.voorkeur_benadering
        document.getElementById("bijzonderheden-beschikbaarheid").value =
          data.deskundige.bijzonderheden_beschikbaarheid
      } else {
        console.log("Error!")
      }
    })
    .catch((error) => {
      console.error("Error:", error)
    })
})
