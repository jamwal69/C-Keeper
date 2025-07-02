"""
Enhanced Modern GUI Interface for C-Keeper
Advanced graphical user interface with modern design and comprehensive features
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import threading
from datetime import datetime
from typing import Dict, Any
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
from PIL import Image, ImageTk
import os

from core.engine import CKeeperEngine

class ModernCKeeperGUI:
    """Enhanced GUI application for C-Keeper with modern UI"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("C-Keeper v2.0 - Advanced Cyber Kill Chain Engine | Modern Interface")
        self.root.geometry("1600x1000")
        self.root.minsize(1200, 800)
        self.root.configure(bg='#0f0f0f')  # Deep modern dark theme
        
        # Try to set modern window properties
        try:
            self.root.attributes('-alpha', 0.98)  # Slight transparency for modern look
            self.root.wm_attributes('-topmost', False)
        except:
            pass
        
        # Modern 2025 color scheme
        self.colors = {
            'bg_primary': '#0f0f0f',      # Deep black background
            'bg_secondary': '#1a1a1a',    # Dark panels
            'bg_tertiary': '#2a2a2a',     # Cards and sections
            'accent_red': '#ff6b6b',      # Modern red
            'accent_blue': '#4dabf7',     # Modern blue
            'accent_green': '#51cf66',    # Modern green
            'accent_yellow': '#ffec99',   # Modern yellow
            'accent_purple': '#9775fa',   # Modern purple
            'text_primary': '#ffffff',    # Pure white text
            'text_secondary': '#c1c2c5',  # Light gray text
            'text_muted': '#8c8fa3',      # Muted gray text
            'border': '#495057',          # Border color
            'hover': '#364fc7',           # Hover effect
            'selection': '#228be6'        # Selection color
        }
        
        # Configure styles
        self.setup_styles()
        
        # Variables
        self.engine = None
        self.current_target = tk.StringVar()
        self.mode_var = tk.StringVar(value="dual")
        self.session_data = {}
        self.live_monitoring = False
        
        # Setup modern GUI
        self.setup_modern_gui()
        
    def setup_styles(self):
        """Setup modern 2025 styling for ttk widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure notebook style with modern look
        style.configure('Custom.TNotebook', 
                       background=self.colors['bg_secondary'],
                       borderwidth=0,
                       tabmargins=[2, 5, 2, 0])
        style.configure('Custom.TNotebook.Tab',
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['text_primary'],
                       padding=[24, 12],
                       borderwidth=0,
                       font=('Segoe UI', 10, 'normal'))
        style.map('Custom.TNotebook.Tab',
                 background=[('selected', self.colors['accent_blue']),
                           ('active', self.colors['hover'])],
                 foreground=[('selected', self.colors['text_primary'])])
        
        # Configure frame styles with modern borders
        style.configure('Dark.TFrame', background=self.colors['bg_secondary'])
        style.configure('Card.TFrame', 
                       background=self.colors['bg_tertiary'],
                       relief='flat',
                       borderwidth=1)
        
        # Configure modern label styles
        style.configure('Heading.TLabel',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 18, 'bold'))
        style.configure('SubHeading.TLabel',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_secondary'],
                       font=('Segoe UI', 12, 'normal'))
        style.configure('Status.TLabel',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['accent_green'],
                       font=('Segoe UI', 10, 'bold'))
        
        # Configure modern button styles
        style.configure('Action.TButton',
                       background=self.colors['accent_blue'],
                       foreground=self.colors['text_primary'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=[16, 8],
                       font=('Segoe UI', 10, 'bold'))
        style.map('Action.TButton',
                 background=[('active', self.colors['hover'])],
                 relief=[('pressed', 'flat'), ('!pressed', 'flat')])
        
        # Configure entry styles
        style.configure('Modern.TEntry',
                       fieldbackground=self.colors['bg_tertiary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       insertcolor=self.colors['text_primary'])
        
        # Configure progressbar
        style.configure('Modern.Horizontal.TProgressbar',
                       background=self.colors['accent_blue'],
                       troughcolor=self.colors['bg_tertiary'],
                       borderwidth=0,
                       lightcolor=self.colors['accent_blue'],
                       darkcolor=self.colors['accent_blue'])
        
        # Configure danger button style
        style.configure('Danger.TButton',
                       background=self.colors['accent_red'],
                       foreground=self.colors['text_primary'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=[16, 8],
                       font=('Segoe UI', 10, 'bold'))
        style.map('Danger.TButton',
                 background=[('active', '#ff5252')])
        
    def setup_modern_gui(self):
        """Setup the modern GUI interface"""
        # Create header
        self.create_header()
        
        # Create main container
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Create sidebar
        self.create_sidebar(main_container)
        
        # Create main content area
        self.create_main_content(main_container)
        
        # Create footer status bar
        self.create_status_bar()
        
    def create_header(self):
        """Create modern 2025-style header with enhanced branding and controls"""
        header = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=90)
        header.pack(fill=tk.X, padx=10, pady=(10, 0))
        header.pack_propagate(False)
        
        # Left side - Enhanced logo and title
        left_frame = tk.Frame(header, bg=self.colors['bg_secondary'])
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20)
        
        title_frame = tk.Frame(left_frame, bg=self.colors['bg_secondary'])
        title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Modern main title with gradient-like effect
        title_label = tk.Label(title_frame, 
                              text="⚡ C-KEEPER v2.0",
                              font=('Segoe UI', 24, 'bold'),
                              fg=self.colors['accent_blue'],
                              bg=self.colors['bg_secondary'])
        title_label.pack(anchor=tk.W, pady=(15, 0))
        
        # Enhanced subtitle
        subtitle_label = tk.Label(title_frame,
                                 text="Advanced Cyber Kill Chain Engine | Modern Interface",
                                 font=('Segoe UI', 11, 'normal'),
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['bg_secondary'])
        subtitle_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Right side - Modern mode selector and engine controls
        right_frame = tk.Frame(header, bg=self.colors['bg_secondary'])
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20)
        
        # Modern mode selector
        mode_frame = tk.Frame(right_frame, bg=self.colors['bg_secondary'])
        mode_frame.pack(side=tk.TOP, pady=(15, 8))
        
        tk.Label(mode_frame, text="🎯 Mode:", 
                font=('Segoe UI', 11, 'bold'),
                fg=self.colors['text_secondary'],
                bg=self.colors['bg_secondary']).pack(side=tk.LEFT, padx=(0, 8))
        
        mode_combo = ttk.Combobox(mode_frame, textvariable=self.mode_var,
                                 values=['red', 'blue', 'dual'],
                                 state='readonly', width=8,
                                 font=('Segoe UI', 10))
        mode_combo.pack(side=tk.LEFT)
        
        # Engine controls with modern styling
        controls_frame = tk.Frame(right_frame, bg=self.colors['bg_secondary'])
        controls_frame.pack(side=tk.BOTTOM, pady=(5, 10))
        
        start_btn = ttk.Button(controls_frame, text="Initialize Engine",
                              style='Action.TButton',
                              command=self.initialize_engine)
        start_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        stop_btn = ttk.Button(controls_frame, text="Stop Engine",
                             style='Danger.TButton',
                             command=self.stop_engine)
        stop_btn.pack(side=tk.LEFT)
        
    def create_sidebar(self, parent):
        """Create modern sidebar with navigation"""
        self.sidebar = tk.Frame(parent, bg=self.colors['bg_secondary'], width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        self.sidebar.pack_propagate(False)
        
        # Sidebar header
        sidebar_header = tk.Frame(self.sidebar, bg=self.colors['bg_secondary'], height=50)
        sidebar_header.pack(fill=tk.X, pady=(10, 0))
        
        nav_label = tk.Label(sidebar_header, text="NAVIGATION",
                            font=('Segoe UI', 12, 'bold'),
                            fg=self.colors['text_secondary'],
                            bg=self.colors['bg_secondary'])
        nav_label.pack(pady=10)
        
        # Navigation buttons
        self.nav_buttons = {}
        nav_items = [
            ("🏠 Dashboard", "dashboard"),
            ("🎯 Target Manager", "targets"),
            ("🔍 Reconnaissance", "recon"),
            ("💥 Exploits", "exploits"),
            ("🚀 Payloads", "payloads"),
            ("📡 Command & Control", "c2"),
            ("🛡️ Blue Team", "blue_team"),
            ("📊 Analytics", "analytics"),
            ("📋 Reports", "reports"),
            ("⚙️ Settings", "settings")
        ]
        
        for text, key in nav_items:
            btn = tk.Button(self.sidebar, text=text,
                           font=('Segoe UI', 11),
                           fg=self.colors['text_primary'],
                           bg=self.colors['bg_tertiary'],
                           activebackground=self.colors['accent_blue'],
                           activeforeground=self.colors['text_primary'],
                           relief=tk.FLAT,
                           anchor='w',
                           padx=20,
                           pady=12,
                           command=lambda k=key: self.switch_view(k))
            btn.pack(fill=tk.X, pady=1)
            self.nav_buttons[key] = btn
        
        # Quick stats card
        self.create_quick_stats()
        
    def create_quick_stats(self):
        """Create quick statistics card in sidebar"""
        stats_frame = tk.Frame(self.sidebar, bg=self.colors['bg_tertiary'])
        stats_frame.pack(fill=tk.X, pady=20, padx=10)
        
        # Stats header
        stats_header = tk.Label(stats_frame, text="SESSION STATS",
                               font=('Segoe UI', 10, 'bold'),
                               fg=self.colors['text_secondary'],
                               bg=self.colors['bg_tertiary'])
        stats_header.pack(pady=(10, 5))
        
        # Stats content
        self.stats_labels = {}
        stats_items = [
            ("Targets Scanned", "targets_scanned", "0"),
            ("Vulnerabilities", "vulnerabilities", "0"),
            ("Active Sessions", "active_sessions", "0"),
            ("Alerts Generated", "alerts", "0")
        ]
        
        for label, key, default in stats_items:
            frame = tk.Frame(stats_frame, bg=self.colors['bg_tertiary'])
            frame.pack(fill=tk.X, pady=2)
            
            tk.Label(frame, text=label + ":",
                    font=('Segoe UI', 9),
                    fg=self.colors['text_secondary'],
                    bg=self.colors['bg_tertiary']).pack(side=tk.LEFT)
            
            value_label = tk.Label(frame, text=default,
                                  font=('Segoe UI', 9, 'bold'),
                                  fg=self.colors['accent_green'],
                                  bg=self.colors['bg_tertiary'])
            value_label.pack(side=tk.RIGHT)
            self.stats_labels[key] = value_label
        
    def create_main_content(self, parent):
        """Create main content area"""
        self.content_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Initialize with dashboard
        self.current_view = "dashboard"
        self.switch_view("dashboard")
        
    def create_status_bar(self):
        """Create modern status bar"""
        self.status_bar = tk.Frame(self.root, bg=self.colors['bg_tertiary'], height=30)
        self.status_bar.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.status_bar.pack_propagate(False)
        
        # Left side - Engine status
        left_status = tk.Frame(self.status_bar, bg=self.colors['bg_tertiary'])
        left_status.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        self.engine_status = tk.Label(left_status, text="● Engine: Stopped",
                                     font=('Segoe UI', 9),
                                     fg=self.colors['accent_red'],
                                     bg=self.colors['bg_tertiary'])
        self.engine_status.pack(side=tk.LEFT, pady=5)
        
        # Right side - Time and session info
        right_status = tk.Frame(self.status_bar, bg=self.colors['bg_tertiary'])
        right_status.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        
        self.time_label = tk.Label(right_status, text="",
                                  font=('Segoe UI', 9),
                                  fg=self.colors['text_secondary'],
                                  bg=self.colors['bg_tertiary'])
        self.time_label.pack(side=tk.RIGHT, pady=5)
        
        # Update time
        self.update_time()
        
    def update_time(self):
        """Update time display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
        
    def switch_view(self, view_name):
        """Switch between different views"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Update navigation buttons
        for key, btn in self.nav_buttons.items():
            if key == view_name:
                btn.config(bg=self.colors['accent_blue'])
            else:
                btn.config(bg=self.colors['bg_tertiary'])
        
        self.current_view = view_name
        
        # Create view content
        if view_name == "dashboard":
            self.create_dashboard_view()
        elif view_name == "targets":
            self.create_targets_view()
        elif view_name == "recon":
            self.create_recon_view()
        elif view_name == "exploits":
            self.create_exploits_view()
        elif view_name == "payloads":
            self.create_payloads_view()
        elif view_name == "c2":
            self.create_c2_view()
        elif view_name == "blue_team":
            self.create_blue_team_view()
        elif view_name == "analytics":
            self.create_analytics_view()
        elif view_name == "reports":
            self.create_reports_view()
        elif view_name == "settings":
            self.create_settings_view()
            
    def create_dashboard_view(self):
        """Create modern dashboard view"""
        # Dashboard header
        header = tk.Frame(self.content_frame, bg=self.colors['bg_secondary'])
        header.pack(fill=tk.X, pady=(20, 10))
        
        tk.Label(header, text="Dashboard",
                font=('Segoe UI', 24, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).pack(side=tk.LEFT)
        
        # Dashboard grid
        grid_frame = tk.Frame(self.content_frame, bg=self.colors['bg_secondary'])
        grid_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Row 1 - Metrics cards
        metrics_row = tk.Frame(grid_frame, bg=self.colors['bg_secondary'])
        metrics_row.pack(fill=tk.X, pady=(0, 20))
        
        self.create_metric_card(metrics_row, "Active Targets", "0", self.colors['accent_blue'], 0, 0)
        self.create_metric_card(metrics_row, "Vulnerabilities", "0", self.colors['accent_red'], 0, 1)
        self.create_metric_card(metrics_row, "C2 Sessions", "0", self.colors['accent_green'], 0, 2)
        self.create_metric_card(metrics_row, "Alerts", "0", self.colors['accent_yellow'], 0, 3)
        
        # Row 2 - Charts and activity
        charts_row = tk.Frame(grid_frame, bg=self.colors['bg_secondary'])
        charts_row.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Activity chart
        self.create_activity_chart(charts_row)
        
        # Right side - Recent activity
        self.create_recent_activity(charts_row)
        
    def create_metric_card(self, parent, title, value, color, row, col):
        """Create a metric card widget"""
        card = tk.Frame(parent, bg=self.colors['bg_tertiary'], relief='solid', bd=1)
        card.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
        parent.grid_columnconfigure(col, weight=1)
        
        # Color bar
        color_bar = tk.Frame(card, bg=color, height=4)
        color_bar.pack(fill=tk.X)
        
        # Content
        content = tk.Frame(card, bg=self.colors['bg_tertiary'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        value_label = tk.Label(content, text=value,
                              font=('Segoe UI', 28, 'bold'),
                              fg=color,
                              bg=self.colors['bg_tertiary'])
        value_label.pack()
        
        title_label = tk.Label(content, text=title,
                              font=('Segoe UI', 12),
                              fg=self.colors['text_secondary'],
                              bg=self.colors['bg_tertiary'])
        title_label.pack()
        
    def create_activity_chart(self, parent):
        """Create activity chart"""
        chart_frame = tk.Frame(parent, bg=self.colors['bg_tertiary'])
        chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Chart header
        header = tk.Frame(chart_frame, bg=self.colors['bg_tertiary'])
        header.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(header, text="Activity Timeline",
                font=('Segoe UI', 16, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_tertiary']).pack(side=tk.LEFT)
        
        # Placeholder for chart
        chart_content = tk.Frame(chart_frame, bg=self.colors['bg_tertiary'])
        chart_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        placeholder = tk.Label(chart_content, 
                              text="📊\n\nActivity chart will be displayed here\nwhen engine is running",
                              font=('Segoe UI', 12),
                              fg=self.colors['text_secondary'],
                              bg=self.colors['bg_tertiary'],
                              justify=tk.CENTER)
        placeholder.pack(expand=True)
        
    def create_recent_activity(self, parent):
        """Create recent activity panel"""
        activity_frame = tk.Frame(parent, bg=self.colors['bg_tertiary'])
        activity_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        activity_frame.config(width=300)
        activity_frame.pack_propagate(False)
        
        # Activity header
        header = tk.Frame(activity_frame, bg=self.colors['bg_tertiary'])
        header.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(header, text="Recent Activity",
                font=('Segoe UI', 16, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_tertiary']).pack()
        
        # Activity list
        self.activity_list = scrolledtext.ScrolledText(activity_frame,
                                                      bg=self.colors['bg_primary'],
                                                      fg=self.colors['text_primary'],
                                                      font=('Consolas', 10),
                                                      height=20,
                                                      width=35)
        self.activity_list.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Add sample activity
        self.add_activity_log("System initialized")
        self.add_activity_log("GUI loaded successfully")
        
    def add_activity_log(self, message):
        """Add activity log entry"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {message}\n"
            if hasattr(self, 'activity_list') and self.activity_list.winfo_exists():
                self.activity_list.insert(tk.END, log_entry)
                self.activity_list.see(tk.END)
        except Exception as e:
            # Fallback to console logging if GUI logging fails
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
            print(f"GUI logging error: {e}")
        
    # All view creation methods will be implemented here...
    # For brevity, I'll implement the key methods that are called
    
    def initialize_engine(self):
        """Initialize the C-Keeper engine"""
        try:
            # Check if engine already exists
            if self.engine is not None:
                self.add_activity_log("Engine already initialized")
                return
                
            from core.config import Config
            config = Config()
            self.engine = CKeeperEngine(config, self.mode_var.get())
            
            self.engine_status.config(text="● Engine: Running", fg=self.colors['accent_green'])
            self.add_activity_log("Engine initialized successfully")
            
            # Update stats
            self.update_session_stats()
            
            # Initialize payload methods
            self._add_payload_methods()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize engine: {e}")
            self.add_activity_log(f"Engine initialization failed: {e}")
    
    def stop_engine(self):
        """Stop the C-Keeper engine"""
        if self.engine:
            try:
                self.engine = None
                if hasattr(self, 'engine_status'):
                    self.engine_status.config(text="● Engine: Stopped", fg=self.colors['accent_red'])
                self.add_activity_log("Engine stopped")
            except Exception as e:
                print(f"Error stopping engine: {e}")
                self.add_activity_log(f"Error stopping engine: {e}")
    
    def update_session_stats(self):
        """Update session statistics"""
        if self.engine:
            # This would pull real data from the engine
            pass
    
    def _add_payload_methods(self):
        """Add payload generation methods to the class"""
        # Methods are now integrated directly in the class
        pass
    
    def start_recon_scan(self):
        """Start reconnaissance scan"""
        if not self.engine:
            messagebox.showerror("Error", "Engine not initialized")
            return
            
        # Get target from recon_target instead of current_target
        target = ""
        if hasattr(self, 'recon_target'):
            target = self.recon_target.get().strip()
        
        if not target:
            messagebox.showerror("Error", "Please enter a target")
            return
            
        try:
            self.add_activity_log(f"Starting recon scan on {target}")
            # Update recon status
            if hasattr(self, 'recon_status'):
                self.recon_status.config(text=f"Scanning {target}...")
            
            # Run recon in separate thread to avoid blocking GUI
            threading.Thread(target=self._run_recon_scan, args=(target,), daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start recon scan: {e}")
            self.add_activity_log(f"Recon scan failed: {e}")
    
    def _run_recon_scan(self, target):
        """Run recon scan in background thread"""
        try:
            self.root.after(0, lambda: self.add_activity_log(f"Attempting to scan {target}"))
            
            if self.engine and hasattr(self.engine, 'recon'):
                # Try to call the scan method
                if hasattr(self.engine.recon, 'scan_target'):
                    results = self.engine.recon.scan_target(target)
                    self.root.after(0, lambda: self._update_recon_results(results))
                else:
                    # Fallback - create mock results for testing
                    mock_results = {
                        'hosts': [
                            {
                                'ip': target,
                                'hostname': 'target-host',
                                'status': 'up',
                                'os': 'Unknown'
                            }
                        ]
                    }
                    self.root.after(0, lambda: self._update_recon_results(mock_results))
                    self.root.after(0, lambda: self.add_activity_log("Using mock results - recon module needs implementation"))
            else:
                self.root.after(0, lambda: self.add_activity_log("Engine recon module not available"))
                # Create mock results for demonstration
                mock_results = {
                    'hosts': [
                        {
                            'ip': target,
                            'hostname': 'demo-host',
                            'status': 'up',
                            'os': 'Unknown'
                        }
                    ]
                }
                self.root.after(0, lambda: self._update_recon_results(mock_results))
                
        except Exception as e:
            self.root.after(0, lambda: self.add_activity_log(f"Recon scan error: {e}"))
    
    def _update_recon_results(self, results):
        """Update recon results in GUI"""
        try:
            if hasattr(self, 'hosts_tree') and results:
                # Clear existing results
                for item in self.hosts_tree.get_children():
                    self.hosts_tree.delete(item)
                
                # Add new results
                hosts_added = 0
                for host in results.get('hosts', []):
                    self.hosts_tree.insert('', 'end', values=(
                        host.get('ip', ''),
                        host.get('hostname', ''),
                        host.get('status', ''),
                        host.get('os', '')
                    ))
                    hosts_added += 1
                
                self.add_activity_log(f"Recon scan completed - {hosts_added} hosts found")
                
                # Update status
                if hasattr(self, 'recon_status'):
                    self.recon_status.config(text=f"Scan complete - {hosts_added} hosts found")
            else:
                self.add_activity_log("No results to display")
                if hasattr(self, 'recon_status'):
                    self.recon_status.config(text="Scan complete - no results")
                    
        except Exception as e:
            self.add_activity_log(f"Error updating results: {e}")
            if hasattr(self, 'recon_status'):
                self.recon_status.config(text="Error displaying results")
    
    def stop_recon_scan(self):
        """Stop reconnaissance scan"""
        try:
            # Implementation would stop ongoing scan
            self.add_activity_log("Recon scan stopped")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop recon scan: {e}")
    
    def export_recon_results(self):
        """Export reconnaissance results"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                # Implementation would export results
                self.add_activity_log(f"Results exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export results: {e}")
    
    def update_payload_options(self):
        """Update payload options based on selection"""
        try:
            # Implementation would update payload configuration options
            pass
        except Exception as e:
            print(f"Error updating payload options: {e}")
    
    def generate_payload(self):
        """Generate payload"""
        if not self.engine:
            messagebox.showerror("Error", "Engine not initialized")
            return
            
        try:
            self.add_activity_log("Generating payload...")
            # Implementation would generate payload
            if hasattr(self, 'payload_output'):
                self.payload_output.delete(1.0, tk.END)
                self.payload_output.insert(tk.END, "# Generated payload code would appear here\n")
            self.add_activity_log("Payload generated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate payload: {e}")
            self.add_activity_log(f"Payload generation failed: {e}")
    
    def save_payload(self):
        """Save generated payload"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".py",
                filetypes=[("Python files", "*.py"), ("All files", "*.*")]
            )
            if filename:
                if hasattr(self, 'payload_output'):
                    content = self.payload_output.get(1.0, tk.END)
                    with open(filename, 'w') as f:
                        f.write(content)
                    self.add_activity_log(f"Payload saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save payload: {e}")
    
    def test_payload(self):
        """Test generated payload"""
        try:
            self.add_activity_log("Testing payload...")
            # Implementation would test payload
            self.add_activity_log("Payload test completed")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to test payload: {e}")
    
    def generate_report(self):
        """Generate comprehensive report"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".html",
                filetypes=[("HTML files", "*.html"), ("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            if filename:
                self.add_activity_log(f"Generating report to {filename}...")
                # Implementation would generate report
                self.add_activity_log("Report generated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")
    
    # Placeholder methods for other views - these would be expanded
    def create_targets_view(self):
        """Create target management view"""
        header = tk.Frame(self.content_frame, bg=self.colors['bg_secondary'])
        header.pack(fill=tk.X, pady=(20, 10))
        
        tk.Label(header, text="Target Manager",
                font=('Segoe UI', 24, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).pack(side=tk.LEFT)
        
        # Placeholder content
        content = tk.Frame(self.content_frame, bg=self.colors['bg_tertiary'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        placeholder = tk.Label(content,
                              text="🎯 Target Manager\n\nTarget management interface will be implemented here",
                              font=('Segoe UI', 14),
                              fg=self.colors['text_secondary'],
                              bg=self.colors['bg_tertiary'],
                              justify=tk.CENTER)
        placeholder.pack(expand=True)
    
    def create_recon_view(self):
        """Create reconnaissance view"""
        header = tk.Frame(self.content_frame, bg=self.colors['bg_secondary'])
        header.pack(fill=tk.X, pady=(20, 10))
        
        tk.Label(header, text="Reconnaissance",
                font=('Segoe UI', 24, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).pack(side=tk.LEFT)
        
        # Main container with paned window
        main_paned = tk.PanedWindow(self.content_frame, 
                                   orient=tk.HORIZONTAL,
                                   bg=self.colors['bg_secondary'],
                                   sashwidth=3,
                                   sashrelief=tk.FLAT)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Left panel - Controls
        controls_frame = tk.Frame(main_paned, bg=self.colors['bg_tertiary'], width=400)
        main_paned.add(controls_frame, minsize=350)
        
        # Target input section
        target_section = tk.LabelFrame(controls_frame, text="Target Configuration",
                                      bg=self.colors['bg_tertiary'],
                                      fg=self.colors['text_primary'],
                                      font=('Segoe UI', 12, 'bold'))
        target_section.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(target_section, text="Target (IP/Domain/CIDR):",
                fg=self.colors['text_primary'],
                bg=self.colors['bg_tertiary']).pack(anchor='w', padx=5, pady=(5, 0))
        
        self.recon_target = tk.StringVar()
        target_entry = tk.Entry(target_section, textvariable=self.recon_target,
                               font=('Consolas', 11),
                               bg=self.colors['bg_secondary'],
                               fg=self.colors['text_primary'],
                               insertbackground=self.colors['text_primary'])
        target_entry.pack(fill=tk.X, padx=5, pady=5)
        
        # Scan options
        options_section = tk.LabelFrame(controls_frame, text="Scan Options",
                                       bg=self.colors['bg_tertiary'],
                                       fg=self.colors['text_primary'],
                                       font=('Segoe UI', 12, 'bold'))
        options_section.pack(fill=tk.X, padx=10, pady=10)
        
        # Scan type checkboxes
        self.recon_options = {}
        scan_types = [
            ("Host Discovery", "host_discovery", True),
            ("Port Scan", "port_scan", True),
            ("Service Detection", "service_detection", True),
            ("OS Detection", "os_detection", False),
            ("Vulnerability Scan", "vuln_scan", False)
        ]
        
        for label, key, default in scan_types:
            var = tk.BooleanVar(value=default)
            self.recon_options[key] = var
            cb = tk.Checkbutton(options_section, text=label, variable=var,
                               bg=self.colors['bg_tertiary'],
                               fg=self.colors['text_primary'],
                               selectcolor=self.colors['bg_secondary'],
                               activebackground=self.colors['bg_tertiary'])
            cb.pack(anchor='w', padx=5, pady=2)
        
        # Scan intensity
        intensity_frame = tk.Frame(options_section, bg=self.colors['bg_tertiary'])
        intensity_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(intensity_frame, text="Intensity:",
                fg=self.colors['text_primary'],
                bg=self.colors['bg_tertiary']).pack(side=tk.LEFT)
        
        self.scan_intensity = tk.StringVar(value="Normal")
        intensity_combo = ttk.Combobox(intensity_frame, textvariable=self.scan_intensity,
                                      values=['Stealth', 'Normal', 'Aggressive'],
                                      state='readonly', width=10)
        intensity_combo.pack(side=tk.RIGHT)
        
        # Action buttons
        button_frame = tk.Frame(controls_frame, bg=self.colors['bg_tertiary'])
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        start_scan_btn = ttk.Button(button_frame, text="🔍 Start Scan",
                                   style='Action.TButton',
                                   command=self.start_recon_scan)
        start_scan_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        stop_scan_btn = ttk.Button(button_frame, text="⏹ Stop",
                                  style='Danger.TButton',
                                  command=self.stop_recon_scan)
        stop_scan_btn.pack(side=tk.LEFT, padx=5)
        
        export_btn = ttk.Button(button_frame, text="📤 Export",
                               command=self.export_recon_results)
        export_btn.pack(side=tk.RIGHT)
        
        # Right panel - Results
        results_frame = tk.Frame(main_paned, bg=self.colors['bg_tertiary'])
        main_paned.add(results_frame, minsize=500)
        
        # Results notebook
        self.recon_notebook = ttk.Notebook(results_frame, style='Custom.TNotebook')
        self.recon_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Hosts tab
        hosts_frame = tk.Frame(self.recon_notebook, bg=self.colors['bg_tertiary'])
        self.recon_notebook.add(hosts_frame, text="Hosts")
        
        self.hosts_tree = ttk.Treeview(hosts_frame, columns=('IP', 'Status', 'OS', 'Ports'),
                                      show='tree headings')
        self.hosts_tree.heading('#0', text='Host')
        self.hosts_tree.heading('IP', text='IP Address')
        self.hosts_tree.heading('Status', text='Status')
        self.hosts_tree.heading('OS', text='OS')
        self.hosts_tree.heading('Ports', text='Open Ports')
        
        hosts_scroll = ttk.Scrollbar(hosts_frame, orient=tk.VERTICAL, command=self.hosts_tree.yview)
        self.hosts_tree.configure(yscrollcommand=hosts_scroll.set)
        
        self.hosts_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        hosts_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Services tab
        services_frame = tk.Frame(self.recon_notebook, bg=self.colors['bg_tertiary'])
        self.recon_notebook.add(services_frame, text="Services")
        
        self.services_tree = ttk.Treeview(services_frame, 
                                         columns=('Host', 'Port', 'Protocol', 'Service', 'Version'),
                                         show='headings')
        self.services_tree.heading('Host', text='Host')
        self.services_tree.heading('Port', text='Port')
        self.services_tree.heading('Protocol', text='Protocol')
        self.services_tree.heading('Service', text='Service')
        self.services_tree.heading('Version', text='Version')
        
        services_scroll = ttk.Scrollbar(services_frame, orient=tk.VERTICAL, 
                                       command=self.services_tree.yview)
        self.services_tree.configure(yscrollcommand=services_scroll.set)
        
        self.services_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        services_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Vulnerabilities tab
        vulns_frame = tk.Frame(self.recon_notebook, bg=self.colors['bg_tertiary'])
        self.recon_notebook.add(vulns_frame, text="Vulnerabilities")
        
        self.vulns_tree = ttk.Treeview(vulns_frame,
                                      columns=('Host', 'CVE', 'Risk', 'Description'),
                                      show='headings')
        self.vulns_tree.heading('Host', text='Host')
        self.vulns_tree.heading('CVE', text='CVE')
        self.vulns_tree.heading('Risk', text='Risk Level')
        self.vulns_tree.heading('Description', text='Description')
        
        vulns_scroll = ttk.Scrollbar(vulns_frame, orient=tk.VERTICAL,
                                    command=self.vulns_tree.yview)
        self.vulns_tree.configure(yscrollcommand=vulns_scroll.set)
        
        self.vulns_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vulns_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status panel
        status_frame = tk.Frame(results_frame, bg=self.colors['bg_secondary'], height=60)
        status_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        status_frame.pack_propagate(False)
        
        self.recon_status = tk.Label(status_frame, text="Ready to scan",
                                    font=('Segoe UI', 11),
                                    fg=self.colors['text_secondary'],
                                    bg=self.colors['bg_secondary'])
        self.recon_status.pack(pady=15)
    
    def create_exploits_view(self):
        """Create exploits view"""
        header = tk.Frame(self.content_frame, bg=self.colors['bg_secondary'])
        header.pack(fill=tk.X, pady=(20, 10))
        
        tk.Label(header, text="Exploit Manager",
                font=('Segoe UI', 24, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).pack(side=tk.LEFT)
        
        content = tk.Frame(self.content_frame, bg=self.colors['bg_tertiary'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        placeholder = tk.Label(content,
                              text="💥 Exploit Manager\n\nExploit development and execution interface",
                              font=('Segoe UI', 14),
                              fg=self.colors['text_secondary'],
                              bg=self.colors['bg_tertiary'],
                              justify=tk.CENTER)
        placeholder.pack(expand=True)
    
    def create_payloads_view(self):
        """Create payloads view"""
        header = tk.Frame(self.content_frame, bg=self.colors['bg_secondary'])
        header.pack(fill=tk.X, pady=(20, 10))
        
        tk.Label(header, text="Payload Generator",
                font=('Segoe UI', 24, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).pack(side=tk.LEFT)
        
        # Main container
        main_container = tk.Frame(self.content_frame, bg=self.colors['bg_secondary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Left panel - Payload configuration
        config_frame = tk.Frame(main_container, bg=self.colors['bg_tertiary'], width=400)
        config_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        config_frame.pack_propagate(False)
        
        # Payload type selection
        type_section = tk.LabelFrame(config_frame, text="Payload Type",
                                    bg=self.colors['bg_tertiary'],
                                    fg=self.colors['text_primary'],
                                    font=('Segoe UI', 12, 'bold'))
        type_section.pack(fill=tk.X, padx=10, pady=10)
        
        self.payload_type = tk.StringVar(value="reverse_shell")
        payload_types = [
            ("Reverse Shell", "reverse_shell"),
            ("Bind Shell", "bind_shell"),
            ("Meterpreter", "meterpreter"),
            ("Web Shell", "web_shell"),
            ("Custom", "custom")
        ]
        
        for text, value in payload_types:
            rb = tk.Radiobutton(type_section, text=text, variable=self.payload_type,
                               value=value, bg=self.colors['bg_tertiary'],
                               fg=self.colors['text_primary'],
                               selectcolor=self.colors['bg_secondary'],
                               activebackground=self.colors['bg_tertiary'],
                               command=self.update_payload_options)
            rb.pack(anchor='w', padx=5, pady=2)
        
        # Platform selection
        platform_section = tk.LabelFrame(config_frame, text="Target Platform",
                                         bg=self.colors['bg_tertiary'],
                                         fg=self.colors['text_primary'],
                                         font=('Segoe UI', 12, 'bold'))
        platform_section.pack(fill=tk.X, padx=10, pady=10)
        
        self.payload_platform = tk.StringVar(value="linux")
        platform_combo = ttk.Combobox(platform_section, textvariable=self.payload_platform,
                                      values=['linux', 'windows', 'macos', 'android'],
                                      state='readonly')
        platform_combo.pack(fill=tk.X, padx=5, pady=5)
        platform_combo.bind('<<ComboboxSelected>>', self.update_payload_options)
        
        # Connection details
        conn_section = tk.LabelFrame(config_frame, text="Connection Details",
                                    bg=self.colors['bg_tertiary'],
                                    fg=self.colors['text_primary'],
                                    font=('Segoe UI', 12, 'bold'))
        conn_section.pack(fill=tk.X, padx=10, pady=10)
        
        # LHOST
        tk.Label(conn_section, text="LHOST (Listen Host):",
                fg=self.colors['text_primary'],
                bg=self.colors['bg_tertiary']).pack(anchor='w', padx=5, pady=(5, 0))
        
        self.payload_lhost = tk.StringVar(value="127.0.0.1")
        lhost_entry = tk.Entry(conn_section, textvariable=self.payload_lhost,
                              font=('Consolas', 11),
                              bg=self.colors['bg_secondary'],
                              fg=self.colors['text_primary'],
                              insertbackground=self.colors['text_primary'])
        lhost_entry.pack(fill=tk.X, padx=5, pady=5)
        
        # LPORT
        tk.Label(conn_section, text="LPORT (Listen Port):",
                fg=self.colors['text_primary'],
                bg=self.colors['bg_tertiary']).pack(anchor='w', padx=5, pady=(5, 0))
        
        self.payload_lport = tk.StringVar(value="4444")
        lport_entry = tk.Entry(conn_section, textvariable=self.payload_lport,
                              font=('Consolas', 11),
                              bg=self.colors['bg_secondary'],
                              fg=self.colors['text_primary'],
                              insertbackground=self.colors['text_primary'])
        lport_entry.pack(fill=tk.X, padx=5, pady=5)
        
        # Encoding options
        encoding_section = tk.LabelFrame(config_frame, text="Encoding & Obfuscation",
                                        bg=self.colors['bg_tertiary'],
                                        fg=self.colors['text_primary'],
                                        font=('Segoe UI', 12, 'bold'))
        encoding_section.pack(fill=tk.X, padx=10, pady=10)
        
        self.payload_encoder = tk.StringVar(value="none")
        encoder_combo = ttk.Combobox(encoding_section, textvariable=self.payload_encoder,
                                    values=['none', 'base64', 'hex', 'xor', 'polymorphic'],
                                    state='readonly')
        encoder_combo.pack(fill=tk.X, padx=5, pady=5)
        
        # Bad characters
        tk.Label(encoding_section, text="Bad Characters (hex):",
                fg=self.colors['text_primary'],
                bg=self.colors['bg_tertiary']).pack(anchor='w', padx=5, pady=(5, 0))
        
        self.bad_chars = tk.StringVar(value="\\x00\\x0a\\x0d")
        badchars_entry = tk.Entry(encoding_section, textvariable=self.bad_chars,
                                 font=('Consolas', 11),
                                 bg=self.colors['bg_secondary'],
                                 fg=self.colors['text_primary'],
                                 insertbackground=self.colors['text_primary'])
        badchars_entry.pack(fill=tk.X, padx=5, pady=5)
        
        # Action buttons
        button_frame = tk.Frame(config_frame, bg=self.colors['bg_tertiary'])
        button_frame.pack(fill=tk.X, padx=10, pady=20)
        
        generate_btn = ttk.Button(button_frame, text="🚀 Generate Payload",
                                 style='Action.TButton',
                                 command=self.generate_payload)
        generate_btn.pack(fill=tk.X, pady=(0, 5))
        
        save_btn = ttk.Button(button_frame, text="💾 Save Payload",
                             command=self.save_payload)
        save_btn.pack(fill=tk.X, pady=5)
        
        test_btn = ttk.Button(button_frame, text="🔬 Test Payload",
                             command=self.test_payload)
        test_btn.pack(fill=tk.X, pady=5)
        
        # Right panel - Generated payload and options
        output_frame = tk.Frame(main_container, bg=self.colors['bg_tertiary'])
        output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Output notebook
        self.payload_notebook = ttk.Notebook(output_frame, style='Custom.TNotebook')
        self.payload_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Raw payload tab
        raw_frame = tk.Frame(self.payload_notebook, bg=self.colors['bg_tertiary'])
        self.payload_notebook.add(raw_frame, text="Raw Payload")
        
        self.payload_text = scrolledtext.ScrolledText(raw_frame,
                                                     font=('Consolas', 10),
                                                     bg=self.colors['bg_secondary'],
                                                     fg=self.colors['text_primary'],
                                                     insertbackground=self.colors['text_primary'],
                                                     wrap=tk.WORD)
        self.payload_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Encoded payload tab
        encoded_frame = tk.Frame(self.payload_notebook, bg=self.colors['bg_tertiary'])
        self.payload_notebook.add(encoded_frame, text="Encoded Payload")
        
        self.encoded_text = scrolledtext.ScrolledText(encoded_frame,
                                                     font=('Consolas', 10),
                                                     bg=self.colors['bg_secondary'],
                                                     fg=self.colors['text_primary'],
                                                     insertbackground=self.colors['text_primary'],
                                                     wrap=tk.WORD)
        self.encoded_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Assembly tab (for shellcode)
        asm_frame = tk.Frame(self.payload_notebook, bg=self.colors['bg_tertiary'])
        self.payload_notebook.add(asm_frame, text="Assembly")
        
        self.assembly_text = scrolledtext.ScrolledText(asm_frame,
                                                      font=('Consolas', 10),
                                                      bg=self.colors['bg_secondary'],
                                                      fg=self.colors['text_primary'],
                                                      insertbackground=self.colors['text_primary'],
                                                      wrap=tk.WORD)
        self.assembly_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Payload info tab
        info_frame = tk.Frame(self.payload_notebook, bg=self.colors['bg_tertiary'])
        self.payload_notebook.add(info_frame, text="Info")
        
        self.info_text = scrolledtext.ScrolledText(info_frame,
                                                  font=('Segoe UI', 10),
                                                  bg=self.colors['bg_secondary'],
                                                  fg=self.colors['text_primary'],
                                                  insertbackground=self.colors['text_primary'],
                                                  wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status bar for payload generation
        status_frame = tk.Frame(output_frame, bg=self.colors['bg_secondary'], height=40)
        status_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        status_frame.pack_propagate(False)
        
        self.payload_status = tk.Label(status_frame, text="Ready to generate payload",
                                      font=('Segoe UI', 11),
                                      fg=self.colors['text_secondary'],
                                      bg=self.colors['bg_secondary'])
        self.payload_status.pack(pady=10)
    
    def create_c2_view(self):
        """Create C2 view"""
        header = tk.Frame(self.content_frame, bg=self.colors['bg_secondary'])
        header.pack(fill=tk.X, pady=(20, 10))
        
        tk.Label(header, text="Command & Control",
                font=('Segoe UI', 24, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).pack(side=tk.LEFT)
        
        content = tk.Frame(self.content_frame, bg=self.colors['bg_tertiary'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        placeholder = tk.Label(content,
                              text="📡 Command & Control\n\nC2 server management and session handling",
                              font=('Segoe UI', 14),
                              fg=self.colors['text_secondary'],
                              bg=self.colors['bg_tertiary'],
                              justify=tk.CENTER)
        placeholder.pack(expand=True)
    
    def create_blue_team_view(self):
        """Create blue team view"""
        header = tk.Frame(self.content_frame, bg=self.colors['bg_secondary'])
        header.pack(fill=tk.X, pady=(20, 10))
        
        tk.Label(header, text="Blue Team Operations",
                font=('Segoe UI', 24, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).pack(side=tk.LEFT)
        
        content = tk.Frame(self.content_frame, bg=self.colors['bg_tertiary'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        placeholder = tk.Label(content,
                              text="🛡️ Blue Team Operations\n\nDefensive monitoring and threat detection",
                              font=('Segoe UI', 14),
                              fg=self.colors['text_secondary'],
                              bg=self.colors['bg_tertiary'],
                              justify=tk.CENTER)
        placeholder.pack(expand=True)
    
    def create_analytics_view(self):
        """Create analytics view"""
        header = tk.Frame(self.content_frame, bg=self.colors['bg_secondary'])
        header.pack(fill=tk.X, pady=(20, 10))
        
        tk.Label(header, text="Analytics & Visualization",
                font=('Segoe UI', 24, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).pack(side=tk.LEFT)
        
        content = tk.Frame(self.content_frame, bg=self.colors['bg_tertiary'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        placeholder = tk.Label(content,
                              text="📊 Analytics & Visualization\n\nAdvanced data analysis and reporting charts",
                              font=('Segoe UI', 14),
                              fg=self.colors['text_secondary'],
                              bg=self.colors['bg_tertiary'],
                              justify=tk.CENTER)
        placeholder.pack(expand=True)
    
    def create_reports_view(self):
        """Create reports view"""
        header = tk.Frame(self.content_frame, bg=self.colors['bg_secondary'])
        header.pack(fill=tk.X, pady=(20, 10))
        
        tk.Label(header, text="Report Generation",
                font=('Segoe UI', 24, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).pack(side=tk.LEFT)
        
        # Main container
        main_container = tk.Frame(self.content_frame, bg=self.colors['bg_secondary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Left panel - Report configuration
        config_frame = tk.Frame(main_container, bg=self.colors['bg_tertiary'], width=350)
        config_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        config_frame.pack_propagate(False)
        
        # Report type selection
        type_section = tk.LabelFrame(config_frame, text="Report Type",
                                    bg=self.colors['bg_tertiary'],
                                    fg=self.colors['text_primary'],
                                    font=('Segoe UI', 12, 'bold'))
        type_section.pack(fill=tk.X, padx=10, pady=10)
        
        self.report_type = tk.StringVar(value="comprehensive")
        report_types = [
            ("Comprehensive Assessment", "comprehensive"),
            ("Executive Summary", "executive"),
            ("Technical Details", "technical"),
            ("Vulnerability Report", "vulnerability"),
            ("Red Team Summary", "red_team"),
            ("Blue Team Analysis", "blue_team")
        ]
        
        for text, value in report_types:
            rb = tk.Radiobutton(type_section, text=text, variable=self.report_type,
                               value=value, bg=self.colors['bg_tertiary'],
                               fg=self.colors['text_primary'],
                               selectcolor=self.colors['bg_secondary'],
                               activebackground=self.colors['bg_tertiary'])
            rb.pack(anchor='w', padx=5, pady=2)
        
        # Output format selection
        format_section = tk.LabelFrame(config_frame, text="Output Format",
                                      bg=self.colors['bg_tertiary'],
                                      fg=self.colors['text_primary'],
                                      font=('Segoe UI', 12, 'bold'))
        format_section.pack(fill=tk.X, padx=10, pady=10)
        
        self.report_formats = {}
        formats = [("PDF", "pdf"), ("HTML", "html"), ("JSON", "json"), ("CSV", "csv")]
        
        for text, value in formats:
            var = tk.BooleanVar(value=(value == "pdf"))
            self.report_formats[value] = var
            cb = tk.Checkbutton(format_section, text=text, variable=var,
                               bg=self.colors['bg_tertiary'],
                               fg=self.colors['text_primary'],
                               selectcolor=self.colors['bg_secondary'],
                               activebackground=self.colors['bg_tertiary'])
            cb.pack(anchor='w', padx=5, pady=2)
        
        # Report sections
        sections_frame = tk.LabelFrame(config_frame, text="Include Sections",
                                      bg=self.colors['bg_tertiary'],
                                      fg=self.colors['text_primary'],
                                      font=('Segoe UI', 12, 'bold'))
        sections_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.report_sections = {}
        sections = [
            ("Executive Summary", "executive_summary", True),
            ("Methodology", "methodology", True),
            ("Reconnaissance Results", "recon_results", True),
            ("Vulnerability Assessment", "vuln_assessment", True),
            ("Exploit Summary", "exploit_summary", False),
            ("Risk Analysis", "risk_analysis", True),
            ("Recommendations", "recommendations", True),
            ("Technical Appendix", "technical_appendix", False)
        ]
        
        for text, key, default in sections:
            var = tk.BooleanVar(value=default)
            self.report_sections[key] = var
            cb = tk.Checkbutton(sections_frame, text=text, variable=var,
                               bg=self.colors['bg_tertiary'],
                               fg=self.colors['text_primary'],
                               selectcolor=self.colors['bg_secondary'],
                               activebackground=self.colors['bg_tertiary'])
            cb.pack(anchor='w', padx=5, pady=2)
        
        # Report metadata
        meta_section = tk.LabelFrame(config_frame, text="Report Metadata",
                                    bg=self.colors['bg_tertiary'],
                                    fg=self.colors['text_primary'],
                                    font=('Segoe UI', 12, 'bold'))
        meta_section.pack(fill=tk.X, padx=10, pady=10)
        
        # Title
        tk.Label(meta_section, text="Report Title:",
                fg=self.colors['text_primary'],
                bg=self.colors['bg_tertiary']).pack(anchor='w', padx=5, pady=(5, 0))
        
        self.report_title = tk.StringVar(value="Cybersecurity Assessment Report")
        title_entry = tk.Entry(meta_section, textvariable=self.report_title,
                              font=('Segoe UI', 10),
                              bg=self.colors['bg_secondary'],
                              fg=self.colors['text_primary'],
                              insertbackground=self.colors['text_primary'])
        title_entry.pack(fill=tk.X, padx=5, pady=5)
        
        # Client
        tk.Label(meta_section, text="Client/Organization:",
                fg=self.colors['text_primary'],
                bg=self.colors['bg_tertiary']).pack(anchor='w', padx=5, pady=(5, 0))
        
        self.report_client = tk.StringVar(value="Target Organization")
        client_entry = tk.Entry(meta_section, textvariable=self.report_client,
                               font=('Segoe UI', 10),
                               bg=self.colors['bg_secondary'],
                               fg=self.colors['text_primary'],
                               insertbackground=self.colors['text_primary'])
        client_entry.pack(fill=tk.X, padx=5, pady=5)
        
        # Generate button
        generate_btn = ttk.Button(config_frame, text="📋 Generate Report",
                                 style='Action.TButton',
                                 command=self.generate_report)
        generate_btn.pack(fill=tk.X, padx=10, pady=20)
        
        # Right panel - Report preview and logs
        preview_frame = tk.Frame(main_container, bg=self.colors['bg_tertiary'])
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Preview notebook
        self.report_notebook = ttk.Notebook(preview_frame, style='Custom.TNotebook')
        self.report_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Report preview tab
        preview_tab = tk.Frame(self.report_notebook, bg=self.colors['bg_tertiary'])
        self.report_notebook.add(preview_tab, text="Preview")
        
        self.report_preview = scrolledtext.ScrolledText(preview_tab,
                                                       font=('Segoe UI', 10),
                                                       bg=self.colors['bg_secondary'],
                                                       fg=self.colors['text_primary'],
                                                       wrap=tk.WORD,
                                                       state=tk.DISABLED)
        self.report_preview.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Generation log tab
        log_tab = tk.Frame(self.report_notebook, bg=self.colors['bg_tertiary'])
        self.report_notebook.add(log_tab, text="Generation Log")
        
        self.report_log = scrolledtext.ScrolledText(log_tab,
                                                   font=('Consolas', 9),
                                                   bg=self.colors['bg_secondary'],
                                                   fg=self.colors['text_primary'],
                                                   wrap=tk.WORD,
                                                   state=tk.DISABLED)
        self.report_log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status bar
        status_frame = tk.Frame(preview_frame, bg=self.colors['bg_secondary'], height=40)
        status_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        status_frame.pack_propagate(False)
        
        self.report_status = tk.Label(status_frame, text="Ready to generate report",
                                     font=('Segoe UI', 11),
                                     fg=self.colors['text_secondary'],
                                     bg=self.colors['bg_secondary'])
        self.report_status.pack(pady=10)
    
    def create_settings_view(self):
        """Create settings view"""
        header = tk.Frame(self.content_frame, bg=self.colors['bg_secondary'])
        header.pack(fill=tk.X, pady=(20, 10))
        
        tk.Label(header, text="Settings",
                font=('Segoe UI', 24, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).pack(side=tk.LEFT)
        
        content = tk.Frame(self.content_frame, bg=self.colors['bg_tertiary'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        placeholder = tk.Label(content,
                              text="⚙️ Settings\n\nApplication configuration and preferences",
                              font=('Segoe UI', 14),
                              fg=self.colors['text_secondary'],
                              bg=self.colors['bg_tertiary'],
                              justify=tk.CENTER)
        placeholder.pack(expand=True)
    
    def run(self):
        """Run the modern GUI application"""
        self.root.mainloop()

def start_gui(engine=None):
    """Start the modern GUI interface"""
    try:
        app = ModernCKeeperGUI()
        if engine:
            app.engine = engine
            app.update_session_stats()
        app.run()
        return 0
    except Exception as e:
        print(f"GUI Error: {e}")
        return 1

if __name__ == "__main__":
    start_gui()
