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

window.addEventListener("load", function () {
  console.log("Wel in deze functie!")
})

// Load type of disablities
// window.addEventListener("load", function () {
//   console.log("Wel in deze functie!")
//   fetch("/api/disabilities", {
//     method: "GET",
//     headers: {
//       "Content-Type": "application/json",
//     },
//   })
//     .then((response) => response.json())
//     .then((data) => {
//       if (data.success) {
//         data.disabilities.forEach((disability) => {
//           const option = document.createElement("option")
//           option.value = disability.beperking_id
//           option.textContent = disability.beperking
//           document.getElementById("type-beperking").appendChild(option)
//         })
//       } else {
//         console.error(data.message)
//       }
//     })
//     .catch((error) => {
//       console.error("Error:", error)
//     })

//   fetch("/api/research", {
//     method: "GET",
//     headers: {
//       "Content-Type": "application/json",
//     },
//   })
//     .then((response) => response.json())
//     .then((data) => {
//       console.log(data)
//       const addedTypes = new Set()
//       data.research.forEach((research) => {
//         if (!addedTypes.has(research.onderzoek_type)) {
//           const option = document.createElement("option")
//           option.value = research.onderzoek_id
//           option.textContent = research.onderzoek_type
//           document.getElementById("type-onderzoek").appendChild(option)
//           addedTypes.add(research.onderzoek_type)
//         }
//       })
//     })
//     .catch((error) => {
//       console.error("Error:", error)
//     })
// })

window.addEventListener("load", function () {
  console.log("Wel in deze functie!")
  // fetch("/api/deskundige?id=1", {
  //   method: "GET",
  //   headers: {
  //     "Content-Type": "application/json",
  //   },
  // })
  //   .then((response) => response.json())
  //   .then((data) => {
  //     if (data.success) {
  //       console.log("Deskundige gevonden!")
  //       console.log(data.deskundige)
  //       document.getElementById("voornaam").value = data.deskundige.voornaam
  //       document.getElementById("achternaam").value = data.deskundige.achternaam
  //       document.getElementById("email").value = data.deskundige.email
  //       document.getElementById("wachtwoord").value = data.deskundige.wachtwoord
  //       document.getElementById("postcode").value = data.deskundige.postcode
  //       document.getElementById("telefoonnummer").value =
  //         data.deskundige.telefoonnummer
  //       document.getElementById("geboortedatum").value =
  //         data.deskundige.geboortedatum
  //       document.getElementById("geslacht").value = data.deskundige.geslacht
  //       document.getElementById("type-beperking").value =
  //         data.deskundige.type_beperking
  //       document.getElementById("hulpmiddelen").value =
  //         data.deskundige.hulpmiddelen
  //       document.getElementById("introductie").value =
  //         data.deskundige.introductie
  //       document.getElementById("bijzonderheden").value =
  //         data.deskundige.bijzonderheden
  //       document.getElementById("toezichthouder").value =
  //         data.deskundige.toezichthouder
  //       document.getElementById("toezichthouder-naam").value =
  //         data.deskundige.toezichthouder_naam
  //       document.getElementById("toezichthouder-email").value =
  //         data.deskundige.toezichthouder_email
  //       document.getElementById("toezichthouder-telefoonnummer").value =
  //         data.deskundige.toezichthouder_telefoonnummer
  //       document.getElementById("type-onderzoek").value =
  //         data.deskundige.type_onderzoek
  //       // document.getElementById("voorkeur-benadering").value =
  //       //   data.deskundige.voorkeur_benadering
  //       document.getElementById("bijzonderheden-beschikbaarheid").value =
  //         data.deskundige.bijzonderheden_beschikbaarheid
  //     } else {
  //       console.log("Error!")
  //     }
  //   })
  //   .catch((error) => {
  //     console.error("Error:", error)
  //   })
})
document
  .getElementById("updateDeskundige")
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
      deskundige_id: 1,
      voornaam: firstName,
      achternaam: lastName,
      email: email,
      wachtwoord: password,
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

    fetch("/api/deskundige?id=1", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(deskundige_data),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          console.log("Deskundige gewijzigd!")
        } else {
          console.log("Error!")
        }
      })
      .catch((error) => {
        console.error("Error:", error)
      })
  })
