const API_URL = "https://scientific-backend.onrender.com";

// Check Admin Auth on Load
document.addEventListener('DOMContentLoaded', () => {
    const userStr = localStorage.getItem('user');
    if (!userStr) {
        window.location.href = 'login.html';
        return;
    }

    try {
        const user = JSON.parse(userStr);
        if (user.role !== 'admin') {
            alert("Access Denied: Admins only.");
            window.location.href = 'index.html';
            return;
        }
    } catch (e) {
        window.location.href = 'login.html';
        return;
    }

    // Load Initial Data
    fetchStats();

    // Set Admin Email in Profile
    const adminUser = JSON.parse(localStorage.getItem('user'));
    if (adminUser && adminUser.email) {
        document.getElementById('adminEmailDisplay').innerText = adminUser.email;
        document.getElementById('profileMenuEmail').innerText = adminUser.email;
    }
});

function toggleProfileMenu() {
    const menu = document.getElementById('profileMenu');
    menu.classList.toggle('active');
}

// Close profile menu when clicking outside
document.addEventListener('click', function (event) {
    const profile = document.querySelector('.user-profile');
    const menu = document.getElementById('profileMenu');

    if (profile && !profile.contains(event.target)) {
        menu.classList.remove('active');
    }
});

function logoutAdmin() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}

function showSection(sectionId) {
    // Hide all sections
    const sections = ['overview', 'users', 'history', 'feedback', 'quiz', 'youtube', 'tree'];
    sections.forEach(id => {
        const el = document.getElementById(`${id}-section`);
        if (el) el.style.display = 'none';

        // Hide/Show Profile Section - Only visible in Overview
        const profile = document.querySelector('.user-profile');
        if (profile) {
            profile.style.display = (sectionId === 'overview') ? 'flex' : 'none';
        }
    });

    // Remove active class from nav links
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));

    // Show selected section
    const selected = document.getElementById(`${sectionId}-section`);
    if (selected) selected.style.display = 'block';

    // Highlight nav link
    event.currentTarget.classList.add('active');

    // Fetch data if needed
    if (sectionId === 'users') fetchUsers();
    if (sectionId === 'history') fetchHistory();
    if (sectionId === 'feedback') fetchFeedback();
    if (sectionId === 'quiz') fetchQuizData();
    if (sectionId === 'youtube') fetchYouTubeData();
    if (sectionId === 'tree') fetchTreeData();
    if (sectionId === 'analytics') fetchComparisonData();
}

let userChartInstance = null;
let termsChartInstance = null;
let levelChartInstance = null;
let languageChartInstance = null;
let feedbackChartInstance = null;

async function fetchStats() {
    try {
        const response = await fetch(`${API_URL}/admin/stats`);
        const data = await response.json();

        document.getElementById('totalUsers').innerText = data.total_users;
        document.getElementById('totalExplanations').innerText = data.total_explanations;
        document.getElementById('totalFeedback').innerText = data.total_feedback;
        document.getElementById('avgRating').innerText = data.average_rating;

        renderUserActivityChart(data.chart_data);
        renderTopTermsChart(data.chart_data.top_terms);
        renderLevelDistributionChart(data.chart_data.levels);
        renderLanguageChart(data.chart_data.languages);
        renderFeedbackChart(data.chart_data.sentiment, data.average_rating);
        renderRecentActivity(data.recent_activity);

        // Fetch comparison data for Overview
        fetchComparisonData();

    } catch (error) {
        console.error("Error fetching stats:", error);
    }
}

function renderUserActivityChart(chartData) {
    const ctx = document.getElementById('userTypeChart').getContext('2d'); // Keep original ID for chart element

    if (userChartInstance) {
        userChartInstance.destroy();
    }

    userChartInstance = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Registered Users', 'Guests'],
            datasets: [{
                data: [chartData.registered, chartData.guest],
                backgroundColor: ['#bb86fc', '#03dac6'],
                borderColor: ['rgba(187, 134, 252, 1)', 'rgba(3, 218, 198, 1)'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#e0e0e0' }
                }
            }
        }
    });
}

function renderTopTermsChart(topTerms) {
    const ctx = document.getElementById('topTermsChart').getContext('2d');
    const terms = topTerms.map(t => t.term);
    const counts = topTerms.map(t => t.count);

    if (termsChartInstance) termsChartInstance.destroy();

    termsChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: terms,
            datasets: [{
                label: 'Search Count',
                data: counts,
                backgroundColor: 'rgba(187, 134, 252, 0.6)',
                borderColor: '#bb86fc',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: '#a0a0a0' },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' }
                },
                x: {
                    ticks: { color: '#a0a0a0' },
                    grid: { display: false }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

function renderLevelDistributionChart(levels) {
    const ctx = document.getElementById('levelDistributionChart').getContext('2d');
    const labels = Object.keys(levels || {});
    const data = Object.values(levels || {});

    // Normalize labels (optional capitalization)
    const formattedLabels = labels.map(l => l ? l.charAt(0).toUpperCase() + l.slice(1) : 'Unknown');

    if (levelChartInstance) levelChartInstance.destroy();

    levelChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: formattedLabels,
            datasets: [{
                data: data,
                backgroundColor: [
                    '#2ecc71', // Green for Beginner
                    '#3498db', // Blue for Intermediate
                    '#e74c3c', // Red for Advanced
                    '#95a5a6'  // Grey for unknown
                ],
                borderColor: '#1e1e28',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#e0e0e0', boxWidth: 12 }
                }
            }
        }
    });
}

function renderLanguageChart(languages) {
    const ctx = document.getElementById('languageUsageChart').getContext('2d');
    const labels = Object.keys(languages || {});
    const data = Object.values(languages || {});

    if (languageChartInstance) languageChartInstance.destroy();

    languageChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Explanations',
                data: data,
                backgroundColor: [
                    '#f1c40f', // Yellow for English or first
                    '#e67e22'  // Orange for Hindi or second
                ],
                borderColor: '#1e1e28',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: { color: '#a0a0a0' },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' }
                },
                y: {
                    ticks: { color: '#fff' },
                    grid: { display: false }
                }
            },
            plugins: {
                legend: { display: false },
                title: { display: false }
            }
        }
    });
}

function renderFeedbackChart(sentiment, avgRating) {
    const ctx = document.getElementById('feedbackSentimentChart').getContext('2d');

    // Update center value
    const gaugeValueElement = document.getElementById('gaugeValue');
    if (gaugeValueElement) {
        gaugeValueElement.innerText = avgRating || "0.0";
    }

    // Order for Gauge: Negative (Left), Medium (Top), Positive (Right)
    const labels = ['Negative', 'Medium', 'Positive'];
    const data = [
        sentiment.Negative || 0,
        sentiment.Medium || 0,
        sentiment.Positive || 0
    ];

    if (feedbackChartInstance) feedbackChartInstance.destroy();

    feedbackChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    '#e74c3c', // Red (Negative)
                    '#f1c40f', // Yellow (Medium)
                    '#2ecc71'  // Green (Positive)
                ],
                borderColor: '#1e1e28',
                borderWidth: 2,
                cutout: '70%'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            rotation: -90,
            circumference: 180,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#e0e0e0', boxWidth: 12 }
                },
                tooltip: {
                    enabled: true
                }
            }
        }
    });
}

function renderRecentActivity(activities) {
    const list = document.getElementById('recentActivityList');
    list.innerHTML = '';

    if (!activities || activities.length === 0) {
        list.innerHTML = '<li>No recent activity.</li>';
        return;
    }

    activities.forEach(item => {
        const time = item.time ? new Date(item.time).toLocaleString() : 'Unknown Time';
        const li = document.createElement('li');
        li.style.padding = '10px 0';
        li.style.borderBottom = '1px solid rgba(255,255,255,0.05)';
        li.innerHTML = `
            <span style="color: #fff; font-weight: 600;">${item.term}</span>
            <span style="color: #bb86fc; font-size: 0.9em; margin-left: 10px;">(${item.user})</span>
            <span style="float: right; font-size: 0.85em; opacity: 0.7;">${time}</span>
        `;
        list.appendChild(li);
    });
}

let allUsers = [];
let allHistory = [];
let allFeedback = [];

async function fetchUsers() {
    const btn = document.querySelector('#users-section button');
    if (btn) { btn.disabled = true; btn.innerText = 'Refreshing...'; }

    try {
        const response = await fetch(`${API_URL}/admin/users`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        allUsers = await response.json();
        filterUsers(); // Initial render with current filter
    } catch (error) {
        console.error("Error fetching users:", error);
        document.getElementById('usersTableBody').innerHTML = `<tr><td colspan="4" style="text-align:center; color: #ff6b6b;">Error loading users. Please check backend.</td></tr>`;
    } finally {
        if (btn) { btn.disabled = false; btn.innerText = 'Refresh'; }
    }
}

function filterUsers() {
    const dateInput = document.getElementById('userDateFilter').value;
    let filteredUsers = allUsers;

    if (dateInput) {
        filteredUsers = allUsers.filter(user => {
            if (!user.created_at) return false;
            try {
                const userDate = new Date(user.created_at).toISOString().split('T')[0];
                return userDate === dateInput;
            } catch (e) {
                console.warn("Invalid date format:", user.created_at);
                return false;
            }
        });
    }

    renderUsers(filteredUsers);
}

function renderUsers(users) {
    const tbody = document.getElementById('usersTableBody');
    tbody.innerHTML = '';

    if (users.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;">No users found</td></tr>';
        return;
    }

    users.forEach(user => {
        let joinedDate = 'N/A';
        if (user.created_at) {
            try {
                const dateObj = new Date(user.created_at);
                joinedDate = dateObj.toLocaleString();
            } catch (e) {
                joinedDate = user.created_at;
            }
        }

        const row = `
            <tr>
                <td>${user.id}</td>
                <td>${user.name || 'N/A'}</td>
                <td>${user.email}</td>
                <td>${joinedDate}</td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
}

// --- Chat History Functions ---

async function fetchHistory() {
    const btn = document.querySelector('#history-section button');
    if (btn) { btn.disabled = true; btn.innerText = 'Refreshing...'; }

    try {
        const response = await fetch(`${API_URL}/admin/history`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        allHistory = await response.json();
        filterHistory();
    } catch (error) {
        console.error("Error fetching history:", error);
        document.getElementById('historyTableBody').innerHTML = `<tr><td colspan="5" style="text-align:center; color: #ff6b6b;">Error loading history. Please check backend.</td></tr>`;
    } finally {
        if (btn) { btn.disabled = false; btn.innerText = 'Refresh'; }
    }
}

function filterHistory() {
    const dateInput = document.getElementById('historyDateFilter').value;
    let filteredHistory = allHistory;

    if (dateInput) {
        filteredHistory = allHistory.filter(item => {
            if (!item.timestamp) return false;
            try {
                const itemDate = new Date(item.timestamp).toISOString().split('T')[0];
                return itemDate === dateInput;
            } catch (e) {
                return false;
            }
        });
    }

    renderHistory(filteredHistory);
}

function renderHistory(history) {
    const tbody = document.getElementById('historyTableBody');
    tbody.innerHTML = '';

    if (history.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">No history found</td></tr>';
        return;
    }

    history.forEach(item => {
        let dateStr = 'N/A';
        try { dateStr = new Date(item.timestamp).toLocaleString(); } catch (e) { }

        // Truncate explanation for viewing
        const shortExplanation = item.explanation.length > 50 ? item.explanation.substring(0, 50) + '...' : item.explanation;

        const row = `
            <tr>
                <td>${dateStr}</td>
                <td>${item.user_email || 'Guest'}</td>
                <td>${item.term}</td>
                <td>${item.level}</td>
                <td title="${item.explanation.replace(/"/g, '&quot;')}">${shortExplanation}</td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
}

async function fetchFeedback() {
    const btn = document.querySelector('#feedback-section button');
    if (btn) { btn.disabled = true; btn.innerText = 'Refreshing...'; }

    try {
        const response = await fetch(`${API_URL}/admin/feedback`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        allFeedback = await response.json();
        filterFeedback();
    } catch (error) {
        console.error("Error fetching feedback:", error);
        // Show specific error for debugging
        document.getElementById('feedbackTableBody').innerHTML = `<tr><td colspan="4" style="text-align:center; color: #ff6b6b;">Error: ${error.message}. Check console.</td></tr>`;
    } finally {
        if (btn) { btn.disabled = false; btn.innerText = 'Refresh'; }
    }
}

function filterFeedback() {
    const dateInput = document.getElementById('feedbackDateFilter').value;
    let filteredFeedback = allFeedback;

    if (dateInput) {
        filteredFeedback = allFeedback.filter(item => {
            if (!item.created_at) return false;
            try {
                const itemDate = new Date(item.created_at).toISOString().split('T')[0];
                return itemDate === dateInput;
            } catch (e) {
                console.warn("Invalid date format:", item.created_at);
                return false;
            }
        });
    }

    renderFeedback(filteredFeedback);
}

function renderFeedback(feedbackList) {
    const tbody = document.getElementById('feedbackTableBody');
    tbody.innerHTML = '';

    if (feedbackList.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;">No feedback found</td></tr>';
        return;
    }

    feedbackList.forEach(item => {
        let dateStr = 'N/A';
        if (item.created_at) {
            try {
                dateStr = new Date(item.created_at).toLocaleString();
            } catch (e) {
                dateStr = item.created_at;
            }
        }

        const ratingStars = '⭐'.repeat(item.rating);

        const row = `
            <tr>
                <td>${dateStr}</td>
                <td>${item.user_email || 'Guest'}</td>
                <td><span class="star-rating">${ratingStars}</span></td>
                <td>${item.comment || '-'}</td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
}

// --- New Tracking Functions ---

let allQuizLogs = [];
let allYoutubeLogs = [];
let allTreeLogs = [];

async function fetchQuizData() {
    const btn = document.querySelector('#quiz-section button');
    if (btn) { btn.disabled = true; btn.innerText = 'Refreshing...'; }

    try {
        const response = await fetch(`${API_URL}/admin/quiz`);
        const data = await response.json();
        renderQuizStats(data.stats);
        allQuizLogs = data.logs;
        filterQuiz();
    } catch (error) {
        console.error("Error fetching quiz data:", error);
        document.querySelector('#quiz-section .stat-card').innerHTML = `<div class="stat-label" style="color:red">Error: ${error.message}</div>`;
    } finally {
        if (btn) { btn.disabled = false; btn.innerText = 'Refresh'; }
    }
}

function filterQuiz() {
    const dateInput = document.getElementById('quizDateFilter').value;
    let filteredLogs = allQuizLogs;

    if (dateInput) {
        filteredLogs = allQuizLogs.filter(log => {
            if (!log.created_at) return false;
            try {
                const logDate = new Date(log.created_at).toISOString().split('T')[0];
                return logDate === dateInput;
            } catch (e) {
                return false;
            }
        });
    }
    renderQuizLogs(filteredLogs);
}

function renderQuizStats(stats) {
    const container = document.querySelector('#quiz-section .stat-card');
    if (!stats || stats.length === 0) {
        container.innerHTML = '<div class="stat-label">No quiz data available</div>';
        return;
    }

    // Simple Table for Stats
    let html = '<h3>Average Scores by Topic</h3><table style="width:100%; margin-top:10px;"><tr><th>Term</th><th>Avg Score</th></tr>';
    stats.forEach(s => {
        html += `<tr><td>${s.term}</td><td>${s.avg_score}%</td></tr>`;
    });
    html += '</table>';
    container.innerHTML = html;
}

function renderQuizLogs(logs) {
    // Remove existing logs if any
    const existingLogs = document.querySelector('#quiz-section .logs-table');
    if (existingLogs) existingLogs.remove();

    if (!logs || logs.length === 0) {
        const container = document.getElementById('quiz-section');
        const emptyMsg = `<div class="logs-table user-table-container" style="margin-top:20px; text-align:center; padding:20px;">No quiz attempts found.</div>`;
        container.insertAdjacentHTML('beforeend', emptyMsg);
        return;
    }

    const container = document.getElementById('quiz-section');

    let html = `
        <div class="logs-table user-table-container" style="margin-top:20px;">
            <h3>Recent Quiz Attempts</h3>
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>User</th>
                        <th>Topic</th>
                        <th>Score</th>
                    </tr>
                </thead>
                <tbody>
    `;

    logs.forEach(log => {
        let dateStr = 'N/A';
        try { dateStr = new Date(log.created_at).toLocaleString(); } catch (e) { }

        html += `
            <tr>
                <td>${dateStr}</td>
                <td>${log.user_email || 'Guest'}</td>
                <td>${log.term}</td>
                <td>${log.score}</td>
            </tr>
        `;
    });

    html += `</tbody></table></div>`;
    container.insertAdjacentHTML('beforeend', html);
}

async function fetchYouTubeData() {
    const btn = document.querySelector('#youtube-section button');
    if (btn) { btn.disabled = true; btn.innerText = 'Refreshing...'; }

    try {
        const response = await fetch(`${API_URL}/admin/youtube`);
        const data = await response.json();
        renderYouTubeStats(data.stats);
        allYoutubeLogs = data.logs;
        filterYouTube();
    } catch (error) {
        console.error("Error fetching youtube data:", error);
        document.querySelector('#youtube-section .stat-card').innerHTML = `<div class="stat-label" style="color:red">Error: ${error.message}</div>`;
    } finally {
        if (btn) { btn.disabled = false; btn.innerText = 'Refresh'; }
    }
}

function filterYouTube() {
    const dateInput = document.getElementById('youtubeDateFilter').value;
    let filteredLogs = allYoutubeLogs;

    if (dateInput) {
        filteredLogs = allYoutubeLogs.filter(log => {
            if (!log.created_at) return false;
            try {
                const logDate = new Date(log.created_at).toISOString().split('T')[0];
                return logDate === dateInput;
            } catch (e) {
                return false;
            }
        });
    }
    renderYouTubeLogs(filteredLogs);
}

function renderYouTubeLogs(logs) {
    const existingLogs = document.querySelector('#youtube-section .logs-table');
    if (existingLogs) existingLogs.remove();

    if (!logs || logs.length === 0) {
        const container = document.getElementById('youtube-section');
        const emptyMsg = `<div class="logs-table user-table-container" style="margin-top:20px; text-align:center; padding:20px;">No video views found.</div>`;
        container.insertAdjacentHTML('beforeend', emptyMsg);
        return;
    }

    const container = document.getElementById('youtube-section');

    let html = `
        <div class="logs-table user-table-container" style="margin-top:20px;">
            <h3>Recent Video Views</h3>
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>User</th>
                        <th>Topic</th>
                        <th>Video ID</th>
                    </tr>
                </thead>
                <tbody>
    `;

    logs.forEach(log => {
        let dateStr = 'N/A';
        try { dateStr = new Date(log.created_at).toLocaleString(); } catch (e) { }

        html += `
            <tr>
                <td>${dateStr}</td>
                <td>${log.user_email || 'Guest'}</td>
                <td>${log.term}</td>
                <td><a href="https://youtu.be/${log.video_id}" target="_blank">${log.video_id}</a></td>
            </tr>
        `;
    });

    html += `</tbody></table></div>`;
    container.insertAdjacentHTML('beforeend', html);
}

function renderYouTubeStats(stats) {
    const container = document.querySelector('#youtube-section .stat-card');
    if (!stats || stats.length === 0) {
        container.innerHTML = '<div class="stat-label">No video data available</div>';
        return;
    }

    let html = '<h3>Most Watched Topics</h3><table style="width:100%; margin-top:10px;"><tr><th>Term</th><th>Views</th></tr>';
    stats.forEach(s => {
        html += `<tr><td>${s.term}</td><td>${s.count}</td></tr>`;
    });
    html += '</table>';
    container.innerHTML = html;
}

async function fetchTreeData() {
    const btn = document.querySelector('#tree-section button');
    if (btn) { btn.disabled = true; btn.innerText = 'Refreshing...'; }

    try {
        const response = await fetch(`${API_URL}/admin/tree`);
        const data = await response.json();
        renderTreeStats(data.stats);
        allTreeLogs = data.logs;
        filterTree();
    } catch (error) {
        console.error("Error fetching tree data:", error);
        document.querySelector('#tree-section .stat-card').innerHTML = `<div class="stat-label" style="color:red">Error: ${error.message}</div>`;
    } finally {
        if (btn) { btn.disabled = false; btn.innerText = 'Refresh'; }
    }
}

function filterTree() {
    const dateInput = document.getElementById('treeDateFilter').value;
    let filteredLogs = allTreeLogs;

    if (dateInput) {
        filteredLogs = allTreeLogs.filter(log => {
            if (!log.created_at) return false;
            try {
                const logDate = new Date(log.created_at).toISOString().split('T')[0];
                return logDate === dateInput;
            } catch (e) {
                return false;
            }
        });
    }
    renderTreeLogs(filteredLogs);
}

function renderTreeLogs(logs) {
    const existingLogs = document.querySelector('#tree-section .logs-table');
    if (existingLogs) existingLogs.remove();

    if (!logs || logs.length === 0) {
        const container = document.getElementById('tree-section');
        const emptyMsg = `<div class="logs-table user-table-container" style="margin-top:20px; text-align:center; padding:20px;">No concept trees found.</div>`;
        container.insertAdjacentHTML('beforeend', emptyMsg);
        return;
    }

    const container = document.getElementById('tree-section');

    let html = `
        <div class="logs-table user-table-container" style="margin-top:20px;">
            <h3>Recent Concept Trees</h3>
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>User</th>
                        <th>Topic</th>
                    </tr>
                </thead>
                <tbody>
    `;

    logs.forEach(log => {
        let dateStr = 'N/A';
        try { dateStr = new Date(log.created_at).toLocaleString(); } catch (e) { }

        html += `
            <tr>
                <td>${dateStr}</td>
                <td>${log.user_email || 'Guest'}</td>
                <td>${log.term}</td>
            </tr>
        `;
    });

    html += `</tbody></table></div>`;
    container.insertAdjacentHTML('beforeend', html);
}

function renderTreeStats(stats) {
    const container = document.querySelector('#tree-section .stat-card');
    if (!stats || stats.length === 0) {
        container.innerHTML = '<div class="stat-label">No tree data available</div>';
        return;
    }

    let html = '<h3>Most Concept Trees Generated</h3><table style="width:100%; margin-top:10px;"><tr><th>Term</th><th>Count</th></tr>';
    stats.forEach(s => {
        html += `<tr><td>${s.term}</td><td>${s.count}</td></tr>`;
    });
    html += '</table>';
    container.innerHTML = html;
}

// --- Analytics Functions ---

let comparisonChart = null;

async function fetchComparisonData() {
    const range = document.getElementById('analyticsRange').value || 30;
    // Button is sibling to select
    const btn = document.querySelector('#analyticsRange + button');

    if (btn) { btn.disabled = true; btn.innerText = 'Refreshing...'; }

    try {
        const response = await fetch(`${API_URL}/admin/comparison?days=${range}`);
        const data = await response.json();
        renderComparisonChart(data);
    } catch (error) {
        console.error("Error fetching comparison data:", error);
    } finally {
        if (btn) { btn.disabled = false; btn.innerText = 'Refresh'; }
    }
}

function renderComparisonChart(data) {
    const ctx = document.getElementById('comparisonChart').getContext('2d');

    if (comparisonChart) {
        comparisonChart.destroy();
    }

    comparisonChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [
                {
                    label: 'Quiz Attempts',
                    data: data.quiz,
                    borderColor: '#8e44ad', // Purple
                    backgroundColor: 'rgba(142, 68, 173, 0.2)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Video Views',
                    data: data.video,
                    borderColor: '#2ecc71', // Green
                    backgroundColor: 'rgba(46, 204, 113, 0.2)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Concept Trees',
                    data: data.tree,
                    borderColor: '#e67e22', // Orange
                    backgroundColor: 'rgba(230, 126, 34, 0.2)',
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: { color: '#fff' }
                },
                title: {
                    display: true,
                    text: 'User Engagement Trends',
                    color: '#fff'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    ticks: { color: '#ddd' }
                },
                x: {
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    ticks: { color: '#ddd' }
                }
            }
        }
    });
}
