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
    } else {
        researchSection.classList.add('hide');
        enlistmentsSection.classList.remove('hide');
    }
}

// Close research modal
document.querySelector('.js-close-modal')
    .addEventListener('click', () => {
        document.querySelector('.js-research-modal-background')
           .classList.add('hide');
    });

// Open research modal
document.querySelectorAll('.js-research-container')
    .forEach(containerElement => {
        containerElement.addEventListener('click', () => {
            document.querySelector('.js-research-modal-background')
                .classList.remove('hide');
        });
    });