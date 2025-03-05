import {renderEnlistmentPage} from "./experts-dashboard/enlistments-page.js";
import {renderResearchPage} from "./experts-dashboard/research-page.js";

renderResearchPage();

export let intervalId;
// Render every 5 seconds
intervalId = setInterval(renderResearchPage, 5000);

function loadAjaxPage(renderFunc) {
    clearInterval(intervalId); // Clear interval currently active

    renderFunc(); //Load page immediately
    intervalId = setInterval(renderFunc, 5000); // Set interval for 5 sec
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
        loadAjaxPage(renderResearchPage)
    } else {
        researchSection.classList.add('hide');
        enlistmentsSection.classList.remove('hide');
        loadAjaxPage(renderEnlistmentPage);
    }
}

export function closeResearchModal() {
    const modal = document.querySelector('.js-research-modal-background')
    modal.classList.add('hide');
    // Empty the modal
    modal.innerHTML = '';
}

export function showResearchModal() {
    // Show the modal visually
    document.querySelector('.js-research-modal-background')
        .classList.remove('hide');

    // Close research modal event listener
    document.querySelector('.js-close-modal')
        .addEventListener('click', closeResearchModal);
}
