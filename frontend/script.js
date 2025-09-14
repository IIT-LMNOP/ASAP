
(function () {
    const heading = document.getElementById('heading');
    const fullText = heading.textContent.trim();
    heading.textContent = '';

    // build structure
    const wrap = document.createElement('span');
    wrap.className = 'typing-wrap';
    const typedEl = document.createElement('span');
    typedEl.className = 'typed';
    const caret = document.createElement('i');
    caret.className = 'caret';
    wrap.appendChild(typedEl);
    wrap.appendChild(caret);
    heading.appendChild(wrap);

    // config
    const typeSpeed = 100;
    const eraseSpeed = 60;
    const pauseAfterTyping = 1000;
    const pauseAfterErasing = 500;

    let index = 0;
    let typing = true; // typing phase or erasing

    function loop() {
      if (typing) {
        if (index < fullText.length) {
          typedEl.textContent += fullText.charAt(index);
          index++;
          setTimeout(loop, typeSpeed);
        } else {
          typing = false;
          setTimeout(loop, pauseAfterTyping);
        }
      } else {
        if (index > 0) {
          typedEl.textContent = fullText.substring(0, index - 1);
          index--;
          setTimeout(loop, eraseSpeed);
        } else {
          typing = true;
          setTimeout(loop, pauseAfterErasing);
        }
      }
    }

    loop();
  })();
let selectedSignupType = '';

// Modal functions
function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Signup type selection
function selectSignupType(type) {
    selectedSignupType = type;
    const options = document.querySelectorAll('.signup-option');
    options.forEach(option => option.classList.remove('selected'));
    event.target.closest('.signup-option').classList.add('selected');
}

function proceedWithSignup() {
    if (!selectedSignupType) {
        alert('Please select an account type to continue.');
        return;
    }
    alert(`Proceeding with ${selectedSignupType} signup...`);
    closeModal('signupModal');
}

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Close modals when clicking outside
window.onclick = function (event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
}

// Add scroll effect to header
window.addEventListener('scroll', function () {
    const header = document.querySelector('.header');
    if (window.scrollY > 100) {
        header.style.background = 'rgba(15, 23, 42, 0.95);';
        header.style.backdropFilter = 'blur(10px)';
    } else {
        header.style.background = 'rgba(15, 23, 42, 0.95);';
        header.style.backdropFilter = 'none';
    }
});

// Animate cards on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function (entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all cards for animation
document.addEventListener('DOMContentLoaded', function () {
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `all 0.6s ease ${index * 0.2}s`;
        observer.observe(card);
    });
});

function toggleChatbot() {
  const chatbot = document.getElementById("chatbotWindow");
  chatbot.style.display = chatbot.style.display === "flex" ? "none" : "flex";
}

function sendMessage() {
  const input = document.getElementById("chatInput");
  const messages = document.getElementById("chatbotMessages");

  if (input.value.trim() === "") return;

  // user message
  const userMsg = document.createElement("div");
  userMsg.className = "user-message";
  userMsg.textContent = input.value;
  messages.appendChild(userMsg);

  // bot reply (basic demo)
  const botMsg = document.createElement("div");
  botMsg.className = "bot-message";
  botMsg.textContent = "🤖 Thanks for your message! (This is a demo)";
  messages.appendChild(botMsg);

  // scroll to bottom
  messages.scrollTop = messages.scrollHeight;

  input.value = "";
}

// Initialize the map
const map = L.map('alumni-map').setView([20, 0], 2); // Center on world, zoom 2

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Alumni locations
const alumni = [
    { city: "New York", coords: [40.7128, -74.0060], count: 150 },
    { city: "London", coords: [51.5074, -0.1278], count: 89 },
    { city: "Tokyo", coords: [35.6895, 139.6917], count: 67 },
    { city: "Mumbai", coords: [19.0760, 72.8777], count: 234 },
    { city: "Singapore", coords: [1.3521, 103.8198], count: 45 },
];

// Add markers
alumni.forEach(a => {
    L.marker(a.coords)
     .addTo(map)
     .bindPopup(`<b>${a.city}</b><br>${a.count} Alumni`);
});


