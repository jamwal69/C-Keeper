#!/usr/bin/env python3
"""
Quick launcher for the Ultra-Modern C-Keeper GUI
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Launch the ultra-modern GUI directly"""
    try:
        print("🚀 Launching Ultra-Modern C-Keeper GUI...")
        print("✨ Features: Modern design, responsive layout, professional interface")
        
        from interfaces.gui_ultra_modern import UltraModernCKeeperGUI
        
        # Create and run the application
        app = UltraModernCKeeperGUI()
        app.run()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("   Make sure all dependencies are installed")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
