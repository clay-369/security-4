import {renderResearchPage} from "./experts-dashboard/research-page.js";
import {renderEnlistmentPage} from "./experts-dashboard/enlistment-page.js";


// Get research items from database and call the render function
let allResearchItems = [];

fetch('/api/onderzoeken', {
    method: 'GET',
    headers: {
        'Accept': 'application/json'
    }
})
    .then(response => response.json())
    .then(data => allResearchItems = data)
    .then(() => {
        renderResearchPage(allResearchItems);
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

        renderResearchPage(allResearchItems);
    } else {
        researchSection.classList.add('hide');
        enlistmentsSection.classList.remove('hide');

        renderEnlistmentPage(allResearchItems);
    }
}
