import {renderEnlistmentPage} from "./experts-dashboard/enlistments-page.js";


// TODO: Switch to sessions
const expertId = 1;

// Get research items from database and call the render function
let allResearchItems = [];

// Load all research items
fetch('/api/onderzoeken', {
    method: 'GET',
    headers: {
        'Accept': 'application/json'
    }
})
    .then(response => response.json())
    .then(data => allResearchItems = data)
    .then(() => {
        renderResearchPage();
    });

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

        renderEnlistmentPage();
    }
}


// TODO: Only show researches that have not been interacted with by this user

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
            renderResearchModal(researchId);
        });
    });
}

// Research Modal
function renderResearchModal(researchId) {
    fetch(`api/onderzoeken?research_id=${researchId}`, {
        method: 'GET',
        headers: {
            'Accept': 'apllication/json'
        }
    })
        .then(response => response.json())
        .then(researchItem => {
            document.querySelector('.js-research-modal-background')
                .innerHTML = `
                    <div class="research-modal">
                        <img class="close-modal js-close-modal" alt="Sluit Popup" src="../static/icons/xmark-solid.svg">
                        <h1 class="research-modal-title">${researchItem.titel}</h1>
                        <p class="research-modal-description">${researchItem.beschrijving}</p>
                        <h2 class="research-modal-organisation">Details</h2>
                        <div class="research-modal-details">
                            <p>Datum</p>
                            <p><time>${researchItem.datum_vanaf}</time> tot <time>${researchItem.datum_tot}</time></p>
                    
                            <p>Waar</p>
                            <p>${researchItem.onderzoek_type.toLowerCase()}</p>
                            
                            <p>Beloning</p>
                            <p>${researchItem.met_beloning ? researchItem.beloning : 'Zonder beloning'}</p>
                            
                            <p>Leeftijd</p>
                            <p>${researchItem.leeftijd_vanaf} tot ${researchItem.leeftijd_tot} jaar</p>
                            
                            <p>Organisatie</p>
                            <p>${researchItem.organisatie_naam}</p>
                        </div>
                        <button class="research-modal-button js-enlist-button">Inschrijven</button>
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
                    enlist(researchId);
                })
    });
}



export function closeResearchModal() {
    // TODO: remove instead of hide
    document.querySelector('.js-research-modal-background')
           .classList.add('hide');
}

function enlist(researchId) {
    fetch('/api/onderzoeken/inschrijvingen', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({research_id: researchId, expert_id: expertId})
        })
            .then(closeResearchModal);
}








