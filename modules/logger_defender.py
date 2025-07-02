"""
Logger/Defender Module for C-Keeper
Handles defensive monitoring, logging, and threat detection
"""

import threading
import time
import re
import psutil
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, List, Set
from pathlib import Path

from core.logger import CKeeperLogger

class LoggerDefenderModule:
    """Logger and defensive monitoring module"""
    
    def __init__(self, config, database):
        self.config = config
        self.db = database
        self.logger = CKeeperLogger(__name__)
        self.monitoring_active = False
        self.monitoring_thread = None
        self.detection_rules = self._load_detection_rules()
        self.alert_count = 0
        self.baseline_processes = set()
        self.baseline_network = set()
    
    def _load_detection_rules(self) -> List[Dict[str, Any]]:
        """Load detection rules"""
        return [
            {
                'name': 'Suspicious Network Connection',
                'type': 'network',
                'pattern': r'.*:(4444|4445|1337|31337).*',
                'severity': 'High',
                'description': 'Common hacker ports detected'
            },
            {
                'name': 'PowerShell Execution',
                'type': 'process',
                'pattern': r'powershell.*-EncodedCommand.*',
                'severity': 'Medium',
                'description': 'Encoded PowerShell command detected'
            },
            {
                'name': 'Nmap Scan Detection',
                'type': 'network',
                'pattern': r'.*nmap.*',
                'severity': 'Medium',
                'description': 'Nmap scanning activity detected'
            },
            {
                'name': 'Privilege Escalation Attempt',
                'type': 'process',
                'pattern': r'.*(sudo|runas).*',
                'severity': 'High',
                'description': 'Privilege escalation attempt detected'
            },
            {
                'name': 'Suspicious File Access',
                'type': 'file',
                'pattern': r'.*/etc/(passwd|shadow|sudoers).*',
                'severity': 'High',
                'description': 'Access to sensitive system files'
            }
        ]
    
    def start_monitoring(self):
        """Start defensive monitoring"""
        if self.monitoring_active:
            self.logger.logger.warning("Monitoring already active")
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        
        # Establish baseline
        self._establish_baseline()
        
        self.logger.log_security_event(
            'MONITORING_STARTED', 'Defensive monitoring activated', 'INFO'
        )
    
    def stop_monitoring(self):
        """Stop defensive monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        self.logger.log_security_event(
            'MONITORING_STOPPED', 'Defensive monitoring deactivated', 'INFO'
        )
    
    def _establish_baseline(self):
        """Establish system baseline"""
        try:
            # Baseline processes
            self.baseline_processes = {proc.name() for proc in psutil.process_iter(['name'])}
            
            # Baseline network connections
            self.baseline_network = {
                f"{conn.laddr.ip}:{conn.laddr.port}" 
                for conn in psutil.net_connections() 
                if conn.laddr
            }
            
            self.logger.logger.info(f"Baseline established: {len(self.baseline_processes)} processes, {len(self.baseline_network)} connections")
            
        except Exception as e:
            self.logger.logger.error(f"Error establishing baseline: {e}")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Monitor processes
                self._monitor_processes()
                
                # Monitor network connections
                self._monitor_network()
                
                # Monitor file system (simplified)
                self._monitor_filesystem()
                
                # Check for anomalies
                self._detect_anomalies()
                
                # Sleep before next iteration
                time.sleep(5)
                
            except Exception as e:
                self.logger.logger.error(f"Monitoring error: {e}")
                time.sleep(10)
    
    def _monitor_processes(self):
        """Monitor running processes"""
        try:
            current_processes = {proc.name() for proc in psutil.process_iter(['name', 'cmdline'])}
            
            # Detect new processes
            new_processes = current_processes - self.baseline_processes
            for proc_name in new_processes:
                self._check_process_against_rules(proc_name)
            
            # Check all processes against rules
            for proc in psutil.process_iter(['name', 'cmdline']):
                try:
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    self._check_command_against_rules(cmdline)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                
        except Exception as e:
            self.logger.logger.debug(f"Process monitoring error: {e}")
    
    def _monitor_network(self):
        """Monitor network connections"""
        try:
            current_connections = {
                f"{conn.laddr.ip}:{conn.laddr.port}" 
                for conn in psutil.net_connections() 
                if conn.laddr
            }
            
            # Detect new connections
            new_connections = current_connections - self.baseline_network
            for connection in new_connections:
                self._check_network_against_rules(connection)
                
        except Exception as e:
            self.logger.logger.debug(f"Network monitoring error: {e}")
    
    def _monitor_filesystem(self):
        """Monitor filesystem for suspicious activity"""
        # This is a simplified implementation
        # Real implementation would use filesystem watchers
        try:
            sensitive_files = [
                '/etc/passwd', '/etc/shadow', '/etc/sudoers',
                'C:\\Windows\\System32\\config\\SAM',
                'C:\\Windows\\System32\\config\\SYSTEM'
            ]
            
            for file_path in sensitive_files:
                if Path(file_path).exists():
                    # Check last modified time
                    stat = Path(file_path).stat()
                    if datetime.fromtimestamp(stat.st_mtime) > datetime.now() - timedelta(minutes=5):
                        self._generate_alert(
                            'FILE_ACCESS',
                            f"Recent access to sensitive file: {file_path}",
                            'High'
                        )
                        
        except Exception as e:
            self.logger.logger.debug(f"Filesystem monitoring error: {e}")
    
    def _detect_anomalies(self):
        """Detect system anomalies"""
        try:
            # CPU usage anomaly
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > 90:
                self._generate_alert(
                    'HIGH_CPU_USAGE',
                    f"High CPU usage detected: {cpu_percent}%",
                    'Medium'
                )
            
            # Memory usage anomaly
            memory = psutil.virtual_memory()
            if memory.percent > 90:
                self._generate_alert(
                    'HIGH_MEMORY_USAGE',
                    f"High memory usage detected: {memory.percent}%",
                    'Medium'
                )
            
            # Unusual network activity
            network_io = psutil.net_io_counters()
            # This would need baseline comparison for meaningful detection
            
        except Exception as e:
            self.logger.logger.debug(f"Anomaly detection error: {e}")
    
    def _check_process_against_rules(self, process_name: str):
        """Check process against detection rules"""
        for rule in self.detection_rules:
            if rule['type'] == 'process':
                if re.search(rule['pattern'], process_name, re.IGNORECASE):
                    self._generate_alert(
                        rule['name'],
                        f"{rule['description']}: {process_name}",
                        rule['severity']
                    )
    
    def _check_command_against_rules(self, command: str):
        """Check command line against detection rules"""
        for rule in self.detection_rules:
            if rule['type'] == 'process':
                if re.search(rule['pattern'], command, re.IGNORECASE):
                    self._generate_alert(
                        rule['name'],
                        f"{rule['description']}: {command}",
                        rule['severity']
                    )
    
    def _check_network_against_rules(self, connection: str):
        """Check network connection against detection rules"""
        for rule in self.detection_rules:
            if rule['type'] == 'network':
                if re.search(rule['pattern'], connection, re.IGNORECASE):
                    self._generate_alert(
                        rule['name'],
                        f"{rule['description']}: {connection}",
                        rule['severity']
                    )
    
    def _generate_alert(self, event_type: str, description: str, severity: str):
        """Generate security alert"""
        self.alert_count += 1
        
        # Log to database
        self.db.log_detection_event(
            event_type=event_type,
            source='LoggerDefender',
            description=description,
            severity=severity,
            data={'alert_id': self.alert_count}
        )
        
        # Log to logger
        self.logger.log_security_event(
            event_type, description, severity,
            alert_id=self.alert_count
        )
        
        # Check alert threshold
        if self.alert_count >= self.config.alert_threshold:
            self._escalate_alert(event_type, description, severity)
    
    def _escalate_alert(self, event_type: str, description: str, severity: str):
        """Escalate alert when threshold reached"""
        escalation_msg = f"ALERT THRESHOLD REACHED: {self.alert_count} alerts. Latest: {description}"
        
        self.logger.log_security_event(
            'ALERT_ESCALATION', escalation_msg, 'CRITICAL'
        )
        
        # Reset alert count
        self.alert_count = 0
    
    def add_detection_rule(self, rule: Dict[str, Any]) -> bool:
        """Add custom detection rule"""
        try:
            required_fields = ['name', 'type', 'pattern', 'severity', 'description']
            if all(field in rule for field in required_fields):
                self.detection_rules.append(rule)
                self.logger.logger.info(f"Added detection rule: {rule['name']}")
                return True
            else:
                self.logger.logger.error("Invalid rule format")
                return False
        except Exception as e:
            self.logger.logger.error(f"Error adding rule: {e}")
            return False
    
    def remove_detection_rule(self, rule_name: str) -> bool:
        """Remove detection rule"""
        try:
            self.detection_rules = [r for r in self.detection_rules if r['name'] != rule_name]
            self.logger.logger.info(f"Removed detection rule: {rule_name}")
            return True
        except Exception as e:
            self.logger.logger.error(f"Error removing rule: {e}")
            return False
    
    def get_detection_rules(self) -> List[Dict[str, Any]]:
        """Get all detection rules"""
        return self.detection_rules.copy()
    
    def get_recent_alerts(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get recent alerts"""
        return self.db.get_detection_events(limit=100)
    
    def analyze_logs(self, log_file: str) -> Dict[str, Any]:
        """Analyze log file for threats"""
        analysis_results = {
            'file': log_file,
            'timestamp': datetime.now().isoformat(),
            'threats_found': 0,
            'alerts': [],
            'summary': {}
        }
        
        try:
            if not Path(log_file).exists():
                analysis_results['error'] = 'Log file not found'
                return analysis_results
            
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    # Check each line against detection rules
                    for rule in self.detection_rules:
                        if re.search(rule['pattern'], line, re.IGNORECASE):
                            alert = {
                                'line_number': line_num,
                                'rule_name': rule['name'],
                                'severity': rule['severity'],
                                'description': rule['description'],
                                'matched_text': line.strip()
                            }
                            analysis_results['alerts'].append(alert)
                            analysis_results['threats_found'] += 1
            
            # Generate summary
            severity_counts = {}
            for alert in analysis_results['alerts']:
                severity = alert['severity']
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            analysis_results['summary'] = {
                'total_threats': analysis_results['threats_found'],
                'severity_breakdown': severity_counts,
                'most_common_threats': self._get_most_common_threats(analysis_results['alerts'])
            }
            
        except Exception as e:
            analysis_results['error'] = str(e)
            self.logger.logger.error(f"Log analysis error: {e}")
        
        return analysis_results
    
    def _get_most_common_threats(self, alerts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get most common threat types"""
        threat_counts = {}
        for alert in alerts:
            rule_name = alert['rule_name']
            threat_counts[rule_name] = threat_counts.get(rule_name, 0) + 1
        
        # Sort by count and return top 5
        sorted_threats = sorted(threat_counts.items(), key=lambda x: x[1], reverse=True)
        return [{'threat': threat, 'count': count} for threat, count in sorted_threats[:5]]
    
    def generate_iocs(self, alerts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate IOCs from alerts"""
        iocs = []
        
        for alert in alerts:
            matched_text = alert.get('matched_text', '')
            
            # Extract IP addresses
            ip_pattern = r'\\b(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\b'
            ips = re.findall(ip_pattern, matched_text)
            for ip in ips:
                iocs.append({
                    'type': 'ip',
                    'value': ip,
                    'description': f"IP from {alert['rule_name']}",
                    'confidence': 0.7
                })
            
            # Extract domains
            domain_pattern = r'\\b[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}\\b'
            domains = re.findall(domain_pattern, matched_text)
            for domain in domains:
                if '.' in domain and not domain.replace('.', '').isdigit():
                    iocs.append({
                        'type': 'domain',
                        'value': domain,
                        'description': f"Domain from {alert['rule_name']}",
                        'confidence': 0.6
                    })
            
            # Extract file hashes (MD5, SHA1, SHA256)
            hash_patterns = {
                'md5': r'\\b[a-fA-F0-9]{32}\\b',
                'sha1': r'\\b[a-fA-F0-9]{40}\\b',
                'sha256': r'\\b[a-fA-F0-9]{64}\\b'
            }
            
            for hash_type, pattern in hash_patterns.items():
                hashes = re.findall(pattern, matched_text)
                for hash_value in hashes:
                    iocs.append({
                        'type': hash_type,
                        'value': hash_value,
                        'description': f"{hash_type.upper()} hash from {alert['rule_name']}",
                        'confidence': 0.8
                    })
        
        # Remove duplicates
        seen = set()
        unique_iocs = []
        for ioc in iocs:
            key = (ioc['type'], ioc['value'])
            if key not in seen:
                seen.add(key)
                unique_iocs.append(ioc)
        
        return unique_iocs
    
    def threat_hunt(self, hunt_query: str) -> Dict[str, Any]:
        """Perform threat hunting based on query"""
        hunt_results = {
            'query': hunt_query,
            'timestamp': datetime.now().isoformat(),
            'matches': [],
            'summary': {}
        }
        
        try:
            # Get recent alerts
            recent_alerts = self.get_recent_alerts(hours=24)
            
            # Search through alerts
            for alert in recent_alerts:
                if re.search(hunt_query, str(alert), re.IGNORECASE):
                    hunt_results['matches'].append(alert)
            
            hunt_results['summary'] = {
                'total_matches': len(hunt_results['matches']),
                'search_period': '24 hours',
                'alerts_searched': len(recent_alerts)
            }
            
        except Exception as e:
            hunt_results['error'] = str(e)
            self.logger.logger.error(f"Threat hunting error: {e}")
        
        return hunt_results
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get current monitoring status"""
        return {
            'monitoring_active': self.monitoring_active,
            'alert_count': self.alert_count,
            'detection_rules_count': len(self.detection_rules),
            'baseline_processes': len(self.baseline_processes),
            'baseline_network': len(self.baseline_network)
        }
