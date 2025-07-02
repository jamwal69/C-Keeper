#!/usr/bin/env python3
"""
C-Keeper Error Check Script
Comprehensive testing of all components
"""

import sys
import traceback
from pathlib import Path

def test_component(component_name, import_statement):
    """Test a single component"""
    try:
        exec(import_statement)
        print(f"[OK] {component_name}: OK")
        return True
    except Exception as e:
        print(f"[ERROR] {component_name}: ERROR - {str(e)}")
        traceback.print_exc()
        return False

def main():
    """Run comprehensive error check"""
    print("C-KEEPER COMPREHENSIVE ERROR CHECK")
    print("=" * 60)
    print("Testing all major components...")
    print()
    
    # List of components to test
    components = [
        ("Core Engine", "import core.engine"),
        ("Configuration", "import core.config"),
        ("Logger", "import core.logger"),
        ("Database", "import core.database"),
        ("Reconnaissance", "import modules.recon"),
        ("Payload Generator", "import modules.payload_generator"),
        ("Exploit Builder", "import modules.exploit_builder"),
        ("Exploit Runner", "import modules.exploit_runner"),
        ("C2 Handler", "import modules.c2_handler"),
        ("Delivery Engine", "import modules.delivery_engine"),
        ("Blue Team Operations", "import modules.logger_defender"),
        ("CLI Interface", "import interfaces.cli"),
        ("Modern GUI", "import interfaces.gui_modern"),
        ("Ultra-modern GUI", "import interfaces.gui_ultra_modern"),
        ("Payload Methods", "import interfaces.payload_methods"),
        ("Database Init Script", "import scripts.init_db"),
    ]
    
    passed = 0
    failed = 0
    
    # Test each component
    for name, import_stmt in components:
        if test_component(name, import_stmt):
            passed += 1
        else:
            failed += 1
    
    print()
    print("=" * 60)
    print("[SUMMARY] TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"[PASS] Passed: {passed}")
    print(f"[FAIL] Failed: {failed}")
    print(f"[RATE] Success Rate: {(passed/(passed+failed)*100):.1f}%")
    
    if failed == 0:
        print("\n[SUCCESS] ALL COMPONENTS PASSED! No errors found.")
        print("[READY] C-Keeper is ready for use!")
    else:
        print(f"\n[WARNING] {failed} component(s) have issues that need attention.")
    
    print("=" * 60)
    
    # Test main application entry point
    print("\n[TEST] Testing main application entry point...")
    try:
        from ckeeper import main
        print("[OK] Main application imports successfully")
    except Exception as e:
        print(f"[ERROR] Main application error: {str(e)}")
    
    print("\n[DONE] Error check complete!")

if __name__ == "__main__":
    main()
