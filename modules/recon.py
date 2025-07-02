"""
Reconnaissance Module for C-Keeper
Handles target discovery, port scanning, and vulnerability assessment
"""

try:
    import nmap
    NMAP_AVAILABLE = True
except ImportError:
    NMAP_AVAILABLE = False
    nmap = None

import socket
import threading
import subprocess
import ipaddress
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging

from core.logger import CKeeperLogger

class ReconModule:
    """Reconnaissance module for both offensive and defensive operations"""
    
    def __init__(self, config, database, defensive_mode: bool = False):
        """
        Initialize reconnaissance module
        
        Args:
            config: Recon configuration
            database: Database instance
            defensive_mode: Whether to operate in defensive mode
        """
        self.config = config
        self.db = database
        self.defensive_mode = defensive_mode
        self.logger = CKeeperLogger(__name__)
        
        # Initialize nmap scanner
        if NMAP_AVAILABLE:
            try:
                self.nm = nmap.PortScanner()
            except Exception as e:
                self.logger.logger.warning(f"Nmap not available: {e}")
                self.nm = None
        else:
            self.logger.logger.warning("Nmap module not installed")
            self.nm = None
    
    def scan_target(self, target: str) -> Dict[str, Any]:
        """
        Perform comprehensive scan of target
        
        Args:
            target: Target IP, domain, or CIDR
            
        Returns:
            Scan results dictionary
        """
        results = {
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'scan_types': [],
            'hosts': [],
            'services': [],
            'vulnerabilities': [],
            'os_detection': {},
            'errors': []
        }
        
        try:
            # Host discovery
            hosts = self._discover_hosts(target)
            results['hosts'] = hosts
            results['scan_types'].append('host_discovery')
            
            # Port scanning for each host
            for host in hosts:
                try:
                    host_services = self._scan_ports(host['ip'])
                    host['services'] = host_services
                    results['services'].extend(host_services)
                    results['scan_types'].append('port_scan')
                    
                    # Service enumeration
                    for service in host_services:
                        service_info = self._enumerate_service(
                            host['ip'], service['port'], service['service']
                        )
                        service.update(service_info)
                    
                    # OS detection
                    if not self.defensive_mode:
                        os_info = self._detect_os(host['ip'])
                        if os_info:
                            host['os'] = os_info
                            results['os_detection'][host['ip']] = os_info
                    
                    # Vulnerability assessment
                    vulns = self._assess_vulnerabilities(host['ip'], host_services)
                    if vulns:
                        results['vulnerabilities'].extend(vulns)
                
                except Exception as e:
                    error_msg = f"Error scanning host {host['ip']}: {e}"
                    results['errors'].append(error_msg)
                    self.logger.logger.error(error_msg)
            
            # Log results to database
            self._log_results(target, results)
            
        except Exception as e:
            error_msg = f"Error during reconnaissance: {e}"
            results['errors'].append(error_msg)
            self.logger.logger.error(error_msg)
        
        return results
    
    def _discover_hosts(self, target: str) -> List[Dict[str, Any]]:
        """Discover live hosts in target range"""
        hosts = []
        
        try:
            # Parse target
            if '/' in target:
                # CIDR notation
                network = ipaddress.ip_network(target, strict=False)
                target_ips = [str(ip) for ip in network.hosts()]
            else:
                # Single IP or hostname
                target_ips = [target]
            
            # Limit hosts for safety
            if len(target_ips) > 254:
                target_ips = target_ips[:254]
                self.logger.logger.warning(f"Limited scan to first 254 hosts")
            
            # Ping sweep
            for ip in target_ips:
                if self._is_host_alive(ip):
                    host_info = {
                        'ip': ip,
                        'hostname': self._resolve_hostname(ip),
                        'status': 'up',
                        'discovered_at': datetime.now().isoformat()
                    }
                    hosts.append(host_info)
                    
                    self.logger.log_operation(
                        'HOST_DISCOVERY', ip, 'ALIVE',
                        hostname=host_info['hostname']
                    )
        
        except Exception as e:
            self.logger.logger.error(f"Host discovery error: {e}")
        
        return hosts
    
    def _is_host_alive(self, ip: str) -> bool:
        """Check if host is alive using ping"""
        try:
            # Use system ping command
            result = subprocess.run(
                ['ping', '-n', '1', '-w', '1000', ip],  # Windows ping
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            # Fallback to socket connection
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, 80))
                sock.close()
                return result == 0
            except:
                return False
    
    def _resolve_hostname(self, ip: str) -> Optional[str]:
        """Resolve IP to hostname"""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except:
            return None
    
    def _scan_ports(self, host: str) -> List[Dict[str, Any]]:
        """Scan ports on target host"""
        services = []
        
        try:
            if self.nm:
                # Use nmap for port scanning
                port_range = self.config.port_range
                self.nm.scan(
                    hosts=host,
                    ports=port_range,
                    arguments=self.config.nmap_options
                )
                
                if host in self.nm.all_hosts():
                    for port in self.nm[host]['tcp']:
                        port_info = self.nm[host]['tcp'][port]
                        service = {
                            'port': port,
                            'protocol': 'tcp',
                            'state': port_info['state'],
                            'service': port_info.get('name', 'unknown'),
                            'version': port_info.get('version', ''),
                            'product': port_info.get('product', ''),
                            'extrainfo': port_info.get('extrainfo', '')
                        }
                        services.append(service)
            else:
                # Fallback to basic socket scanning
                services = self._basic_port_scan(host)
            
            # Log discovered services
            for service in services:
                if service['state'] == 'open':
                    self.logger.log_operation(
                        'PORT_SCAN', f"{host}:{service['port']}", 'OPEN',
                        service=service['service'], version=service.get('version', '')
                    )
        
        except Exception as e:
            self.logger.logger.error(f"Port scan error for {host}: {e}")
        
        return services
    
    def _basic_port_scan(self, host: str) -> List[Dict[str, Any]]:
        """Basic port scan using sockets"""
        services = []
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 1433, 3306, 3389, 5432]
        
        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((host, port))
                sock.close()
                
                if result == 0:
                    service = {
                        'port': port,
                        'protocol': 'tcp',
                        'state': 'open',
                        'service': self._guess_service(port),
                        'version': '',
                        'product': '',
                        'extrainfo': ''
                    }
                    services.append(service)
            except:
                pass
        
        # Threaded port scanning
        threads = []
        for port in common_ports:
            thread = threading.Thread(target=scan_port, args=(port,))
            thread.start()
            threads.append(thread)
        
        # Wait for all threads
        for thread in threads:
            thread.join()
        
        return services
    
    def _guess_service(self, port: int) -> str:
        """Guess service based on port number"""
        port_services = {
            21: 'ftp', 22: 'ssh', 23: 'telnet', 25: 'smtp',
            53: 'dns', 80: 'http', 110: 'pop3', 143: 'imap',
            443: 'https', 993: 'imaps', 995: 'pop3s',
            1433: 'mssql', 3306: 'mysql', 3389: 'rdp', 5432: 'postgresql'
        }
        return port_services.get(port, 'unknown')
    
    def _enumerate_service(self, host: str, port: int, service: str) -> Dict[str, Any]:
        """Enumerate specific service for more information"""
        info = {}
        
        try:
            # Basic banner grabbing
            banner = self._grab_banner(host, port)
            if banner:
                info['banner'] = banner
            
            # Service-specific enumeration
            if service == 'http' or service == 'https':
                info.update(self._enumerate_http(host, port, service == 'https'))
            elif service == 'ftp':
                info.update(self._enumerate_ftp(host, port))
            elif service == 'ssh':
                info.update(self._enumerate_ssh(host, port))
            
        except Exception as e:
            self.logger.logger.debug(f"Service enumeration error for {host}:{port}: {e}")
        
        return info
    
    def _grab_banner(self, host: str, port: int) -> Optional[str]:
        """Grab service banner"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((host, port))
            
            # Send generic request
            sock.send(b'\r\n')
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            sock.close()
            
            return banner if banner else None
        except:
            return None
    
    def _enumerate_http(self, host: str, port: int, is_https: bool) -> Dict[str, Any]:
        """Enumerate HTTP service"""
        info = {}
        try:
            import requests
            protocol = 'https' if is_https else 'http'
            url = f"{protocol}://{host}:{port}"
            
            response = requests.get(url, timeout=10, verify=False)
            info['http_status'] = response.status_code
            info['http_headers'] = dict(response.headers)
            info['http_title'] = self._extract_title(response.text)
            
        except Exception as e:
            info['http_error'] = str(e)
        
        return info
    
    def _enumerate_ftp(self, host: str, port: int) -> Dict[str, Any]:
        """Enumerate FTP service"""
        info = {}
        try:
            import ftplib
            ftp = ftplib.FTP()
            ftp.connect(host, port, timeout=10)
            info['ftp_banner'] = ftp.getwelcome()
            
            # Test anonymous login
            try:
                ftp.login('anonymous', 'anonymous@example.com')
                info['ftp_anonymous'] = True
                ftp.quit()
            except:
                info['ftp_anonymous'] = False
                
        except Exception as e:
            info['ftp_error'] = str(e)
        
        return info
    
    def _enumerate_ssh(self, host: str, port: int) -> Dict[str, Any]:
        """Enumerate SSH service"""
        info = {}
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((host, port))
            
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            if 'SSH' in banner:
                info['ssh_banner'] = banner
                # Extract SSH version
                if 'SSH-' in banner:
                    info['ssh_version'] = banner.split('SSH-')[1].split()[0]
            
            sock.close()
        except Exception as e:
            info['ssh_error'] = str(e)
        
        return info
    
    def _extract_title(self, html: str) -> Optional[str]:
        """Extract title from HTML"""
        try:
            import re
            match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
            return match.group(1).strip() if match else None
        except:
            return None
    
    def _detect_os(self, host: str) -> Optional[Dict[str, Any]]:
        """Detect operating system"""
        if not self.nm:
            return None
        
        try:
            # OS detection with nmap
            self.nm.scan(host, arguments='-O')
            if host in self.nm.all_hosts() and 'osmatch' in self.nm[host]:
                os_matches = self.nm[host]['osmatch']
                if os_matches:
                    best_match = os_matches[0]
                    return {
                        'name': best_match['name'],
                        'accuracy': best_match['accuracy'],
                        'line': best_match['line']
                    }
        except Exception as e:
            self.logger.logger.debug(f"OS detection error for {host}: {e}")
        
        return None
    
    def _assess_vulnerabilities(self, host: str, services: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Assess vulnerabilities based on discovered services"""
        vulnerabilities = []
        
        for service in services:
            if service['state'] != 'open':
                continue
            
            # Check for common vulnerabilities
            vulns = self._check_service_vulnerabilities(
                host, service['port'], service['service'], service.get('version', '')
            )
            vulnerabilities.extend(vulns)
        
        return vulnerabilities
    
    def _check_service_vulnerabilities(self, host: str, port: int, 
                                     service: str, version: str) -> List[Dict[str, Any]]:
        """Check for vulnerabilities in specific service"""
        vulnerabilities = []
        
        # Common vulnerability checks
        vuln_checks = {
            'ftp': self._check_ftp_vulnerabilities,
            'ssh': self._check_ssh_vulnerabilities,
            'http': self._check_http_vulnerabilities,
            'https': self._check_http_vulnerabilities,
            'telnet': self._check_telnet_vulnerabilities,
            'smtp': self._check_smtp_vulnerabilities
        }
        
        if service in vuln_checks:
            try:
                vulns = vuln_checks[service](host, port, version)
                vulnerabilities.extend(vulns)
            except Exception as e:
                self.logger.logger.debug(f"Vulnerability check error: {e}")
        
        return vulnerabilities
    
    def _check_ftp_vulnerabilities(self, host: str, port: int, version: str) -> List[Dict[str, Any]]:
        """Check FTP vulnerabilities"""
        vulns = []
        
        # Check for anonymous FTP
        try:
            import ftplib
            ftp = ftplib.FTP()
            ftp.connect(host, port, timeout=10)
            ftp.login('anonymous', 'anonymous@example.com')
            
            vulns.append({
                'type': 'Anonymous FTP Access',
                'severity': 'Medium',
                'description': 'FTP server allows anonymous access',
                'service': 'ftp',
                'port': port,
                'host': host
            })
            ftp.quit()
        except:
            pass
        
        return vulns
    
    def _check_ssh_vulnerabilities(self, host: str, port: int, version: str) -> List[Dict[str, Any]]:
        """Check SSH vulnerabilities"""
        vulns = []
        
        # Check for weak SSH versions
        if version:
            if 'SSH-1' in version:
                vulns.append({
                    'type': 'Weak SSH Protocol',
                    'severity': 'High',
                    'description': 'SSH version 1.x is vulnerable',
                    'service': 'ssh',
                    'port': port,
                    'host': host,
                    'version': version
                })
        
        return vulns
    
    def _check_http_vulnerabilities(self, host: str, port: int, version: str) -> List[Dict[str, Any]]:
        """Check HTTP vulnerabilities"""
        vulns = []
        
        try:
            import requests
            protocol = 'https' if port == 443 else 'http'
            url = f"{protocol}://{host}:{port}"
            
            response = requests.get(url, timeout=10, verify=False)
            headers = response.headers
            
            # Check for missing security headers
            security_headers = ['X-Frame-Options', 'X-Content-Type-Options', 'X-XSS-Protection']
            for header in security_headers:
                if header not in headers:
                    vulns.append({
                        'type': f'Missing {header}',
                        'severity': 'Low',
                        'description': f'Missing security header: {header}',
                        'service': 'http',
                        'port': port,
                        'host': host
                    })
            
            # Check for directory listing
            dir_response = requests.get(f"{url}/", timeout=10, verify=False)
            if 'Index of' in dir_response.text:
                vulns.append({
                    'type': 'Directory Listing',
                    'severity': 'Medium',
                    'description': 'Web server allows directory listing',
                    'service': 'http',
                    'port': port,
                    'host': host
                })
        
        except:
            pass
        
        return vulns
    
    def _check_telnet_vulnerabilities(self, host: str, port: int, version: str) -> List[Dict[str, Any]]:
        """Check Telnet vulnerabilities"""
        return [{
            'type': 'Insecure Protocol',
            'severity': 'High',
            'description': 'Telnet transmits data in cleartext',
            'service': 'telnet',
            'port': port,
            'host': host
        }]
    
    def _check_smtp_vulnerabilities(self, host: str, port: int, version: str) -> List[Dict[str, Any]]:
        """Check SMTP vulnerabilities"""
        vulns = []
        
        # Check for open relay
        try:
            import smtplib
            server = smtplib.SMTP(host, port, timeout=10)
            # Test if server accepts mail for external domains
            try:
                server.mail('test@example.com')
                server.rcpt('test@external.com')
                vulns.append({
                    'type': 'Open Mail Relay',
                    'severity': 'High',
                    'description': 'SMTP server may be an open relay',
                    'service': 'smtp',
                    'port': port,
                    'host': host
                })
            except:
                pass
            server.quit()
        except:
            pass
        
        return vulns
    
    def _log_results(self, target: str, results: Dict[str, Any]):
        """Log reconnaissance results to database"""
        try:
            # Log general recon results
            self.db.log_recon_results(
                session_id='current',  # This should be passed from engine
                target=target,
                scan_type='comprehensive',
                results=results
            )
            
            # Log individual vulnerabilities
            for vuln in results['vulnerabilities']:
                self.db.add_vulnerability(
                    target=vuln['host'],
                    service=vuln['service'],
                    port=vuln['port'],
                    vulnerability=vuln['type'],
                    severity=vuln['severity']
                )
        
        except Exception as e:
            self.logger.logger.error(f"Error logging results: {e}")
    
    def get_scan_history(self, target: str = None) -> List[Dict[str, Any]]:
        """Get scan history from database"""
        # This would query the database for historical scan results
        # Implementation depends on database schema
        return []
    
    def continuous_monitoring(self, targets: List[str], interval: int = 3600):
        """Start continuous monitoring of targets (blue team mode)"""
        if not self.defensive_mode:
            self.logger.logger.warning("Continuous monitoring should only be used in defensive mode")
        
        # Implementation for continuous monitoring
        # This would run scans at regular intervals and detect changes
        pass
