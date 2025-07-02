#!/usr/bin/env python3
"""
C-Keeper - Dual-Use Cyber Kill Chain Engine
Main entry point for the application
"""

import argparse
import sys
import os
from pathlib import Path

# Add the project root to Python path
try:
    project_root = Path(__file__).parent
except NameError:
    # Handle case when __file__ is not defined (e.g., when using exec())
    project_root = Path(os.getcwd())
sys.path.insert(0, str(project_root))

from core.engine import CKeeperEngine
from core.logger import setup_logging
from core.config import Config
from interfaces.cli import CLIInterface
from interfaces.gui import start_gui

def main():
    """Main entry point for C-Keeper"""
    parser = argparse.ArgumentParser(
        description="C-Keeper - Dual-Use Cyber Kill Chain Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ckeeper.py --mode red --target 192.168.1.0/24
  python ckeeper.py --mode blue --monitor
  python ckeeper.py --gui
  python ckeeper.py --config custom_config.yaml
        """
    )
    
    # Interface options
    parser.add_argument('--gui', action='store_true', 
                       help='Start GUI interface')
    parser.add_argument('--cli', action='store_true', default=True,
                       help='Start CLI interface (default)')
    
    # Mode selection
    parser.add_argument('--mode', choices=['red', 'blue', 'dual'], 
                       default='dual', help='Operation mode')
    
    # Target specification
    parser.add_argument('--target', type=str,
                       help='Target IP/CIDR for red team operations')
    
    # Configuration
    parser.add_argument('--config', type=str, default='config/settings.yaml',
                       help='Configuration file path')
    
    # Monitoring options
    parser.add_argument('--monitor', action='store_true',
                       help='Start monitoring mode for blue team')
    
    # Logging
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       default='INFO', help='Logging level')
    parser.add_argument('--log-file', type=str,
                       help='Log file path (default: logs/ckeeper.log)')
    
    # Database options
    parser.add_argument('--init-db', action='store_true',
                       help='Initialize database and exit')
    
    args = parser.parse_args()
    
    # Setup logging
    log_file = args.log_file or 'logs/ckeeper.log'
    setup_logging(args.log_level, log_file)
    
    try:
        # Load configuration
        config = Config(args.config)
        
        # Initialize database if requested
        if args.init_db:
            from scripts.init_db import initialize_database
            initialize_database(config)
            print("Database initialized successfully!")
            return 0
        
        # Create engine instance
        engine = CKeeperEngine(config, args.mode)
        
        # Start appropriate interface
        if args.gui:
            print("Starting GUI interface...")
            return start_gui(engine)
        else:
            print(f"Starting CLI interface in {args.mode} mode...")
            cli = CLIInterface(engine)
            return cli.run(args)
            
    except KeyboardInterrupt:
        print("\nShutting down C-Keeper...")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())