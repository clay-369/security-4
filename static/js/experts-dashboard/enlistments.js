export async function get_enlistments_by_expert(expertId) {
    const response = await fetch(`/api/onderzoeken/inschrijvingen?expert_id=${expertId}`);
    const enlistments = await response.json();

    return enlistments;
}

