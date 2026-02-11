// ==========================================
// Board Page - JavaScript
// ==========================================

// Mock data for professionals
const professionals = [
    {
        name: "Carlos Silva",
        role: "Barbeiro Master",
        rating: 5.0,
        reviews: 127,
        specialties: ["Cortes", "Barba", "Coloração"],
        availableTimes: ["09:00", "11:00", "14:00", "16:00"]
    },
    {
        name: "Ana Rodrigues",
        role: "Cabeleireira Expert",
        rating: 5.0,
        reviews: 189,
        specialties: ["Cortes Femininos", "Coloração", "Tratamentos"],
        availableTimes: ["10:00", "13:00", "15:00", "17:00"]
    },
    {
        name: "Roberto Martins",
        role: "Barbeiro Profissional",
        rating: 5.0,
        reviews: 94,
        specialties: ["Cortes Masculinos", "Barba"],
        availableTimes: ["09:30", "12:00", "14:30", "18:00"]
    },
    {
        name: "Juliana Costa",
        role: "Manicure & Pedicure",
        rating: 5.0,
        reviews: 156,
        specialties: ["Manicure", "Pedicure", "Nail Art"],
        availableTimes: ["10:30", "13:30", "15:30", "17:30"]
    },
    {
        name: "Pedro Santos",
        role: "Colorista Expert",
        rating: 5.0,
        reviews: 112,
        specialties: ["Coloração", "Mechas", "Luzes"],
        availableTimes: ["11:00", "14:00", "16:30"]
    },
    {
        name: "Mariana Lima",
        role: "Tratamentos Capilares",
        rating: 5.0,
        reviews: 143,
        specialties: ["Hidratação", "Botox Capilar", "Reconstrução"],
        availableTimes: ["09:00", "12:30", "15:00"]
    }
];

// Set default date to today
document.addEventListener('DOMContentLoaded', () => {
    const dateFilter = document.getElementById('date-filter');
    if (dateFilter) {
        const today = new Date().toISOString().split('T')[0];
        dateFilter.value = today;
        dateFilter.min = today;
    }
    
    // Add event listeners to filters
    setupFilters();
    
    // Add event listeners to time slots
    setupTimeSlots();
});

// Setup filter event listeners
function setupFilters() {
    const serviceFilter = document.getElementById('service-filter');
    const dateFilter = document.getElementById('date-filter');
    const timeFilter = document.getElementById('time-filter');
    
    if (serviceFilter) {
        serviceFilter.addEventListener('change', applyFilters);
    }
    
    if (dateFilter) {
        dateFilter.addEventListener('change', applyFilters);
    }
    
    if (timeFilter) {
        timeFilter.addEventListener('change', applyFilters);
    }
}

// Apply filters to professional cards
function applyFilters() {
    const serviceFilter = document.getElementById('service-filter')?.value || 'all';
    const timeFilter = document.getElementById('time-filter')?.value || 'all';
    
    const cards = document.querySelectorAll('.professional-card');
    
    cards.forEach(card => {
        let show = true;
        
        // Service filter
        if (serviceFilter !== 'all') {
            const specialties = Array.from(card.querySelectorAll('.specialty-tag'))
                .map(tag => tag.textContent.toLowerCase());
            
            const serviceMatch = specialties.some(specialty => 
                specialty.includes(serviceFilter.toLowerCase())
            );
            
            if (!serviceMatch) {
                show = false;
            }
        }
        
        // Time filter
        if (timeFilter !== 'all' && show) {
            const timeSlots = Array.from(card.querySelectorAll('.time-slot'))
                .map(slot => slot.textContent);
            
            let hasMatchingTime = false;
            
            timeSlots.forEach(time => {
                const hour = parseInt(time.split(':')[0]);
                
                if (timeFilter === 'morning' && hour >= 8 && hour < 12) {
                    hasMatchingTime = true;
                } else if (timeFilter === 'afternoon' && hour >= 12 && hour < 18) {
                    hasMatchingTime = true;
                } else if (timeFilter === 'evening' && hour >= 18 && hour < 22) {
                    hasMatchingTime = true;
                }
            });
            
            if (!hasMatchingTime) {
                show = false;
            }
        }
        
        // Show/hide card with animation
        if (show) {
            card.style.display = 'flex';
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 10);
        } else {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            setTimeout(() => {
                card.style.display = 'none';
            }, 300);
        }
    });
    
    // Check if any cards are visible
    const visibleCards = Array.from(cards).filter(card => 
        card.style.display !== 'none'
    );
    
    if (visibleCards.length === 0) {
        showEmptyState();
    } else {
        hideEmptyState();
    }
}

// Show empty state
function showEmptyState() {
    let emptyState = document.querySelector('.empty-state');
    
    if (!emptyState) {
        emptyState = document.createElement('div');
        emptyState.className = 'empty-state';
        emptyState.innerHTML = `
            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="12"/>
                <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            <h3>Nenhum profissional encontrado</h3>
            <p>Tente ajustar os filtros para ver mais resultados</p>
        `;
        
        document.querySelector('.professionals-grid').appendChild(emptyState);
    }
    
    emptyState.style.display = 'block';
}

// Hide empty state
function hideEmptyState() {
    const emptyState = document.querySelector('.empty-state');
    if (emptyState) {
        emptyState.style.display = 'none';
    }
}

// Setup time slot event listeners
function setupTimeSlots() {
    const timeSlots = document.querySelectorAll('.time-slot');
    
    timeSlots.forEach(slot => {
        slot.addEventListener('click', function() {
            // Remove selected class from all slots in this card
            const card = this.closest('.professional-card');
            const cardSlots = card.querySelectorAll('.time-slot');
            cardSlots.forEach(s => s.classList.remove('selected'));
            
            // Add selected class to clicked slot
            this.classList.add('selected');
            
            // Update the booking button
            const bookBtn = card.querySelector('.btn-block');
            const professionalName = card.querySelector('.professional-name').textContent;
            const time = this.textContent;
            
            bookBtn.textContent = `Agendar ${time}`;
            bookBtn.onclick = () => bookAppointment(professionalName, time);
        });
    });
}

// Book appointment function
function bookAppointment(professionalName, time = null) {
    const dateFilter = document.getElementById('date-filter');
    const selectedDate = dateFilter ? dateFilter.value : new Date().toISOString().split('T')[0];
    
    // Format date
    const date = new Date(selectedDate + 'T00:00:00');
    const formattedDate = date.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: 'long',
        year: 'numeric'
    });
    
    const message = time 
        ? `Agendamento com ${professionalName}\nData: ${formattedDate}\nHorário: ${time}\n\nFaça login para confirmar o agendamento!`
        : `Agendamento com ${professionalName}\nData: ${formattedDate}\n\nSelecione um horário e faça login para confirmar!`;
    
    alert(message);
    
    // In production, this would redirect to login or open a booking modal
    // handleLogin();
}

// Filter by service from URL parameter
function filterByService() {
    const urlParams = new URLSearchParams(window.location.search);
    const service = urlParams.get('service');
    
    if (service) {
        const serviceFilter = document.getElementById('service-filter');
        if (serviceFilter) {
            serviceFilter.value = service;
            applyFilters();
        }
    }
}

// Initialize on load
window.addEventListener('load', () => {
    filterByService();
});

// Add loading animation to professional avatars
const avatars = document.querySelectorAll('.professional-avatar');
avatars.forEach((avatar, index) => {
    avatar.style.opacity = '0';
    avatar.style.transform = 'scale(0.8)';
    
    setTimeout(() => {
        avatar.style.transition = 'all 0.5s ease-out';
        avatar.style.opacity = '1';
        avatar.style.transform = 'scale(1)';
    }, 100 * index);
});

// Random availability simulator (for demo)
function simulateAvailability() {
    const timeSlots = document.querySelectorAll('.time-slot');
    
    timeSlots.forEach(slot => {
        // 10% chance of being unavailable
        if (Math.random() < 0.1) {
            slot.classList.add('disabled');
            slot.disabled = true;
        }
    });
}

// Uncomment to enable random availability
// simulateAvailability();

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        bookAppointment,
        applyFilters,
        professionals
    };
}
