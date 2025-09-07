// WPSG Main Application JavaScript - External File

// Global state
let currentCommittees = [];
let currentFilter = 'CEN';
let isLoading = false;

// DOM Elements (will be initialized when DOM loads)
let committeeList, addButton, scanButton, lastUpdatedElement, cenBtn, isoBtn;

// Edit icon SVG
const editIconSvg = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
    <path d="m18.5 2.5 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
</svg>`;

// Initialize application
document.addEventListener('DOMContentLoaded', async function() {
    console.log('WPSG App - DOM Content Loaded');
    
    // Initialize DOM elements
    initializeDOMElements();
    
    try {
        console.log('Loading app status...');
        await loadAppStatus();
        
        console.log('Loading committees...');
        await loadCommittees();
        
        console.log('Setting up event listeners...');
        setupEventListeners();
        
        console.log('WPSG App initialized successfully');
        showMessage('Application loaded successfully', 'success');
        
    } catch (error) {
        console.error('Error initializing app:', error);
        showMessage('Failed to initialize application: ' + error.message, 'error');
    }
});

// Initialize DOM element references
function initializeDOMElements() {
    committeeList = document.getElementById('committeeList');
    addButton = document.getElementById('addCommittee');
    scanButton = document.getElementById('scanUpdates');
    lastUpdatedElement = document.getElementById('lastUpdatedDate');
    cenBtn = document.getElementById('cenBtn');
    isoBtn = document.getElementById('isoBtn');
    
    // Verify all elements exist
    const elements = {
        committeeList, addButton, scanButton, lastUpdatedElement, cenBtn, isoBtn
    };
    
    for (const [name, element] of Object.entries(elements)) {
        if (!element) {
            console.error(`Missing DOM element: ${name}`);
        }
    }
}

// Load application status
async function loadAppStatus() {
    try {
        console.log('Calling eel.get_app_status()...');
        const status = await eel.get_app_status()();
        
        if (status && status.last_update && lastUpdatedElement) {
            lastUpdatedElement.textContent = status.last_update;
        }
        
        console.log('App status loaded:', status);
        return status;
        
    } catch (error) {
        console.error('Error loading app status:', error);
        if (lastUpdatedElement) {
            lastUpdatedElement.textContent = '23 August 2025';
        }
        throw error;
    }
}

// Load committees from backend
async function loadCommittees() {
    try {
        console.log(`Loading committees for ${currentFilter}...`);
        currentCommittees = await eel.get_committees(currentFilter)();
        
        console.log(`Loaded ${currentCommittees.length} committees`);
        renderCommittees();
        return currentCommittees;
        
    } catch (error) {
        console.error('Error loading committees:', error);
        showMessage('Failed to load committees: ' + error.message, 'error');
        throw error;
    }
}

// Filter functionality
async function switchFilter(filter) {
    if (isLoading) {
        console.log('Already loading, ignoring filter switch');
        return;
    }
    
    console.log(`Switching filter from ${currentFilter} to ${filter}`);
    currentFilter = filter;
    
    // Update UI
    if (filter === 'CEN') {
        cenBtn.classList.add('active');
        isoBtn.classList.remove('active');
    } else {
        isoBtn.classList.add('active');
        cenBtn.classList.remove('active');
    }
    
    // Load committees for selected filter
    try {
        await loadCommittees();
        showMessage(`Switched to ${filter} committees`, 'info');
    } catch (error) {
        showMessage(`Failed to switch to ${filter}: ${error.message}`, 'error');
    }
}

// Render committee list
function renderCommittees() {
    if (!committeeList) {
        console.error('Committee list element not found');
        return;
    }
    
    if (!currentCommittees || currentCommittees.length === 0) {
        committeeList.innerHTML = '<div class="error" style="padding: 20px; text-align: center; color: #666;">No committees loaded</div>';
        return;
    }
    
    committeeList.innerHTML = '';
    
    currentCommittees.forEach((committee, index) => {
        const item = document.createElement('div');
        item.className = 'committee-item';
        item.innerHTML = `
            <span class="committee-name" data-index="${index}">${committee}</span>
            <div class="edit-icon" data-index="${index}" title="Edit committee">${editIconSvg}</div>
        `;
        committeeList.appendChild(item);
    });
    
    console.log(`Rendered ${currentCommittees.length} committees`);
}

// Handle inline editing
function enableEditing(element, index) {
    const currentText = element.textContent;
    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'committee-input';
    input.value = currentText;
    
    element.replaceWith(input);
    input.focus();
    input.select();
    
    const saveEdit = async () => {
        const newValue = input.value.trim();
        if (newValue && newValue !== currentText) {
            try {
                console.log(`Updating committee: ${currentText} -> ${newValue}`);
                
                // Update local array
                currentCommittees[index] = newValue;
                
                // Update in backend
                const success = await eel.update_committees(currentFilter, currentCommittees)();
                
                if (success) {
                    console.log(`Committee updated successfully`);
                    showMessage('Committee updated successfully', 'success');
                } else {
                    console.error('Failed to update committee in backend');
                    showMessage('Failed to update committee', 'error');
                    // Revert local change
                    currentCommittees[index] = currentText;
                }
                
            } catch (error) {
                console.error('Error updating committee:', error);
                showMessage('Error updating committee: ' + error.message, 'error');
                // Revert local change
                currentCommittees[index] = currentText;
            }
        }
        renderCommittees();
    };
    
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            saveEdit();
        }
    });
    
    input.addEventListener('blur', saveEdit);
}

// Add new committee
async function addNewCommittee() {
    if (isLoading) {
        console.log('Already loading, ignoring add committee');
        return;
    }
    
    const newCommitteeName = `New ${currentFilter} Committee`;
    
    try {
        console.log(`Adding new committee: ${newCommitteeName}`);
        
        const success = await eel.add_committee(currentFilter, newCommitteeName)();
        
        if (success) {
            await loadCommittees(); // Reload to get updated list
            
            // Find the new committee and enable editing
            setTimeout(() => {
                const newIndex = currentCommittees.indexOf(newCommitteeName);
                if (newIndex !== -1) {
                    const newElement = committeeList.querySelector(`[data-index="${newIndex}"].committee-name`);
                    if (newElement) {
                        enableEditing(newElement, newIndex);
                    }
                }
            }, 100);
            
            showMessage('Committee added successfully', 'success');
            
        } else {
            showMessage('Failed to add committee', 'error');
        }
        
    } catch (error) {
        console.error('Error adding committee:', error);
        showMessage('Error adding committee: ' + error.message, 'error');
    }
}

// Perform scan
async function performScan() {
    if (isLoading) {
        console.log('Already loading, ignoring scan');
        return;
    }
    
    isLoading = true;
    scanButton.textContent = 'Scanning...';
    scanButton.disabled = true;
    
    try {
        console.log('Starting scan...');
        const result = await eel.perform_scan()();
        
        if (result && result.success) {
            console.log('Scan completed successfully:', result);
            showMessage(result.message || 'Scan completed successfully', 'success');
            
            // Update last scanned date
            try {
                const newDate = await eel.update_last_scan()();
                if (lastUpdatedElement) {
                    lastUpdatedElement.textContent = newDate;
                }
            } catch (dateError) {
                console.error('Error updating last scan date:', dateError);
            }
            
        } else {
            console.error('Scan failed:', result ? result.message : 'Unknown error');
            showMessage(result ? result.message : 'Scan failed with unknown error', 'error');
        }
        
    } catch (error) {
        console.error('Error during scan:', error);
        showMessage('Scan failed: ' + error.message, 'error');
    } finally {
        isLoading = false;
        scanButton.textContent = 'Scan Updates';
        scanButton.disabled = false;
    }
}

// Test connection
async function testConnection() {
    try {
        console.log('Testing connection...');
        const result = await eel.test_connection()();
        
        if (result && result.success) {
            showMessage('Connection test successful', 'success');
            console.log('Connection test result:', result);
        } else {
            showMessage('Connection test failed: ' + (result ? result.message : 'Unknown error'), 'error');
        }
        
        return result;
        
    } catch (error) {
        console.error('Error testing connection:', error);
        showMessage('Connection test error: ' + error.message, 'error');
        return { success: false, message: error.message };
    }
}

// Event listeners
function setupEventListeners() {
    // Filter buttons
    if (cenBtn && isoBtn) {
        cenBtn.addEventListener('click', () => switchFilter('CEN'));
        isoBtn.addEventListener('click', () => switchFilter('ISO'));
    }
    
    // Committee list interactions
    if (committeeList) {
        committeeList.addEventListener('click', (e) => {
            const target = e.target;
            
            if (target.closest('.edit-icon')) {
                const index = parseInt(target.closest('.edit-icon').dataset.index);
                const nameElement = committeeList.querySelector(`[data-index="${index}"].committee-name`);
                if (nameElement) {
                    enableEditing(nameElement, index);
                }
            }
        });
        
        // Double-click to edit committee names
        committeeList.addEventListener('dblclick', (e) => {
            if (e.target.classList.contains('committee-name')) {
                const index = parseInt(e.target.dataset.index);
                enableEditing(e.target, index);
            }
        });
    }
    
    // Add committee button
    if (addButton) {
        addButton.addEventListener('click', addNewCommittee);
    }
    
    // Scan button
    if (scanButton) {
        scanButton.addEventListener('click', performScan);
    }
    
    // Dataset links
    document.querySelectorAll('.dataset-link').forEach((link, index) => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            if (index === 0 || index === 1) {
                // Navigate to database viewer
                console.log('Navigating to database viewer...');
                window.location.href = 'database_viewer.html';
            } else {
                // "Do I need more?" - show info
                showMessage('Additional datasets can be configured in the settings.', 'info');
            }
        });
    });
    
    console.log('Event listeners set up successfully');
}

// Utility functions
function showMessage(message, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${message}`);
    
    // For now, just use console.log and alerts for important messages
    // In a production app, you'd implement a proper notification system
    if (type === 'error') {
        console.error(message);
        // Optionally show alert for errors
        // alert('Error: ' + message);
    } else if (type === 'success') {
        console.log('✓ ' + message);
    }
}

// Expose functions for debugging and external access
window.wpsgApp = {
    // Data access
    getCurrentCommittees: () => currentCommittees,
    getCurrentFilter: () => currentFilter,
    
    // Actions
    performScan,
    testConnection,
    loadCommittees,
    switchFilter,
    
    // Debug functions
    debug: {
        loadAppStatus,
        isLoading: () => isLoading,
        showMessage
    }
};

console.log('WPSG App JavaScript loaded - External file version');