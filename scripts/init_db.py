#!/usr/bin/env python3
"""
Database Initialization Script for C-Keeper
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.config import Config
from core.database import Database

def initialize_database(config=None):
    """Initialize the C-Keeper database"""
    if config is None:
        config = Config()
    
    print("Initializing C-Keeper database...")
    
    try:
        # Create database instance (this will create tables)
        db = Database(config.database)
        
        print(f"✓ Database created at: {config.database.path}")
        print("✓ Tables created successfully")
        
        # Add some initial data
        _add_initial_data(db)
        
        print("✓ Initial data added")
        print("Database initialization completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        return False

def _add_initial_data(db):
    """Add initial data to database"""
    try:
        # Add some common IOCs
        common_iocs = [
            {
                'type': 'ip',
                'value': '192.168.1.1',
                'description': 'Common private IP range',
                'confidence': 0.3
            },
            {
                'type': 'domain',
                'value': 'malware.example.com',
                'description': 'Example malware domain',
                'confidence': 0.9
            },
            {
                'type': 'hash',
                'value': 'd41d8cd98f00b204e9800998ecf8427e',
                'description': 'Empty file MD5 hash',
                'confidence': 0.1
            }
        ]
        
        for ioc in common_iocs:
            db.add_ioc(
                ioc['type'],
                ioc['value'],
                ioc['description'],
                ioc['confidence']
            )
        
        print(f"  Added {len(common_iocs)} IOCs")
        
    except Exception as e:
        print(f"Warning: Could not add initial data: {e}")

if __name__ == "__main__":
    initialize_database()
