import eel
import json
import os
from datetime import datetime
from config_manager import config_manager


# Initialize EEL with correct web folder path
eel.init('web')


# Global state tracking
app_state = {
    'last_scan': None,
    'is_scanning': False,
    'language': 'en'  # CHANGED: Default to English
}


@eel.expose
def get_app_status():
    """Get current application status"""
    try:
        config = config_manager.load_config()
        status = {
            'success': True,
            'last_update': config['settings'].get('last_update', '07 September 2025'),
            'language': config['settings'].get('language', 'en'),  # CHANGED: Default to English
            'scan_interval': config['settings'].get('scan_interval', 30),
            'version': '1.0.0',
            'total_committees': len(config['committees']['CEN']) + len(config['committees']['ISO'])
        }
        print(f"App status: {status}")
        return status
    except Exception as e:
        print(f"Error getting app status: {e}")
        return {
            'success': False,
            'error': str(e),
            'last_update': '07 September 2025',
            'language': 'en'
        }


@eel.expose 
def get_committees(organization):
    """Get committees for specified organization (CEN or ISO)"""
    try:
        committees = config_manager.get_committees(organization)
        print(f"Loaded {len(committees)} {organization} committees")
        return committees
    except Exception as e:
        print(f"Error loading {organization} committees: {e}")
        return []


@eel.expose
def update_committees(organization, committees):
    """Update committees list for organization"""
    try:
        success = config_manager.update_committees(organization, committees)
        print(f"Updated {organization} committees: {success}")
        return success
    except Exception as e:
        print(f"Error updating {organization} committees: {e}")
        return False


@eel.expose
def add_committee(organization, committee):
    """Add new committee"""
    try:
        success = config_manager.add_committee(organization, committee)
        print(f"Added committee '{committee}' to {organization}: {success}")
        return success
    except Exception as e:
        print(f"Error adding committee: {e}")
        return False


@eel.expose
def remove_committee(organization, committee):
    """Remove committee"""
    try:
        success = config_manager.remove_committee(organization, committee)
        print(f"Removed committee '{committee}' from {organization}: {success}")
        return success
    except Exception as e:
        print(f"Error removing committee: {e}")
        return False


@eel.expose
def get_language():
    """Get current language setting"""
    try:
        language = config_manager.get_language()
        print(f"Current language: {language}")
        return language
    except Exception as e:
        print(f"Error getting language: {e}")
        return 'en'  # CHANGED: Default to English


@eel.expose
def set_language(language):
    """Set language preference"""
    try:
        success = config_manager.set_language(language)
        app_state['language'] = language
        print(f"Set language to {language}: {success}")
        return success
    except Exception as e:
        print(f"Error setting language: {e}")
        return False


@eel.expose
def get_translations(language='en'):
    """Get translations for specified language"""
    try:
        translations = config_manager.get_translations(language)
        print(f"Loaded translations for {language}")
        return translations
    except Exception as e:
        print(f"Error getting translations for {language}: {e}")
        # Fallback translations
        fallback = {
            'en': {
                "app_title": "WPSG Automation Tool",
                "filter_committees": "Filter Committees:",
                "scan_updates": "Scan Updates",
                "last_run": "Last Scan:",
                "loading": "Loading...",
            },
            'nl': {
                "app_title": "WPSG Automatiseringstool",
                "filter_committees": "Filter Commissies:",
                "scan_updates": "Updates Scannen",
                "last_run": "Laatste Scan:",
                "loading": "Laden...",
            }
        }
        return fallback.get(language, fallback['en'])


@eel.expose
def get_standards_data(organization=None, db_type='under_development'):
    """Get standards data from database"""
    try:
        data = config_manager.get_standards_data(organization, db_type)
        print(f"Loaded {db_type} data - Total: {data['metadata']['total_records']} records")
        return data
    except Exception as e:
        print(f"Error getting standards data: {e}")
        # Return minimal structure to prevent frontend errors
        return {
            'metadata': {
                'last_updated': datetime.now().isoformat(),
                'version': '1.0',
                'total_records': 0
            },
            'cen_standards': [],
            'iso_standards': []
        }


@eel.expose
def perform_scan():
    """Perform standards scanning operation"""
    if app_state['is_scanning']:
        return {'success': False, 'message': 'Scan already in progress'}

    try:
        app_state['is_scanning'] = True
        print("Starting standards scan...")

        # Simulate scanning process
        import time
        time.sleep(2)  # Simulate work

        # Update last scan time
        new_date = config_manager.update_last_scan()
        app_state['last_scan'] = new_date

        print("Mock scan completed successfully")
        return {
            'success': True,
            'message': 'Standards scan completed successfully',
            'last_update': new_date,
            'changes_found': 0,  # In real implementation, this would be actual changes
            'duration': '2 seconds'
        }

    except Exception as e:
        print(f"Error during scan: {e}")
        return {
            'success': False,
            'message': f'Scan failed: {str(e)}'
        }
    finally:
        app_state['is_scanning'] = False


@eel.expose
def update_last_scan():
    """Update last scan timestamp"""
    try:
        new_date = config_manager.update_last_scan()
        app_state['last_scan'] = new_date
        print(f"Updated last scan date to: {new_date}")
        return new_date
    except Exception as e:
        print(f"Error updating last scan date: {e}")
        return datetime.now().strftime("%d %B %Y")


@eel.expose
def assess_committee_ai(committee_name, committee_url=''):
    """AI-powered committee assessment"""
    try:
        print(f"Assessing committee: {committee_name}")

        # Simple keyword-based assessment for demo
        packaging_keywords = [
            'packaging', 'pack', 'container', 'bottle', 'box', 'bag', 'wrap', 
            'label', 'recyclable', 'biodegradable', 'plastic', 'paper', 'board',
            'food contact', 'barrier', 'sterilization', 'medical device'
        ]

        found_keywords = []
        text_to_check = (committee_name + ' ' + committee_url).lower()

        for keyword in packaging_keywords:
            if keyword in text_to_check:
                found_keywords.append(keyword)

        # Calculate relevance score
        base_score = min(len(found_keywords) * 15, 80)

        # Boost score for specific committees
        if 'tc 261' in text_to_check or 'tc 122' in text_to_check:
            base_score += 20
        if 'packaging' in text_to_check:
            base_score += 15

        relevance_score = min(base_score, 100)

        # Generate assessment text
        if relevance_score > 70:
            assessment = "Highly relevant to packaging standards"
            recommendation = "Strongly recommend including in monitoring"
            confidence = "High"
        elif relevance_score > 30:
            assessment = "Moderately relevant to packaging"
            recommendation = "Consider including with regular review"
            confidence = "Medium"
        else:
            assessment = "Limited relevance to packaging standards"
            recommendation = "Low priority for packaging focus"
            confidence = "Medium"

        result = {
            'success': True,
            'relevance_score': relevance_score,
            'assessment': assessment,
            'recommendation': recommendation,
            'keywords_found': found_keywords,
            'confidence': confidence,
            'committee_name': committee_name
        }

        print(f"AI Assessment result: {relevance_score}% relevance")
        return result

    except Exception as e:
        print(f"Error in AI assessment: {e}")
        return {
            'success': False,
            'message': str(e),
            'relevance_score': 0,
            'assessment': 'Assessment failed',
            'recommendation': 'Manual review required',
            'keywords_found': [],
            'confidence': 'None'
        }


@eel.expose
def test_connection():
    """Test the EEL connection"""
    try:
        print("Connection test successful")
        return {
            'success': True,
            'message': 'EEL connection working properly',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        }
    except Exception as e:
        print(f"Connection test failed: {e}")
        return {
            'success': False,
            'message': str(e)
        }


def main():
    try:
        print("Starting WPSG Automation Tool...")
        config = config_manager.load_config()
        app_state['language'] = config['settings'].get('language', 'en')
        
        # Allow for resizable window
        eel.start('index.html', 
                 size=(930, 650),           # Initial size
                 position=(100, 100),
                 disable_cache=True,
                 port=8080,
                 mode='chrome',             # Better for resizing
                 cmdline_args=['--disable-web-security'])  # If needed
        
    except Exception as e:
        print(f"Error starting application: {e}")


if __name__ == '__main__':
    main()
