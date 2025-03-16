import {closeResearchModal, showResearchModal} from "../experts-dashboard.js";
import {get_enlistments_by_expert} from "./enlistments.js";
import {renderEnlistmentPage} from "./enlistments-page.js";


export async function renderResearchPage() {
    // Get all research items from server
    // Set parameters to which research items you need: available, status
    fetch('/api/onderzoeken', {
        method: 'GET',
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${sessionStorage.getItem('accessToken')}`
        }
    })
        .then(response => response.json())
        .then(async allResearchItems => {

            if (allResearchItems['error'] === 'token_expired') {
                refreshAccessToken(renderResearchPage);
                return;
            }

            // Create list with ids of research items that expert already interacted with
            const enlistmentsByExpert = await get_enlistments_by_expert();
            if (enlistmentsByExpert['error'] === 'token_expired') {
                refreshAccessToken(renderResearchPage);
                return;
            }

            const enlistedResearchIds = [];

            enlistmentsByExpert.forEach(enlistment => enlistedResearchIds.push(enlistment.onderzoek_id));

            // Generate the HTML
            let html = '';
            allResearchItems.forEach(researchItem => {
                if (!enlistedResearchIds.includes(researchItem.onderzoek_id)) {
                    html += `
                    <div tabindex="0" class="research-container js-research-container" data-research-id="${researchItem.onderzoek_id}">
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
                    containerElement.addEventListener('keydown', (event) => {
                        if (event['key'] === 'Enter') {
                            renderResearchModal(researchId);
                        }
                    });
                });
        });
}

async function renderResearchModal(researchId) {
    // Getting research item from server
    fetch(`api/onderzoeken/${researchId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${sessionStorage.getItem('accessToken')}`
        }
    })
        .then(response => response.json())
        .then(researchItem => {

            if (researchItem['error'] === 'token_expired') {
                refreshAccessToken(renderResearchModal, researchId);
                return;
            }

            document.querySelector('.js-research-modal-background')
                .innerHTML = `
            <div class="research-modal">
                <img tabindex="0" class="close-modal js-close-modal" alt="Sluit Popup" src="../static/icons/xmark-solid.svg">
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
        });
}

// Create enlistment in DB
function enlist(researchId) {
    fetch('/api/onderzoeken/inschrijvingen', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${sessionStorage.getItem('accessToken')}`
            },
            body: JSON.stringify({research_id: researchId})
        })
        .then(response => response.json())
        .then((data) => {
            if (data['error'] === 'token_expired') {
                refreshAccessToken(enlist, researchId);
                return;
            }

            showSnackbar("U bent succesvol ingeschreven.", 'success');
            closeResearchModal();
            renderResearchPage();
        });
}

