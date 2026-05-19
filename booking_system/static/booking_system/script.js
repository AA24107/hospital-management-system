
slotCards = document.querySelectorAll('.slot-card');

slotCards.forEach(card => {
    //const slotId = card.getAttribute('data-slot-id');
    card.addEventListener("click", () => {
        console.log(`Slot ID: ${slotId}`);
        window.location.href = `/slot/${slotId}/`;
    });

});