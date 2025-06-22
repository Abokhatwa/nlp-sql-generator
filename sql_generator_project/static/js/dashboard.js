// API Configuration
const API_BASE_URL = '/api';
let accessToken = localStorage.getItem('access_token');
let currentDatabase = null;
let queryResults = null;
let sessionCheckInterval = null;

// Example queries for each database
const exampleQueries = {
    'E-Commerce': [
        'Show me the top 5 customers by total order amount',
        'Find all products with stock less than 10',
        'Get all orders from the last 30 days',
        'Which product categories have the highest revenue?',
        'List all cancelled orders with their customer details'
    ],
    'Hospital Management': [
        'Show all appointments scheduled for tomorrow',
        'Find all patients with blood type O+',
        'List the top 10 doctors by number of appointments',
        'Get all prescriptions for patient ID 5',
        'Show departments with their head doctors'
    ],
    'School Management': [
        'Show all students in grade 10',
        'Find the average grade for each course',
        'List all students enrolled in Computer Science courses',
        'Show teachers and their course load',
        'Get the top 10 students by average grade'
    ]
};

// Validate session before any action
async function validateSession() {
    const token = localStorage.getItem('access_token');
    
    if (!token) {
        redirectToLogin();
        return false;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/validate/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                clearSessionAndRedirect();
                return false;
            }
        }
        
        return true;
    } catch (error) {
        console.error('Session validation error:', error);
        clearSessionAndRedirect();
        return false;
    }
}

// Clear session and redirect
function clearSessionAndRedirect() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    sessionStorage.clear();
    redirectToLogin();
}

// Redirect to login
function redirectToLogin() {
    window.location.replace('/login'); // Using replace to prevent back button
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', async () => {
    // Prevent caching
    preventPageCache();
    
    // Validate session immediately
    const isValid = await validateSession();
    if (!isValid) {
        return;
    }
    
    // Set up periodic session validation (every 30 seconds)
    sessionCheckInterval = setInterval(async () => {
        const valid = await validateSession();
        if (!valid) {
            clearInterval(sessionCheckInterval);
        }
    }, 30000);
    
    // Check for page visibility changes
    document.addEventListener('visibilitychange', async () => {
        if (!document.hidden) {
            const valid = await validateSession();
            if (!valid) {
                clearInterval(sessionCheckInterval);
            }
        }
    });
    
    // Load user info and setup
    await loadUserInfo();
    setupEventListeners();
});

// Prevent page caching
function preventPageCache() {
    // Set meta tags to prevent caching
    const metaNoCache = document.createElement('meta');
    metaNoCache.setAttribute('http-equiv', 'Cache-Control');
    metaNoCache.setAttribute('content', 'no-cache, no-store, must-revalidate');
    document.head.appendChild(metaNoCache);
    
    const metaPragma = document.createElement('meta');
    metaPragma.setAttribute('http-equiv', 'Pragma');
    metaPragma.setAttribute('content', 'no-cache');
    document.head.appendChild(metaPragma);
    
    const metaExpires = document.createElement('meta');
    metaExpires.setAttribute('http-equiv', 'Expires');
    metaExpires.setAttribute('content', '0');
    document.head.appendChild(metaExpires);
}

// Setup event listeners
function setupEventListeners() {
    document.getElementById('logoutBtn').addEventListener('click', logout);
    document.getElementById('databaseSelect').addEventListener('change', handleDatabaseChange);
    document.getElementById('generateBtn').addEventListener('click', generateAndExecuteSQL);
    document.getElementById('copySqlBtn').addEventListener('click', copySQLToClipboard);
    document.getElementById('exportCsvBtn').addEventListener('click', exportToCSV);
    
    // Intercept browser back button
    window.addEventListener('popstate', async (event) => {
        const valid = await validateSession();
        if (!valid) {
            event.preventDefault();
            clearSessionAndRedirect();
        }
    });
}

// Load user information with session validation
async function loadUserInfo() {
    try {
        const token = localStorage.getItem('access_token');
        if (!token) {
            clearSessionAndRedirect();
            return;
        }
        
        const response = await fetch(`${API_BASE_URL}/auth/user/`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                clearSessionAndRedirect();
                return;
            }
            throw new Error('Failed to load user info');
        }
        
        const data = await response.json();
        
        // Update UI with user info
        document.getElementById('username').textContent = data.user.username;
        document.getElementById('userRole').textContent = data.role || 'User';
        document.getElementById('userAvatar').textContent = data.user.username.charAt(0).toUpperCase();
        
        // Populate database dropdown
        const databaseSelect = document.getElementById('databaseSelect');
        databaseSelect.innerHTML = '<option value="">Select a database...</option>';
        data.accessible_databases.forEach(db => {
            const option = document.createElement('option');
            option.value = db;
            option.textContent = db;
            databaseSelect.appendChild(option);
        });
        
    } catch (error) {
        console.error('Error loading user info:', error);
        showToast('Failed to load user information', 'error');
        setTimeout(() => clearSessionAndRedirect(), 2000);
    }
}

// Handle database selection change
async function handleDatabaseChange(event) {
    // Validate session before proceeding
    const isValid = await validateSession();
    if (!isValid) return;
    
    currentDatabase = event.target.value;
    
    if (!currentDatabase) {
        document.getElementById('schemaSection').style.display = 'none';
        document.getElementById('statsSection').style.display = 'none';
        document.getElementById('exampleQueries').style.display = 'none';
        document.getElementById('generateBtn').disabled = true;
        return;
    }
    
    document.getElementById('generateBtn').disabled = false;
    
    // Load database schema
    await loadDatabaseSchema(currentDatabase);
    
    // Load database statistics
    await loadDatabaseStats(currentDatabase);
    
    // Show example queries
    showExampleQueries(currentDatabase);
    
    // Load query history for this database
    await loadQueryHistory(currentDatabase);
}

// Load database schema with session validation
async function loadDatabaseSchema(database) {
    try {
        const token = localStorage.getItem('access_token');
        if (!token) {
            clearSessionAndRedirect();
            return;
        }
        
        const response = await fetch(`${API_BASE_URL}/query/schema/?database=${encodeURIComponent(database)}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                clearSessionAndRedirect();
                return;
            }
            throw new Error('Failed to load schema');
        }
        
        const data = await response.json();
        
        if (data.success) {
            displaySchema(data.schema);
            document.getElementById('schemaSection').style.display = 'block';
        }
    } catch (error) {
        console.error('Error loading schema:', error);
        showToast('Failed to load database schema', 'error');
    }
}

// Display database schema
function displaySchema(schema) {
    const schemaInfo = document.getElementById('schemaInfo');
    schemaInfo.innerHTML = '';
    
    for (const [tableName, tableInfo] of Object.entries(schema.tables)) {
        const tableDiv = document.createElement('div');
        tableDiv.className = 'table-info';
        
        const tableTitle = document.createElement('h4');
        tableTitle.textContent = tableName;
        tableDiv.appendChild(tableTitle);
        
        const tableDesc = document.createElement('p');
        tableDesc.textContent = tableInfo.description;
        tableDiv.appendChild(tableDesc);
        
        const columnList = document.createElement('ul');
        columnList.className = 'column-list';
        
        tableInfo.columns.forEach(column => {
            const li = document.createElement('li');
            li.textContent = `• ${column}`;
            columnList.appendChild(li);
        });
        
        tableDiv.appendChild(columnList);
        schemaInfo.appendChild(tableDiv);
    }
}

// Load database statistics with session validation
async function loadDatabaseStats(database) {
    try {
        const token = localStorage.getItem('access_token');
        if (!token) {
            clearSessionAndRedirect();
            return;
        }
        
        const response = await fetch(`${API_BASE_URL}/query/stats/?database=${encodeURIComponent(database)}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                clearSessionAndRedirect();
                return;
            }
            throw new Error('Failed to load stats');
        }
        
        const data = await response.json();
        
        if (data.success) {
            displayStats(data.stats);
            document.getElementById('statsSection').style.display = 'block';
        }
    } catch (error) {
        console.error('Error loading stats:', error);
        showToast('Failed to load database statistics', 'error');
    }
}

// Display database statistics
function displayStats(stats) {
    const statsDiv = document.getElementById('databaseStats');
    statsDiv.innerHTML = '';
    
    for (const [table, count] of Object.entries(stats)) {
        const statItem = document.createElement('div');
        statItem.className = 'stat-item';
        statItem.innerHTML = `
            <span>${table}</span>
            <span class="stat-value">${count.toLocaleString()} rows</span>
        `;
        statsDiv.appendChild(statItem);
    }
}

// Show example queries
function showExampleQueries(database) {
    const exampleSection = document.getElementById('exampleQueries');
    const exampleButtons = document.getElementById('exampleButtons');
    
    exampleButtons.innerHTML = '';
    
    const queries = exampleQueries[database] || [];
    queries.forEach(query => {
        const btn = document.createElement('button');
        btn.className = 'example-btn';
        btn.textContent = query;
        btn.onclick = () => {
            document.getElementById('queryInput').value = query;
        };
        exampleButtons.appendChild(btn);
    });
    
    exampleSection.style.display = 'block';
}

// Generate and execute SQL with session validation
async function generateAndExecuteSQL() {
    // Validate session before executing
    const isValid = await validateSession();
    if (!isValid) return;
    
    const queryInput = document.getElementById('queryInput');
    const query = queryInput.value.trim();
    
    if (!query) {
        showToast('Please enter a query', 'warning');
        return;
    }
    
    if (!currentDatabase) {
        showToast('Please select a database', 'warning');
        return;
    }
    
    const generateBtn = document.getElementById('generateBtn');
    generateBtn.classList.add('loading');
    generateBtn.disabled = true;
    
    try {
        const token = localStorage.getItem('access_token');
        if (!token) {
            clearSessionAndRedirect();
            return;
        }
        
        const response = await fetch(`${API_BASE_URL}/query/execute/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query,
                database: currentDatabase
            })
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                clearSessionAndRedirect();
                return;
            }
        }
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data);
            showToast('Query executed successfully!', 'success');
        } else {
            showToast(data.error || 'Failed to execute query', 'error');
        }
    } catch (error) {
        console.error('Error executing query:', error);
        showToast('Failed to execute query', 'error');
    } finally {
        generateBtn.classList.remove('loading');
        generateBtn.disabled = false;
    }
}

// Display query results
function displayResults(data) {
    // Store results for export
    queryResults = data;
    
    // Show results section
    document.getElementById('resultsSection').style.display = 'block';
    
    // Display SQL query
    const sqlQuery = document.getElementById('sqlQuery');
    sqlQuery.textContent = data.sql_query;
    if (typeof Prism !== 'undefined') {
        Prism.highlightElement(sqlQuery);
    }
    
    // Display explanation
    const explanation = document.getElementById('sqlExplanation');
    if (data.explanation) {
        explanation.textContent = `💡 ${data.explanation}`;
        explanation.style.display = 'block';
    } else {
        explanation.style.display = 'none';
    }
    
    // Display statistics
    document.getElementById('resultStats').textContent = 
        `${data.row_count} rows • ${data.execution_time}s`;
    
    // Display table
    displayResultTable(data.columns, data.data);
    
    // Scroll to results
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

// Display result table
function displayResultTable(columns, data) {
    const table = document.getElementById('resultsTable');
    table.innerHTML = '';
    
    // Create header
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    
    columns.forEach(column => {
        const th = document.createElement('th');
        th.textContent = column;
        headerRow.appendChild(th);
    });
    
    thead.appendChild(headerRow);
    table.appendChild(thead);
    
    // Create body
    const tbody = document.createElement('tbody');
    
    data.forEach(row => {
        const tr = document.createElement('tr');
        columns.forEach(column => {
            const td = document.createElement('td');
            td.textContent = row[column] !== null ? row[column] : 'NULL';
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
    
    table.appendChild(tbody);
}

// Copy SQL to clipboard
async function copySQLToClipboard() {
    const sqlText = document.getElementById('sqlQuery').textContent;
    try {
        await navigator.clipboard.writeText(sqlText);
        showToast('SQL copied to clipboard!', 'success');
    } catch (err) {
        showToast('Failed to copy SQL', 'error');
    }
}

// Export results to CSV
function exportToCSV() {
    if (!queryResults || !queryResults.data || queryResults.data.length === 0) {
        showToast('No data to export', 'warning');
        return;
    }
    
    const columns = queryResults.columns;
    const data = queryResults.data;
    
    // Create CSV content
    let csv = columns.join(',') + '\n';
    
    data.forEach(row => {
        const values = columns.map(col => {
            const value = row[col];
            // Escape quotes and wrap in quotes if contains comma
            if (value === null) return '';
            const strValue = String(value);
            if (strValue.includes(',') || strValue.includes('"') || strValue.includes('\n')) {
                return `"${strValue.replace(/"/g, '""')}"`;
            }
            return strValue;
        });
        csv += values.join(',') + '\n';
    });
    
    // Download file
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', `query_results_${currentDatabase.toLowerCase().replace(' ', '_')}_${Date.now()}.csv`);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showToast('Results exported successfully!', 'success');
}

// Load query history with session validation
async function loadQueryHistory(database) {
    try {
        const token = localStorage.getItem('access_token');
        if (!token) {
            clearSessionAndRedirect();
            return;
        }
        
        const response = await fetch(`${API_BASE_URL}/query/history/?database=${encodeURIComponent(database)}&limit=5`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                clearSessionAndRedirect();
                return;
            }
            throw new Error('Failed to load history');
        }
        
        const data = await response.json();
        
        if (data.success && data.history.length > 0) {
            displayQueryHistory(data.history);
            document.getElementById('historySection').style.display = 'block';
        } else {
            document.getElementById('historySection').style.display = 'none';
        }
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

// Display query history
function displayQueryHistory(history) {
    const historyDiv = document.getElementById('queryHistory');
    historyDiv.innerHTML = '';
    
    history.forEach((item, index) => {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        
        const date = new Date(item.created_at);
        const timeAgo = getTimeAgo(date);
        
        historyItem.innerHTML = `
            <div class="history-header">
                <div class="history-query">${item.natural_language}</div>
                <div class="history-meta">
                    <span>${item.row_count} rows</span>
                    <span>${item.execution_time}s</span>
                    <span>${timeAgo}</span>
                </div>
            </div>
            <div class="history-sql">${item.sql}</div>
        `;
        
        historyDiv.appendChild(historyItem);
    });
}

// Get time ago string
function getTimeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);
    
    let interval = seconds / 31536000;
    if (interval > 1) return Math.floor(interval) + ' years ago';
    
    interval = seconds / 2592000;
    if (interval > 1) return Math.floor(interval) + ' months ago';
    
    interval = seconds / 86400;
    if (interval > 1) return Math.floor(interval) + ' days ago';
    
    interval = seconds / 3600;
    if (interval > 1) return Math.floor(interval) + ' hours ago';
    
    interval = seconds / 60;
    if (interval > 1) return Math.floor(interval) + ' minutes ago';
    
    return Math.floor(seconds) + ' seconds ago';
}

// Show toast notification
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icon = document.createElement('svg');
    icon.style.width = '20px';
    icon.style.height = '20px';
    icon.setAttribute('fill', 'none');
    icon.setAttribute('stroke', 'currentColor');
    icon.setAttribute('viewBox', '0 0 24 24');
    
    if (type === 'success') {
        icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>';
    } else if (type === 'error') {
        icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>';
    } else if (type === 'warning') {
        icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>';
    } else {
        icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>';
    }
    
    toast.appendChild(icon);
    toast.appendChild(document.createTextNode(message));
    
    container.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

// Logout function
async function logout() {
    try {
        const token = localStorage.getItem('access_token');
        const refreshToken = localStorage.getItem('refresh_token');
        
        if (token) {
            await fetch(`${API_BASE_URL}/auth/logout/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    refresh: refreshToken
                })
            });
        }
    } catch (error) {
        console.error('Error during logout:', error);
    } finally {
        // Clear all storage
        localStorage.clear();
        sessionStorage.clear();
        
        // Clear interval
        if (sessionCheckInterval) {
            clearInterval(sessionCheckInterval);
        }
        
        // Redirect to login (using replace to prevent back button)
        window.location.replace('/login');
    }
}

// Handle page unload
window.addEventListener('beforeunload', () => {
    // Clear interval on page unload
    if (sessionCheckInterval) {
        clearInterval(sessionCheckInterval);
    }
});

// Add CSS for slide out animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        to {
            transform: translateX(120%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);