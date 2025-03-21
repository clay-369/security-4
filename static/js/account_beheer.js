// Toezichthouder checkbox
// Global variable
let toezichthouder = false

document
  .getElementById("geboortedatum")
  .addEventListener("change", function () {
    const dateToday = new Date()
    const dateOfBirth = new Date(this.value)
    const age = dateToday.getFullYear() - dateOfBirth.getFullYear()

    if (age < 18) {
      showSnackbar("U moet een voogd hebben om te registreren.", "error")
      document.getElementById("toezichthouder-wrapper").style.display = "block"
      toezichthouder = true
      return
    } else {
      document.getElementById("toezichthouder-wrapper").style.display = "none"
      toezichthouder = false
    }
  })

// Load type of disablities
window.addEventListener("load", function () {
  fetch("/api/deskundige/beperkingen", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${sessionStorage.getItem("accessToken")}`,
    },
  })
    .then((response) => response.json())
    .then((dis) => {
      const disabilityIds = dis["disability_ids"]
      fetch("/api/disabilities", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            data["disabilities"].forEach((disability) => {
              const insideLabelHTML = `
                    <input type="checkbox" value="${
                      disability.beperking_id
                    }" class="disability-checkbox-${
                disability.beperking_id
              }" tabindex="-1"
                    ${
                      disabilityIds.includes(disability.beperking_id)
                        ? 'checked="checked"'
                        : ""
                    }
                    >
                    <span class="checkmark dropdown-checkmark"></span>
                `

              const label = document.createElement("label")
              label.classList.add("checkbox-container")
              label.tabIndex = 0
              label.innerHTML = insideLabelHTML
              label.innerHTML += disability.beperking
              label.addEventListener("keydown", (event) => {
                if (event["key"] === "Enter") {
                  let checkbox = document.querySelector(
                    `.disability-checkbox-${disability.beperking_id}`
                  )
                  checkbox.checked = !checkbox.checked
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
})

window.addEventListener("load", function () {
  fillPage()
})

function fillPage() {
  fetch("/api/deskundige", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${sessionStorage.getItem("accessToken")}`,
    },
  })
    .then((response) => response.json())
    .then((expert) => {
      if (expert["error"] === "token_expired") {
        refreshAccessToken(fillPage)
        return
      }
      // Update the title and input fields with the user data
      document.getElementById(
        "naam-title"
      ).textContent = `${expert.voornaam} ${expert.achternaam}`
      document.getElementById("voornaam").value = expert.voornaam
      document.getElementById("achternaam").value = expert.achternaam
      document.getElementById("email").value = expert.email
      document.getElementById("postcode").value = expert.postcode
      document.getElementById("geboortedatum").value = expert.geboortedatum
      document.getElementById("geslacht").value = expert.geslacht
      document.getElementById("telefoonnummer").value = expert.telefoonnummer
      document.getElementById("type-beperking").value = expert.type_beperking
      document.getElementById("hulpmiddelen").value = expert.hulpmiddelen
      document.getElementById("introductie").value = expert.introductie
      document.getElementById("bijzonderheden").value = expert.bijzonderheden
      document.getElementById("toezichthouder-naam").value =
        expert.toezichthouder_naam
      document.getElementById("toezichthouder-email").value =
        expert.toezichthouder_email
      document.getElementById("toezichthouder-telefoonnummer").value =
        expert.toezichthouder_telefoonnummer
      document.getElementById("type-onderzoek").value = expert.type_onderzoeken
      document.getElementById("bijzonderheden-beschikbaarheid").value =
        expert.bijzonderheden_beschikbaarheid
      if (expert.voorkeur_benadering === "TELEFONISCH") {
        document.getElementById("preference-email").checked = false
        document.getElementById("preference-telefoon").checked = true
      } else {
        document.getElementById("preference-email").checked = true
        document.getElementById("preference-telephone").checked = false
      }

      if (expert.toezichthouder == true) {
        document.getElementById("toezichthouder-wrapper").style.display =
          "block"
        toezichthouder = true
      } else {
        document.getElementById("toezichthouder-wrapper").style.display = "none"
        toezichthouder = false
      }
    })
    .catch((error) => {
      console.error("Error:", error)
    })
}

function submitEdit() {
    const firstName = document.getElementById("voornaam").value
    const lastName = document.getElementById("achternaam").value
    const email = document.getElementById("email").value
    let password = document.getElementById("wachtwoord").value
    if (password === "") {
      password = null
    }
    const postcode = document.getElementById("postcode").value.toUpperCase()
    const telefoonnummer = document.getElementById("telefoonnummer").value
    const geboortedatum = document.getElementById("geboortedatum").value
    const geslacht = document.getElementById("geslacht").value
    const hulpmiddelen = document.getElementById("hulpmiddelen").value
    const introductie = document.getElementById("introductie").value
    const bijzonderheden = document.getElementById("bijzonderheden").value
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

    const beperkingen = collectSelectedDisabilities()
    if (beperkingen.length < 1) {
      showSnackbar("Selecteer alstublieft een beperking.")
      return
    }

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
      beperkingen: beperkingen,
    }

    const { success, message } = check_account(deskundige_data)
    if (!success) {
      showSnackbar(message, "error")
      return
    }

    editExpert(deskundige_data)
  }

function editExpert(expertData) {
  fetch("/api/deskundige", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${sessionStorage.getItem("accessToken")}`,
    },
    body: JSON.stringify(expertData),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data["error"] === "token_expired") {
        refreshAccessToken(editExpert, expertData)
        return
      }
      if (data.success) {
        showSnackbar("Deskundige gewijzigd!", "success")
        fillPage();
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

function check_account(deskundige) {
  const neccesary_fields = [
    "email",
    "wachtwoord",
    "voornaam",
    "achternaam",
    "postcode",
    "telefoonnummer",
    "geboortedatum",
    "introductie",
    "voorkeur_benadering",
    "type_beperking",
  ]
  const email_regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  const wachtwoord_regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/
  const telefoonnummer_regex = /^\d{10}$/
  const postcode_regex = /^[1-9][0-9]{3} ?[A-Z]{2}$/

  if (deskundige["voorkeur_benadering"] == "") {
    return {
      success: false,
      message: "U moet een voorkeur benadering selecteren.",
    }
  }

  if (deskundige["introductie"].length < 10) {
    return {
      success: false,
      message: "Vertel wat meer in je introductie.",
    }
  }

  if (deskundige["akkoord"] == false) {
    return {
      success: false,
      message: "U moet akkoord gaan met de voorwaarden en privacy.",
    }
  }

  if (toezichthouder == true) {
    neccesary_fields.push("toezichthouder_naam")
    neccesary_fields.push("toezichthouder_email")
    neccesary_fields.push("toezichthouder_telefoonnummer")

    if (deskundige["toezichthouder_naam"] == "") {
      return {
        success: false,
        message:
          "U moet een naam invullen voor de toezichthouder omdat u toezichthouder heeft geselecteerd.",
      }
    }

    if (deskundige["toezichthouder_email"] == "") {
      return {
        success: false,
        message:
          "U moet een e-mailadres invullen voor de toezichthouder omdat u toezichthouder heeft geselecteerd.",
      }
    }

    if (deskundige["toezichthouder_telefoonnummer"] == "") {
      return {
        success: false,
        message:
          "U moet een telefoonnummer invullen voor de toezichthouder omdat u toezichthouder heeft geselecteerd.",
      }
    }
  }

  if (!email_regex.test(deskundige["email"])) {
    return {
      success: false,
      message: "U moet een geldig e-mailadres invullen.",
    }
  }
    console.log(deskundige['wachtwoord'])

    if (deskundige['wachtwoord'] !== '' && deskundige['wachtwoord'] !== null) {
        if (!wachtwoord_regex.test(deskundige["wachtwoord"])) {
            return {
                success: false,
                message:
                    "Het wachtwoord moet minimaal 8 tekens lang zijn, ten minste één kleine letter, één hoofdletter en één cijfer bevatten. Het mag alleen letters en cijfers bevatten.",
            }
        }
    }

  if (!telefoonnummer_regex.test(deskundige["telefoonnummer"])) {
    return {
      success: false,
      message: "U moet een geldig telefoonnummer invullen.",
    }
  }

  if (!postcode_regex.test(deskundige["postcode"])) {
    return {
      success: false,
      message: "U moet een geldige postcode invullen.",
    }
  }

  if (deskundige["type_onderzoek"] == "") {
    return {
      success: false,
      message: "U moet een type onderzoek selecteren.",
    }
  }

  for (const field of neccesary_fields) {
    if (deskundige[field] == "") {
      return {
        success: false,
        message: `Het veld ${field} is verplicht.`,
      }
    }
  }

  return {
    success: true,
    message: "Account is geldig.",
  }
}
