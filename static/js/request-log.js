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

      const adminsData = data.admins
      const expertsData = data.experts
      const expertsBody = document.querySelector("#requestLogTable tbody")

      // Dit stukje code is met behulp van ChatGPT gemaakt
      const adminLookup = adminsData.reduce((acc, admin) => {
          acc[admin.beheerder_id] = `${admin.voornaam} ${admin.achternaam}`;
          return acc;
        }, {});
      // Einde stukje code ChatGPT

      expertsData.forEach((expert) => {
        const row = document.createElement("tr")
        if (expert.status === "GOEDGEKEURD" || expert.status === "AFGEKEURD") {
            const adminName = adminLookup[expert.beheerder_id] || "Unknown Admin";

          row.innerHTML = `
                        <th scope="row"> ${expert.voornaam} ${expert.achternaam}</th>
                        <td> Registratie</td>
                        <td> ${expert.status}</td>
                        <td> ${adminName}</td>
                        `
          expertsBody.appendChild(row)
        }
      })

      const enlistmentData = data.enlistments
      const enlistmentBody = document.querySelector("#requestLogTable tbody")

      enlistmentData.forEach((enlistment) => {
        const row = document.createElement("tr")
        if (enlistment.status === "GOEDGEKEURD" || enlistment.status === "AFGEKEURD") {
          const adminName = adminLookup[enlistment.beheerder_id] || "Unknown Admin";

          row.innerHTML = `
                        <th scope="row">${enlistment.voornaam} ${enlistment.achternaam}</th>
                        <td>Onderzoek ${enlistment.titel}</td>
                        <td>${enlistment.status}</td>
                        <td> ${adminName}</td>
                        `
          enlistmentBody.appendChild(row)
        }
      })

      const researchData = data.researches
      const researchesBody = document.querySelector("#requestLogTable tbody")

      researchData.forEach((research) => {
        const row = document.createElement("tr")
        if (research.status === "GOEDGEKEURD" || research.status === "AFGEKEURD") {
          const adminName = adminLookup[research.beheerder_id] || "Unknown Admin";

          row.innerHTML = `
                        <th scope="row">${research.titel}</th>
                        <td>Onderzoek</td>
                        <td>${research.status}</td>
                        <td> ${adminName}</td>
                        `
          researchesBody.appendChild(row)
        }
      })
    })
}

loadTable()