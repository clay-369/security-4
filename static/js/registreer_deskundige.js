const disabilities = []
const research = []

// Show snackbar method
function showSnackbar(message, type = "error") {
  // Snackbar
  let snackbar = document.getElementById("snackbar")
  snackbar.className = "show"
  snackbar.innerHTML = message
  if (type === "error") {
    snackbar.style.backgroundColor = "#ff4444"
  } else if (type === "success") {
    snackbar.style.backgroundColor = "#3dbb56"
  }

  setTimeout(function () {
    snackbar.className = snackbar.className.replace("show", "")
  }, 3000)
}

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
          disabilities.push(disability)
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
})

document
  .getElementById("createDeskundige")
  .addEventListener("submit", function (event) {
    event.preventDefault()

    const voornaam = document.getElementById("voornaam").value
    const achternaam = document.getElementById("achternaam").value
    const email = document.getElementById("email").value
    const wachtwoord = document.getElementById("wachtwoord").value
    const postcode = document.getElementById("postcode").value
    const telefoonnummer = document.getElementById("telefoonnummer").value
    const geboortedatum = document.getElementById("geboortedatum").value
    const geslacht = document.getElementById("geslacht").value
    const type_beperking = document.getElementById("type-beperking").value
    const hulpmiddelen = document.getElementById("hulpmiddelen").value
    const introductie = document.getElementById("introductie").value
    const bijzonderheden = document.getElementById("bijzonderheden").value
    const toezichthouder = document.getElementById("toezichthouder").checked
    const akkoord = document.getElementById("akkoord").checked
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
    } else if (document.getElementsByName("voorkeur-benadering")[1].checked) {
      voorkeur_benadering = "E-mail"
    } else {
      voorkeur_benadering = ""
    }

    const bijzonderheden_beschikbaarheid = document.getElementById(
      "bijzonderheden-beschikbaarheid"
    ).value

    let deskundige_data = {
      voornaam: voornaam,
      achternaam: achternaam,
      email: email,
      wachtwoord: wachtwoord,
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
      akkoord: akkoord,
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
          console.log(data.message)
          showSnackbar(data.message, "success")
        } else {
          console.error(data.message)
          showSnackbar(data.message, "error")
        }
      })
      .catch((error) => {
        console.error("Error:", error)
        showSnackbar("Er is een fout opgetreden bij het registreren.", "error")
      })
  })
