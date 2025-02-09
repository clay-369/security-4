let allResearchItems = [];

fetch('/api/onderzoeken', {
    method: 'GET',
    headers: {
        'Accept': 'application/json'
    }
})
    .then(response => response.json())
    .then(data => allResearchItems = data)
    .then(renderResearchPage);

// Research page
function renderResearchPage() {
    let html = '';
    allResearchItems.forEach(researchItem => {
        html += `
            <div class="research-container js-research-container" data-research-id="${researchItem.onderzoek_id}">
                <h2 class="research-title">${researchItem.titel}</h2>
                <div class="research-details">
                    <p><time>${researchItem.datum_vanaf}</time> tot <time>${researchItem.datum_tot}</time></p>
                    <p>${researchItem.onderzoek_type.toLowerCase()}</p>
                </div>
                <div class="research-details">
                    <p>${researchItem.met_beloning ? 'Met beloning' : 'Zonder beloning'}</p>
                    <p>${researchItem.organisatie_naam}</p>
                </div>
            </div>
        `;
    });

    document.querySelector('.js-research-grid-container')
        .innerHTML = html;

    // Open research modal event listener
    document.querySelectorAll('.js-research-container')
    .forEach(containerElement => {
        const researchId = containerElement.dataset.researchId;

        containerElement.addEventListener('click', () => {
            renderResearchModal(Number(researchId));
        });
    });
}


// Page toggler
document.querySelectorAll('.js-page-toggler')
    .forEach(togglerElement => {
        togglerElement.addEventListener('click' , () => {
            toggleSections();
        });
    });

function toggleSections() {
    const researchSection = document.querySelector('.js-research-section');
    const enlistmentsSection = document.querySelector('.js-enlistments-section');

    if (researchSection.classList.contains('hide')) {
        researchSection.classList.remove('hide');
        enlistmentsSection.classList.add('hide');

        renderResearchPage();
    } else {
        researchSection.classList.add('hide');
        enlistmentsSection.classList.remove('hide');
    }
}

// Research Modal
function renderResearchModal(researchId) {
    let matchingResearchItem;

    allResearchItems.forEach(researchItem => {
        if (researchItem.onderzoek_id === researchId) {
            matchingResearchItem = researchItem;
        }
    });

    document.querySelector('.js-research-modal-background')
        .innerHTML = `
            <div class="research-modal">
                <img class="close-modal js-close-modal" alt="Sluit Popup" src="../static/icons/xmark-solid.svg">
                <h1 class="research-modal-title">${matchingResearchItem.titel}</h1>
                <p class="research-modal-description">${matchingResearchItem.beschrijving}</p>
                <h2 class="research-modal-organisation">Details</h2>
                <div class="research-modal-details">
                    <p>Datum</p>
                    <p><time>${matchingResearchItem.datum_vanaf}</time> tot <time>${matchingResearchItem.datum_tot}</time></p>
            
                    <p>Waar</p>
                    <p>${matchingResearchItem.onderzoek_type.toLowerCase()}</p>
                    
                    <p>Beloning</p>
                    <p>${matchingResearchItem.met_beloning ? matchingResearchItem.beloning : 'Zonder beloning'}</p>
                    
                    <p>Leeftijd</p>
                    <p>${matchingResearchItem.leeftijd_vanaf} tot ${matchingResearchItem.leeftijd_tot} jaar</p>
                    
                    <p>Organisatie</p>
                    <p>${matchingResearchItem.organisatie_naam}</p>
                </div>
                <button class="research-modal-enlist js-enlist-button">Inschrijven</button>
            </div>
        `;

    document.querySelector('.js-research-modal-background')
                .classList.remove('hide');

    // Close research modal event listener
    document.querySelector('.js-close-modal')
    .addEventListener('click', closeResearchModal);

    // Enlist event listener
    document.querySelector('.js-enlist-button')
        .addEventListener('click', () => {

            const expertId = 1 // TODO: Use expertId from session

            fetch('/api/onderzoeken/inschrijvingen', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({research_id: researchId, expert_id: expertId})
            })
                .then(closeResearchModal)
        })
}


function closeResearchModal() {
    document.querySelector('.js-research-modal-background')
           .classList.add('hide');
}