export async function get_enlistments_by_expert() {
    const response = await fetch(`/api/onderzoeken/inschrijvingen/deskundige`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${sessionStorage.getItem('accessToken')}`
        }
    });
    return await response.json();
}

export async function get_filtered_enlistments_by_expert(search_words) {
    const response = await fetch(`/api/onderzoeken/inschrijvingen/deskundige?search=${search_words}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${sessionStorage.getItem('accessToken')}`
        }
    });
    return await response.json();
}

