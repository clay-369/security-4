import {closeResearchModal, showResearchModal} from "../experts-dashboard.js";
import {get_enlistments_by_expert} from "./enlistments.js";


// TODO: Switch to sessions
const expertId = 1;

export async function renderResearchPage() {
    // Get all research items from server
    // Set parameters to which research items you need: available, status
    const response = await fetch('/api/onderzoeken');
    const allResearchItems = await response.json();

    // Create list with ids of research items that expert already interacted with
    const enlistments_by_expert = await get_enlistments_by_expert(expertId);

    const enlistedResearchIds = [];
    enlistments_by_expert.forEach(enlistment => enlistedResearchIds.push(enlistment.onderzoek_id));

    // Generate the HTML
    let html = '';
    allResearchItems.forEach(researchItem => {
        if (!enlistedResearchIds.includes(researchItem.onderzoek_id)) {
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
        }
    });

    // Setting the HTML
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

async function renderResearchModal(researchId) {
    // Getting research item from server
    const response = await fetch(`api/onderzoeken/${researchId}`)
    const researchItem = await response.json();

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

    showResearchModal();

    // Enlist event listener
    document.querySelector('.js-enlist-button')
        .addEventListener('click', () => {
            enlist(researchId);
        })
}

// Create enlistment in DB
function enlist(researchId) {
    fetch('/api/onderzoeken/inschrijvingen', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({research_id: researchId, expert_id: expertId})
        })
        .then(() => {
            closeResearchModal();
            renderResearchPage();
        });
}

