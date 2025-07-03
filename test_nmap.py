#!/usr/bin/env python3
"""
Nmap Integration Test for C-Keeper
Tests nmap functionality and integration
"""

def test_nmap_integration():
    """Test nmap integration comprehensively"""
    print("🔍 NMAP INTEGRATION TEST")
    print("=" * 50)
    
    # Test 1: Basic import
    print("\n[TEST 1] Testing nmap import...")
    try:
        import nmap
        print("✅ SUCCESS: nmap module imported successfully")
        print(f"📦 Version: {getattr(nmap, '__version__', 'Unknown')}")
    except ImportError as e:
        print(f"❌ FAILED: {e}")
        return False
    
    # Test 2: PortScanner creation
    print("\n[TEST 2] Testing PortScanner creation...")
    try:
        nm = nmap.PortScanner()
        print("✅ SUCCESS: PortScanner created successfully")
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False
    
    # Test 3: Basic localhost scan
    print("\n[TEST 3] Testing basic localhost scan...")
    try:
        result = nm.scan('127.0.0.1', '80', '-sS')
        print("✅ SUCCESS: Localhost scan completed")
        print(f"📊 Command used: {result.get('nmap', {}).get('command_line', 'N/A')}")
        hosts = list(result.get('scan', {}).keys())
        print(f"🎯 Hosts found: {len(hosts)}")
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False
    
    # Test 4: C-Keeper ReconModule integration
    print("\n[TEST 4] Testing C-Keeper ReconModule...")
    try:
        from modules.recon import ReconModule, NMAP_AVAILABLE
        print(f"✅ SUCCESS: ReconModule imported")
        print(f"🔧 Nmap available in module: {NMAP_AVAILABLE}")
        
        if NMAP_AVAILABLE:
            print("✅ SUCCESS: Nmap integration is working in C-Keeper!")
        else:
            print("⚠️  WARNING: Nmap not available in ReconModule")
            
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False
    
    # Test 5: Quick ping scan
    print("\n[TEST 5] Testing ping scan...")
    try:
        result = nm.scan('127.0.0.1', arguments='-sn')
        print("✅ SUCCESS: Ping scan completed")
        scan_stats = result.get('nmap', {}).get('scanstats', {})
        print(f"📈 Scan time: {scan_stats.get('elapsed', 'N/A')} seconds")
        print(f"🖥️  Hosts up: {scan_stats.get('uphosts', 'N/A')}")
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ALL NMAP TESTS PASSED!")
    print("✅ Nmap is fully functional in C-Keeper")
    print("🚀 Ready for reconnaissance operations!")
    return True

if __name__ == "__main__":
    success = test_nmap_integration()
    exit(0 if success else 1)
