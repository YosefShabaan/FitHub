/* =============================
   FitHub — Dashboard JS
   ============================= */

const API_URL = window.location.origin.startsWith('http')
  ? window.location.origin
  : 'http://127.0.0.1:8000';

function getToken() {
  const token = localStorage.getItem('token');
  if (!token) { window.location.href = 'login.html'; return null; }
  return token;
}

function logout() {
  localStorage.clear();
  window.location.href = 'login.html';
}

function setUsername() {
  const el = document.getElementById('username-display');
  if (el) el.textContent = localStorage.getItem('username') || 'Admin';
  const av = document.getElementById('user-avatar');
  const name = localStorage.getItem('username') || 'A';
  if (av) av.textContent = name[0].toUpperCase();
}

function setDate() {
  const el = document.getElementById('current-date');
  if (el) el.textContent = new Date().toLocaleDateString('en-US', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
  });
}

async function loadStats() {
  const token = getToken(); if (!token) return;
  try {
    const res = await fetch(`${API_URL}/dashboard/stats`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await res.json();

    document.getElementById('total-members').textContent    = data.total_members ?? 0;
    document.getElementById('active-subs').textContent      = data.active_subscriptions ?? 0;
    document.getElementById('expired-subs').textContent     = data.expired_subscriptions ?? 0;
    document.getElementById('monthly-plans').textContent    = data.monthly_plans ?? 0;
  } catch (e) {
    console.error('Stats error:', e);
  }
}

async function loadRecentMembers() {
  const token = getToken(); if (!token) return;
  try {
    const res = await fetch(`${API_URL}/members/`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const members = await res.json();
    const tbody = document.getElementById('recent-members-body');
    if (!tbody) return;

    tbody.innerHTML = '';
    const recent = members.slice(-5).reverse();

    if (recent.length === 0) {
      tbody.innerHTML = `<tr><td colspan="3" style="text-align:center;color:#bbb;padding:30px">No members yet</td></tr>`;
      return;
    }

    recent.forEach(m => {
      tbody.innerHTML += `
        <tr>
          <td>${m.name}</td>
          <td>${m.phone}</td>
          <td>${new Date(m.created_at).toLocaleDateString('en-US')}</td>
        </tr>`;
    });
  } catch (e) { console.error(e); }
}

async function loadRecentSubscriptions() {
  const token = getToken(); if (!token) return;
  try {
    const res = await fetch(`${API_URL}/subscriptions/`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const subs = await res.json();
    const tbody = document.getElementById('recent-subs-body');
    if (!tbody) return;

    tbody.innerHTML = '';
    const recent = subs.slice(-5).reverse();

    if (recent.length === 0) {
      tbody.innerHTML = `<tr><td colspan="4" style="text-align:center;color:#bbb;padding:30px">No subscriptions yet</td></tr>`;
      return;
    }

    recent.forEach(s => {
      const badge = s.status === 'active'
        ? `<span class="badge badge-active">Active</span>`
        : `<span class="badge badge-expired">Expired</span>`;
      tbody.innerHTML += `
        <tr>
          <td>#${s.member_id}</td>
          <td>${s.plan}</td>
          <td>${s.end_date}</td>
          <td>${badge}</td>
        </tr>`;
    });
  } catch (e) { console.error(e); }
}

document.addEventListener('DOMContentLoaded', () => {
  setUsername();
  setDate();
  loadStats();
  loadRecentMembers();
  loadRecentSubscriptions();
});
