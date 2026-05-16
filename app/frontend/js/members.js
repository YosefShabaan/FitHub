/* =============================
   FitHub — Members JS
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

let editingId = null;

// ── Load Members ──
async function loadMembers(query = '') {
  const token = getToken(); if (!token) return;
  const url = query
    ? `${API_URL}/members/search?query=${encodeURIComponent(query)}`
    : `${API_URL}/members/`;

  const res = await fetch(url, { headers: { 'Authorization': `Bearer ${token}` } });
  const members = await res.json();
  renderMembers(members);
}

function renderMembers(members) {
  const tbody = document.getElementById('members-body');
  tbody.innerHTML = '';

  if (members.length === 0) {
    tbody.innerHTML = `
      <tr><td colspan="5">
        <div class="empty-state">
          <div class="empty-icon">👥</div>
          <p>No members found</p>
        </div>
      </td></tr>`;
    return;
  }

  members.forEach(m => {
    tbody.innerHTML += `
      <tr>
        <td>#${m.id}</td>
        <td>${m.name}</td>
        <td>${m.phone}</td>
        <td>${m.email || '—'}</td>
        <td>
          <div class="action-btns">
            <button class="btn-edit" onclick="openEdit(${m.id},'${m.name}','${m.phone}','${m.email||''}')">Edit</button>
            <button class="btn-delete" onclick="deleteMember(${m.id})">Delete</button>
          </div>
        </td>
      </tr>`;
  });
}

// ── Modal ──
function openAdd() {
  editingId = null;
  document.getElementById('modal-title').textContent = 'ADD MEMBER';
  document.getElementById('member-name').value  = '';
  document.getElementById('member-phone').value = '';
  document.getElementById('member-email').value = '';
  document.getElementById('modal').classList.add('open');
}

function openEdit(id, name, phone, email) {
  editingId = id;
  document.getElementById('modal-title').textContent = 'EDIT MEMBER';
  document.getElementById('member-name').value  = name;
  document.getElementById('member-phone').value = phone;
  document.getElementById('member-email').value = email;
  document.getElementById('modal').classList.add('open');
}

function closeModal() {
  document.getElementById('modal').classList.remove('open');
}

// ── Save ──
async function saveMember() {
  const token = getToken(); if (!token) return;
  const name  = document.getElementById('member-name').value.trim();
  const phone = document.getElementById('member-phone').value.trim();
  const email = document.getElementById('member-email').value.trim();

  if (!name || !phone) return alert('Name and phone are required!');

  const body = { name, phone, email: email || null };
  const url  = editingId ? `${API_URL}/members/${editingId}` : `${API_URL}/members/`;
  const method = editingId ? 'PUT' : 'POST';

  const res = await fetch(url, {
    method,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(body)
  });

  if (res.ok) {
    closeModal();
    loadMembers();
    showToast(editingId ? 'MEMBER UPDATED ✓' : 'MEMBER ADDED ✓');
  } else {
    const err = await res.json();
    alert(err.detail || 'Error saving member');
  }
}

// ── Delete ──
async function deleteMember(id) {
  if (!confirm('Delete this member and all their subscriptions?')) return;
  const token = getToken(); if (!token) return;

  const res = await fetch(`${API_URL}/members/${id}`, {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${token}` }
  });

  if (res.ok) {
    loadMembers();
    showToast('MEMBER DELETED ✓');
  }
}

// ── Search ──
let searchTimeout;
function onSearch(e) {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => loadMembers(e.target.value), 400);
}

// ── Init ──
document.addEventListener('DOMContentLoaded', () => {
  const u = localStorage.getItem('username') || 'Admin';
  const el = document.getElementById('username-display');
  if (el) el.textContent = u;
  const av = document.getElementById('user-avatar');
  if (av) av.textContent = u[0].toUpperCase();
  loadMembers();
});

function logout() {
  localStorage.clear();
  window.location.href = 'login.html';
}
