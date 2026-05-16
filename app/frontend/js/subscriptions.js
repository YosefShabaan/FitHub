/* =============================
   FitHub — Subscriptions JS
   ============================= */

const API_URL = window.location.origin.startsWith('http')
  ? window.location.origin
  : 'http://127.0.0.1:8000';

function getToken() {
  const token = localStorage.getItem('token');
  if (!token) { window.location.href = 'login.html'; return null; }
  return token;
}

function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2500);
}

// ── Load Subscriptions ──
async function loadSubscriptions() {
  const token = getToken(); if (!token) return;
  const res = await fetch(`${API_URL}/subscriptions/`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  const subs = await res.json();
  renderSubscriptions(subs);
}

function renderSubscriptions(subs) {
  const tbody = document.getElementById('subs-body');
  tbody.innerHTML = '';

  if (subs.length === 0) {
    tbody.innerHTML = `
      <tr><td colspan="6">
        <div class="empty-state">
          <div class="empty-icon">💳</div>
          <p>No subscriptions found</p>
        </div>
      </td></tr>`;
    return;
  }

  subs.forEach(s => {
    const badge = s.status === 'active'
      ? `<span class="badge badge-active">Active</span>`
      : `<span class="badge badge-expired">Expired</span>`;
    tbody.innerHTML += `
      <tr>
        <td>#${s.id}</td>
        <td>#${s.member_id}</td>
        <td style="text-transform:capitalize">${s.plan}</td>
        <td>${s.start_date}</td>
        <td>${s.end_date}</td>
        <td>${badge}</td>
        <td>
          <div class="action-btns">
            <button class="btn-delete" onclick="deleteSubscription(${s.id})">Delete</button>
          </div>
        </td>
      </tr>`;
  });
}

// ── Modal ──
function openAdd() {
  document.getElementById('sub-member-id').value = '';
  document.getElementById('sub-plan').value      = 'monthly';
  document.getElementById('sub-start').value     = new Date().toISOString().split('T')[0];
  document.getElementById('modal').classList.add('open');
}

function closeModal() {
  document.getElementById('modal').classList.remove('open');
}

// ── Save ──
async function saveSubscription() {
  const token     = getToken(); if (!token) return;
  const member_id = parseInt(document.getElementById('sub-member-id').value);
  const plan       = document.getElementById('sub-plan').value;
  const start_date = document.getElementById('sub-start').value;

  if (!member_id || !plan || !start_date) return alert('All fields required!');

  const res = await fetch(`${API_URL}/subscriptions/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ member_id, plan, start_date })
  });

  if (res.ok) {
    closeModal();
    loadSubscriptions();
    showToast('SUBSCRIPTION ADDED ✓');
  } else {
    const err = await res.json();
    alert(err.detail || 'Error creating subscription');
  }
}

// ── Delete ──
async function deleteSubscription(id) {
  if (!confirm('Delete this subscription?')) return;
  const token = getToken(); if (!token) return;

  const res = await fetch(`${API_URL}/subscriptions/${id}`, {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${token}` }
  });

  if (res.ok) {
    loadSubscriptions();
    showToast('SUBSCRIPTION DELETED ✓');
  }
}

// ── Init ──
document.addEventListener('DOMContentLoaded', () => {
  const u = localStorage.getItem('username') || 'Admin';
  const el = document.getElementById('username-display');
  if (el) el.textContent = u;
  const av = document.getElementById('user-avatar');
  if (av) av.textContent = u[0].toUpperCase();
  loadSubscriptions();
});

function logout() {
  localStorage.clear();
  window.location.href = 'login.html';
}
