"""
Configuration management for C-Keeper
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any

class Config:
    """Configuration manager for C-Keeper"""
    
    def __init__(self, config_path: str = None):
        """
        Initialize configuration
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path or 'config/settings.yaml'
        self.config = self._load_config()
        
        # Create configuration sections
        self.database = DatabaseConfig(self.config.get('database', {}))
        self.recon = ReconConfig(self.config.get('recon', {}))
        self.exploit_builder = ExploitBuilderConfig(self.config.get('exploit_builder', {}))
        self.payload_generator = PayloadGeneratorConfig(self.config.get('payload_generator', {}))
        self.delivery_engine = DeliveryEngineConfig(self.config.get('delivery_engine', {}))
        self.c2_handler = C2HandlerConfig(self.config.get('c2_handler', {}))
        self.exploit_runner = ExploitRunnerConfig(self.config.get('exploit_runner', {}))
        self.logger_defender = LoggerDefenderConfig(self.config.get('logger_defender', {}))
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return yaml.safe_load(f) or {}
            else:
                # Return default configuration
                return self._get_default_config()
        except Exception as e:
            print(f"Error loading config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'database': {
                'type': 'sqlite',
                'path': 'data/ckeeper.db'
            },
            'recon': {
                'timeout': 30,
                'threads': 10,
                'port_range': '1-1000',
                'nmap_options': '-sS -sV'
            },
            'exploit_builder': {
                'exploit_db_path': 'data/exploits',
                'custom_exploits_path': 'data/custom_exploits'
            },
            'payload_generator': {
                'payloads_path': 'data/payloads',
                'encoders': ['x86/shikata_ga_nai', 'x64/xor'],
                'formats': ['exe', 'dll', 'elf', 'raw']
            },
            'delivery_engine': {
                'methods': ['http', 'ftp', 'email', 'smb'],
                'web_server_port': 8080,
                'ftp_server_port': 21
            },
            'c2_handler': {
                'listeners': {
                    'http': {'port': 443, 'ssl': True},
                    'tcp': {'port': 4444},
                    'dns': {'domain': 'example.com'}
                }
            },
            'exploit_runner': {
                'timeout': 60,
                'retries': 3,
                'cleanup': True
            },
            'logger_defender': {
                'log_level': 'INFO',
                'log_file': 'logs/defender.log',
                'detection_rules': 'data/rules',
                'alert_threshold': 5
            }
        }
    
    def save_config(self):
        """Save configuration to file"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False)
        except Exception as e:
            print(f"Error saving config: {e}")

class DatabaseConfig:
    """Database configuration"""
    def __init__(self, config: Dict[str, Any]):
        self.type = config.get('type', 'sqlite')
        self.path = config.get('path', 'data/ckeeper.db')
        self.host = config.get('host', 'localhost')
        self.port = config.get('port', 5432)
        self.username = config.get('username', '')
        self.password = config.get('password', '')
        self.database = config.get('database', 'ckeeper')

class ReconConfig:
    """Reconnaissance configuration"""
    def __init__(self, config: Dict[str, Any]):
        self.timeout = config.get('timeout', 30)
        self.threads = config.get('threads', 10)
        self.port_range = config.get('port_range', '1-1000')
        self.nmap_options = config.get('nmap_options', '-sS -sV')
        self.wordlists = config.get('wordlists', 'data/wordlists')

class ExploitBuilderConfig:
    """Exploit builder configuration"""
    def __init__(self, config: Dict[str, Any]):
        self.exploit_db_path = config.get('exploit_db_path', 'data/exploits')
        self.custom_exploits_path = config.get('custom_exploits_path', 'data/custom_exploits')
        self.templates_path = config.get('templates_path', 'data/templates')

class PayloadGeneratorConfig:
    """Payload generator configuration"""
    def __init__(self, config: Dict[str, Any]):
        self.payloads_path = config.get('payloads_path', 'data/payloads')
        self.encoders = config.get('encoders', ['x86/shikata_ga_nai', 'x64/xor'])
        self.formats = config.get('formats', ['exe', 'dll', 'elf', 'raw'])
        self.obfuscation = config.get('obfuscation', True)

class DeliveryEngineConfig:
    """Delivery engine configuration"""
    def __init__(self, config: Dict[str, Any]):
        self.methods = config.get('methods', ['http', 'ftp', 'email', 'smb'])
        self.web_server_port = config.get('web_server_port', 8080)
        self.ftp_server_port = config.get('ftp_server_port', 21)
        self.email_server = config.get('email_server', {})

class C2HandlerConfig:
    """C2 handler configuration"""
    def __init__(self, config: Dict[str, Any]):
        self.listeners = config.get('listeners', {
            'http': {'port': 443, 'ssl': True},
            'tcp': {'port': 4444},
            'dns': {'domain': 'example.com'}
        })
        self.encryption = config.get('encryption', True)
        self.obfuscation = config.get('obfuscation', True)

class ExploitRunnerConfig:
    """Exploit runner configuration"""
    def __init__(self, config: Dict[str, Any]):
        self.timeout = config.get('timeout', 60)
        self.retries = config.get('retries', 3)
        self.cleanup = config.get('cleanup', True)
        self.verify_success = config.get('verify_success', True)

class LoggerDefenderConfig:
    """Logger/Defender configuration"""
    def __init__(self, config: Dict[str, Any]):
        self.log_level = config.get('log_level', 'INFO')
        self.log_file = config.get('log_file', 'logs/defender.log')
        self.detection_rules = config.get('detection_rules', 'data/rules')
        self.alert_threshold = config.get('alert_threshold', 5)
        self.monitoring_enabled = config.get('monitoring_enabled', True)
