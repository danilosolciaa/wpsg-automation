# WPSG Configuration Manager - UPDATED VERSION WITH TRANSLATIONS AND NORMALIZATION FIX
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional


class ConfigManager:
    """Manages JSON configuration files for the WPSG automation tool"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir
        self.config_file = os.path.join(config_dir, "wpsg_config.json")
        # Database file names
        self.standards_db_file = os.path.join(config_dir, "under_development_database.json")
        self.recently_published_db_file = os.path.join(config_dir, "recently_published_database.json")
        self.iso_deleted_db_file = os.path.join(config_dir, "iso_deleted_database.json")
        
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
            
        if not os.path.exists(self.recently_published_db_file):
            self._create_recently_published_database()
            
        if not os.path.exists(self.iso_deleted_db_file):
            self._create_iso_deleted_database()
    
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
                "last_update": "07 September 2025",
                "scan_interval": 30,
                "auto_backup": True,
                "notification_email": "automate.wpsg@gmail.com",
                "debug_mode": False,
                "language": "en"  # CHANGED: English as default
            },
            "api_config": {
                "cen": {
                    "enabled": False,
                    "base_url": "https://api.cen.eu/harmonized",
                    "rate_limit": 100,
                    "timeout": 30
                },
                "iso": {
                    "enabled": False,
                    "note": "API access will be implemented later"
                }
            }
        }
        
        self.save_config(default_config)
    
    def _create_default_database(self):
        """Create default under development standards database with proper JSON structure"""
        # Using the provided JSON structure from paste-8.txt
        default_db = {
            "metadata": {
                "last_updated": "2025-09-07T14:27:03.273105",
                "source": "NVC WPSG Automation Tool",
                "version": "1.0",
                "total_records": 3
            },
            "cen_standards": [
                {
                    "id": "cen_en_1034_1_2021",
                    "reference": "EN 1034-1:2021",
                    "title": "Safety of machinery - Safety requirements for the design and construction of paper making and finishing machines - Part 1: Common requirements",
                    "committee": "CEN/TC 198",
                    "wi_number": "WI=00198092",
                    "organization": "CEN",
                    "category": "paper_machinery",
                    "last_updated": "2025-09-07T14:27:03.273054"
                },
                {
                    "id": "cen_en_18120_1",
                    "reference": "EN 18120-1",
                    "title": "Packaging - Design for recycling for plastic packaging products - Part 1: Definitions and principles for design-for-recycling of plastic packaging",
                    "committee": "CEN/TC 261",
                    "wi_number": "WI=00261514",
                    "organization": "CEN",
                    "category": "packaging",
                    "last_updated": "2025-09-07T14:27:03.273092"
                }
            ],
            "iso_standards": [
                {
                    "id": "iso_iso_25968",
                    "reference": "ISO 25968",
                    "title": "Accessible Packaging Design - Usability",
                    "committee": "ISO/TC 122",
                    "wi_number": "",
                    "organization": "ISO",
                    "category": "packaging",
                    "last_updated": "2025-09-07T14:27:03.273094"
                }
            ]
        }
        
        self.save_database(default_db)
    
    def _create_recently_published_database(self):
        """Create recently published standards database"""
        sample_standards = [
            {
                'id': 'cen_en_15344_2025',
                'reference': 'EN 15344:2025',
                'title': 'Plastics - Recycled plastics - Characterization of Polyethylene (PE) recyclates',
                'committee': 'CEN/TC 249/WG 11',
                'wi_number': 'WI=00249A3C',
                'organization': 'CEN',
                'category': 'plastics',
                'publication_date': '2025-07-15',
                'last_updated': datetime.now().isoformat()
            },
            {
                'id': 'iso_iso_24112',
                'reference': 'ISO 24112',
                'title': 'Robotics — Electrical interfaces — Connectivity and interoperability for end-effectors',
                'committee': 'ISO/TC 299',
                'wi_number': '',
                'organization': 'ISO',
                'category': 'robotics',
                'publication_date': '2025-06-20',
                'last_updated': datetime.now().isoformat()
            }
        ]
        
        database = {
            "metadata": {
                "last_updated": datetime.now().isoformat(),
                "source": "NVC WPSG Automation Tool - Recently Published",
                "version": "1.0",
                "total_records": len(sample_standards)
            },
            "cen_standards": [s for s in sample_standards if s['organization'] == 'CEN'],
            "iso_standards": [s for s in sample_standards if s['organization'] == 'ISO']
        }
        
        with open(self.recently_published_db_file, 'w', encoding='utf-8') as f:
            json.dump(database, f, indent=2, ensure_ascii=False)
    
    def _create_iso_deleted_database(self):
        """Create ISO deleted standards database"""
        sample_standards = [
            {
                'id': 'iso_iso_old_standard',
                'reference': 'ISO 12345:2010',
                'title': 'Withdrawn standard for demonstration purposes',
                'committee': 'ISO/TC 122',
                'wi_number': '',
                'organization': 'ISO',
                'category': 'withdrawn',
                'deletion_date': '2025-01-15',
                'reason': 'Superseded by newer standard',
                'last_updated': datetime.now().isoformat()
            }
        ]
        
        database = {
            "metadata": {
                "last_updated": datetime.now().isoformat(),
                "source": "NVC WPSG Automation Tool - ISO Deleted",
                "version": "1.0",
                "total_records": len(sample_standards)
            },
            "iso_standards": sample_standards
        }
        
        with open(self.iso_deleted_db_file, 'w', encoding='utf-8') as f:
            json.dump(database, f, indent=2, ensure_ascii=False)
    
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
    
    def load_database(self, db_type: str = "under_development") -> Dict[str, Any]:
        """Load database from JSON file based on type"""
        db_files = {
            "under_development": self.standards_db_file,
            "recently_published": self.recently_published_db_file,
            "iso_deleted": self.iso_deleted_db_file
        }
        
        db_file = db_files.get(db_type, self.standards_db_file)
        
        try:
            with open(db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading database {db_type}: {e}")
            if db_type == "under_development":
                self._create_default_database()
            elif db_type == "recently_published":
                self._create_recently_published_database()
            elif db_type == "iso_deleted":
                self._create_iso_deleted_database()
            return self.load_database(db_type)
    
    def save_database(self, database: Dict[str, Any], db_type: str = "under_development") -> bool:
        """Save database to JSON file"""
        db_files = {
            "under_development": self.standards_db_file,
            "recently_published": self.recently_published_db_file,
            "iso_deleted": self.iso_deleted_db_file
        }
        
        db_file = db_files.get(db_type, self.standards_db_file)
        
        try:
            database["metadata"]["last_updated"] = datetime.now().isoformat()
            with open(db_file, 'w', encoding='utf-8') as f:
                json.dump(database, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving database {db_type}: {e}")
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
    
    def get_standards_data(self, organization: str = None, db_type: str = "under_development") -> Dict[str, Any]:
        """Get standards data filtered by organization and database type"""
        database = self.load_database(db_type)
        # Normalize structures coming from legacy/alternate JSON exports
        database = self._normalize_db_structure(database, db_type)
        return database

    # NEW: Keep minimal and self-contained – flattens and harmonizes keys
    def _normalize_db_structure(self, database: Dict[str, Any], db_type: str) -> Dict[str, Any]:
        def flatten_section(section):
            # Expect a list; if dict with 'under_development' or other list-bearing keys, flatten to a single list
            if isinstance(section, list):
                return section
            if isinstance(section, dict):
                # Preferred key
                for key in ("under_development", "records", "items", "data"):
                    if key in section and isinstance(section[key], list):
                        return section[key]
                # Fallback: merge all list values
                merged = []
                for v in section.values():
                    if isinstance(v, list):
                        merged.extend(v)
                return merged
            return []

        # Ensure keys exist
        cen = database.get("cen_standards", [])
        iso = database.get("iso_standards", [])

        cen_list = flatten_section(cen)
        iso_list = flatten_section(iso)

        # Harmonize field names (winumber -> wi_number)
        def fix_record(rec: Dict[str, Any]) -> Dict[str, Any]:
            if isinstance(rec, dict):
                if "winumber" in rec and "wi_number" not in rec:
                    rec["wi_number"] = rec.pop("winumber")
            return rec

        cen_list = [fix_record(r) for r in cen_list]
        iso_list = [fix_record(r) for r in iso_list]

        database["cen_standards"] = cen_list
        database["iso_standards"] = iso_list

        # Recalculate metadata counts and ensure numeric type
        meta = database.setdefault("metadata", {})
        meta["total_records"] = len(cen_list) + len(iso_list)
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
    
    def get_language(self) -> str:
        """Get current language setting"""
        config = self.load_config()
        return config["settings"].get("language", "en")  # CHANGED: Default to English
    
    def set_language(self, language: str) -> bool:
        """Set language preference"""
        config = self.load_config()
        config["settings"]["language"] = language
        return self.save_config(config)
    
    def get_translations(self, language: str = "en") -> Dict[str, str]:
        """Get translations for specified language"""
        translations = {
            'en': {
                "app_title": "WPSG Automation Tool",
                "filter_committees": "Filter Committees:",
                "scan_updates": "Scan Updates",
                "last_run": "Last Scan:",
                "loading": "Loading...",
                "view_datasets": "View Datasets:",
                "standards_under_development": "Standards Under Development",
                "recently_published_standards": "Recently Published Standards",
                "iso_deleted_standards": "ISO Deleted Standards",
                "does_it_need_more": "Need More?",
                "github_repository": "Github Repository",
                "for_support_contact": "For support, contact:",
                "add_committee": "Add Committee",
                "edit_committee": "Edit Committee",
                "remove_committee": "Remove Committee",
                "ai_assessment": "AI Assessment",
                "committee_name": "Committee Name:",
                "committee_url": "Committee URL (optional):",
                "cancel": "Cancel",
                "assess": "Assess",
                "relevance_score": "Relevance Score",
                "assessment": "Assessment",
                "recommendation": "Recommendation",
                "found_keywords": "Found Keywords",
                "confidence": "Confidence",
                "none": "None"
            },
            'nl': {
                "app_title": "WPSG Automatiseringstool",
                "filter_committees": "Filter Commissies:",
                "scan_updates": "Updates Scannen",
                "last_run": "Laatste Scan:",
                "loading": "Laden...",
                "view_datasets": "Bekijk Datasets:",
                "standards_under_development": "Normen in Ontwikkeling",
                "recently_published_standards": "Recent Gepubliceerde Normen",
                "iso_deleted_standards": "ISO Verwijderde Normen",
                "does_it_need_more": "Meer Nodig?",
                "github_repository": "Github Repository",
                "for_support_contact": "Voor ondersteuning, neem contact op:",
                "add_committee": "Commissie Toevoegen",
                "edit_committee": "Bewerk Commissie",
                "remove_committee": "Verwijder Commissie",
                "ai_assessment": "AI Beoordeling",
                "committee_name": "Commissie Naam:",
                "committee_url": "Commissie URL (optioneel):",
                "cancel": "Annuleren",
                "assess": "Beoordelen",
                "relevance_score": "Relevantie Score",
                "assessment": "Beoordeling",
                "recommendation": "Aanbeveling",
                "found_keywords": "Gevonden Sleutelwoorden",
                "confidence": "Vertrouwen",
                "none": "Geen"
            }
        }
        
        return translations.get(language, translations['en'])


# Create and export the global instance
config_manager = ConfigManager()


# Test the config manager
if __name__ == "__main__":
    print("Testing ConfigManager...")
    print(f"CEN Committees: {len(config_manager.get_committees('CEN'))}")
    print(f"ISO Committees: {len(config_manager.get_committees('ISO'))}")
    print(f"Last update: {config_manager.get_last_update()}")
    print(f"Current language: {config_manager.get_language()}")
    
    db = config_manager.get_standards_data()
    print(f"Total standards in database: {db['metadata']['total_records']}")
    
    # Test translations
    en_translations = config_manager.get_translations('en')
    nl_translations = config_manager.get_translations('nl')
    print(f"English translations: {len(en_translations)} keys")
    print(f"Dutch translations: {len(nl_translations)} keys")
    
    print("ConfigManager test completed successfully!")