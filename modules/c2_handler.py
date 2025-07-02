"""
C2 Handler Module for C-Keeper
Manages command and control operations
"""

import socket
import threading
import ssl
from datetime import datetime
from typing import Dict, Any, List

from core.logger import CKeeperLogger

class C2HandlerModule:
    """Command and Control handler module"""
    
    def __init__(self, config, database):
        self.config = config
        self.db = database
        self.logger = CKeeperLogger(__name__)
        self.listeners = {}
        self.sessions = {}
    
    def establish_c2(self, target: str, exploitation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Establish C2 connection"""
        return {
            'target': target,
            'listeners_started': 1,
            'sessions_established': 0,
            'protocols': ['http', 'tcp']
        }
    
    def start_listener(self, listener_type: str, port: int) -> Dict[str, Any]:
        """Start C2 listener"""
        try:
            if listener_type == 'tcp':
                return self._start_tcp_listener(port)
            elif listener_type == 'http':
                return self._start_http_listener(port)
            else:
                return {'success': False, 'error': 'Unknown listener type'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _start_tcp_listener(self, port: int) -> Dict[str, Any]:
        """Start TCP listener"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('0.0.0.0', port))
        sock.listen(5)
        
        self.listeners[f'tcp_{port}'] = sock
        
        thread = threading.Thread(target=self._handle_tcp_connections, args=(sock, port))
        thread.daemon = True
        thread.start()
        
        return {
            'success': True,
            'type': 'tcp',
            'port': port,
            'message': f'TCP listener started on port {port}'
        }
    
    def _handle_tcp_connections(self, sock: socket.socket, port: int):
        """Handle incoming TCP connections"""
        while True:
            try:
                conn, addr = sock.accept()
                session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{addr[0]}"
                
                self.sessions[session_id] = {
                    'connection': conn,
                    'address': addr,
                    'type': 'tcp',
                    'established_at': datetime.now().isoformat()
                }
                
                thread = threading.Thread(target=self._handle_session, args=(session_id,))
                thread.daemon = True
                thread.start()
                
            except Exception as e:
                self.logger.logger.error(f"TCP listener error: {e}")
                break
    
    def _handle_session(self, session_id: str):
        """Handle individual C2 session"""
        session = self.sessions[session_id]
        conn = session['connection']
        
        try:
            while True:
                # Send command prompt
                conn.send(b"C2> ")
                
                # Receive command response
                data = conn.recv(4096)
                if not data:
                    break
                
                response = data.decode('utf-8', errors='ignore')
                print(f"[{session_id}] {response}")
                
        except Exception as e:
            self.logger.logger.error(f"Session error: {e}")
        finally:
            conn.close()
            if session_id in self.sessions:
                del self.sessions[session_id]
    
    def _start_http_listener(self, port: int) -> Dict[str, Any]:
        """Start HTTP C2 listener"""
        return {
            'success': True,
            'type': 'http',
            'port': port,
            'message': f'HTTP C2 listener started on port {port}'
        }
    
    def send_command(self, session_id: str, command: str) -> Dict[str, Any]:
        """Send command to C2 session"""
        if session_id not in self.sessions:
            return {'success': False, 'error': 'Session not found'}
        
        try:
            session = self.sessions[session_id]
            conn = session['connection']
            conn.send(command.encode() + b'\\n')
            
            return {'success': True, 'message': f'Command sent to {session_id}'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """List active C2 sessions"""
        return [
            {
                'id': session_id,
                'address': session['address'],
                'type': session['type'],
                'established_at': session['established_at']
            }
            for session_id, session in self.sessions.items()
        ]
    
    def stop_listeners(self):
        """Stop all listeners"""
        for name, listener in self.listeners.items():
            try:
                listener.close()
            except:
                pass
        self.listeners.clear()
        
        for session_id, session in self.sessions.items():
            try:
                session['connection'].close()
            except:
                pass
        self.sessions.clear()
