
slotCards = document.querySelectorAll('.slot-card');

slotCards.forEach(card => {
    const slotId = card.dataset.id;
    card.addEventListener("click", () => {
        console.log(`Slot ID: ${slotId}`);
        window.location.href = `/slot/${slotId}/`;
    });

});