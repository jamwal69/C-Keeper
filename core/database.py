"""
Database management for C-Keeper
"""

import sqlite3
import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from contextlib import contextmanager

class Database:
    """Database manager for C-Keeper"""
    
    def __init__(self, config):
        """
        Initialize database connection
        
        Args:
            config: Database configuration object
        """
        self.config = config
        # Convert relative path to absolute path
        if hasattr(config, 'path'):
            self.db_path = os.path.abspath(config.path) if config.path else 'data/ckeeper.db'
        else:
            self.db_path = os.path.abspath('data/ckeeper.db')
        self._ensure_database_exists()
        self._create_tables()
    
    def _ensure_database_exists(self):
        """Ensure database directory exists"""
        if self.db_path:
            directory = os.path.dirname(self.db_path)
            if directory:
                os.makedirs(directory, exist_ok=True)
    
    def _create_tables(self):
        """Create database tables if they don't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    mode TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    status TEXT DEFAULT 'active'
                )
            """)
            
            # Kill chain executions
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS kill_chain_executions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    target TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    stages TEXT NOT NULL,
                    status TEXT DEFAULT 'completed',
                    FOREIGN KEY (session_id) REFERENCES sessions (id)
                )
            """)
            
            # Reconnaissance results
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS recon_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    target TEXT NOT NULL,
                    scan_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    results TEXT NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES sessions (id)
                )
            """)
            
            # Vulnerabilities
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vulnerabilities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target TEXT NOT NULL,
                    service TEXT NOT NULL,
                    port INTEGER NOT NULL,
                    vulnerability TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    cve_id TEXT,
                    discovered_at TEXT NOT NULL
                )
            """)
            
            # Exploits
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS exploits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    target_service TEXT NOT NULL,
                    exploit_code TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            
            # Payloads
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS payloads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    payload_data TEXT NOT NULL,
                    encoder TEXT,
                    created_at TEXT NOT NULL
                )
            """)
            
            # Payload history
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS payload_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    payload_type TEXT NOT NULL,
                    payload_data TEXT NOT NULL,
                    created TEXT NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES sessions (id)
                )
            """)
            
            # C2 sessions
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS c2_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    target TEXT NOT NULL,
                    listener_type TEXT NOT NULL,
                    listener_config TEXT NOT NULL,
                    status TEXT DEFAULT 'active',
                    established_at TEXT NOT NULL,
                    last_checkin TEXT,
                    FOREIGN KEY (session_id) REFERENCES sessions (id)
                )
            """)
            
            # Detection events
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS detection_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    source TEXT NOT NULL,
                    description TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    data TEXT
                )
            """)
            
            # IOCs (Indicators of Compromise)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS iocs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    value TEXT NOT NULL,
                    description TEXT,
                    created_at TEXT NOT NULL,
                    confidence REAL DEFAULT 0.5
                )
            """)
            
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """Get database connection with context manager"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
        finally:
            conn.close()
    
    def log_session_start(self, session_id: str, mode: str) -> None:
        """Log session start"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sessions (id, mode, start_time)
                VALUES (?, ?, ?)
            """, (session_id, mode, datetime.now().isoformat()))
            conn.commit()
    
    def log_session_end(self, session_id: str) -> None:
        """Log session end"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE sessions 
                SET end_time = ?, status = 'completed'
                WHERE id = ?
            """, (datetime.now().isoformat(), session_id))
            conn.commit()
    
    def log_kill_chain_execution(self, execution_data: Dict[str, Any]) -> None:
        """Log kill chain execution"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO kill_chain_executions 
                (session_id, target, timestamp, stages)
                VALUES (?, ?, ?, ?)
            """, (
                execution_data['session_id'],
                execution_data['target'],
                execution_data['timestamp'],
                json.dumps(execution_data['stages'])
            ))
            conn.commit()
    
    def log_recon_results(self, session_id: str, target: str, 
                         scan_type: str, results: Dict[str, Any]) -> None:
        """Log reconnaissance results"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO recon_results 
                (session_id, target, scan_type, timestamp, results)
                VALUES (?, ?, ?, ?, ?)
            """, (
                session_id, target, scan_type,
                datetime.now().isoformat(), json.dumps(results)
            ))
            conn.commit()
    
    def add_vulnerability(self, target: str, service: str, port: int,
                         vulnerability: str, severity: str, cve_id: str = None) -> None:
        """Add vulnerability to database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO vulnerabilities 
                (target, service, port, vulnerability, severity, cve_id, discovered_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                target, service, port, vulnerability, severity, cve_id,
                datetime.now().isoformat()
            ))
            conn.commit()
    
    def get_vulnerabilities(self, target: str = None) -> List[Dict[str, Any]]:
        """Get vulnerabilities from database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if target:
                cursor.execute("""
                    SELECT * FROM vulnerabilities 
                    WHERE target = ?
                    ORDER BY discovered_at DESC
                """, (target,))
            else:
                cursor.execute("""
                    SELECT * FROM vulnerabilities 
                    ORDER BY discovered_at DESC
                """)
            
            return [dict(row) for row in cursor.fetchall()]
    
    def add_exploit(self, name: str, description: str, target_service: str,
                   exploit_code: str) -> int:
        """Add exploit to database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            cursor.execute("""
                INSERT INTO exploits 
                (name, description, target_service, exploit_code, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, description, target_service, exploit_code, now, now))
            conn.commit()
            return cursor.lastrowid
    
    def get_exploits(self, target_service: str = None) -> List[Dict[str, Any]]:
        """Get exploits from database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if target_service:
                cursor.execute("""
                    SELECT * FROM exploits 
                    WHERE target_service = ?
                    ORDER BY updated_at DESC
                """, (target_service,))
            else:
                cursor.execute("""
                    SELECT * FROM exploits 
                    ORDER BY updated_at DESC
                """)
            
            return [dict(row) for row in cursor.fetchall()]
    
    def log_detection_event(self, event_type: str, source: str, 
                          description: str, severity: str, data: Dict[str, Any] = None) -> None:
        """Log detection event"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO detection_events 
                (timestamp, event_type, source, description, severity, data)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(), event_type, source,
                description, severity, json.dumps(data) if data else None
            ))
            conn.commit()
    
    def get_detection_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent detection events"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM detection_events 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def add_ioc(self, ioc_type: str, value: str, description: str = None,
               confidence: float = 0.5) -> None:
        """Add IOC to database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO iocs 
                (type, value, description, created_at, confidence)
                VALUES (?, ?, ?, ?, ?)
            """, (
                ioc_type, value, description,
                datetime.now().isoformat(), confidence
            ))
            conn.commit()
    
    def get_iocs(self, ioc_type: str = None) -> List[Dict[str, Any]]:
        """Get IOCs from database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if ioc_type:
                cursor.execute("""
                    SELECT * FROM iocs 
                    WHERE type = ?
                    ORDER BY created_at DESC
                """, (ioc_type,))
            else:
                cursor.execute("""
                    SELECT * FROM iocs 
                    ORDER BY created_at DESC
                """)
            
            return [dict(row) for row in cursor.fetchall()]
    
    def close(self):
        """Close database connection (placeholder for cleanup)"""
        pass
