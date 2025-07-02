"""
CLI Interface for C-Keeper
Command-line interface for the cyber kill chain engine
"""

import cmd
import json
import sys
import os
from typing import Dict, Any, List
from datetime import datetime

from core.engine import CKeeperEngine
from core.logger import CKeeperLogger

# ANSI Color codes for enhanced CLI experience
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    # Additional colors for better UI
    PURPLE = '\033[35m'
    YELLOW = '\033[33m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    GRAY = '\033[90m'

def colored_text(text, color):
    """Return colored text if terminal supports it"""
    if os.name == 'nt':  # Windows
        try:
            os.system('color')  # Enable ANSI colors on Windows
        except:
            pass
    return f"{color}{text}{Colors.ENDC}"

def print_banner():
    """Print a cool ASCII banner"""
    banner = f"""
{Colors.CYAN}
 ██████╗      ██╗  ██╗███████╗███████╗██████╗ ███████╗██████╗ 
██╔════╝      ██║ ██╔╝██╔════╝██╔════╝██╔══██╗██╔════╝██╔══██╗
██║     █████╗█████╔╝ █████╗  █████╗  ██████╔╝█████╗  ██████╔╝
██║     ╚════╝██╔═██╗ ██╔══╝  ██╔══╝  ██╔═══╝ ██╔══╝  ██╔══██╗
╚██████╗      ██║  ██╗███████╗███████╗██║     ███████╗██║  ██║
 ╚═════╝      ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝
{Colors.ENDC}
{Colors.BOLD}{Colors.YELLOW}              Cyber Kill Chain Engine v2.0              {Colors.ENDC}
{Colors.GRAY}            Dual-Use Security Assessment Platform            {Colors.ENDC}
{Colors.PURPLE}═══════════════════════════════════════════════════════════════{Colors.ENDC}
"""
    print(banner)

class CLIInterface(cmd.Cmd):
    """Enhanced command-line interface for C-Keeper"""
    
    intro = f"""
{colored_text("╔═══════════════════════════════════════════════════════════════╗", Colors.CYAN)}
{colored_text("║", Colors.CYAN)} {colored_text("Welcome to C-KEEPER - Cyber Kill Chain Engine", Colors.BOLD + Colors.WHITE)}            {colored_text("║", Colors.CYAN)}
{colored_text("║", Colors.CYAN)} {colored_text("Type 'help' or '?' to list commands", Colors.YELLOW)}                           {colored_text("║", Colors.CYAN)}
{colored_text("║", Colors.CYAN)} {colored_text("Type 'help <command>' for detailed help", Colors.YELLOW)}                      {colored_text("║", Colors.CYAN)}
{colored_text("║", Colors.CYAN)} {colored_text("Type 'demo' for a quick demonstration", Colors.GREEN)}                        {colored_text("║", Colors.CYAN)}
{colored_text("╚═══════════════════════════════════════════════════════════════╝", Colors.CYAN)}

{colored_text("Quick Start:", Colors.BOLD + Colors.WHITE)}
  1. {colored_text("set_target <ip/domain>", Colors.CYAN)} - Set your target
  2. {colored_text("recon", Colors.CYAN)} - Run reconnaissance
  3. {colored_text("status", Colors.CYAN)} - Check system status
"""
    
    prompt = f'{colored_text("(", Colors.GRAY)}{colored_text("C-Keeper", Colors.BOLD + Colors.CYAN)}{colored_text(")", Colors.GRAY)} {colored_text("➤", Colors.GREEN)} '
    
    def __init__(self, engine: CKeeperEngine):
        super().__init__()
        self.engine = engine
        self.logger = CKeeperLogger(__name__)
        self.current_target = None
        self.session_data = {}
        
        # Print banner on startup
        print_banner()
    
    def run(self, args) -> int:
        """Run the CLI interface"""
        try:
            # Set target if provided
            if args.target:
                self.current_target = args.target
                print(colored_text(f"✓ Target set to: {self.current_target}", Colors.GREEN))
            
            # Start monitoring if requested
            if args.monitor:
                print(colored_text("🔍 Starting monitoring system...", Colors.YELLOW))
                self.do_monitor('start')
            
            # Start command loop
            self.cmdloop()
            
            return 0
            
        except KeyboardInterrupt:
            print(colored_text("\n👋 Exiting C-Keeper... Stay secure!", Colors.YELLOW))
            return 0
        except Exception as e:
            print(colored_text(f"❌ CLI Error: {e}", Colors.FAIL))
            return 1
    
    # ==== GENERAL COMMANDS ====
    
    def do_demo(self, args):
        """🎯 Run a quick demonstration of C-Keeper capabilities"""
        print(colored_text("🎯 C-Keeper Demo Mode", Colors.BOLD + Colors.CYAN))
        print(colored_text("═" * 50, Colors.CYAN))
        
        demo_target = "demo.testfire.net"
        print(f"\n{colored_text('1.', Colors.YELLOW)} Setting demo target: {colored_text(demo_target, Colors.WHITE)}")
        self.current_target = demo_target
        
        print(f"\n{colored_text('2.', Colors.YELLOW)} Running reconnaissance...")
        self.do_recon("")
        
        print(f"\n{colored_text('3.', Colors.YELLOW)} Checking system status...")
        self.do_status("")
        
        print(f"\n{colored_text('✓', Colors.GREEN)} Demo complete! You can now explore other commands.")
        print(f"   Try: {colored_text('help', Colors.CYAN)} to see all available commands")
    
    def do_banner(self, args):
        """🎨 Display the C-Keeper banner"""
        print_banner()
    
    def do_status(self, args):
        """📊 Show system status and session information"""
        session_info = self.engine.get_session_info()
        
        print(f"\n{colored_text('📊 C-KEEPER SYSTEM STATUS', Colors.BOLD + Colors.CYAN)}")
        print(colored_text("═" * 50, Colors.CYAN))
        
        # Main status info with icons
        print(f"{colored_text('🔧 Mode:', Colors.YELLOW)} {colored_text(session_info['mode'].upper(), Colors.WHITE)}")
        print(f"{colored_text('🆔 Session ID:', Colors.YELLOW)} {colored_text(session_info['session_id'], Colors.WHITE)}")
        print(f"{colored_text('🎯 Current Target:', Colors.YELLOW)} {colored_text(self.current_target or 'None', Colors.WHITE if self.current_target else Colors.GRAY)}")
        print(f"{colored_text('⏰ Start Time:', Colors.YELLOW)} {colored_text(session_info['start_time'], Colors.WHITE)}")
        
        # Module status with better formatting
        print(f"\n{colored_text('📦 MODULE STATUS', Colors.BOLD + Colors.BLUE)}")
        print(colored_text("─" * 30, Colors.BLUE))
        for module_name in session_info['modules']:
            module = self.engine.get_module(module_name)
            if module:
                status_icon = colored_text("✅", Colors.GREEN)
                status_text = colored_text("Active", Colors.GREEN)
            else:
                status_icon = colored_text("❌", Colors.RED)
                status_text = colored_text("Inactive", Colors.RED)
            
            print(f"  {status_icon} {module_name.ljust(20)} {status_text}")
        
        # Session data summary
        if self.session_data:
            print(f"\n{colored_text('💾 SESSION DATA', Colors.BOLD + Colors.PURPLE)}")
            print(colored_text("─" * 30, Colors.PURPLE))
            if 'last_recon' in self.session_data:
                recon = self.session_data['last_recon']
                print(f"  {colored_text('🔍', Colors.CYAN)} Last Recon: {len(recon.get('hosts', []))} hosts found")
            if 'last_exploits' in self.session_data:
                exploits = self.session_data['last_exploits']
                print(f"  {colored_text('💥', Colors.RED)} Exploits: {len(exploits.get('exploits', []))} built")
    
    def do_set_target(self, target):
        """🎯 Set target for operations
        Usage: set_target <IP/CIDR/domain>
        Examples: 
          set_target 192.168.1.100
          set_target example.com
          set_target 10.0.0.0/24
        """
        if not target:
            print(colored_text("❌ Error: Target required", Colors.FAIL))
            print(f"Usage: {colored_text('set_target <IP/CIDR/domain>', Colors.CYAN)}")
            return
        
        self.current_target = target
        print(colored_text(f"✅ Target set to: {target}", Colors.GREEN))
        print(f"   You can now run: {colored_text('recon', Colors.CYAN)} to scan this target")
    
    def do_show_target(self, args):
        """🎯 Show current target"""
        if self.current_target:
            print(f"{colored_text('🎯 Current target:', Colors.YELLOW)} {colored_text(self.current_target, Colors.WHITE)}")
        else:
            print(colored_text("❌ No target set", Colors.GRAY))
            print(f"   Use: {colored_text('set_target <target>', Colors.CYAN)} to set a target")
    
    def do_clear_target(self, args):
        """🧹 Clear current target"""
        self.current_target = None
        print(colored_text("✅ Target cleared", Colors.GREEN))
    
    # ==== RECONNAISSANCE COMMANDS ====
    
    def do_recon(self, args):
        """🔍 Perform reconnaissance on target
        Usage: recon [target]
        
        This command performs comprehensive reconnaissance including:
        • Host discovery and port scanning
        • Service detection and enumeration  
        • Vulnerability assessment
        • Banner grabbing and OS detection
        """
        target = args or self.current_target
        if not target:
            print(colored_text("❌ Error: No target specified", Colors.FAIL))
            print(f"   Use: {colored_text('set_target <target>', Colors.CYAN)} first, or")
            print(f"   Use: {colored_text('recon <target>', Colors.CYAN)} directly")
            return
        
        print(f"\n{colored_text('🔍 RECONNAISSANCE SCAN', Colors.BOLD + Colors.CYAN)}")
        print(colored_text("═" * 50, Colors.CYAN))
        print(f"{colored_text('🎯 Target:', Colors.YELLOW)} {colored_text(target, Colors.WHITE)}")
        print(f"{colored_text('⏰ Started:', Colors.YELLOW)} {colored_text(datetime.now().strftime('%H:%M:%S'), Colors.WHITE)}")
        
        recon_module = self.engine.get_module('recon')
        if not recon_module:
            print(colored_text("❌ Error: Reconnaissance module not available", Colors.FAIL))
            return
        
        try:
            print(colored_text("\n🚀 Initiating scan...", Colors.YELLOW))
            results = recon_module.scan_target(target)
            self._display_recon_results(results)
            
            # Store results for session
            self.session_data['last_recon'] = results
            print(colored_text("\n✅ Reconnaissance completed successfully!", Colors.GREEN))
            
        except Exception as e:
            print(colored_text(f"\n❌ Reconnaissance failed: {e}", Colors.FAIL))
    
    def _display_recon_results(self, results: Dict[str, Any]):
        """Display reconnaissance results with enhanced formatting"""
        print(f"\n{colored_text('📋 RECONNAISSANCE RESULTS', Colors.BOLD + Colors.GREEN)}")
        print(colored_text("═" * 50, Colors.GREEN))
        
        print(f"{colored_text('🎯 Target:', Colors.YELLOW)} {colored_text(results['target'], Colors.WHITE)}")
        print(f"{colored_text('⏰ Scan Time:', Colors.YELLOW)} {colored_text(results['timestamp'], Colors.WHITE)}")
        print(f"{colored_text('🖥️  Hosts Found:', Colors.YELLOW)} {colored_text(str(len(results['hosts'])), Colors.WHITE)}")
        
        # Display hosts with better formatting
        if results['hosts']:
            print(f"\n{colored_text('🖥️  DISCOVERED HOSTS', Colors.BOLD + Colors.BLUE)}")
            print(colored_text("─" * 40, Colors.BLUE))
            
            for i, host in enumerate(results['hosts'], 1):
                hostname = host.get('hostname', 'Unknown')
                print(f"  {colored_text(f'{i}.', Colors.CYAN)} {colored_text(host['ip'], Colors.WHITE)} {colored_text(f'({hostname})', Colors.GRAY)}")
                
                if 'services' in host:
                    open_ports = [s for s in host['services'] if s['state'] == 'open']
                    if open_ports:
                        print(f"     {colored_text('🔓 Open Ports:', Colors.GREEN)}")
                        for service in open_ports[:5]:  # Show first 5 ports
                            port_info = f"{service['port']}/{service['protocol']}"
                            service_name = service.get('service', 'unknown')
                            print(f"       • {colored_text(port_info, Colors.CYAN)} - {colored_text(service_name, Colors.WHITE)}")
                        
                        if len(open_ports) > 5:
                            print(f"       ... and {colored_text(str(len(open_ports) - 5), Colors.YELLOW)} more ports")
        
        # Display vulnerabilities with severity colors
        if results['vulnerabilities']:
            print(f"\n{colored_text('⚠️  VULNERABILITIES FOUND', Colors.BOLD + Colors.RED)}")
            print(colored_text("─" * 40, Colors.RED))
            
            # Group by severity
            high_vulns = [v for v in results['vulnerabilities'] if v.get('severity') == 'HIGH']
            medium_vulns = [v for v in results['vulnerabilities'] if v.get('severity') == 'MEDIUM']
            low_vulns = [v for v in results['vulnerabilities'] if v.get('severity') == 'LOW']
            
            if high_vulns:
                print(f"  {colored_text('🚨 HIGH SEVERITY:', Colors.RED + Colors.BOLD)}")
                for vuln in high_vulns:
                    print(f"    • {vuln['host']}:{vuln['port']} - {colored_text(vuln['type'], Colors.RED)}")
            
            if medium_vulns:
                print(f"  {colored_text('⚠️  MEDIUM SEVERITY:', Colors.YELLOW + Colors.BOLD)}")
                for vuln in medium_vulns:
                    print(f"    • {vuln['host']}:{vuln['port']} - {colored_text(vuln['type'], Colors.YELLOW)}")
            
            if low_vulns:
                print(f"  {colored_text('ℹ️  LOW SEVERITY:', Colors.BLUE + Colors.BOLD)}")
                for vuln in low_vulns:
                    print(f"    • {vuln['host']}:{vuln['port']} - {colored_text(vuln['type'], Colors.BLUE)}")
        else:
            print(f"\n{colored_text('✅ No vulnerabilities detected', Colors.GREEN)}")
        
        # Display errors if any
        if results['errors']:
            print(f"\n{colored_text('⚠️  SCAN ERRORS', Colors.BOLD + Colors.YELLOW)}")
            print(colored_text("─" * 40, Colors.YELLOW))
            for error in results['errors']:
                print(f"  {colored_text('•', Colors.YELLOW)} {error}")
    
    def do_scan_ports(self, args):
        """🔓 Quick port scan on target
        Usage: scan_ports [target]
        """
        target = args or self.current_target
        if not target:
            print(colored_text("❌ Error: No target specified", Colors.FAIL))
            return
        
        print(f"{colored_text('🔓 Port scanning:', Colors.CYAN)} {colored_text(target, Colors.WHITE)}")
        print(colored_text("⏳ Running quick port scan...", Colors.YELLOW))
        
        # Mock port scan results for demo
        print(colored_text("✅ Quick scan completed", Colors.GREEN))
        print(f"   Use: {colored_text('recon', Colors.CYAN)} for comprehensive scanning")
    
    # ==== EXPLOITATION COMMANDS ====
    
    def do_exploit(self, args):
        """Build and run exploits against target
        Usage: exploit [target]
        """
        target = args or self.current_target
        if not target:
            print("Error: No target specified")
            return
        
        # Check if we have reconnaissance data
        if 'last_recon' not in self.session_data:
            print("Warning: No reconnaissance data available. Running recon first...")
            self.do_recon(target)
        
        print(f"Building exploits for {target}...")
        
        exploit_builder = self.engine.get_module('exploit_builder')
        if not exploit_builder:
            print("Error: Exploit builder module not available")
            return
        
        try:
            vulnerabilities = self.session_data.get('last_recon', {}).get('vulnerabilities', [])
            if not vulnerabilities:
                print("No vulnerabilities found to exploit")
                return
            
            results = exploit_builder.build_exploits(vulnerabilities)
            self._display_exploit_results(results)
            
            # Store results
            self.session_data['last_exploits'] = results
            
        except Exception as e:
            print(f"Exploit building failed: {e}")
    
    def _display_exploit_results(self, results: Dict[str, Any]):
        """Display exploit building results"""
        print("\\n=== Exploit Building Results ===")
        print(f"Vulnerabilities Processed: {results['vulnerabilities_processed']}")
        print(f"Exploits Built: {len(results['exploits'])}")
        print(f"Failed: {len(results['failed'])}")
        
        if results['exploits']:
            print("\\n--- Built Exploits ---")
            for exploit in results['exploits']:
                print(f"  {exploit['name']} ({exploit['type']})")
                print(f"    Target: {exploit['target']}")
                print(f"    Reliability: {exploit.get('reliability', 'Unknown')}")
        
        if results['recommendations']:
            print("\\n--- Recommendations ---")
            for rec in results['recommendations']:
                print(f"  • {rec}")
    
    def do_run_exploit(self, exploit_id):
        """Run specific exploit
        Usage: run_exploit <exploit_id>
        """
        if not exploit_id:
            print("Error: Exploit ID required")
            return
        
        # Find exploit in session data
        exploits = self.session_data.get('last_exploits', {}).get('exploits', [])
        exploit = None
        for exp in exploits:
            if exp['id'] == exploit_id or exp['name'] == exploit_id:
                exploit = exp
                break
        
        if not exploit:
            print(f"Error: Exploit '{exploit_id}' not found")
            return
        
        print(f"Running exploit: {exploit['name']}")
        
        exploit_runner = self.engine.get_module('exploit_runner')
        if not exploit_runner:
            print("Error: Exploit runner module not available")
            return
        
        try:
            result = exploit_runner.run_exploit(exploit, self.current_target)
            self._display_exploit_execution_result(result)
            
        except Exception as e:
            print(f"Exploit execution failed: {e}")
    
    def _display_exploit_execution_result(self, result: Dict[str, Any]):
        """Display exploit execution result"""
        print("\\n=== Exploit Execution Result ===")
        print(f"Execution ID: {result['execution_id']}")
        print(f"Target: {result['target']}")
        print(f"Success: {result['success']}")
        print(f"Duration: {result['duration']:.2f} seconds")
        
        if result['output']:
            print("\\n--- Output ---")
            print(result['output'])
        
        if result['errors']:
            print("\\n--- Errors ---")
            for error in result['errors']:
                print(f"  {error}")
    
    # ==== PAYLOAD COMMANDS ====
    
    def do_generate_payload(self, args):
        """Generate payload
        Usage: generate_payload <type> <platform> [options]
        Example: generate_payload reverse_shell windows lhost=192.168.1.100 lport=4444
        """
        if not args:
            print("Usage: generate_payload <type> <platform> [options]")
            print("Types: reverse_shell, bind_shell, meterpreter, exec")
            print("Platforms: windows, linux, macos, web")
            return
        
        parts = args.split()
        if len(parts) < 2:
            print("Error: Type and platform required")
            return
        
        payload_type = parts[0]
        platform = parts[1]
        
        # Parse options
        options = {}
        for part in parts[2:]:
            if '=' in part:
                key, value = part.split('=', 1)
                options[key] = value
        
        # Set defaults
        if 'lhost' not in options:
            options['lhost'] = '127.0.0.1'
        if 'lport' not in options:
            options['lport'] = 4444
        
        print(f"Generating {payload_type} payload for {platform}...")
        
        payload_generator = self.engine.get_module('payload_generator')
        if not payload_generator:
            print("Error: Payload generator module not available")
            return
        
        try:
            result = payload_generator.generate_payload(payload_type, platform, options)
            self._display_payload_result(result)
            
        except Exception as e:
            print(f"Payload generation failed: {e}")
    
    def _display_payload_result(self, result: Dict[str, Any]):
        """Display payload generation result"""
        print("\\n=== Payload Generation Result ===")
        print(f"Payload ID: {result['id']}")
        print(f"Type: {result['type']}")
        print(f"Platform: {result['platform']}")
        print(f"Encoder: {result['encoder']}")
        print(f"Size: {result['size']} bytes")
        print(f"Success: {result['success']}")
        
        if result.get('file_path'):
            print(f"Saved to: {result['file_path']}")
        
        if result['errors']:
            print("\\n--- Errors ---")
            for error in result['errors']:
                print(f"  {error}")
    
    # ==== C2 COMMANDS ====
    
    def do_start_listener(self, args):
        """Start C2 listener
        Usage: start_listener <type> <port>
        Types: tcp, http, https
        """
        if not args:
            print("Usage: start_listener <type> <port>")
            return
        
        parts = args.split()
        if len(parts) != 2:
            print("Error: Type and port required")
            return
        
        listener_type = parts[0]
        try:
            port = int(parts[1])
        except ValueError:
            print("Error: Invalid port number")
            return
        
        print(f"Starting {listener_type} listener on port {port}...")
        
        c2_handler = self.engine.get_module('c2_handler')
        if not c2_handler:
            print("Error: C2 handler module not available")
            return
        
        try:
            result = c2_handler.start_listener(listener_type, port)
            if result['success']:
                print(f"✓ {result['message']}")
            else:
                print(f"✗ {result['error']}")
                
        except Exception as e:
            print(f"Failed to start listener: {e}")
    
    def do_list_sessions(self, args):
        """List active C2 sessions"""
        c2_handler = self.engine.get_module('c2_handler')
        if not c2_handler:
            print("Error: C2 handler module not available")
            return
        
        sessions = c2_handler.list_sessions()
        
        if not sessions:
            print("No active sessions")
            return
        
        print("\\n=== Active C2 Sessions ===")
        for session in sessions:
            print(f"  {session['id']} - {session['address']} ({session['type']}) - {session['established_at']}")
    
    # ==== MONITORING COMMANDS ====
    
    def do_monitor(self, action):
        """🔍 Control monitoring system
        Usage: monitor <start|stop|status>
        
        Controls the security monitoring and logging system:
        • start  - Begin monitoring network activity
        • stop   - Stop monitoring
        • status - Check monitoring status
        """
        if not action:
            print(colored_text("❌ Usage: monitor <start|stop|status>", Colors.FAIL))
            return
        
        logger_defender = self.engine.get_module('logger_defender')
        if not logger_defender:
            print(colored_text("❌ Error: Logger/Defender module not available", Colors.FAIL))
            return
        
        if action == 'start':
            print(colored_text("🚀 Starting monitoring system...", Colors.YELLOW))
            self.engine.start_monitoring()
            print(colored_text("✅ Monitoring system activated", Colors.GREEN))
            print(f"   Use: {colored_text('show_alerts', Colors.CYAN)} to view alerts")
            
        elif action == 'stop':
            print(colored_text("🛑 Stopping monitoring system...", Colors.YELLOW))
            self.engine.stop_monitoring()
            print(colored_text("✅ Monitoring system deactivated", Colors.GREEN))
            
        elif action == 'status':
            status = logger_defender.get_monitoring_status()
            print(f"\n{colored_text('🔍 MONITORING STATUS', Colors.BOLD + Colors.BLUE)}")
            print(colored_text("═" * 30, Colors.BLUE))
            
            # Status indicators
            active_icon = colored_text("🟢", Colors.GREEN) if status['monitoring_active'] else colored_text("🔴", Colors.RED)
            active_text = colored_text("ACTIVE", Colors.GREEN) if status['monitoring_active'] else colored_text("INACTIVE", Colors.RED)
            
            print(f"  {active_icon} Status: {active_text}")
            print(f"  {colored_text('🚨', Colors.YELLOW)} Alert Count: {colored_text(str(status['alert_count']), Colors.WHITE)}")
            print(f"  {colored_text('📋', Colors.CYAN)} Detection Rules: {colored_text(str(status['detection_rules_count']), Colors.WHITE)}")
            
        else:
            print(colored_text("❌ Error: Invalid action. Use start, stop, or status", Colors.FAIL))
    
    def do_show_alerts(self, args):
        """Show recent security alerts
        Usage: show_alerts [hours]
        """
        hours = 24
        if args:
            try:
                hours = int(args)
            except ValueError:
                print("Error: Invalid hours value")
                return
        
        logger_defender = self.engine.get_module('logger_defender')
        if not logger_defender:
            print("Error: Logger/Defender module not available")
            return
        
        alerts = logger_defender.get_recent_alerts(hours)
        
        if not alerts:
            print(f"No alerts in the last {hours} hours")
            return
        
        print(f"\\n=== Recent Alerts (Last {hours} hours) ===")
        for alert in alerts[:10]:  # Show latest 10
            print(f"  {alert['timestamp']} - {alert['event_type']} ({alert['severity']})")
            print(f"    {alert['description']}")
    
    # ==== KILL CHAIN COMMANDS ====
    
    def do_run_killchain(self, args):
        """Execute complete kill chain against target
        Usage: run_killchain [target]
        """
        target = args or self.current_target
        if not target:
            print("Error: No target specified")
            return
        
        if self.engine.mode == 'blue':
            print("Error: Kill chain execution not available in blue team mode")
            return
        
        print(f"Executing kill chain against {target}...")
        print("This will run: Recon -> Weaponization -> Delivery -> Exploitation -> Installation")
        
        confirm = input("Continue? (y/N): ")
        if confirm.lower() != 'y':
            print("Kill chain execution cancelled")
            return
        
        try:
            chain_config = {
                'run_recon': True,
                'run_weaponization': True,
                'run_delivery': True,
                'run_exploitation': True,
                'run_installation': True
            }
            
            results = self.engine.execute_kill_chain(target, chain_config)
            self._display_killchain_results(results)
            
        except Exception as e:
            print(f"Kill chain execution failed: {e}")
    
    def _display_killchain_results(self, results: Dict[str, Any]):
        """Display kill chain execution results"""
        print("\\n=== Kill Chain Execution Results ===")
        print(f"Session ID: {results['session_id']}")
        print(f"Target: {results['target']}")
        print(f"Execution Time: {results['timestamp']}")
        
        if 'error' in results:
            print(f"Error: {results['error']}")
            return
        
        print("\\n--- Stages Completed ---")
        for stage, data in results['stages'].items():
            print(f"  ✓ {stage.title()}")
            
            # Show brief summary for each stage
            if stage == 'reconnaissance' and 'hosts' in data:
                print(f"    Hosts found: {len(data['hosts'])}")
                print(f"    Vulnerabilities: {len(data.get('vulnerabilities', []))}")
            elif stage == 'weaponization' and 'exploits' in data:
                print(f"    Exploits built: {len(data['exploits'])}")
            elif stage == 'installation' and 'listeners_started' in data:
                print(f"    Listeners: {data['listeners_started']}")
    
    # ==== UTILITY COMMANDS ====
    
    def do_save_session(self, filename):
        """Save session data to file
        Usage: save_session <filename>
        """
        if not filename:
            print("Error: Filename required")
            return
        
        try:
            session_data = {
                'session_info': self.engine.get_session_info(),
                'current_target': self.current_target,
                'session_data': self.session_data,
                'timestamp': datetime.now().isoformat()
            }
            
            with open(filename, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            print(f"Session saved to {filename}")
            
        except Exception as e:
            print(f"Failed to save session: {e}")
    
    def do_load_session(self, filename):
        """Load session data from file
        Usage: load_session <filename>
        """
        if not filename:
            print("Error: Filename required")
            return
        
        try:
            with open(filename, 'r') as f:
                session_data = json.load(f)
            
            self.current_target = session_data.get('current_target')
            self.session_data = session_data.get('session_data', {})
            
            print(f"Session loaded from {filename}")
            print(f"Target: {self.current_target}")
            
        except Exception as e:
            print(f"Failed to load session: {e}")
    
    def do_export_report(self, filename):
        """Export session report
        Usage: export_report <filename>
        """
        if not filename:
            print("Error: Filename required")
            return
        
        try:
            report = self._generate_report()
            
            with open(filename, 'w') as f:
                f.write(report)
            
            print(f"Report exported to {filename}")
            
        except Exception as e:
            print(f"Failed to export report: {e}")
    
    def _generate_report(self) -> str:
        """Generate session report"""
        session_info = self.engine.get_session_info()
        
        report = f"""
C-KEEPER SESSION REPORT
=======================

Session Information:
- Session ID: {session_info['session_id']}
- Mode: {session_info['mode']}
- Start Time: {session_info['start_time']}
- Target: {self.current_target or 'None'}

Modules Used:
{chr(10).join(f"- {module}" for module in session_info['modules'])}

"""
        
        # Add reconnaissance results if available
        if 'last_recon' in self.session_data:
            recon = self.session_data['last_recon']
            report += f"""
Reconnaissance Results:
- Hosts Found: {len(recon.get('hosts', []))}
- Services Found: {len(recon.get('services', []))}
- Vulnerabilities: {len(recon.get('vulnerabilities', []))}
"""
        
        # Add exploit results if available
        if 'last_exploits' in self.session_data:
            exploits = self.session_data['last_exploits']
            report += f"""
Exploitation Results:
- Exploits Built: {len(exploits.get('exploits', []))}
- Failed Builds: {len(exploits.get('failed', []))}
"""
        
        report += f"""
Report Generated: {datetime.now().isoformat()}
"""
        
        return report
    
    def do_exit(self, args):
        """👋 Exit C-Keeper"""
        print(f"\n{colored_text('🛑 Shutting down C-Keeper...', Colors.YELLOW)}")
        
        # Show session summary before exit
        if self.session_data:
            print(f"\n{colored_text('📊 SESSION SUMMARY', Colors.BOLD + Colors.CYAN)}")
            print(colored_text("─" * 30, Colors.CYAN))
            
            if 'last_recon' in self.session_data:
                recon = self.session_data['last_recon']
                print(f"  {colored_text('🔍', Colors.CYAN)} Reconnaissance: {len(recon.get('hosts', []))} hosts scanned")
            
            if 'last_exploits' in self.session_data:
                exploits = self.session_data['last_exploits']
                print(f"  {colored_text('💥', Colors.RED)} Exploits: {len(exploits.get('exploits', []))} built")
            
            if self.current_target:
                print(f"  {colored_text('🎯', Colors.YELLOW)} Last Target: {self.current_target}")
        
        self.engine.shutdown()
        print(colored_text("👋 Thanks for using C-Keeper! Stay secure!", Colors.GREEN))
        return True
    
    def do_quit(self, args):
        """👋 Exit C-Keeper (alias for exit)"""
        return self.do_exit(args)
    
    def do_EOF(self, args):
        """Handle Ctrl+D"""
        print()
        return self.do_exit(args)
    
    def emptyline(self):
        """Handle empty line - show a helpful tip"""
        tips = [
            f"💡 Tip: Type {colored_text('help', Colors.CYAN)} to see all commands",
            f"💡 Tip: Use {colored_text('demo', Colors.CYAN)} for a quick demonstration",
            f"💡 Tip: Set a target with {colored_text('set_target <ip>', Colors.CYAN)}",
            f"💡 Tip: Check system status with {colored_text('status', Colors.CYAN)}",
            f"💡 Tip: Run reconnaissance with {colored_text('recon', Colors.CYAN)}",
        ]
        import random
        print(random.choice(tips))
    
    def default(self, line):
        """Handle unknown commands with helpful suggestions"""
        print(colored_text(f"❌ Unknown command: {line}", Colors.FAIL))
        
        # Suggest similar commands
        all_commands = [method[3:] for method in dir(self) if method.startswith('do_')]
        
        # Simple similarity check
        suggestions = []
        for cmd in all_commands:
            if line.lower() in cmd.lower() or cmd.lower() in line.lower():
                suggestions.append(cmd)
        
        if suggestions:
            print(f"{colored_text('💡 Did you mean:', Colors.YELLOW)} {colored_text(' | '.join(suggestions[:3]), Colors.CYAN)}")
        else:
            print(f"{colored_text('💡 Type', Colors.YELLOW)} {colored_text('help', Colors.CYAN)} {colored_text('for available commands', Colors.YELLOW)}")
    
    def precmd(self, line):
        """Pre-process commands - add timestamp for logging"""
        if line.strip():
            self.logger.info(f"Command executed: {line}")
        return line.strip()
    
    def postcmd(self, stop, line):
        """Post-process commands"""
        # Add a small separator for readability
        if line.strip() and not stop:
            print()
        return stop
    
    def do_help(self, arg):
        """🆘 Show help information"""
        if arg:
            # Show help for specific command
            super().do_help(arg)
        else:
            # Show categorized command list
            print(f"\n{colored_text('🆘 C-KEEPER COMMAND REFERENCE', Colors.BOLD + Colors.CYAN)}")
            print(colored_text("═" * 60, Colors.CYAN))
            
            # Command categories
            categories = {
                "🎯 Target Management": [
                    ("set_target", "Set target for operations"),
                    ("show_target", "Display current target"),
                    ("clear_target", "Clear current target"),
                ],
                "🔍 Reconnaissance": [
                    ("recon", "Run comprehensive reconnaissance"),
                    ("scan_ports", "Quick port scan"),
                ],
                "💥 Exploitation": [
                    ("exploit", "Build and prepare exploits"),
                    ("run_exploit", "Execute specific exploit"),
                ],
                "🎭 Payload Generation": [
                    ("generate_payload", "Create custom payloads"),
                ],
                "🎛️  Command & Control": [
                    ("start_listener", "Start C2 listener"),
                    ("list_sessions", "Show active sessions"),
                ],
                "🔒 Security Monitoring": [
                    ("monitor", "Control monitoring system"),
                    ("show_alerts", "Display security alerts"),
                ],
                "⚡ Advanced Operations": [
                    ("run_killchain", "Execute full kill chain"),
                ],
                "💾 Session Management": [
                    ("status", "Show system status"),
                    ("save_session", "Save current session"),
                    ("load_session", "Load saved session"),
                    ("export_report", "Generate report"),
                ],
                "🎨 Utilities": [
                    ("demo", "Run interactive demo"),
                    ("banner", "Show C-Keeper banner"),
                    ("exit/quit", "Exit C-Keeper"),
                ]
            }
            
            for category, commands in categories.items():
                print(f"\n{colored_text(category, Colors.BOLD + Colors.YELLOW)}")
                print(colored_text("─" * (len(category) - 4), Colors.YELLOW))
                
                for cmd, desc in commands:
                    print(f"  {colored_text(cmd.ljust(15), Colors.CYAN)} {colored_text(desc, Colors.WHITE)}")
            
            print(f"\n{colored_text('💡 Tips:', Colors.BOLD + Colors.GREEN)}")
            print(f"  • Type {colored_text('help <command>', Colors.CYAN)} for detailed help")
            print(f"  • Type {colored_text('demo', Colors.CYAN)} for a quick demonstration")
            print(f"  • Use {colored_text('Tab', Colors.YELLOW)} for command completion")
            print(f"  • Use {colored_text('Ctrl+C', Colors.YELLOW)} to interrupt operations")
    
    def do_commands(self, args):
        """📋 List all available commands (alias for help)"""
        self.do_help("")
