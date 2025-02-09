import {renderResearchModal} from "./research-page.js";

// TODO: Switch to sessions
const expertId = 1;

export function renderEnlistmentPage(allResearchItems) {
    fetch('/api/onderzoeken/inschrijvingen', {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
        }
    })
        .then(response => response.json())
        .then(data => {
            renderPending(data, allResearchItems);
        });
}

function renderPending(enlistments, allResearchItems) {
    let html = '';

    enlistments.forEach((enlistment) => {
        if (enlistment['deskundige_id'] === expertId) {
            html += `
                <div class="enlistment">
                    <h3 class="enlistment-name">${enlistment['titel']}</h3>
                    <button class="enlistment-details-button js-enlistment-details-button" 
                        data-research-id="${enlistment['onderzoek_id']}"
                        data-enlistment-id="${enlistment['inschrijving_id']}"
                    >Details</button>
                </div>
            `;
        }
    })

    document.querySelector('.js-pending-enlistments')
        .innerHTML = html;

    // Eventlisteners
    document.querySelectorAll('.js-enlistment-details-button')
        .forEach(button => {
            const researchId = button.dataset.researchId;
            const enlistmentId = button.dataset.enlistmentId;

            button.addEventListener('click', () => {
                renderResearchModal(researchId, allResearchItems, enlistmentId);
            });
        });
}
