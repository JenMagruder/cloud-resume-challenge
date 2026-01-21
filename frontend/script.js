// Typing animation
const phrases = [
    'Cloud Engineer',
    'DevOps Engineer',
    'AWS SolutionsArchitect',
    'Problem Solver',
    'Serverless Developer',
];

let currentPhraseIndex = 0;
let currentCharIndex = 0;
let isDeleting = false;
let isPaused = false;
let typingSpeed = 200;

function typeText() {
    const typedTextElement = document.querySelector('.typed-text');
    const currentPhrase = phrases[currentPhraseIndex];
    
    if (isPaused) {
        // Wait at the end of the phrase
        setTimeout(() => {
            isPaused = false;
            isDeleting = true;
            typeText();
        }, 2500);
        return;
    }
    
    if (isDeleting) {
        // Deleting text
        typedTextElement.textContent = currentPhrase.substring(0, currentCharIndex - 1);
        currentCharIndex--;
        typingSpeed = 300;
    } else {
        // Typing text
        typedTextElement.textContent = currentPhrase.substring(0, currentCharIndex + 1);
        currentCharIndex++;
        typingSpeed = 200;
    }
    
    // Handle completion of typing or deleting
    if (!isDeleting && currentCharIndex === currentPhrase.length) {
        // Finished typing, pause before deleting
        isPaused = true;
    } else if (isDeleting && currentCharIndex === 0) {
        // Finished deleting
        isDeleting = false;
        currentPhraseIndex = (currentPhraseIndex + 1) % phrases.length;
    }
    
    setTimeout(typeText, typingSpeed);
}

// Start the animation when the page loads
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(typeText, 1000);  // Initial delay before starting

    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.bubble-link');
    
    // Section observer for navigation
    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const sectionId = entry.target.getAttribute('id');
                
                // Update active navigation
                navLinks.forEach(link => {
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    } else {
                        link.classList.remove('active');
                    }
                });
            }
        });
    }, { threshold: 0.5 });
    
    sections.forEach(section => sectionObserver.observe(section));

    // Smooth scroll for bubble links
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            document.querySelector(targetId).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Visitor counter functionality
    const visitorCount = document.getElementById('visitor-count');
    
    async function getAndUpdateVisitorCount() {
        try {
            const response = await fetch('https://24jlr6fgs1.execute-api.us-east-1.amazonaws.com/count', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error('Failed to fetch visitor count');
            }
            
            const data = await response.json();
            visitorCount.textContent = data.count.toString();
        } catch (error) {
            console.error('Error updating visitor count:', error);
            visitorCount.textContent = '...';  // Show dots if there's an error
        }
    }

    // Get initial visitor count
    getAndUpdateVisitorCount();
});