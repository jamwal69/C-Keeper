#!/usr/bin/env python3
"""
C-Keeper GUI Test Script
Test the graphical user interface
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main function to start the GUI"""
    try:
        print("Starting C-Keeper GUI...")
        print("Loading interface modules...")
        
        # Import and start the GUI
        from interfaces.gui import start_gui
        
        print("GUI loaded successfully!")
        print("Opening C-Keeper interface...")
        
        # Start the GUI
        return start_gui()
        
    except ImportError as e:
        print(f"Import Error: {e}")
        print("Some dependencies may be missing.")
        return 1
    except Exception as e:
        print(f"Error starting GUI: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
