#!/usr/bin/env python3
"""
C-Keeper CLI Demo Script
This script demonstrates the enhanced CLI capabilities of C-Keeper
"""

import subprocess
import time
import sys
import os

def run_cli_command(command):
    """Run a single CLI command and capture output"""
    try:
        # Use echo to pipe command to CLI
        cmd = f'echo "{command}" | python ckeeper.py --cli'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=r"c:\Faizan Sir\Cyberkillchain\C-Keeper")
        return result.stdout
    except Exception as e:
        return f"Error running command: {e}"

def print_section(title):
    """Print a section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def demo_cli():
    """Run a comprehensive CLI demonstration"""
    
    print("""
 ██████╗      ██╗  ██╗███████╗███████╗██████╗ ███████╗██████╗ 
██╔════╝      ██║ ██╔╝██╔════╝██╔════╝██╔══██╗██╔════╝██╔══██╗
██║     █████╗█████╔╝ █████╗  █████╗  ██████╔╝█████╗  ██████╔╝
██║     ╚════╝██╔═██╗ ██╔══╝  ██╔══╝  ██╔═══╝ ██╔══╝  ██╔══██╗
╚██████╗      ██║  ██╗███████╗███████╗██║     ███████╗██║  ██║
 ╚═════╝      ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝

              C-KEEPER CLI DEMONSTRATION
          Enhanced Command Line Interface Demo
    """)
    
    print_section("🎯 C-KEEPER CLI DEMONSTRATION")
    print("This demo showcases the enhanced CLI interface with:")
    print("• Colorized output and improved visual design")
    print("• Organized command categories") 
    print("• Enhanced help system")
    print("• Better error handling and feedback")
    print("• Professional reconnaissance workflow")
    
    input("\nPress Enter to start the demo...")
    
    # Demo commands with explanations
    demo_commands = [
        ("help", "📋 Show the enhanced categorized help system"),
        ("banner", "🎨 Display the ASCII banner"), 
        ("status", "📊 Check system status and module information"),
        ("set_target demo.testfire.net", "🎯 Set a demo target for testing"),
        ("show_target", "👁️  Verify the current target"),
        ("recon", "🔍 Run comprehensive reconnaissance scan"),
        ("monitor start", "🔍 Start the monitoring system"),
        ("monitor status", "📈 Check monitoring system status"),
        ("scan_ports", "🔓 Quick port scan demonstration"),
        ("exit", "👋 Exit the CLI gracefully")
    ]
    
    for i, (command, description) in enumerate(demo_commands, 1):
        print_section(f"Step {i}: {description}")
        print(f"Command: {command}")
        print("\nOutput:")
        print("-" * 40)
        
        # Run the command (simplified for demo)
        if command == "help":
            print("🆘 C-KEEPER COMMAND REFERENCE")
            print("═" * 60)
            print("\n🎯 Target Management")
            print("─" * 20)
            print("  set_target       Set target for operations")
            print("  show_target      Display current target")
            print("  clear_target     Clear current target")
            print("\n🔍 Reconnaissance")
            print("─" * 15)
            print("  recon            Run comprehensive reconnaissance")
            print("  scan_ports       Quick port scan")
            print("\n... and many more categorized commands!")
            
        elif command == "status":
            print("📊 C-KEEPER SYSTEM STATUS")
            print("═" * 50)
            print("🔧 Mode: DUAL")
            print("🆔 Session ID: demo-session-12345")
            print("🎯 Current Target: demo.testfire.net")
            print("⏰ Start Time: 2025-01-03 02:15:00")
            print("\n📦 MODULE STATUS")
            print("─" * 30)
            print("  ✅ recon                  Active")
            print("  ✅ exploit_builder        Active")
            print("  ✅ payload_generator      Active")
            print("  ✅ c2_handler             Active")
            
        elif command == "set_target demo.testfire.net":
            print("✅ Target set to: demo.testfire.net")
            print("   You can now run: recon to scan this target")
            
        elif command == "show_target":
            print("🎯 Current target: demo.testfire.net")
            
        elif command == "recon":
            print("🔍 RECONNAISSANCE SCAN")
            print("═" * 50)
            print("🎯 Target: demo.testfire.net")
            print("⏰ Started: 02:16:15")
            print("\n🚀 Initiating scan...")
            print("📋 RECONNAISSANCE RESULTS")
            print("═" * 50)
            print("🎯 Target: demo.testfire.net")
            print("⏰ Scan Time: 2025-01-03 02:16:45")
            print("🖥️  Hosts Found: 1")
            print("\n🖥️  DISCOVERED HOSTS")
            print("─" * 40)
            print("  1. 72.52.4.119 (demo.testfire.net)")
            print("     🔓 Open Ports:")
            print("       • 80/tcp - http")
            print("       • 443/tcp - https")
            print("       • 8080/tcp - http-proxy")
            print("\n✅ Reconnaissance completed successfully!")
            
        elif command == "monitor start":
            print("🚀 Starting monitoring system...")
            print("✅ Monitoring system activated")
            print("   Use: show_alerts to view alerts")
            
        elif command == "monitor status":
            print("🔍 MONITORING STATUS")
            print("═" * 30)
            print("  🟢 Status: ACTIVE")
            print("  🚨 Alert Count: 0")
            print("  📋 Detection Rules: 25")
            
        elif command == "scan_ports":
            print("🔓 Port scanning: demo.testfire.net")
            print("⏳ Running quick port scan...")
            print("✅ Quick scan completed")
            print("   Use: recon for comprehensive scanning")
            
        elif command == "exit":
            print("🛑 Shutting down C-Keeper...")
            print("📊 SESSION SUMMARY")
            print("─" * 30)
            print("  🔍 Reconnaissance: 1 hosts scanned")
            print("  🎯 Last Target: demo.testfire.net")
            print("👋 Thanks for using C-Keeper! Stay secure!")
            
        print("-" * 40)
        
        if i < len(demo_commands):
            input(f"\nPress Enter to continue to step {i+1}...")
    
    print_section("🎉 DEMO COMPLETE!")
    print("The enhanced CLI interface provides:")
    print("✅ Professional visual design with colors and icons")
    print("✅ Categorized help system for easy navigation")
    print("✅ Enhanced error handling and user feedback")
    print("✅ Comprehensive reconnaissance capabilities")
    print("✅ Session management and monitoring features")
    print("✅ Intuitive command structure and auto-completion")
    
    print("\n🚀 Ready to use C-Keeper for real security assessments!")
    print("📖 Use 'help' command to explore all available features")

if __name__ == "__main__":
    try:
        demo_cli()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Thanks for watching!")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
