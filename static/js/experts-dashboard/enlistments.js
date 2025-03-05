export async function get_enlistments_by_expert(expertId) {
    const response = await fetch(`/api/onderzoeken/inschrijvingen/${expertId}`);
    return await response.json();
}

export async function get_filtered_enlistments_by_expert(expertId, search_words) {
    const response = await fetch(`/api/onderzoeken/inschrijvingen/${expertId}?search=${search_words}`);
    return await response.json();
}

