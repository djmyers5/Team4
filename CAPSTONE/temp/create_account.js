// JavaScript for create_account.html page
function createAccount() {
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
  
    // Send create account details to the server for saving
    fetch('/create_account', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name, email, password })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Redirect to the login page after successful account creation
        window.location.href = '/login';
      } else {
        alert('Account creation failed. Please try again.');
      }
    })
    .catch(error => {
      console.error('Error during account creation:', error);
    });
  }
  