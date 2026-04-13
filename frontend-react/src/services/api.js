// ===== API Service Layer =====
// All backend calls go through here

const API_BASE = import.meta.env.VITE_API_URL || '';

// Helper to get headers with Bearer token
function getHeaders(extraHeaders = {}) {
  const token = localStorage.getItem('access_token');
  const headers = { ...extraHeaders };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

export async function sendOtp(phone) {
  const res = await fetch(`${API_BASE}/auth/send-otp`, {
    method: 'POST',
    headers: getHeaders({ 'Content-Type': 'application/json' }),
    credentials: 'include',
    body: JSON.stringify({ phone }),
  });
  return res.json();
}

export async function verifyOtp(phone, otp) {
  const res = await fetch(`${API_BASE}/auth/verify-otp`, {
    method: 'POST',
    headers: getHeaders({ 'Content-Type': 'application/json' }),
    credentials: 'include',
    body: JSON.stringify({ phone, otp }),
  });
  return res.json();
}

export async function registerManual(email, password, name = '') {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: 'POST',
    headers: getHeaders({ 'Content-Type': 'application/json' }),
    credentials: 'include',
    body: JSON.stringify({ email, password, name }),
  });
  return res.json();
}

export async function loginManual(email, password) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: getHeaders({ 'Content-Type': 'application/json' }),
    credentials: 'include',
    body: JSON.stringify({ email, password }),
  });
  return res.json();
}

export async function getMe() {
  const res = await fetch(`${API_BASE}/auth/me`, {
    headers: getHeaders(),
    credentials: 'include',
  });
  if (!res.ok) throw new Error('Not authenticated');
  return res.json();
}

export async function logout() {
  localStorage.removeItem('access_token');
  await fetch(`${API_BASE}/auth/logout`, {
    method: 'POST',
    headers: getHeaders(),
    credentials: 'include',
  });
}

export async function fetchJobs(limit = 20, keyword = '') {
  let url = `${API_BASE}/jobs?limit=${limit}`;
  if (keyword) url += `&keyword=${encodeURIComponent(keyword)}`;
  const res = await fetch(url, { 
    headers: getHeaders(),
    credentials: 'include' 
  });
  return res.json();
}
