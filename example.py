#!/usr/bin/env python3
"""
Example usage script for C-Keeper
Demonstrates basic functionality
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Example usage of C-Keeper"""
    print("C-Keeper Example Usage")
    print("=" * 50)
    
    try:
        # Import C-Keeper components
        from core.config import Config
        from core.engine import CKeeperEngine
        
        print("1. Loading configuration...")
        config = Config()
        
        print("2. Initializing engine in dual mode...")
        engine = CKeeperEngine(config, mode='dual')
        
        print("3. Getting session information...")
        session_info = engine.get_session_info()
        print(f"   Session ID: {session_info['session_id']}")
        print(f"   Mode: {session_info['mode']}")
        print(f"   Available modules: {', '.join(session_info['modules'])}")
        
        print("\\n4. Testing reconnaissance module...")
        recon_module = engine.get_module('recon')
        if recon_module:
            print("   ✓ Reconnaissance module loaded")
            
            # Example: scan localhost
            target = "127.0.0.1"
            print(f"   Scanning {target}...")
            
            # This would perform actual scanning
            # results = recon_module.scan_target(target)
            # print(f"   Found {len(results.get('hosts', []))} hosts")
            print("   (Skipped actual scanning for demo)")
        else:
            print("   ✗ Reconnaissance module not available")
        
        print("\\n5. Testing payload generator...")
        payload_generator = engine.get_module('payload_generator')
        if payload_generator:
            print("   ✓ Payload generator loaded")
            
            # Example: generate a simple payload
            options = {
                'lhost': '127.0.0.1',
                'lport': 4444,
                'encoder': 'base64'
            }
            
            # This would generate actual payload
            # payload = payload_generator.generate_payload('reverse_shell', 'windows', options)
            # print(f"   Generated payload: {payload['id']}")
            print("   (Skipped actual payload generation for demo)")
        else:
            print("   ✗ Payload generator not available")
        
        print("\\n6. Testing defensive monitoring...")
        logger_defender = engine.get_module('logger_defender')
        if logger_defender:
            print("   ✓ Logger/Defender module loaded")
            
            # Example: check monitoring status
            status = logger_defender.get_monitoring_status()
            print(f"   Monitoring active: {status['monitoring_active']}")
            print(f"   Detection rules: {status['detection_rules_count']}")
        else:
            print("   ✗ Logger/Defender module not available")
        
        print("\\n7. Shutting down engine...")
        engine.shutdown()
        
        print("\\n✓ Example completed successfully!")
        print("\\nTo run C-Keeper interactively:")
        print("  python ckeeper.py                    # CLI mode")
        print("  python ckeeper.py --gui              # GUI mode")
        print("  python ckeeper.py --mode red --target 192.168.1.0/24")
        print("  python ckeeper.py --mode blue --monitor")
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure to install dependencies: pip install -r requirements.txt")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
