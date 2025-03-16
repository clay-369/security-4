import {closeResearchModal, showResearchModal, intervalId} from "../experts-dashboard.js";
import {get_enlistments_by_expert, get_filtered_enlistments_by_expert} from "./enlistments.js";


// Enlistment Page
export async function renderEnlistmentPage() {
    const enlistments = await get_enlistments_by_expert();

    if (enlistments['error'] === 'token_expired') {
        refreshAccessToken(renderEnlistmentPage);
        return;
    }
    renderPartitions(enlistments);
}

async function renderFilteredEnlistmentPage(search_words) {
    const enlistments = await get_filtered_enlistments_by_expert(search_words);
    if (enlistments['error'] === 'token_expired') {
        refreshAccessToken(renderFilteredEnlistmentPage, search_words);
        return;
    }
    renderPartitions(enlistments);
}

function renderPartitions(enlistments) {
    let pendingHTML = '';
    let acceptedHTML = '';
    let rejectedHTML = '';

    // Generating the HTML for each part
    enlistments.forEach((enlistment) => {
        // Pending
        if (enlistment['status'] === 'NIEUW') {
            pendingHTML += renderEnlistment(enlistment)
        }
        // Accpeted
        else if (enlistment['status'] === 'GOEDGEKEURD') {
            acceptedHTML += renderEnlistment(enlistment);
        }
        // Rejected
        else if (enlistment['status'] === 'AFGEKEURD') {
            rejectedHTML += renderEnlistment(enlistment);
        }
    })

    // Setting the HTML for each part
    document.querySelector('.js-pending-enlistments')
        .innerHTML = pendingHTML;

    document.querySelector('.js-accepted-enlistments')
        .innerHTML = acceptedHTML;

    document.querySelector('.js-rejected-enlistments')
        .innerHTML = rejectedHTML;

    // Adding Eventlisteners to open modal
    document.querySelectorAll('.js-enlistment-details-button')
        .forEach(button => {
            const researchId = button.dataset.researchId;
            const status = button.dataset.status;
            button.addEventListener('click', () => {
                renderEnlistmentModal(researchId, status);
            });
        });
}

function renderEnlistment(enlistment) {
    return `
                <div class="enlistment">
                    <h3 class="enlistment-name">${enlistment['titel']}</h3>
                    <button class="enlistment-details-button js-enlistment-details-button" 
                        data-research-id="${enlistment['onderzoek_id']}"
                        data-status="${enlistment['status']}"
                    >Details</button>
                </div>
            `;
}

async function renderEnlistmentModal(researchId, status) {
    // Get research item information from server
    const response = await fetch(`api/onderzoeken/${researchId}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${sessionStorage.getItem('accessToken')}`
        }
    })
    const researchItem = await response.json();

    if (researchItem['error'] === 'token_expired') {
        refreshAccessToken(renderEnlistmentModal, [researchId, status]);
        return;
    }

    // Generate the HTML
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
                    
                    <p>Status</p>
                    <p>${status.toLowerCase()}</p>
                </div>
                ${
                    status === 'NIEUW' || status === 'GOEDGEKEURD'
                    ? '<button class="research-modal-button red js-delist-button">Uitschrijven</button>'
                    : ''
                }
                    
            </div>
        `;

    showResearchModal();

    // Enlist event listener
    document.querySelector('.js-delist-button')
        .addEventListener('click', () => {
            delist(researchId);
        })
}

// Remove the enlistment from database
function delist(researchId) {
    fetch('/api/onderzoeken/inschrijvingen', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${sessionStorage.getItem('accessToken')}`
            },
            body: JSON.stringify({research_id: researchId})
        })
        .then(response => response.json())
        .then((data) => {

            if (data['error'] === 'token_expired') {
                refreshAccessToken(delist, researchId);
                return;
            }

            showSnackbar("U bent succesvol uitgeschreven.", "success");
            closeResearchModal();
            renderEnlistmentPage();
        })
}

// Search Bar functionality
const searchInputElem = document.querySelector('#enlistments-input');
searchInputElem.addEventListener('keydown', event => {
    if (event.key === 'Enter') {
        clearInterval(intervalId);
        const searchWords = searchInputElem.value;
        renderFilteredEnlistmentPage(searchWords);
    }
});