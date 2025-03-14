document.querySelector('.js-submit')
    .addEventListener('click', () => {
        const collectedInfo = collectInfo();
        if (collectedInfo) {
            createOrganisation(collectedInfo);
        }
    });

function collectInfo() {
    const name = document.querySelector('#name').value;
    const organisationType = document.querySelector('#organisation-type').value;
    const website = document.querySelector('#website').value;
    const contactPerson = document.querySelector('#contact-person').value;
    const description = document.querySelector('#description').value;
    const email = document.querySelector('#email').value;
    const phoneNumber = document.querySelector('#phone-number').value;
    const password = document.querySelector('#password').value;
    let details = document.querySelector('#details').value;
    if (details === '') {
        details = null;
    }

    if (!name) {
        showSnackbar("Vul een naam in");
        return false;
    }
    if (!website) {
        showSnackbar("Vul een website in");
        return false;
    }
    if (!contactPerson) {
        showSnackbar("Vul een contact persoon in");
        return false;
    }
    if (!email) {
        showSnackbar("Vul een email adres in");
        return false;
    }
    if (!phoneNumber) {
        showSnackbar("Vul een telefoonnummer in");
        return false;
    }
    if (!password) {
        showSnackbar("Vul een wachtwoord in");
        return false;
    }

    return {name, "organisation_type": organisationType, website, "contact_person": contactPerson,
        description, email, "phone_number": phoneNumber, password, details};
}

function createOrganisation(data) {
    fetch('/api/organisatie', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${sessionStorage.getItem('accessToken')}`
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data['error'] === 'token_expired') {
                window.location.replace("/logout");
            }
            const type = data['success'] ? 'success' : 'error'
            showSnackbar(data['message'], type);

            if (data['success']) {
                clearInputs();
            }
        });
}

function clearInputs() {
    document.querySelector('#name').value = '';
    document.querySelector('#website').value = '';
    document.querySelector('#contact-person').value = '';
    document.querySelector('#description').value = '';
    document.querySelector('#email').value = '';
    document.querySelector('#phone-number').value = '';
    document.querySelector('#password').value = '';
    document.querySelector('#details').value = '';
}