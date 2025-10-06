

// WPSG Main Application JavaScript - UPDATED VERSION

// Global state
let currentCommittees = [];
let currentFilter = 'CEN';
let isLoading = false;
let currentLanguage = 'en'; // CHANGED: Default to English
let translations = {};

// DOM Elements (will be initialized when DOM loads)
let committeeList, addButton, scanButton, lastUpdatedElement, cenBtn, isoBtn;

// Edit and delete icon SVGs
const editIconSvg = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
    <path d="m18.5 2.5 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
</svg>`;

const deleteIconSvg = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <polyline points="3,6 5,6 21,6"></polyline>
    <path d="m19,6v14a2,2 0 0,1 -2,2H7a2,2 0 0,1 -2,-2V6m3,0V4a2,2 0 0,1 2,-2h4a2,2 0 0,1 2,2v2"></path>
    <line x1="10" y1="11" x2="10" y2="17"></line>
    <line x1="14" y1="11" x2="14" y2="17"></line>
</svg>`;

// Initialize application
document.addEventListener('DOMContentLoaded', async function() {
    console.log('WPSG App - DOM Content Loaded');
    
    // Initialize DOM elements
    initializeDOMElements();
    
    // CHANGED: Check if we need to reset window size from database viewer
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('resetSize') === 'true') {
        resetWindowSize();
    }
    
    try {
        console.log('Loading language and translations...');
        await loadLanguageAndTranslations();
        
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

// CHANGED: Function to reset window size
function resetWindowSize() {
    try {
        // Try to resize window back to 850x520
        window.resizeTo(930, 650);
    } catch (error) {
        console.log('Cannot programmatically resize window:', error);
    }
}

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

// Load language and translations
async function loadLanguageAndTranslations() {
    try {
        // CHANGED: First check localStorage for language congruency
        const savedLanguage = localStorage.getItem('wpsg_language');
        if (savedLanguage) {
            currentLanguage = savedLanguage;
        } else {
            // Get current language from backend
            currentLanguage = await eel.get_language()();
        }
        
        // Get translations for current language
        translations = await eel.get_translations(currentLanguage)();
        
        // Update UI with translations
        updateLanguageUI();
        
        console.log(`Language loaded: ${currentLanguage}`);
        return true;
        
    } catch (error) {
        console.error('Error loading language:', error);
        // Fallback to English
        currentLanguage = 'en';
        translations = {
            app_title: "WPSG Automation Tool",
            filter_committees: "Filter Committees:",
            scan_updates: "Scan Updates",
            last_run: "Last Scan:",
            loading: "Loading..."
        };
        updateLanguageUI();
        throw error;
    }
}

// Update UI with current language
function updateLanguageUI() {
    // Update page title
    document.getElementById('pageTitle').textContent = translations.app_title || "WPSG Automation Tool";
    
    // Update subtitle
    document.getElementById('subtitleText').textContent = 
        currentLanguage === 'nl' ? "Automatiseringstool" : "Automation Tool";
    
    // Update filter header
    document.getElementById('filterHeader').textContent = translations.filter_committees || "Filter Committees:";
    
    // Update scan button
    document.getElementById('scanUpdates').textContent = translations.scan_updates || "Scan Updates";
    
    // Update last run text
    document.getElementById('lastRunText').textContent = translations.last_run || "Last Scan:";
    
    // Update dataset section
    document.getElementById('viewDatasetsText').textContent = translations.view_datasets || "View Datasets:";
    document.getElementById('underDevText').textContent = translations.standards_under_development || "Standards Under Development";
    document.getElementById('recentPubText').textContent = translations.recently_published_standards || "Recently Published Standards";
    document.getElementById('isoDeletedText').textContent = translations.iso_deleted_standards || "ISO Deleted Standards";
    document.getElementById('needMoreText').textContent = translations.does_it_need_more || "Need More?";
    
    // Update footer
    document.getElementById('githubText').textContent = translations.github_repository || "Github Repository";
    document.getElementById('supportText').textContent = translations.for_support_contact || "For support, contact:";
    
    // Update loading text
    const loadingElement = document.getElementById('loadingText');
    if (loadingElement) {
        loadingElement.textContent = translations.loading || "Loading...";
    }
    
    // Update language toggle buttons - CHANGED: Default to English
    document.getElementById('nlBtn').classList.toggle('active', currentLanguage === 'nl');
    document.getElementById('enBtn').classList.toggle('active', currentLanguage === 'en');
    
    // Update tooltips and titles
    document.getElementById('addCommittee').title = translations.add_committee || "Add Committee";
}

// Switch language
async function switchLanguage(language) {
    if (isLoading || language === currentLanguage) {
        return;
    }
    
    try {
        isLoading = true;
        
        // CHANGED: Save language to localStorage for congruency
        localStorage.setItem('wpsg_language', language);
        
        // Update language in backend
        const success = await eel.set_language(language)();
        
        if (success) {
            currentLanguage = language;
            
            // Reload translations
            translations = await eel.get_translations(currentLanguage)();
            
            // Update UI
            updateLanguageUI();
            
            showMessage(
                currentLanguage === 'nl' ? 'Taal gewijzigd naar Nederlands' : 'Language changed to English', 
                'success'
            );
        } else {
            showMessage('Failed to change language', 'error');
        }
        
    } catch (error) {
        console.error('Error switching language:', error);
        showMessage('Error changing language: ' + error.message, 'error');
    } finally {
        isLoading = false;
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
        
        // CHANGED: Update language if different from saved language
        if (status.language && status.language !== currentLanguage) {
            currentLanguage = status.language;
            localStorage.setItem('wpsg_language', status.language);
            await loadLanguageAndTranslations();
        }
        
        console.log('App status loaded:', status);
        return status;
        
    } catch (error) {
        console.error('Error loading app status:', error);
        if (lastUpdatedElement) {
            lastUpdatedElement.textContent = '07 September 2025';
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
        showMessage(
            currentLanguage === 'nl' ? `Omgeschakeld naar ${filter} commissies` : `Switched to ${filter} committees`, 
            'info'
        );
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
        committeeList.innerHTML = `<div class="error" style="padding: 20px; text-align: center; color: #666;">${translations.loading || 'No committees loaded'}</div>`;
        return;
    }
    
    committeeList.innerHTML = '';
    
    currentCommittees.forEach((committee, index) => {
        const item = document.createElement('div');
        item.className = 'committee-item';
        item.innerHTML = `
            <span class="committee-name" data-index="${index}">${committee}</span>
            <div class="edit-icon" data-index="${index}" title="${translations.edit_committee || 'Edit committee'}">${editIconSvg}</div>
            <div class="delete-icon" data-index="${index}" title="${translations.remove_committee || 'Remove committee'}">${deleteIconSvg}</div>
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
                    showMessage(
                        currentLanguage === 'nl' ? 'Commissie succesvol bijgewerkt' : 'Committee updated successfully', 
                        'success'
                    );
                } else {
                    console.error('Failed to update committee in backend');
                    showMessage(
                        currentLanguage === 'nl' ? 'Bijwerken commissie mislukt' : 'Failed to update committee', 
                        'error'
                    );
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

// Delete committee
async function deleteCommittee(index) {
    if (isLoading || index < 0 || index >= currentCommittees.length) {
        return;
    }
    
    const committee = currentCommittees[index];
    const confirmMsg = currentLanguage === 'nl' ? 
        `Weet u zeker dat u "${committee}" wilt verwijderen?` : 
        `Are you sure you want to remove "${committee}"?`;
    
    if (!confirm(confirmMsg)) {
        return;
    }
    
    try {
        console.log(`Removing committee: ${committee}`);
        
        const success = await eel.remove_committee(currentFilter, committee)();
        
        if (success) {
            await loadCommittees(); // Reload to get updated list
            showMessage(
                currentLanguage === 'nl' ? 'Commissie succesvol verwijderd' : 'Committee removed successfully', 
                'success'
            );
        } else {
            showMessage(
                currentLanguage === 'nl' ? 'Verwijderen commissie mislukt' : 'Failed to remove committee', 
                'error'
            );
        }
        
    } catch (error) {
        console.error('Error removing committee:', error);
        showMessage('Error removing committee: ' + error.message, 'error');
    }
}

// Add new committee
async function addNewCommittee() {
    if (isLoading) {
        console.log('Already loading, ignoring add committee');
        return;
    }
    
    const newCommitteeName = currentLanguage === 'nl' ? 
        `Nieuwe ${currentFilter} Commissie` : 
        `New ${currentFilter} Committee`;
    
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
            
            showMessage(
                currentLanguage === 'nl' ? 'Commissie succesvol toegevoegd' : 'Committee added successfully', 
                'success'
            );
            
        } else {
            showMessage(
                currentLanguage === 'nl' ? 'Toevoegen commissie mislukt' : 'Failed to add committee', 
                'error'
            );
        }
        
    } catch (error) {
        console.error('Error adding committee:', error);
        showMessage('Error adding committee: ' + error.message, 'error');
    }
}

// AI Assessment functionality removed

// Perform scan
async function performScan() {
    if (isLoading) {
        console.log('Already loading, ignoring scan');
        return;
    }
    
    isLoading = true;
    scanButton.textContent = translations.loading || 'Scanning...';
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
        scanButton.textContent = translations.scan_updates || 'Scan Updates';
        scanButton.disabled = false;
    }
}

// Event listeners
function setupEventListeners() {
    // Language buttons
    document.getElementById('nlBtn').addEventListener('click', () => switchLanguage('nl'));
    document.getElementById('enBtn').addEventListener('click', () => switchLanguage('en'));
    
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
            } else if (target.closest('.delete-icon')) {
                const index = parseInt(target.closest('.delete-icon').dataset.index);
                deleteCommittee(index);
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
    
    // AI Assessment button
    const aiButton = document.getElementById('aiAssessment');
    if (aiButton) {
        aiButton.addEventListener('click', openAIAssessmentModal);
    }
    
    // AI Modal handlers
    document.getElementById('aiCancelBtn').addEventListener('click', () => {
        document.getElementById('aiModal').style.display = 'none';
    });
    
    document.getElementById('aiAssessBtn').addEventListener('click', performAIAssessment);
    
    // Close AI modal when clicking outside
    document.getElementById('aiModal').addEventListener('click', (e) => {
        if (e.target.id === 'aiModal') {
            document.getElementById('aiModal').style.display = 'none';
        }
    });
    
    // Dataset links
    document.querySelectorAll('.dataset-link').forEach((link, index) => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            const dataType = link.getAttribute('data-type');
            
            if (dataType && ['under_development', 'recently_published', 'iso_deleted'].includes(dataType)) {
                // CHANGED: Navigate to database viewer with language parameter for congruency
                console.log(`Navigating to database viewer with type: ${dataType}`);
                window.location.href = `database_viewer.html?type=${dataType}&lang=${currentLanguage}`;
            } else if (index === 3) {
                // "Do I need more?" - show info
                showMessage(
                    currentLanguage === 'nl' ? 
                    'Aanvullende datasets kunnen worden geconfigureerd in de instellingen.' :
                    'Additional datasets can be configured in the settings.', 
                    'info'
                );
            }
        });
    });
    
    console.log('Event listeners set up successfully');
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

// Function to resize window for different pages - Standardized to 900x590
function resizeWindowForPage(targetPage) {
    try {
        // Consistent 900x590 for both main and database views
        window.resizeTo(930, 650);
        console.log('Window resized to standard dimensions: 900x590');
    } catch (error) {
        console.log('Cannot resize window programmatically:', error);
    }
}

// MODIFICATION: Update the dataset links event listener in setupEventListeners function
// Replace the existing dataset links section with this:

// Dataset links
document.querySelectorAll('.dataset-link').forEach((link, index) => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        
        const dataType = link.getAttribute('data-type');
        
        if (dataType && ['under_development', 'recently_published', 'iso_deleted'].includes(dataType)) {
            console.log(`Navigating to database viewer with type: ${dataType}`);
            // ADDED: Resize window before navigation
            resizeWindowForPage('database');
            // Small delay to ensure resize happens
            setTimeout(() => {
                window.location.href = `database_viewer.html?type=${dataType}&lang=${currentLanguage}`;
            }, 100);
        } else if (index === 3) {
            // "Do I need more?" - show info
            showMessage(
                currentLanguage === 'nl' ? 
                'Aanvullende datasets kunnen worden geconfigureerd in de instellingen.' :
                'Additional datasets can be configured in the settings.', 
                'info'
            );
        }
    });
});

// Expose functions for debugging and external access
window.wpsgApp = {
    // Data access
    getCurrentCommittees: () => currentCommittees,
    getCurrentFilter: () => currentFilter,
    getCurrentLanguage: () => currentLanguage,
    getTranslations: () => translations,
    
    // Actions
    performScan,
    testConnection,
    loadCommittees,
    switchFilter,
    switchLanguage,
    addNewCommittee,
    deleteCommittee,
    
    // Debug functions
    debug: {
        loadAppStatus,
        isLoading: () => isLoading,
        showMessage,
        updateLanguageUI
    }
};

console.log('WPSG App JavaScript loaded - Updated multilingual version');
