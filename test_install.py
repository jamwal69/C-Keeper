#!/usr/bin/env python3
"""
Test script for C-Keeper installation
Verifies that all components are working correctly
"""

import sys
import os
import importlib
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing module imports...")
    
    modules_to_test = [
        'core.config',
        'core.database', 
        'core.engine',
        'core.logger',
        'modules.recon',
        'modules.exploit_builder',
        'modules.payload_generator',
        'modules.delivery_engine',
        'modules.c2_handler',
        'modules.exploit_runner',
        'modules.logger_defender',
        'interfaces.cli',
        'interfaces.gui'
    ]
    
    failed_imports = []
    
    for module_name in modules_to_test:
        try:
            importlib.import_module(module_name)
            print(f"  ✓ {module_name}")
        except ImportError as e:
            print(f"  ✗ {module_name}: {e}")
            failed_imports.append(module_name)
    
    return failed_imports

def test_dependencies():
    """Test external dependencies"""
    print("\\nTesting external dependencies...")
    
    dependencies = [
        ('yaml', 'PyYAML'),
        ('requests', 'requests'),
        ('sqlite3', 'sqlite3 (built-in)'),
        ('tkinter', 'tkinter (built-in)'),
        ('threading', 'threading (built-in)'),
        ('socket', 'socket (built-in)')
    ]
    
    missing_deps = []
    
    for dep, package in dependencies:
        try:
            importlib.import_module(dep)
            print(f"  ✓ {dep}")
        except ImportError:
            print(f"  ✗ {dep} (install: {package})")
            missing_deps.append(package)
    
    return missing_deps

def test_file_structure():
    """Test that required files and directories exist"""
    print("\\nTesting file structure...")
    
    required_files = [
        'ckeeper.py',
        'core/config.py',
        'core/database.py',
        'core/engine.py',
        'modules/recon.py',
        'interfaces/cli.py',
        'requirements.txt',
        'config/settings.yaml'
    ]
    
    required_dirs = [
        'core',
        'modules', 
        'interfaces',
        'config',
        'data',
        'logs',
        'scripts'
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path}")
            missing_files.append(file_path)
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"  ✓ {dir_path}/")
        else:
            print(f"  ✗ {dir_path}/")
            missing_dirs.append(dir_path)
    
    return missing_files, missing_dirs

def test_configuration():
    """Test configuration loading"""
    print("\\nTesting configuration...")
    
    try:
        from core.config import Config
        config = Config('config/settings.yaml')
        print("  ✓ Configuration loaded successfully")
        print(f"  ✓ Database type: {config.database.type}")
        print(f"  ✓ Recon timeout: {config.recon.timeout}")
        return True
    except Exception as e:
        print(f"  ✗ Configuration loading failed: {e}")
        return False

def test_database():
    """Test database initialization"""
    print("\\nTesting database...")
    
    try:
        from core.config import Config
        from core.database import Database
        
        config = Config('config/settings.yaml')
        
        # Create test database in memory
        config.database.path = ':memory:'
        db = Database(config.database)
        
        print("  ✓ Database created successfully")
        print("  ✓ Tables created")
        
        # Test basic operations
        db.add_ioc('test', 'test_value', 'test description')
        iocs = db.get_iocs('test')
        if iocs:
            print("  ✓ Database operations working")
        else:
            print("  ✗ Database operations failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ✗ Database test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("C-Keeper Installation Test")
    print("=" * 50)
    
    all_passed = True
    
    # Test imports
    failed_imports = test_imports()
    if failed_imports:
        all_passed = False
        print(f"\\n⚠️  Failed imports: {len(failed_imports)}")
    
    # Test dependencies
    missing_deps = test_dependencies()
    if missing_deps:
        all_passed = False
        print(f"\\n⚠️  Missing dependencies: {', '.join(missing_deps)}")
        print("   Install with: pip install -r requirements.txt")
    
    # Test file structure
    missing_files, missing_dirs = test_file_structure()
    if missing_files or missing_dirs:
        all_passed = False
        print(f"\\n⚠️  Missing files: {len(missing_files)}, Missing directories: {len(missing_dirs)}")
    
    # Test configuration
    if not test_configuration():
        all_passed = False
    
    # Test database
    if not test_database():
        all_passed = False
    
    print("\\n" + "=" * 50)
    
    if all_passed:
        print("✅ All tests passed! C-Keeper is ready to use.")
        print("\\nTo get started:")
        print("  1. Initialize the database: python scripts/init_db.py")
        print("  2. Run CLI: python ckeeper.py")
        print("  3. Run GUI: python ckeeper.py --gui")
        print("  4. Run example: python example.py")
        return 0
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\\nCommon fixes:")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Check file permissions")
        print("  - Verify Python version (3.8+ required)")
        return 1

if __name__ == "__main__":
    sys.exit(main())
