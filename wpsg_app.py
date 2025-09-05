import eel
import json
import os
from datetime import datetime
from config_manager import config_manager

# Initialize EEL with correct web folder path
eel.init('web')

# EEL exposed functions for frontend interaction
@eel.expose
def get_committees(organization=None):
    """Get committee list for specified organization"""
    try:
        committees = config_manager.get_committees(organization)
        print(f"Retrieved {len(committees)} committees for {organization}")
        return committees
    except Exception as e:
        print(f"Error getting committees: {e}")
        return []

@eel.expose
def update_committees(organization, committees):
    """Update committee list for specified organization"""
    try:
        result = config_manager.update_committees(organization, committees)
        print(f"Updated committees for {organization}: {result}")
        return result
    except Exception as e:
        print(f"Error updating committees: {e}")
        return False

@eel.expose
def add_committee(organization, committee):
    """Add a new committee to the list"""
    try:
        result = config_manager.add_committee(organization, committee)
        print(f"Added committee {committee} to {organization}: {result}")
        return result
    except Exception as e:
        print(f"Error adding committee: {e}")
        return False

@eel.expose
def remove_committee(organization, committee):
    """Remove a committee from the list"""
    try:
        result = config_manager.remove_committee(organization, committee)
        print(f"Removed committee {committee} from {organization}: {result}")
        return result
    except Exception as e:
        print(f"Error removing committee: {e}")
        return False
@eel.expose
def get_standards_data(organization=None, status=None):
    """Get standards data filtered by organization and status"""
    try:
        data = config_manager.get_standards_data(organization, status)
        print(f"Retrieved standards data: {data['metadata']['total_records']} total records")
        return data
    except Exception as e:
        print(f"Error getting standards data: {e}")
        return {
            "metadata": {"total_records": 0, "last_updated": datetime.now().isoformat()},
            "cen_standards": {"under_development": [], "recently_published": [], "withdrawn_deleted": []},
            "iso_standards": {"under_development": [], "recently_published": [], "withdrawn_deleted": []}
        }


@eel.expose
def get_app_status():
    """Get current application status"""
    try:
        config = config_manager.load_config()
        database = config_manager.load_database()
        
        status = {
            'version': '1.0.0',
            'last_update': config['settings']['last_update'],
            'total_committees': len(config['committees']['CEN']) + len(config['committees']['ISO']),
            'total_standards': database['metadata']['total_records'],
            'database_last_updated': database['metadata']['last_updated']
        }
        print(f"App status: {status}")
        return status
    except Exception as e:
        print(f"Error getting app status: {e}")
        return {
            'version': '1.0.0',
            'last_update': '23 August 2025',
            'total_committees': 0,
            'total_standards': 0,
            'database_last_updated': datetime.now().isoformat()
        }

@eel.expose
def get_last_update():
    """Get the last update timestamp"""
    try:
        return config_manager.get_last_update()
    except Exception as e:
        print(f"Error getting last update: {e}")
        return "23 August 2025"

@eel.expose
def update_last_scan():
    """Update the last scan timestamp and return new date"""
    try:
        new_date = config_manager.update_last_scan()
        print(f"Updated last scan date: {new_date}")
        return new_date
    except Exception as e:
        print(f"Error updating last scan: {e}")
        return datetime.now().strftime("%d %B %Y")

@eel.expose
def perform_scan():
    """Perform a mock scan (no API calls for now)"""
    try:
        print("Performing mock scan...")
        
        # Simulate scan process
        import time
        time.sleep(1)  # Simulate processing time
        
        # Update last scan time
        new_date = config_manager.update_last_scan()
        
        result = {
            'success': True,
            'message': f'Mock scan completed successfully. Found 4 sample standards.',
            'results': {
                'total_checked': 80,  # Total committees checked
                'new_items': 2,      # New items found
                'updated_items': 1,   # Updated items
                'timestamp': datetime.now().isoformat()
            }
        }
        
        print(f"Scan result: {result}")
        return result
        
    except Exception as e:
        print(f"Error during scan: {e}")
        return {
            'success': False,
            'message': f'Scan failed: {str(e)}',
            'results': None
        }

@eel.expose
def test_connection():
    """Test basic connectivity and configuration"""
    try:
        config = config_manager.load_config()
        database = config_manager.load_database()
        
        return {
            'success': True,
            'message': 'Configuration loaded successfully',
            'config_loaded': True,
            'database_loaded': True,
            'committees_loaded': len(config['committees']['CEN']) + len(config['committees']['ISO']),
            'standards_loaded': database['metadata']['total_records']
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Connection test failed: {str(e)}'
        }

def main():
    """Main application entry point"""
    try:
        print("=" * 50)
        print("WPSG Automation Tool Starting...")
        print("=" * 50)
        
        # Test configuration loading
        print("Testing configuration...")
        test_result = test_connection()
        if test_result['success']:
            print("✓ Configuration loaded successfully")
            print(f"✓ {test_result['committees_loaded']} committees loaded")
            print(f"✓ {test_result['standards_loaded']} standards loaded")
        else:
            print(f"⚠ Configuration test failed: {test_result['message']}")
        
        # Check if web folder exists
        web_path = os.path.join(os.getcwd(), 'web')
        if not os.path.exists(web_path):
            print(f"⚠ Web folder not found at {web_path}")
            print("Please ensure you have a 'web' folder with your HTML files")
        else:
            print(f"✓ Web folder found at {web_path}")
            
            # Check for required files
            required_files = ['index.html']
            for file in required_files:
                file_path = os.path.join(web_path, file)
                if os.path.exists(file_path):
                    print(f"✓ Found {file}")
                else:
                    print(f"⚠ Missing {file}")
        
        print("=" * 50)
        print("Starting web interface...")
        print("If the app doesn't open automatically, go to: http://localhost:8000")
        print("=" * 50)
        
        # Start the EEL application
        eel.start('index.html', size=(850, 520), position=(100, 100), port=8000)
        
    except Exception as e:
        print(f"Error starting application: {e}")
        print("Press Enter to exit...")
        input()


    

if __name__ == '__main__':
    main()