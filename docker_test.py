#!/usr/bin/env python3
"""
Docker Test Script for C-Keeper
Tests that all core functionality works in the Docker environment
"""

import sys
import os
import subprocess
import importlib
from pathlib import Path

def test_python_environment():
    """Test Python version and basic imports"""
    print(f"🐍 Python version: {sys.version}")
    
    # Test core Python modules
    core_modules = ['tkinter', 'sqlite3', 'json', 'threading', 'socket']
    for module in core_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            return False
    return True

def test_external_dependencies():
    """Test external Python packages"""
    external_packages = [
        'yaml', 'matplotlib', 'seaborn', 'plotly', 
        'dash', 'PIL', 'nmap', 'requests'
    ]
    
    failed = []
    for package in external_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed.append(package)
    
    return len(failed) == 0

def test_ckeeper_modules():
    """Test C-Keeper specific modules"""
    sys.path.insert(0, '/app')
    
    ckeeper_modules = [
        'core.config', 'core.database', 'core.engine', 'core.logger',
        'modules.payload_generator', 'modules.c2_handler', 'modules.recon',
        'interfaces.cli', 'interfaces.gui_modern'
    ]
    
    failed = []
    for module in ckeeper_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed.append(module)
    
    return len(failed) == 0

def test_system_commands():
    """Test system commands availability"""
    commands = ['nmap', 'netcat', 'curl', 'wget']
    
    failed = []
    for cmd in commands:
        try:
            result = subprocess.run(['which', cmd], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {cmd}: {result.stdout.strip()}")
            else:
                print(f"❌ {cmd}: not found")
                failed.append(cmd)
        except Exception as e:
            print(f"❌ {cmd}: {e}")
            failed.append(cmd)
    
    return len(failed) == 0

def test_file_structure():
    """Test that required files and directories exist"""
    required_paths = [
        '/app/ckeeper.py',
        '/app/core',
        '/app/modules',
        '/app/interfaces',
        '/app/data',
        '/app/logs',
        '/app/config'
    ]
    
    failed = []
    for path in required_paths:
        if os.path.exists(path):
            print(f"✅ {path}")
        else:
            print(f"❌ {path}: missing")
            failed.append(path)
    
    return len(failed) == 0

def test_database():
    """Test database connectivity"""
    try:
        sys.path.insert(0, '/app')
        from core.database import DatabaseManager
        
        db = DatabaseManager()
        db.create_tables()
        print("✅ Database: connection and tables OK")
        return True
    except Exception as e:
        print(f"❌ Database: {e}")
        return False

def test_gui_availability():
    """Test GUI environment"""
    try:
        import tkinter as tk
        # Try to create a root window
        root = tk.Tk()
        root.withdraw()  # Hide the window
        root.destroy()
        print("✅ GUI: Tkinter available")
        return True
    except Exception as e:
        print(f"❌ GUI: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 C-Keeper Docker Environment Test")
    print("=" * 50)
    
    tests = [
        ("Python Environment", test_python_environment),
        ("External Dependencies", test_external_dependencies),
        ("C-Keeper Modules", test_ckeeper_modules),
        ("System Commands", test_system_commands),
        ("File Structure", test_file_structure),
        ("Database", test_database),
        ("GUI Availability", test_gui_availability)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Testing {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}: EXCEPTION - {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! C-Keeper is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
