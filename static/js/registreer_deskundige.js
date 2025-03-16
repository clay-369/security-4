const disabilities = []
const research = []

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
          const checkbox = document.createElement("input")
          checkbox.type = "checkbox"
          checkbox.value = disability.beperking_id
          checkbox.classList.add(
            `disability-checkbox-${disability.beperking_id}`
          )
          checkbox.tabIndex = -1
          checkbox.checked = true;

          const checkmarkSpan = document.createElement("span")
          checkmarkSpan.classList.add("checkmark")
          checkmarkSpan.classList.add("dropdown-checkmark")

          const label = document.createElement("label")
          label.classList.add("checkbox-container")
          label.tabIndex = 0

          label.appendChild(checkbox)
          label.appendChild(checkmarkSpan)
          label.innerHTML += disability.beperking
          label.addEventListener("keydown", (event) => {
            if (event["key"] === "Enter") {
              let checkbox = document.querySelector(`.disability-checkbox-${disability.beperking_id}`);
              checkbox.checked = !checkbox.checked;
            }
          })

          document.getElementById("disability-dropdown").appendChild(label)
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
  .addEventListener("click", function (event) {
    event.preventDefault()

    const voornaam = document.getElementById("voornaam").value
    const achternaam = document.getElementById("achternaam").value
    const email = document.getElementById("email").value
    const wachtwoord = document.getElementById("wachtwoord").value
    const postcode = document.getElementById("postcode").value
    const telefoonnummer = document.getElementById("telefoonnummer").value
    const geboortedatum = document.getElementById("geboortedatum").value
    const geslacht = document.getElementById("geslacht").value
    let hulpmiddelen = document.getElementById("hulpmiddelen").value
    if (hulpmiddelen === "") {
      hulpmiddelen = null
    }
    const introductie = document.getElementById("introductie").value
    let bijzonderheden = document.getElementById("bijzonderheden").value
    if (bijzonderheden === "") {
      bijzonderheden = null
    }
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
    const beperkingen = collectSelectedDisabilities()
    if (beperkingen.length < 1) {
      showSnackbar("Selecteer alstublieft een beperking.")
      return
    }
    const type_onderzoek = document.getElementById("type-onderzoek").value
    let voorkeur_benadering = ""
    if (document.getElementsByName("voorkeur-benadering")[0].checked) {
      voorkeur_benadering = "Telefoon"
    } else if (document.getElementsByName("voorkeur-benadering")[1].checked) {
      voorkeur_benadering = "E-mail"
    } else {
      voorkeur_benadering = ""
    }

    let bijzonderheden_beschikbaarheid = document.getElementById(
      "bijzonderheden-beschikbaarheid"
    ).value
    if (bijzonderheden_beschikbaarheid === "") {
      bijzonderheden_beschikbaarheid = null
    }

    let deskundige_data = {
      voornaam: voornaam,
      achternaam: achternaam,
      email: email,
      wachtwoord: wachtwoord,
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
      akkoord: akkoord,
      beperkingen: beperkingen,
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

function collectSelectedDisabilities() {
  const checkboxes = document.querySelectorAll(
    '.dropdown-content input[type="checkbox"]'
  )

  const selectedDisabilities = []
  checkboxes.forEach((checkbox) => {
    if (checkbox.checked) {
      selectedDisabilities.push(checkbox.value)
    }
  })

  return selectedDisabilities
}

function toggleDisabilityDropdown() {
  const containerElem = document.querySelector(
    ".js-disability-dropdown-container"
  )

  if (containerElem.classList.contains("show-dropdown")) {
    containerElem.classList.remove("show-dropdown")
  } else {
    containerElem.classList.add("show-dropdown")
  }
}
