// ==========================================
// Barber & Beauty - Main JavaScript
// ==========================================

// Authentication Handler
function handleLogin() {
    // Mock authentication - replace with real OAuth flow
    const authUrl = 'https://manus.im/app-auth?appId=YAc6osGP6zccqyUT7e7qqG&redirectUri=https%3A%2F%2Fbarber-sched-yac6osgp.manus.space%2Fapi%2Foauth%2Fcallback&state=aHR0cHM6Ly9iYXJiZXItc2NoZWQteWFjNm9zZ3AubWFudXMuc3BhY2UvYXBpL29hdXRoL2NhbGxiYWNr&type=signIn';
    
    // For demo purposes, show an alert
    alert('Redirecionando para login... Em produção, isso conectaria com o sistema de autenticação.');
    
    // Uncomment to redirect to actual auth
    // window.location.href = authUrl;
}

// Smooth Scroll for anchor links
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

// Header scroll effect
let lastScroll = 0;
const header = document.querySelector('.header');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll <= 0) {
        header.style.boxShadow = 'none';
    } else {
        header.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.3)';
    }
    
    lastScroll = currentScroll;
});

// Service card animations on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all service cards
document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.service-card, .feature-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `all 0.6s ease-out ${index * 0.1}s`;
        observer.observe(card);
    });
});

// Service card click handler
document.querySelectorAll('.service-card').forEach(card => {
    card.addEventListener('click', function() {
        const serviceName = this.querySelector('.service-name').textContent;
        const servicePrice = this.querySelector('.service-price').textContent;
        
        // Show service details (mock)
        alert(`Serviço: ${serviceName}\nPreço: ${servicePrice}\n\nFaça login para agendar!`);
    });
});

// Loading animation for images
const imageObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            img.style.opacity = '1';
            imageObserver.unobserve(img);
        }
    });
});

document.querySelectorAll('img').forEach(img => {
    img.style.opacity = '0';
    img.style.transition = 'opacity 0.5s ease-in';
    imageObserver.observe(img);
});

// Stats counter animation
function animateCounter(element, target, duration) {
    let start = 0;
    const increment = target / (duration / 16);
    
    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(start);
        }
    }, 16);
}

// Animate stats on scroll
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
            const statNumbers = entry.target.querySelectorAll('.stat-number');
            statNumbers.forEach(stat => {
                const text = stat.textContent;
                const number = parseInt(text.replace(/\D/g, ''));
                if (number) {
                    stat.textContent = '0';
                    animateCounter(stat, number, 2000);
                    stat.textContent += text.includes('+') ? '+' : (text.includes('★') ? '★' : '');
                }
            });
            entry.target.classList.add('animated');
        }
    });
}, { threshold: 0.5 });

const statsSection = document.querySelector('.stats');
if (statsSection) {
    statsObserver.observe(statsSection);
}

// Made with badge click handler
const madeWithBadge = document.querySelector('.made-with-badge');
if (madeWithBadge) {
    madeWithBadge.addEventListener('click', () => {
        window.open('https://manus.im', '_blank');
    });
}

// Form validation helper (for future use)
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    const re = /^[\d\s\-\+\(\)]+$/;
    return re.test(phone);
}

// Local storage helper for user preferences
const AppStorage = {
    set: (key, value) => {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (e) {
            console.error('Storage error:', e);
            return false;
        }
    },
    get: (key) => {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (e) {
            console.error('Storage error:', e);
            return null;
        }
    },
    remove: (key) => {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (e) {
            console.error('Storage error:', e);
            return false;
        }
    }
};

// Check if user is logged in (mock)
const isLoggedIn = () => {
    return AppStorage.get('user') !== null;
};

// Console welcome message
console.log('%c🪒 Barber & Beauty Scheduler', 'color: #FF6B00; font-size: 24px; font-weight: bold;');
console.log('%cSistema de agendamento profissional', 'color: #B0B0B0; font-size: 14px;');
console.log('%c© 2026 - Todos os direitos reservados', 'color: #707070; font-size: 12px;');

// Prevent context menu on images (optional security)
document.querySelectorAll('img').forEach(img => {
    img.addEventListener('contextmenu', (e) => {
        // Uncomment to prevent right-click
        // e.preventDefault();
    });
});

// Add loading state
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
});

// Service Worker registration (for PWA - optional)
if ('serviceWorker' in navigator) {
    // Uncomment to enable PWA
    /*
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered:', registration);
            })
            .catch(error => {
                console.log('SW registration failed:', error);
            });
    });
    */
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        handleLogin,
        validateEmail,
        validatePhone,
        AppStorage,
        isLoggedIn
    };
}
