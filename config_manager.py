# WPSG Configuration Manager - FIXED VERSION
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class ConfigManager:
    """Manages JSON configuration files for the WPSG automation tool"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir
        self.config_file = os.path.join(config_dir, "wpsg_config.json")
        self.standards_db_file = os.path.join(config_dir, "standards_database.json")
        
        # Ensure config directory exists
        os.makedirs(config_dir, exist_ok=True)
        
        # Initialize configuration if it doesn't exist
        self._initialize_config()
    
    def _initialize_config(self):
        """Initialize default configuration if files don't exist"""
        if not os.path.exists(self.config_file):
            self._create_default_config()
        
        if not os.path.exists(self.standards_db_file):
            self._create_default_database()
    
    def _create_default_config(self):
        """Create default configuration file"""
        default_config = {
            "committees": {
                "CEN": [
                    'CEN/CLC/JTC 3', 'CEN/CLC/JTC 10', 'CEN/TC 102', 'CEN/TC 132', 'CEN/TC 145', 
                    'CEN/TC 146', 'CEN/TC 172/WG2', 'CEN/TC 172/WG3', 'CEN/TC 172', 'CEN 175/WG 34',
                    'CEN/TC 193/WG3', 'CEN/TC 193', 'CEN/TC 194', 'CEN/TC 198', 'CEN/TC 225',
                    'CEN/TC 249/WG 11', 'CEN/TC 249/WG 24', 'CEN/TC 249/WG 9', 'CEN/TC 249',
                    'CEN/TC 261/SC 4/WG 2', 'CEN/TC 261/SC4/WG3', 'CEN/TC 261/SC4/WG6', 'CEN/TC 261/SC4/WG7',
                    'CEN/TC 261/SC4/WG8', 'CEN/TC 261/SC4', 'CEN/TC 261/SC5/WG14', 'CEN/TC 261/SC5/WG16',
                    'CEN/TC 261/SC5/WG21', 'CEN/TC 261/SC5/WG25', 'CEN/TC 261/SC5/WG26', 'CEN/TC 261/SC5/WG27',
                    'CEN/TC 261/SC5/WG34', 'CEN/TC 261/SC5', 'CEN/TC 261/WG1', 'CEN/TC 261',
                    'CEN/TC 411', 'CEN/TC 413', 'CEN/TC 459/SC9', 'CEN/TC 473', 'CEN/TC 52',
                    'CEN/WS 086', 'CEN/WS 096', 'CEN/WS COVR', 'CEN/WS CircThread'
                ],
                "ISO": [
                    'ISO TMBG', 'ISO/CASCO', 'ISO/COPOLCO', 'ISO/IEC JTC 1/SC 31', 'ISO/TC 122/SC 3',
                    'ISO/TC 122/SC 4', 'ISO/TC 122', 'ISO/TC 130', 'ISO/TC 159/SC 4', 'ISO/TC 166',
                    'ISO/TC 17/SC 9', 'ISO/TC 198', 'ISO/TC 207/SC 3', 'ISO/TC 210', 'ISO/TC 215',
                    'ISO/TC 217', 'ISO/TC 229', 'ISO/TC 287', 'ISO/TC 299', 'ISO/TC 313',
                    'ISO/TC314', 'ISO/TC 323', 'ISO/TC 34/SC 12', 'ISO/TC 34/SC 17', 'ISO/TC 42',
                    'ISO/TC 51', 'ISO TC/52', 'ISO/TC 6/SC 2', 'ISO/TC 6', 'ISO/TC 61/SC 11',
                    'ISO/TC 61/SC 14', 'ISO/TC 61/SC 9', 'ISO/TC 63', 'ISO/TC 76', 'ISO/TC 84', 'ISO/TC 87'
                ]
            },
            "settings": {
                "last_update": "23 August 2025",
                "scan_interval": 30,
                "auto_backup": True,
                "notification_email": "automate.wpsg@gmail.com",
                "debug_mode": False
            },
            "api_config": {
                "cen": {
                    "enabled": False,  # Disabled for now
                    "base_url": "https://api.cen.eu/harmonized",
                    "rate_limit": 100,
                    "timeout": 30
                },
                "iso": {
                    "enabled": False,  # Disabled for now 
                    "note": "API access will be implemented later"
                }
            }
        }
        
        self.save_config(default_config)
    
    def _create_default_database(self):
        """Create default standards database file with sample data"""
        # Sample standards data based on your Excel
        sample_standards = [
            {
                'id': 'cen_en_1034_1_2021',
                'reference': 'EN 1034-1:2021',
                'title': 'Safety of machinery - Safety requirements for the design and construction of paper making and finishing machines - Part 1: Common requirements',
                'committee': 'CEN/TC 198',
                'wi_number': 'WI=00198092',
                'status': 'published',
                'organization': 'CEN',
                'category': 'packaging_machinery',
                'relevance_score': 8.5,
                'last_updated': datetime.now().isoformat()
            },
            {
                'id': 'cen_en_18120_1',
                'reference': 'EN 18120-1',
                'title': 'Packaging - Design for recycling for plastic packaging products - Part 1: Definitions and principles for design-for-recycling of plastic packaging',
                'committee': 'CEN/TC 261',
                'wi_number': 'WI=00261514',
                'status': 'under_development',
                'organization': 'CEN',
                'category': 'packaging',
                'relevance_score': 10.0,
                'last_updated': datetime.now().isoformat()
            },
            {
                'id': 'iso_iso_25968',
                'reference': 'ISO 25968',
                'title': 'Accessible Packaging Design - Usability',
                'committee': 'ISO/TC 122',
                'wi_number': '',
                'status': 'under_development',
                'organization': 'ISO',
                'category': 'packaging',
                'relevance_score': 9.5,
                'last_updated': datetime.now().isoformat()
            },
            {
                'id': 'iso_iso_11040_8',
                'reference': 'ISO 11040-8:2016',
                'title': 'Prefilled syringes - Part 8: Requirements and test methods for finished prefilled syringes',
                'committee': 'ISO/TC 76',
                'wi_number': '',
                'status': 'published',
                'organization': 'ISO',
                'category': 'medical_packaging',
                'relevance_score': 6.5,
                'last_updated': datetime.now().isoformat()
            }
        ]
        
        default_db = {
            "metadata": {
                "last_updated": datetime.now().isoformat(),
                "source": "NVC WPSG Automation Tool",
                "version": "1.0",
                "total_records": len(sample_standards)
            },
            "cen_standards": {
                "under_development": [s for s in sample_standards if s['organization'] == 'CEN' and s['status'] == 'under_development'],
                "recently_published": [s for s in sample_standards if s['organization'] == 'CEN' and s['status'] == 'published'],
                "withdrawn_deleted": []
            },
            "iso_standards": {
                "under_development": [s for s in sample_standards if s['organization'] == 'ISO' and s['status'] == 'under_development'],
                "recently_published": [s for s in sample_standards if s['organization'] == 'ISO' and s['status'] == 'published'],
                "withdrawn_deleted": []
            }
        }
        
        self.save_database(default_db)
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading config: {e}")
            self._create_default_config()
            return self.load_config()
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration to JSON file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def load_database(self) -> Dict[str, Any]:
        """Load standards database from JSON file"""
        try:
            with open(self.standards_db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading database: {e}")
            self._create_default_database()
            return self.load_database()
    
    def save_database(self, database: Dict[str, Any]) -> bool:
        """Save standards database to JSON file"""
        try:
            # Update metadata
            database["metadata"]["last_updated"] = datetime.now().isoformat()
            
            with open(self.standards_db_file, 'w', encoding='utf-8') as f:
                json.dump(database, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving database: {e}")
            return False
    
    def get_committees(self, organization: str = None) -> List[str]:
        """Get committee list for specified organization"""
        config = self.load_config()
        if organization and organization.upper() in config["committees"]:
            return config["committees"][organization.upper()]
        return config["committees"]
    
    def update_committees(self, organization: str, committees: List[str]) -> bool:
        """Update committee list for specified organization"""
        config = self.load_config()
        if organization.upper() in config["committees"]:
            config["committees"][organization.upper()] = committees
            return self.save_config(config)
        return False
    
    def add_committee(self, organization: str, committee: str) -> bool:
        """Add a new committee to the list"""
        config = self.load_config()
        if organization.upper() in config["committees"]:
            if committee not in config["committees"][organization.upper()]:
                config["committees"][organization.upper()].append(committee)
                return self.save_config(config)
        return False
    
    def remove_committee(self, organization: str, committee: str) -> bool:
        """Remove a committee from the list"""
        config = self.load_config()
        if organization.upper() in config["committees"]:
            if committee in config["committees"][organization.upper()]:
                config["committees"][organization.upper()].remove(committee)
                return self.save_config(config)
        return False
    
    def get_standards_data(self, organization: str = None, status: str = None) -> Dict[str, Any]:
        """Get standards data filtered by organization and status"""
        database = self.load_database()
        
        if organization and status:
            org_key = f"{organization.lower()}_standards"
            if org_key in database and status in database[org_key]:
                return {
                    "metadata": database["metadata"],
                    "standards": database[org_key][status]
                }
        
        return database
    
    def get_last_update(self) -> str:
        """Get the last update timestamp"""
        config = self.load_config()
        return config["settings"]["last_update"]
    
    def update_last_scan(self) -> str:
        """Update the last scan timestamp and return new date"""
        config = self.load_config()
        new_date = datetime.now().strftime("%d %B %Y")
        config["settings"]["last_update"] = new_date
        self.save_config(config)
        return new_date

# Create and export the global instance - THIS FIXES THE IMPORT ERROR
config_manager = ConfigManager()

# Test the config manager
if __name__ == "__main__":
    print("Testing ConfigManager...")
    print(f"CEN Committees: {len(config_manager.get_committees('CEN'))}")
    print(f"ISO Committees: {len(config_manager.get_committees('ISO'))}")
    print(f"Last update: {config_manager.get_last_update()}")
    
    db = config_manager.get_standards_data()
    print(f"Total standards in database: {db['metadata']['total_records']}")
    print("ConfigManager test completed successfully!")