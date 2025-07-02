"""
Core Engine for C-Keeper
Manages all modules and provides central coordination
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

from modules.recon import ReconModule
from modules.exploit_builder import ExploitBuilderModule
from modules.payload_generator import PayloadGeneratorModule
from modules.delivery_engine import DeliveryEngineModule
from modules.c2_handler import C2HandlerModule
from modules.exploit_runner import ExploitRunnerModule
from modules.logger_defender import LoggerDefenderModule
from core.database import Database
from core.config import Config

class CKeeperEngine:
    """
    Main engine class that coordinates all modules
    """
    
    def __init__(self, config: Config, mode: str = 'dual'):
        """
        Initialize the C-Keeper engine
        
        Args:
            config: Configuration object
            mode: Operation mode ('red', 'blue', 'dual')
        """
        self.config = config
        self.mode = mode
        self.logger = logging.getLogger(__name__)
        self.session_id = self._generate_session_id()
        
        # Initialize database
        self.db = Database(config.database)
        
        # Initialize modules based on mode
        self.modules = {}
        self._initialize_modules()
        
        self.logger.info(f"C-Keeper engine initialized in {mode} mode")
        
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def _initialize_modules(self):
        """Initialize modules based on operation mode"""
        if self.mode in ['red', 'dual']:
            self._initialize_red_modules()
        
        if self.mode in ['blue', 'dual']:
            self._initialize_blue_modules()
        
        # Always initialize logger/defender for monitoring
        self.modules['logger_defender'] = LoggerDefenderModule(
            self.config.logger_defender, self.db
        )
    
    def _initialize_red_modules(self):
        """Initialize red team modules"""
        self.modules['recon'] = ReconModule(
            self.config.recon, self.db
        )
        self.modules['exploit_builder'] = ExploitBuilderModule(
            self.config.exploit_builder, self.db
        )
        self.modules['payload_generator'] = PayloadGeneratorModule(
            self.config.payload_generator, self.db
        )
        self.modules['delivery_engine'] = DeliveryEngineModule(
            self.config.delivery_engine, self.db
        )
        self.modules['c2_handler'] = C2HandlerModule(
            self.config.c2_handler, self.db
        )
        self.modules['exploit_runner'] = ExploitRunnerModule(
            self.config.exploit_runner, self.db
        )
    
    def _initialize_blue_modules(self):
        """Initialize blue team modules"""
        # Blue team modules can reuse some red team modules for detection
        if 'recon' not in self.modules:
            self.modules['recon'] = ReconModule(
                self.config.recon, self.db, defensive_mode=True
            )
    
    def get_module(self, module_name: str):
        """Get a specific module by name"""
        return self.modules.get(module_name)
    
    def list_modules(self) -> list:
        """Get list of available modules"""
        return list(self.modules.keys())
    
    def start_monitoring(self):
        """Start blue team monitoring"""
        if 'logger_defender' in self.modules:
            self.modules['logger_defender'].start_monitoring()
            self.logger.info("Started defensive monitoring")
    
    def stop_monitoring(self):
        """Stop blue team monitoring"""
        if 'logger_defender' in self.modules:
            self.modules['logger_defender'].stop_monitoring()
            self.logger.info("Stopped defensive monitoring")
    
    def execute_kill_chain(self, target: str, chain_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a complete kill chain against a target
        
        Args:
            target: Target specification (IP, domain, etc.)
            chain_config: Configuration for kill chain execution
            
        Returns:
            Results from kill chain execution
        """
        if self.mode == 'blue':
            raise ValueError("Kill chain execution not available in blue mode")
        
        results = {
            'session_id': self.session_id,
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'stages': {}
        }
        
        try:
            # Stage 1: Reconnaissance
            if chain_config.get('run_recon', True):
                self.logger.info(f"Starting reconnaissance on {target}")
                recon_results = self.modules['recon'].scan_target(target)
                results['stages']['reconnaissance'] = recon_results
            
            # Stage 2: Weaponization (Exploit Building)
            if chain_config.get('run_weaponization', True) and 'reconnaissance' in results['stages']:
                self.logger.info("Building exploits based on reconnaissance")
                vulns = results['stages']['reconnaissance'].get('vulnerabilities', [])
                exploit_results = self.modules['exploit_builder'].build_exploits(vulns)
                results['stages']['weaponization'] = exploit_results
            
            # Stage 3: Delivery
            if chain_config.get('run_delivery', True) and 'weaponization' in results['stages']:
                self.logger.info("Preparing payload delivery")
                exploits = results['stages']['weaponization'].get('exploits', [])
                delivery_results = self.modules['delivery_engine'].prepare_delivery(
                    target, exploits
                )
                results['stages']['delivery'] = delivery_results
            
            # Stage 4: Exploitation
            if chain_config.get('run_exploitation', True) and 'delivery' in results['stages']:
                self.logger.info("Executing exploits")
                delivery_data = results['stages']['delivery']
                exploit_results = self.modules['exploit_runner'].execute_exploits(
                    target, delivery_data
                )
                results['stages']['exploitation'] = exploit_results
            
            # Stage 5: Installation (C2)
            if chain_config.get('run_installation', True) and 'exploitation' in results['stages']:
                self.logger.info("Setting up command and control")
                exploitation_data = results['stages']['exploitation']
                c2_results = self.modules['c2_handler'].establish_c2(
                    target, exploitation_data
                )
                results['stages']['installation'] = c2_results
            
            # Log the complete kill chain execution
            self.db.log_kill_chain_execution(results)
            
        except Exception as e:
            self.logger.error(f"Kill chain execution failed: {e}")
            results['error'] = str(e)
        
        return results
    
    def get_session_info(self) -> Dict[str, Any]:
        """Get current session information"""
        return {
            'session_id': self.session_id,
            'mode': self.mode,
            'modules': self.list_modules(),
            'start_time': datetime.now().isoformat()
        }
    
    def shutdown(self):
        """Shutdown the engine and cleanup resources"""
        self.logger.info("Shutting down C-Keeper engine")
        
        # Stop monitoring if running
        self.stop_monitoring()
        
        # Shutdown all modules
        for module_name, module in self.modules.items():
            try:
                if hasattr(module, 'shutdown'):
                    module.shutdown()
            except Exception as e:
                self.logger.error(f"Error shutting down {module_name}: {e}")
        
        # Close database connection
        if hasattr(self.db, 'close'):
            self.db.close()
        
        self.logger.info("C-Keeper engine shutdown complete")
