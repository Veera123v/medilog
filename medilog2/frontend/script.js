const API = 'http://localhost:5000';

function login() {
  fetch(`${API}/login`, {
    method: 'POST',
    credentials: 'include',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      username: document.getElementById('username').value,
      password: document.getElementById('password').value
    })
  }).then(res => res.ok ? location.href = 'index.html' : alert('Login failed'));
}

function register() {
  fetch(`${API}/register`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      username: document.getElementById('username').value,
      password: document.getElementById('password').value
    })
  }).then(res => res.ok ? location.href = 'login.html' : alert('Registration failed'));
}

function logout() {
  fetch(`${API}/logout`, {
    credentials: 'include'
  }).then(() => location.href = 'login.html');
}

function loadMedications() {
  const status = document.getElementById('statusFilter').value;
  const sort = document.getElementById('sortOption').value;
  let url = `${API}/medications?`;
  if (status) url += `status=${status}&`;
  if (sort) url += `sort=${sort}`;
  fetch(url, { credentials: 'include' })
    .then(res => res.json())
    .then(data => {
      const list = document.getElementById('medicationList');
      list.innerHTML = '';
      data.medications.forEach(m => {
        const item = document.createElement('div');
        item.innerText = `${m.name} - ${m.status}`;
        list.appendChild(item);
      });
      document.getElementById('summary').innerText = `Total Active Medications: ${data.active_count}`;
    });
}

function submitMedication() {
  const med = {
    name: document.getElementById('name').value,
    dosage: document.getElementById('dosage').value,
    frequency: document.getElementById('frequency').value,
    start_date: document.getElementById('start_date').value,
    notes: document.getElementById('notes').value,
    status: document.getElementById('status').value
  };
  fetch(`${API}/medications`, {
    method: 'POST',
    credentials: 'include',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(med)
  }).then(res => res.ok ? location.href = 'index.html' : alert('Failed to add medication'));
}
