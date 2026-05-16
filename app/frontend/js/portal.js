const API_URL = window.location.origin.startsWith('http')
  ? window.location.origin
  : 'http://127.0.0.1:8000';

function selectPlan(plan) {
  const planSelect = document.getElementById('join-plan');
  if (planSelect) planSelect.value = plan;
}

function setJoinMessage(message, type) {
  const messageEl = document.getElementById('join-message');
  messageEl.textContent = message;
  messageEl.className = `join-message ${type}`;
}

async function handleJoin(event) {
  event.preventDefault();

  const button = document.getElementById('join-submit');
  const payload = {
    name: document.getElementById('join-name').value.trim(),
    phone: document.getElementById('join-phone').value.trim(),
    email: document.getElementById('join-email').value.trim() || null,
    plan: document.getElementById('join-plan').value
  };

  button.disabled = true;
  button.textContent = 'CREATING...';
  setJoinMessage('', '');

  try {
    const response = await fetch(`${API_URL}/portal/join`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || 'Could not create membership');
    }

    setJoinMessage(
      `Membership created for ${data.name}. Member #${data.member_id}, ${data.plan} plan active until ${data.end_date}.`,
      'success'
    );
    event.target.reset();
    selectPlan(payload.plan);
  } catch (err) {
    setJoinMessage(err.message, 'error');
  } finally {
    button.disabled = false;
    button.textContent = 'CREATE MEMBERSHIP';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('join-form');
  if (form) form.addEventListener('submit', handleJoin);
});
