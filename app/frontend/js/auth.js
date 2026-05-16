const API_URL = window.location.origin.startsWith('http')
  ? window.location.origin
  : 'http://127.0.0.1:8000';

async function handleLogin(event) {
  event.preventDefault();

  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value;
  const error = document.getElementById('error-msg');
  const button = document.getElementById('loginBtn');

  error.textContent = '';
  button.disabled = true;
  button.textContent = 'LOGGING IN...';

  try {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new Error(data.detail || 'Invalid username or password');
    }

    const data = await response.json();
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('username', username);
    window.location.href = 'dashboard.html';
  } catch (err) {
    error.textContent = err.message;
  } finally {
    button.disabled = false;
    button.textContent = 'LOGIN';
  }
}
