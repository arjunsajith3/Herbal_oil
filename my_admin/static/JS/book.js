
    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('bookingForm');
        const togglePassword = document.getElementById('togglePassword');
        const passwordInput = document.getElementById('password');
        const successMessage = document.getElementById('successMessage');

        // Toggle password visibility
        togglePassword.addEventListener('click', function() {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            this.textContent = type === 'password' ? '👁️' : '🔒';
        });

        // Form validation and submission
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            let isValid = true;

            // Reset error messages
            document.querySelectorAll('.error-message').forEach(msg => {
                msg.style.display = 'none';
            });

            // Validate name
            const name = document.getElementById('name').value.trim();
            if (name === '') {
                document.getElementById('nameError').style.display = 'block';
                isValid = false;
            }

            // Validate email
            const email = document.getElementById('email').value.trim();
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                document.getElementById('emailError').style.display = 'block';
                isValid = false;
            }

            // Validate phone
            const phone = document.getElementById('phone').value.trim();
            const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
            if (!phoneRegex.test(phone.replace(/[\s\-\(\)]/g, ''))) {
                document.getElementById('phoneError').style.display = 'block';
                isValid = false;
            }

            // Validate username
            const username = document.getElementById('username').value.trim();
            if (username === '') {
                document.getElementById('usernameError').style.display = 'block';
                isValid = false;
            }

            // Validate password
            const password = document.getElementById('password').value;
            if (password.length < 8) {
                document.getElementById('passwordError').style.display = 'block';
                isValid = false;
            }

            // Validate confirm password
            const confirmPassword = document.getElementById('confirmPassword').value;
            if (password !== confirmPassword) {
                document.getElementById('confirmPasswordError').style.display = 'block';
                isValid = false;
            }

            // If form is valid, show success message
            if (isValid) {
                successMessage.style.display = 'block';
                form.reset();

                // Scroll to success message
                successMessage.scrollIntoView({ behavior: 'smooth' });

                // Hide success message after 5 seconds
                setTimeout(() => {
                    successMessage.style.display = 'none';
                }, 5000);
            }
        });
    });
