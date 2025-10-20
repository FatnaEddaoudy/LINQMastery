document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.card').forEach(card => {
        const sizeButtons = card.querySelectorAll('.size-btn');
        const priceLabel = card.querySelector('.selectedPriceLabel');
        const sizeInput = card.querySelector('.selectedSizeInput');
        const priceContainer = card.querySelector('.selectedPriceContainer');

        if (!sizeInput || !priceLabel || !priceContainer) return;

        sizeButtons.forEach(btn => {
            btn.addEventListener('click', function () {
                // Reset all buttons in this card
                sizeButtons.forEach(b => b.classList.remove('bg-danger'));
                sizeButtons.forEach(b => b.classList.add('bg-secondary'));

                // Highlight clicked button
                this.classList.remove('bg-secondary');
                this.classList.add('bg-danger');

                // Update hidden input and label
                sizeInput.value = this.dataset.size;
                priceLabel.textContent = this.dataset.price;

                // Show the price container
                priceContainer.style.display = "block";
            });
        });
    });
});
