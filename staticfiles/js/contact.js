document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contact-form');
    const contactSuccess = document.getElementById('contact-success');
    
    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(contactForm);
            const submitButton = contactForm.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.innerHTML;
            
            // Disable all form inputs
            const formInputs = contactForm.querySelectorAll('input, textarea, button');
            formInputs.forEach(input => input.disabled = true);
            
            // Show loading state
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Sending...';
            
            try {
                const response = await fetch('/send-message/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                });
                
                if (!response.ok) {
                    throw new Error(`Server responded with status: ${response.status}`);
                }
                
                const data = await response.json();
                
                if (data.status === 'success') {
                    // Show success message
                    contactForm.classList.add('hidden');
                    if (contactSuccess) {
                        // Update success message if in development mode
                        if (data.message.includes('Development mode')) {
                            const successText = contactSuccess.querySelector('p');
                            if (successText) {
                                successText.textContent = data.message;
                            }
                        }
                        contactSuccess.classList.remove('hidden');
                    } else {
                        showNotification('Success!', data.message, 'success');
                    }
                    contactForm.reset();
                } else {
                    showNotification('Error!', data.message, 'error');
                    // Re-enable form inputs
                    formInputs.forEach(input => input.disabled = false);
                }
            } catch (error) {
                console.error('Contact form error:', error);
                showNotification(
                    'Error!', 
                    'Something went wrong with the request. Please try again later or contact me directly at rahul.edu.ranjan98153@gmail.com', 
                    'error'
                );
                // Re-enable form inputs
                formInputs.forEach(input => input.disabled = false);
            } finally {
                submitButton.innerHTML = originalButtonText;
            }
        });
    }
    
    // Add test email button if in development
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        const contactSection = document.getElementById('contact');
        if (contactSection) {
            const testButton = document.createElement('button');
            testButton.className = 'mt-4 bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded text-sm';
            testButton.textContent = 'Test Email System';
            testButton.addEventListener('click', async () => {
                try {
                    const response = await fetch('/test-email/');
                    const data = await response.json();
                    showNotification(
                        data.status === 'success' ? 'Success!' : 'Error!',
                        data.message,
                        data.status
                    );
                } catch (error) {
                    showNotification('Error!', 'Failed to test email system', 'error');
                }
            });
            
            const container = contactSection.querySelector('.container');
            if (container) {
                const devNote = document.createElement('div');
                devNote.className = 'text-center text-sm text-gray-500 mt-8';
                devNote.innerHTML = '<p>Development Mode: Emails will be printed to the console</p>';
                devNote.appendChild(testButton);
                container.appendChild(devNote);
            }
        }
    }
});

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Helper function to show notifications
function showNotification(title, message, type) {
    // Remove any existing notifications
    const existingNotifications = document.querySelectorAll('.notification-toast');
    existingNotifications.forEach(notification => notification.remove());
    
    const notification = document.createElement('div');
    notification.className = `notification-toast fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
        type === 'success' ? 'bg-green-500' : 'bg-red-500'
    } text-white transform transition-transform duration-300 ease-in-out`;
    
    notification.innerHTML = `
        <div class="flex items-center">
            <div class="flex-shrink-0">
                <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'} text-xl"></i>
            </div>
            <div class="ml-3">
                <p class="font-bold">${title}</p>
                <p class="text-sm">${message}</p>
            </div>
            <div class="ml-4 flex-shrink-0">
                <button type="button" class="text-white focus:outline-none">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Add entrance animation
    setTimeout(() => {
        notification.classList.add('translate-y-2');
    }, 10);
    
    // Add click event to close button
    const closeButton = notification.querySelector('button');
    closeButton.addEventListener('click', () => {
        notification.classList.add('-translate-y-2', 'opacity-0');
        setTimeout(() => {
            notification.remove();
        }, 300);
    });
    
    // Remove notification after 5 seconds
    setTimeout(() => {
        notification.classList.add('-translate-y-2', 'opacity-0');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 5000);
} 