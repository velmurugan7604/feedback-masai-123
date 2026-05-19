document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('feedbackForm');
    const submitBtn = document.getElementById('submitBtn');
    const errorMessage = document.getElementById('errorMessage');
    const successMessage = document.getElementById('successMessage');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Reset messages
        errorMessage.style.display = 'none';
        successMessage.style.display = 'none';
        
        // Get form values
        const username = document.getElementById('username').value.trim();
        const email = document.getElementById('email').value.trim();
        const experience = document.getElementById('experience').value.trim();
        const ratingElement = document.querySelector('input[name="rating"]:checked');
        
        // Basic validation (though HTML required attributes handle most of this)
        if (!username || !email || !experience || !ratingElement) {
            showError('Please fill out all required fields, including the star rating.');
            return;
        }
        
        const rating = parseInt(ratingElement.value);
        
        // Prepare data
        const data = {
            username,
            email,
            rating,
            experience
        };
        
        // Show loading state
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;
        
        try {
            const response = await fetch('/api/feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                showSuccess('Thank you! Your feedback has been submitted successfully.');
                form.reset();
                // Clear star rating visually
                document.querySelectorAll('.star-rating input').forEach(input => input.checked = false);
            } else {
                showError(result.error || 'An error occurred while submitting feedback.');
            }
        } catch (error) {
            showError('Network error. Please try checking your internet connection.');
            console.error('Error:', error);
        } finally {
            // Remove loading state
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
        }
    });
    
    function showError(msg) {
        errorMessage.textContent = msg;
        errorMessage.style.display = 'block';
    }
    
    function showSuccess(msg) {
        successMessage.textContent = msg;
        successMessage.style.display = 'block';
    }
});
