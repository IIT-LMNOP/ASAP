
let selectedAmounts = {};

function selectAmount(button, amount) {
    const card = button.closest('.donation-card');
    const allButtons = card.querySelectorAll('.amount-btn');
    allButtons.forEach(btn => btn.classList.remove('selected'));

    button.classList.add('selected');

    const category = card.querySelector('.card-title').textContent.toLowerCase().replace(/\s+/g, '-').replace('&', 'and');
    selectedAmounts[category] = amount;
}

function donate(category) {
    let amount = selectedAmounts[category.toLowerCase()];

    if (category === 'general') {
        amount = prompt('Enter your donation amount (₹):');
        if (!amount || isNaN(amount) || amount <= 0) {
            alert('Please enter a valid amount.');
            return;
        }
    } else if (!amount) {
        alert('Please select a donation amount first.');
        return;
    }

    const categoryNames = {
        'holistic': 'Holistic Development',
        'infrastructure': 'Infrastructure Support',
        'financial': 'Student Financial Support',
        'corporate': 'Alumni & Corporate Connect',
        'culture': 'Art & Culture',
        'sports': 'Sports & Athletics',
        'entrepreneurship': 'Entrepreneurship Support',
        'general': 'General Fund'
    };

    const categoryName = categoryNames[category] || category;

    if (confirm(`Proceed with donation of ₹${amount.toLocaleString()} to ${categoryName}?`)) {
        alert(`Thank you for your generous donation of ₹${amount.toLocaleString()} to ${categoryName}!\n\nYou will receive a tax-deductible receipt and updates on how your contribution is making a difference.`);
    }
}

// Initialize animations
document.addEventListener('DOMContentLoaded', function () {
    const cards = document.querySelectorAll('.donation-card');
    cards.forEach((card, index) => {
        card.classList.add('fade-in');
        card.style.animationDelay = `${index * 0.1}s`;
    });

    // Header scroll effect
    window.addEventListener('scroll', function () {
        const header = document.querySelector('.header');
        if (window.scrollY > 50) {
            header.style.background = 'rgba(44,82,130,0.95)';
            header.style.backdropFilter = 'blur(10px)';
        } else {
            header.style.background = '#2c5282';
            header.style.backdropFilter = 'none';
        }
    });
});