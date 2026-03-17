const API = 'http://127.0.0.1:8000';
let token = localStorage.getItem('token') || null;
let isLoginMode = true;

if (token) showDashboard();

function toggleForm() {
    isLoginMode = !isLoginMode;
    document.getElementById('auth-title').textContent = isLoginMode ? 'Welcome Back' : 'Create Account';
    document.getElementById('auth-btn').textContent = isLoginMode ? 'Login' : 'Register';
    document.getElementById('toggle-text').textContent = isLoginMode ? "Don't have an account?" : 'Already have an account?';
    document.getElementById('toggle-link-btn').textContent = isLoginMode ? 'Register here' : 'Login';
    document.getElementById('email-group').style.display = isLoginMode ? 'none' : 'block';
    document.getElementById('auth-error').textContent = '';
}

async function handleAuth() {
    if (isLoginMode) await login();
    else await register();
}

async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    document.getElementById('auth-error').textContent = '';

    try {
        const res = await fetch(`${API}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
        });

        if (!res.ok) {
            document.getElementById('auth-error').textContent = 'Invalid username or password.';
            return;
        }

        const data = await res.json();
        token = data.access_token;
        localStorage.setItem('token', token);
        showDashboard();

    } catch (err) {
        document.getElementById('auth-error').textContent = 'Connection error. Please try again.';
    }
}

async function register() {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    document.getElementById('auth-error').textContent = '';

    try {
        const res = await fetch(`${API}/users`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });

        if (!res.ok) {
            const err = await res.json();
            document.getElementById('auth-error').textContent = err.detail || 'Registration failed.';
            return;
        }

        // Auto login after register
        await login();

    } catch (err) {
        document.getElementById('auth-error').textContent = 'Connection error. Please try again.';
    }
}

function logout() {
    token = null;
    localStorage.removeItem('token');
    document.getElementById('dashboard-section').style.display = 'none';
    document.getElementById('auth-section').style.display = 'flex';
    document.getElementById('logout-btn').style.display = 'none';
    // Clear input fields
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
    document.getElementById('email').value = '';
    document.getElementById('auth-error').textContent = '';
}

function showDashboard() {
    document.getElementById('auth-section').style.display = 'none';
    document.getElementById('dashboard-section').style.display = 'block';
    document.getElementById('logout-btn').style.display = 'block';
    // Set greeting with username
    const username = document.getElementById('username').value;
    if (username) {
        document.getElementById('greeting').textContent = `Hello, ${username}!`;
    }
    loadAll();
}

function authHeaders() {
    return { 'Authorization': `Bearer ${token}` };
}

async function loadAll() {
    await Promise.all([
        loadSummary(),
        loadProductivity(),
        loadStreaks(),
        loadWeekly(),
        loadHeatmap()
    ]);
}

async function loadSummary() {
    try {
        const res = await fetch(`${API}/analytics/summary`, { headers: authHeaders() });
        if (res.status === 401) { logout(); return; }
        const data = await res.json();
        document.getElementById('tasks-completed').textContent = data.completed_tasks;
        document.getElementById('tasks-label').textContent = `of ${data.total_tasks} tasks`;
        document.getElementById('completion-rate').textContent = `${Math.round(data.completion_rate * 100)}%`;
        document.getElementById('habit-logs').textContent = data.total_habit_logs;
        document.getElementById('habits-label').textContent = `across ${data.total_habits} habits`;
        document.getElementById('welcome-msg').textContent = `You have ${data.total_habits} active habits and ${data.total_tasks} tasks tracked.`;
    } catch (e) { console.error(e); }
}

async function loadProductivity() {
    try {
        const res = await fetch(`${API}/analytics/productivity`, { headers: authHeaders() });
        const data = await res.json();
        const score = data.productivity_score;
        document.getElementById('prod-score').textContent = score;
        document.getElementById('score-fill').style.width = `${score}%`;
    } catch (e) { console.error(e); }
}

async function loadStreaks() {
    try {
        const res = await fetch(`${API}/analytics/streaks`, { headers: authHeaders() });
        const data = await res.json();
        const grid = document.getElementById('streaks-grid');

        if (!data.length) {
            grid.innerHTML = '<p class="loading">No habits tracked yet.</p>';
            return;
        }

        grid.innerHTML = data.map(s => `
            <div class="streak-card">
                <div class="habit-name">${s.habit_name}</div>
                <div class="streak-num">🔥 ${s.current_streak}</div>
                <div class="streak-label">day streak</div>
                <div style="margin-top:0.5rem;font-size:0.8rem;color:#64748b;">
                    Longest: ${s.longest_streak} days
                </div>
            </div>
        `).join('');
    } catch (e) { console.error(e); }
}

async function loadWeekly() {
    try {
        const res = await fetch(`${API}/analytics/weekly`, { headers: authHeaders() });
        const data = await res.json();
        document.getElementById('week-created').textContent = data.tasks_created;
        document.getElementById('week-completed').textContent = data.tasks_completed;
        document.getElementById('week-habits').textContent = data.habit_logs_completed;

        if (data.holidays && data.holidays.length > 0) {
            document.getElementById('holidays-section').innerHTML = `
                <div style="margin-top:1rem;font-size:0.8rem;color:#94a3b8;">UK Holidays this week:</div>
                ${data.holidays.map(h => `<span class="holiday-tag">🇬🇧 ${h.name}</span>`).join('')}
            `;
        }
    } catch (e) { console.error(e); }
}

async function loadHeatmap() {
    try {
        const res = await fetch(`${API}/analytics/heatmap`, { headers: authHeaders() });
        const data = await res.json();
        const heatmap = document.getElementById('heatmap');

        if (!data.length) {
            heatmap.innerHTML = '<p class="loading">No activity yet.</p>';
            return;
        }

        const max = Math.max(...data.map(d => d.activity));

        heatmap.innerHTML = data.map(d => {
            const intensity = max > 0 ? d.activity / max : 0;
            const color = intensity === 0 ? '#1e293b' :
                intensity < 0.3 ? '#164e63' :
                intensity < 0.6 ? '#0e7490' :
                intensity < 0.8 ? '#0284c7' : '#38bdf8';
            return `<div class="heatmap-cell" style="background:${color}" title="${d.date}: ${d.activity} activities"></div>`;
        }).join('');
    } catch (e) { console.error(e); }
}

document.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleAuth();
});