// JavaScript for login.html page
function login() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
  
    // Send login details to the server for verification
    fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Redirect to the dashboard if login is successful
        window.location.href = '/dashboard';
      } else {
        alert('Invalid credentials. Please try again.');
      }
    })
    .catch(error => {
      console.error('Error during login:', error);
    });
  }
  