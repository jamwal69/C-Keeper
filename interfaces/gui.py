"""
Enhanced GUI Interface for C-Keeper
Modern graphical user interface with advanced features
"""

# Use the working modern GUI with enhanced 2025 styling
try:
    from interfaces.gui_modern import ModernCKeeperGUI
    from interfaces.gui_modern import start_gui as start_modern_gui
    GUI_TYPE = "modern"
    print("🎨 Loading Enhanced Modern GUI Interface...")
except ImportError as e:
    print(f"Modern GUI dependencies missing: {e}")
    print("Falling back to basic GUI...")
    GUI_TYPE = "basic"

if GUI_TYPE == "basic":
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog, scrolledtext
    import json
    import threading
    from datetime import datetime
    from typing import Dict, Any
    import os

    from core.engine import CKeeperEngine

    class CKeeperGUI:
        """Basic GUI application for C-Keeper"""
        
        def __init__(self):
            self.root = tk.Tk()
            self.root.title("C-Keeper - Cyber Kill Chain Engine")
            self.root.geometry("1200x800")
            
            # Variables
            self.engine = None
            self.current_target = tk.StringVar()
            self.mode_var = tk.StringVar(value="dual")
            
            # Setup GUI
            self.setup_gui()
            
        def setup_gui(self):
            """Setup the GUI interface"""
            # Create menu
            self.create_menu()
            
            # Create notebook for tabs
            self.notebook = ttk.Notebook(self.root)
            self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Create tabs
            self.create_overview_tab()
            self.create_recon_tab()
            self.create_exploit_tab()
            self.create_payload_tab()
            self.create_c2_tab()
            self.create_monitor_tab()
            self.create_logs_tab()
            
            # Create status bar
            self.create_status_bar()
        
        def create_menu(self):
            """Create menu bar"""
            menubar = tk.Menu(self.root)
            self.root.config(menu=menubar)
            
            # File menu
            file_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="File", menu=file_menu)
            file_menu.add_command(label="Initialize Engine", command=self.initialize_engine)
            file_menu.add_separator()
            file_menu.add_command(label="Save Session", command=self.save_session)
            file_menu.add_command(label="Load Session", command=self.load_session)
            file_menu.add_separator()
            file_menu.add_command(label="Export Report", command=self.export_report)
            file_menu.add_separator()
            file_menu.add_command(label="Exit", command=self.root.quit)
            
            # Tools menu
            tools_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Tools", menu=tools_menu)
            tools_menu.add_command(label="Kill Chain Executor", command=self.open_killchain_window)
            tools_menu.add_command(label="Threat Hunter", command=self.open_threat_hunter)
            
            # Help menu
            help_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Help", menu=help_menu)
            help_menu.add_command(label="About", command=self.show_about)
        
        def create_overview_tab(self):
            """Create overview tab"""
            overview_frame = ttk.Frame(self.notebook)
            self.notebook.add(overview_frame, text="Overview")
            
            # Engine status
            status_frame = ttk.LabelFrame(overview_frame, text="Engine Status")
            status_frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Label(status_frame, text="Mode:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
            mode_combo = ttk.Combobox(status_frame, textvariable=self.mode_var, 
                                      values=["red", "blue", "dual"], state="readonly")
            mode_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
            
            ttk.Button(status_frame, text="Initialize Engine", 
                      command=self.initialize_engine).grid(row=0, column=2, padx=5, pady=2)
            
            # Target configuration
            target_frame = ttk.LabelFrame(overview_frame, text="Target Configuration")
            target_frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Label(target_frame, text="Target:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
            ttk.Entry(target_frame, textvariable=self.current_target, width=30).grid(row=0, column=1, padx=5, pady=2)
            ttk.Button(target_frame, text="Set Target", 
                      command=self.set_target).grid(row=0, column=2, padx=5, pady=2)
            
            # Quick actions
            actions_frame = ttk.LabelFrame(overview_frame, text="Quick Actions")
            actions_frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Button(actions_frame, text="Quick Recon", 
                      command=self.quick_recon).pack(side=tk.LEFT, padx=5, pady=5)
            ttk.Button(actions_frame, text="Start Monitoring", 
                      command=self.start_monitoring).pack(side=tk.LEFT, padx=5, pady=5)
            ttk.Button(actions_frame, text="Run Kill Chain", 
                      command=self.run_killchain).pack(side=tk.LEFT, padx=5, pady=5)
            
            # Session info
            self.session_info = scrolledtext.ScrolledText(overview_frame, height=15)
            self.session_info.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        def create_recon_tab(self):
            """Create reconnaissance tab"""
            recon_frame = ttk.Frame(self.notebook)
            self.notebook.add(recon_frame, text="Reconnaissance")
            
            # Controls
            controls_frame = ttk.Frame(recon_frame)
            controls_frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Button(controls_frame, text="Scan Target", 
                      command=self.scan_target).pack(side=tk.LEFT, padx=5)
            ttk.Button(controls_frame, text="Port Scan", 
                      command=self.port_scan).pack(side=tk.LEFT, padx=5)
            ttk.Button(controls_frame, text="Clear Results", 
                      command=self.clear_recon_results).pack(side=tk.LEFT, padx=5)
            
            # Results
            self.recon_results = scrolledtext.ScrolledText(recon_frame)
            self.recon_results.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        def create_exploit_tab(self):
            """Create exploitation tab"""
            exploit_frame = ttk.Frame(self.notebook)
            self.notebook.add(exploit_frame, text="Exploitation")
            
            # Controls
            controls_frame = ttk.Frame(exploit_frame)
            controls_frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Button(controls_frame, text="Build Exploits", 
                      command=self.build_exploits).pack(side=tk.LEFT, padx=5)
            ttk.Button(controls_frame, text="Run Selected", 
                      command=self.run_selected_exploit).pack(side=tk.LEFT, padx=5)
            
            # Exploit list
            self.exploit_tree = ttk.Treeview(exploit_frame, columns=("Type", "Target", "Reliability"), show="tree headings")
            self.exploit_tree.heading("#0", text="Name")
            self.exploit_tree.heading("Type", text="Type")
            self.exploit_tree.heading("Target", text="Target")
            self.exploit_tree.heading("Reliability", text="Reliability")
            self.exploit_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        def create_payload_tab(self):
            """Create payload tab"""
            payload_frame = ttk.Frame(self.notebook)
            self.notebook.add(payload_frame, text="Payloads")
            
            # Payload configuration
            config_frame = ttk.LabelFrame(payload_frame, text="Payload Configuration")
            config_frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Label(config_frame, text="Type:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
            self.payload_type = ttk.Combobox(config_frame, values=["reverse_shell", "bind_shell", "meterpreter", "exec"])
            self.payload_type.grid(row=0, column=1, padx=5, pady=2)
            
            ttk.Label(config_frame, text="Platform:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
            self.payload_platform = ttk.Combobox(config_frame, values=["windows", "linux", "macos", "web"])
            self.payload_platform.grid(row=0, column=3, padx=5, pady=2)
            
            ttk.Label(config_frame, text="LHOST:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
            self.lhost = ttk.Entry(config_frame)
            self.lhost.grid(row=1, column=1, padx=5, pady=2)
            self.lhost.insert(0, "127.0.0.1")
            
            ttk.Label(config_frame, text="LPORT:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
            self.lport = ttk.Entry(config_frame)
            self.lport.grid(row=1, column=3, padx=5, pady=2)
            self.lport.insert(0, "4444")
            
            ttk.Button(config_frame, text="Generate Payload", 
                      command=self.generate_payload).grid(row=2, column=0, columnspan=4, pady=10)
            
            # Payload results
            self.payload_results = scrolledtext.ScrolledText(payload_frame)
            self.payload_results.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        def create_c2_tab(self):
            """Create C2 tab"""
            c2_frame = ttk.Frame(self.notebook)
            self.notebook.add(c2_frame, text="Command & Control")
            
            # Listener controls
            listener_frame = ttk.LabelFrame(c2_frame, text="Listeners")
            listener_frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Label(listener_frame, text="Type:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
            self.listener_type = ttk.Combobox(listener_frame, values=["tcp", "http", "https"])
            self.listener_type.grid(row=0, column=1, padx=5, pady=2)
            
            ttk.Label(listener_frame, text="Port:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
            self.listener_port = ttk.Entry(listener_frame, width=10)
            self.listener_port.grid(row=0, column=3, padx=5, pady=2)
            self.listener_port.insert(0, "4444")
            
            ttk.Button(listener_frame, text="Start Listener", 
                      command=self.start_listener).grid(row=0, column=4, padx=5, pady=2)
            
            # Sessions
            sessions_frame = ttk.LabelFrame(c2_frame, text="Active Sessions")
            sessions_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            self.sessions_tree = ttk.Treeview(sessions_frame, columns=("Address", "Type", "Time"), show="tree headings")
            self.sessions_tree.heading("#0", text="Session ID")
            self.sessions_tree.heading("Address", text="Address")
            self.sessions_tree.heading("Type", text="Type")
            self.sessions_tree.heading("Time", text="Established")
            self.sessions_tree.pack(fill=tk.BOTH, expand=True)
        
        def create_monitor_tab(self):
            """Create monitoring tab"""
            monitor_frame = ttk.Frame(self.notebook)
            self.notebook.add(monitor_frame, text="Monitoring")
            
            # Controls
            controls_frame = ttk.Frame(monitor_frame)
            controls_frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Button(controls_frame, text="Start Monitoring", 
                      command=self.start_monitoring).pack(side=tk.LEFT, padx=5)
            ttk.Button(controls_frame, text="Stop Monitoring", 
                      command=self.stop_monitoring).pack(side=tk.LEFT, padx=5)
            ttk.Button(controls_frame, text="Refresh Alerts", 
                      command=self.refresh_alerts).pack(side=tk.LEFT, padx=5)
            
            # Alerts
            alerts_frame = ttk.LabelFrame(monitor_frame, text="Recent Alerts")
            alerts_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            self.alerts_tree = ttk.Treeview(alerts_frame, columns=("Time", "Type", "Severity"), show="tree headings")
            self.alerts_tree.heading("#0", text="Description")
            self.alerts_tree.heading("Time", text="Time")
            self.alerts_tree.heading("Type", text="Type")
            self.alerts_tree.heading("Severity", text="Severity")
            self.alerts_tree.pack(fill=tk.BOTH, expand=True)
        
        def create_logs_tab(self):
            """Create logs tab"""
            logs_frame = ttk.Frame(self.notebook)
            self.notebook.add(logs_frame, text="Logs")
            
            # Controls
            controls_frame = ttk.Frame(logs_frame)
            controls_frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Button(controls_frame, text="Refresh Logs", 
                      command=self.refresh_logs).pack(side=tk.LEFT, padx=5)
            ttk.Button(controls_frame, text="Clear Logs", 
                      command=self.clear_logs).pack(side=tk.LEFT, padx=5)
            ttk.Button(controls_frame, text="Export Logs", 
                      command=self.export_logs).pack(side=tk.LEFT, padx=5)
            
            # Log viewer
            self.log_viewer = scrolledtext.ScrolledText(logs_frame)
            self.log_viewer.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        def create_status_bar(self):
            """Create status bar"""
            self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
            self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        def initialize_engine(self):
            """Initialize the C-Keeper engine"""
            try:
                from core.config import Config
                config = Config()
                self.engine = CKeeperEngine(config, self.mode_var.get())
                
                self.update_status("Engine initialized successfully")
                self.update_session_info()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to initialize engine: {e}")
        
        def set_target(self):
            """Set the current target"""
            target = self.current_target.get()
            if target:
                self.update_status(f"Target set to: {target}")
            else:
                messagebox.showwarning("Warning", "Please enter a target")
        
        def quick_recon(self):
            """Perform quick reconnaissance"""
            if not self.engine:
                messagebox.showerror("Error", "Engine not initialized")
                return
            
            target = self.current_target.get()
            if not target:
                messagebox.showwarning("Warning", "Please set a target first")
                return
            
            self.update_status("Running reconnaissance...")
            
            # Run in thread to prevent GUI blocking
            thread = threading.Thread(target=self._run_recon, args=(target,))
            thread.daemon = True
            thread.start()
        
        def _run_recon(self, target):
            """Run reconnaissance in background thread"""
            try:
                recon_module = self.engine.get_module('recon')
                if recon_module:
                    results = recon_module.scan_target(target)
                    
                    # Update GUI in main thread
                    self.root.after(0, self._update_recon_results, results)
                else:
                    self.root.after(0, self.update_status, "Recon module not available")
                    
            except Exception as e:
                self.root.after(0, self.update_status, f"Recon failed: {e}")
        
        def _update_recon_results(self, results):
            """Update recon results in GUI"""
            self.recon_results.delete(1.0, tk.END)
            
            output = f"=== Reconnaissance Results ===\\n"
            output += f"Target: {results['target']}\\n"
            output += f"Hosts Found: {len(results['hosts'])}\\n"
            output += f"Vulnerabilities: {len(results['vulnerabilities'])}\\n\\n"
            
            if results['hosts']:
                output += "--- Discovered Hosts ---\\n"
                for host in results['hosts']:
                    output += f"  {host['ip']} ({host.get('hostname', 'Unknown')})\\n"
                    if 'services' in host:
                        for service in host['services']:
                            if service['state'] == 'open':
                                output += f"    {service['port']}/{service['protocol']} - {service['service']}\\n"
                output += "\\n"
            
            if results['vulnerabilities']:
                output += "--- Vulnerabilities ---\\n"
                for vuln in results['vulnerabilities']:
                    output += f"  {vuln['host']}:{vuln['port']} - {vuln['type']} ({vuln['severity']})\\n"
            
            self.recon_results.insert(tk.END, output)
            self.update_status("Reconnaissance completed")
        
        # Simplified method implementations for basic GUI
        def scan_target(self): self.quick_recon()
        def port_scan(self): self.update_status("Port scan feature coming soon...")
        def clear_recon_results(self): self.recon_results.delete(1.0, tk.END)
        def build_exploits(self): self.update_status("Exploit building feature coming soon...")
        def run_selected_exploit(self): self.update_status("Exploit execution feature coming soon...")
        def generate_payload(self): self.update_status("Payload generation feature coming soon...")
        def start_listener(self): self.update_status("C2 listener feature coming soon...")
        def start_monitoring(self): self.update_status("Monitoring started (simulated)")
        def stop_monitoring(self): self.update_status("Monitoring stopped")
        def refresh_alerts(self): self.update_status("Alerts refreshed")
        def refresh_logs(self): self.log_viewer.insert(tk.END, "Log refresh feature coming soon...\\n")
        def clear_logs(self): self.log_viewer.delete(1.0, tk.END)
        def export_logs(self): self.update_status("Log export feature coming soon...")
        def run_killchain(self): self.update_status("Kill chain execution feature coming soon...")
        def open_killchain_window(self): messagebox.showinfo("Info", "Kill chain window coming soon...")
        def open_threat_hunter(self): messagebox.showinfo("Info", "Threat hunter coming soon...")
        def save_session(self): self.update_status("Session save feature coming soon...")
        def load_session(self): self.update_status("Session load feature coming soon...")
        def export_report(self): self.update_status("Report export feature coming soon...")
        def show_about(self): messagebox.showinfo("About", "C-Keeper v1.0\\nCyber Kill Chain Engine")
        
        def update_status(self, message):
            """Update status bar"""
            self.status_bar.config(text=message)
        
        def update_session_info(self):
            """Update session information"""
            if self.engine:
                session_info = self.engine.get_session_info()
                
                info_text = f"""Session Information:
    Session ID: {session_info['session_id']}
    Mode: {session_info['mode']}
    Start Time: {session_info['start_time']}

    Available Modules:
    {chr(10).join(f"• {module}" for module in session_info['modules'])}

    Current Target: {self.current_target.get() or 'None'}
    """
                
                self.session_info.delete(1.0, tk.END)
                self.session_info.insert(tk.END, info_text)
        
        def run(self):
            """Run the GUI application"""
            self.root.mainloop()

    def start_gui(engine=None):
        """Start the basic GUI interface"""
        try:
            app = CKeeperGUI()
            if engine:
                app.engine = engine
                app.update_session_info()
            app.run()
            return 0
        except Exception as e:
            print(f"GUI Error: {e}")
            return 1
    """Enhanced GUI application for C-Keeper with modern UI"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("C-Keeper - Advanced Cyber Kill Chain Engine")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1e1e1e')  # Dark theme
        
        # Modern color scheme
        self.colors = {
            'bg_primary': '#1e1e1e',
            'bg_secondary': '#2d2d2d',
            'bg_tertiary': '#3d3d3d',
            'accent_red': '#ff4757',
            'accent_blue': '#3742fa',
            'accent_green': '#2ed573',
            'accent_yellow': '#ffa502',
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0',
            'border': '#404040'
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
        """Setup modern styling for ttk widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure notebook style
        style.configure('Custom.TNotebook', 
                       background=self.colors['bg_secondary'],
                       borderwidth=0)
        style.configure('Custom.TNotebook.Tab',
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['text_primary'],
                       padding=[20, 8],
                       borderwidth=0)
        style.map('Custom.TNotebook.Tab',
                 background=[('selected', self.colors['accent_blue'])],
                 foreground=[('selected', self.colors['text_primary'])])
        
        # Configure frame styles
        style.configure('Dark.TFrame', background=self.colors['bg_secondary'])
        style.configure('Card.TFrame', 
                       background=self.colors['bg_tertiary'],
                       relief='solid',
                       borderwidth=1)
        
        # Configure label styles
        style.configure('Heading.TLabel',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 16, 'bold'))
        style.configure('SubHeading.TLabel',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_secondary'],
                       font=('Segoe UI', 12))
        style.configure('Status.TLabel',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['accent_green'],
                       font=('Segoe UI', 10, 'bold'))
        
        # Configure button styles
        style.configure('Action.TButton',
                       background=self.colors['accent_blue'],
                       foreground=self.colors['text_primary'],
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'))
        style.map('Action.TButton',
                 background=[('active', '#4c5bfc')])
        
        style.configure('Danger.TButton',
                       background=self.colors['accent_red'],
                       foreground=self.colors['text_primary'],
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'))
        
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
        """Create modern header with branding and controls"""
        header = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=80)
        header.pack(fill=tk.X, padx=10, pady=(10, 0))
        header.pack_propagate(False)
        
        # Left side - Logo and title
        left_frame = tk.Frame(header, bg=self.colors['bg_secondary'])
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20)
        
        title_frame = tk.Frame(left_frame, bg=self.colors['bg_secondary'])
        title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Main title
        title_label = tk.Label(title_frame, 
                              text="C-KEEPER",
                              font=('Segoe UI', 24, 'bold'),
                              fg=self.colors['text_primary'],
                              bg=self.colors['bg_secondary'])
        title_label.pack(anchor='w')
        
        # Subtitle
        subtitle_label = tk.Label(title_frame,
                                 text="Advanced Cyber Kill Chain Engine",
                                 font=('Segoe UI', 12),
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['bg_secondary'])
        subtitle_label.pack(anchor='w')
        
        # Right side - Mode selector and engine controls
        right_frame = tk.Frame(header, bg=self.colors['bg_secondary'])
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20)
        
        # Mode selector
        mode_frame = tk.Frame(right_frame, bg=self.colors['bg_secondary'])
        mode_frame.pack(side=tk.TOP, pady=(10, 5))
        
        tk.Label(mode_frame, text="Mode:", 
                font=('Segoe UI', 10),
                fg=self.colors['text_secondary'],
                bg=self.colors['bg_secondary']).pack(side=tk.LEFT, padx=(0, 5))
        
        mode_combo = ttk.Combobox(mode_frame, textvariable=self.mode_var,
                                 values=['red', 'blue', 'dual'],
                                 state='readonly', width=8)
        mode_combo.pack(side=tk.LEFT)
        
        # Engine controls
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
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.activity_list.insert(tk.END, log_entry)
        self.activity_list.see(tk.END)
        
# ... (continuing with more methods)
        self.create_logs_tab()
        
        # Create status bar
        self.create_status_bar()
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Initialize Engine", command=self.initialize_engine)
        file_menu.add_separator()
        file_menu.add_command(label="Save Session", command=self.save_session)
        file_menu.add_command(label="Load Session", command=self.load_session)
        file_menu.add_separator()
        file_menu.add_command(label="Export Report", command=self.export_report)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Kill Chain Executor", command=self.open_killchain_window)
        tools_menu.add_command(label="Threat Hunter", command=self.open_threat_hunter)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_overview_tab(self):
        """Create overview tab"""
        overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(overview_frame, text="Overview")
        
        # Engine status
        status_frame = ttk.LabelFrame(overview_frame, text="Engine Status")
        status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(status_frame, text="Mode:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        mode_combo = ttk.Combobox(status_frame, textvariable=self.mode_var, 
                                  values=["red", "blue", "dual"], state="readonly")
        mode_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Button(status_frame, text="Initialize Engine", 
                  command=self.initialize_engine).grid(row=0, column=2, padx=5, pady=2)
        
        # Target configuration
        target_frame = ttk.LabelFrame(overview_frame, text="Target Configuration")
        target_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(target_frame, text="Target:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(target_frame, textvariable=self.current_target, width=30).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(target_frame, text="Set Target", 
                  command=self.set_target).grid(row=0, column=2, padx=5, pady=2)
        
        # Quick actions
        actions_frame = ttk.LabelFrame(overview_frame, text="Quick Actions")
        actions_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(actions_frame, text="Quick Recon", 
                  command=self.quick_recon).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(actions_frame, text="Start Monitoring", 
                  command=self.start_monitoring).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(actions_frame, text="Run Kill Chain", 
                  command=self.run_killchain).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Session info
        self.session_info = scrolledtext.ScrolledText(overview_frame, height=15)
        self.session_info.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_recon_tab(self):
        """Create reconnaissance tab"""
        recon_frame = ttk.Frame(self.notebook)
        self.notebook.add(recon_frame, text="Reconnaissance")
        
        # Controls
        controls_frame = ttk.Frame(recon_frame)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(controls_frame, text="Scan Target", 
                  command=self.scan_target).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Port Scan", 
                  command=self.port_scan).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Clear Results", 
                  command=self.clear_recon_results).pack(side=tk.LEFT, padx=5)
        
        # Results
        self.recon_results = scrolledtext.ScrolledText(recon_frame)
        self.recon_results.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_exploit_tab(self):
        """Create exploitation tab"""
        exploit_frame = ttk.Frame(self.notebook)
        self.notebook.add(exploit_frame, text="Exploitation")
        
        # Controls
        controls_frame = ttk.Frame(exploit_frame)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(controls_frame, text="Build Exploits", 
                  command=self.build_exploits).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Run Selected", 
                  command=self.run_selected_exploit).pack(side=tk.LEFT, padx=5)
        
        # Exploit list
        self.exploit_tree = ttk.Treeview(exploit_frame, columns=("Type", "Target", "Reliability"), show="tree headings")
        self.exploit_tree.heading("#0", text="Name")
        self.exploit_tree.heading("Type", text="Type")
        self.exploit_tree.heading("Target", text="Target")
        self.exploit_tree.heading("Reliability", text="Reliability")
        self.exploit_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_payload_tab(self):
        """Create payload tab"""
        payload_frame = ttk.Frame(self.notebook)
        self.notebook.add(payload_frame, text="Payloads")
        
        # Payload configuration
        config_frame = ttk.LabelFrame(payload_frame, text="Payload Configuration")
        config_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(config_frame, text="Type:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.payload_type = ttk.Combobox(config_frame, values=["reverse_shell", "bind_shell", "meterpreter", "exec"])
        self.payload_type.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(config_frame, text="Platform:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.payload_platform = ttk.Combobox(config_frame, values=["windows", "linux", "macos", "web"])
        self.payload_platform.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(config_frame, text="LHOST:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.lhost = ttk.Entry(config_frame)
        self.lhost.grid(row=1, column=1, padx=5, pady=2)
        self.lhost.insert(0, "127.0.0.1")
        
        ttk.Label(config_frame, text="LPORT:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        self.lport = ttk.Entry(config_frame)
        self.lport.grid(row=1, column=3, padx=5, pady=2)
        self.lport.insert(0, "4444")
        
        ttk.Button(config_frame, text="Generate Payload", 
                  command=self.generate_payload).grid(row=2, column=0, columnspan=4, pady=10)
        
        # Payload results
        self.payload_results = scrolledtext.ScrolledText(payload_frame)
        self.payload_results.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_c2_tab(self):
        """Create C2 tab"""
        c2_frame = ttk.Frame(self.notebook)
        self.notebook.add(c2_frame, text="Command & Control")
        
        # Listener controls
        listener_frame = ttk.LabelFrame(c2_frame, text="Listeners")
        listener_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(listener_frame, text="Type:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.listener_type = ttk.Combobox(listener_frame, values=["tcp", "http", "https"])
        self.listener_type.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(listener_frame, text="Port:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.listener_port = ttk.Entry(listener_frame, width=10)
        self.listener_port.grid(row=0, column=3, padx=5, pady=2)
        self.listener_port.insert(0, "4444")
        
        ttk.Button(listener_frame, text="Start Listener", 
                  command=self.start_listener).grid(row=0, column=4, padx=5, pady=2)
        
        # Sessions
        sessions_frame = ttk.LabelFrame(c2_frame, text="Active Sessions")
        sessions_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.sessions_tree = ttk.Treeview(sessions_frame, columns=("Address", "Type", "Time"), show="tree headings")
        self.sessions_tree.heading("#0", text="Session ID")
        self.sessions_tree.heading("Address", text="Address")
        self.sessions_tree.heading("Type", text="Type")
        self.sessions_tree.heading("Time", text="Established")
        self.sessions_tree.pack(fill=tk.BOTH, expand=True)
    
    def create_monitor_tab(self):
        """Create monitoring tab"""
        monitor_frame = ttk.Frame(self.notebook)
        self.notebook.add(monitor_frame, text="Monitoring")
        
        # Controls
        controls_frame = ttk.Frame(monitor_frame)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(controls_frame, text="Start Monitoring", 
                  command=self.start_monitoring).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Stop Monitoring", 
                  command=self.stop_monitoring).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Refresh Alerts", 
                  command=self.refresh_alerts).pack(side=tk.LEFT, padx=5)
        
        # Alerts
        alerts_frame = ttk.LabelFrame(monitor_frame, text="Recent Alerts")
        alerts_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.alerts_tree = ttk.Treeview(alerts_frame, columns=("Time", "Type", "Severity"), show="tree headings")
        self.alerts_tree.heading("#0", text="Description")
        self.alerts_tree.heading("Time", text="Time")
        self.alerts_tree.heading("Type", text="Type")
        self.alerts_tree.heading("Severity", text="Severity")
        self.alerts_tree.pack(fill=tk.BOTH, expand=True)
    
    def create_logs_tab(self):
        """Create logs tab"""
        logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(logs_frame, text="Logs")
        
        # Controls
        controls_frame = ttk.Frame(logs_frame)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(controls_frame, text="Refresh Logs", 
                  command=self.refresh_logs).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Clear Logs", 
                  command=self.clear_logs).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Export Logs", 
                  command=self.export_logs).pack(side=tk.LEFT, padx=5)
        
        # Log viewer
        self.log_viewer = scrolledtext.ScrolledText(logs_frame)
        self.log_viewer.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def initialize_engine(self):
        """Initialize the C-Keeper engine"""
        try:
            from core.config import Config
            config = Config()
            self.engine = CKeeperEngine(config, self.mode_var.get())
            
            self.update_status("Engine initialized successfully")
            self.update_session_info()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize engine: {e}")
    
    def set_target(self):
        """Set the current target"""
        target = self.current_target.get()
        if target:
            self.update_status(f"Target set to: {target}")
        else:
            messagebox.showwarning("Warning", "Please enter a target")
    
    def quick_recon(self):
        """Perform quick reconnaissance"""
        if not self.engine:
            messagebox.showerror("Error", "Engine not initialized")
            return
        
        target = self.current_target.get()
        if not target:
            messagebox.showwarning("Warning", "Please set a target first")
            return
        
        self.update_status("Running reconnaissance...")
        
        # Run in thread to prevent GUI blocking
        thread = threading.Thread(target=self._run_recon, args=(target,))
        thread.daemon = True
        thread.start()
    
    def _run_recon(self, target):
        """Run reconnaissance in background thread"""
        try:
            recon_module = self.engine.get_module('recon')
            if recon_module:
                results = recon_module.scan_target(target)
                
                # Update GUI in main thread
                self.root.after(0, self._update_recon_results, results)
            else:
                self.root.after(0, self.update_status, "Recon module not available")
                
        except Exception as e:
            self.root.after(0, self.update_status, f"Recon failed: {e}")
    
    def _update_recon_results(self, results):
        """Update recon results in GUI"""
        self.recon_results.delete(1.0, tk.END)
        
        output = f"=== Reconnaissance Results ===\\n"
        output += f"Target: {results['target']}\\n"
        output += f"Hosts Found: {len(results['hosts'])}\\n"
        output += f"Vulnerabilities: {len(results['vulnerabilities'])}\\n\\n"
        
        if results['hosts']:
            output += "--- Discovered Hosts ---\\n"
            for host in results['hosts']:
                output += f"  {host['ip']} ({host.get('hostname', 'Unknown')})\\n"
                if 'services' in host:
                    for service in host['services']:
                        if service['state'] == 'open':
                            output += f"    {service['port']}/{service['protocol']} - {service['service']}\\n"
            output += "\\n"
        
        if results['vulnerabilities']:
            output += "--- Vulnerabilities ---\\n"
            for vuln in results['vulnerabilities']:
                output += f"  {vuln['host']}:{vuln['port']} - {vuln['type']} ({vuln['severity']})\\n"
        
        self.recon_results.insert(tk.END, output)
        self.update_status("Reconnaissance completed")
    
    def scan_target(self):
        """Scan target"""
        self.quick_recon()
    
    def port_scan(self):
        """Perform port scan"""
        target = self.current_target.get()
        if not target:
            messagebox.showwarning("Warning", "Please set a target first")
            return
        
        self.update_status(f"Port scanning {target}...")
        # Implementation would go here
        
    def clear_recon_results(self):
        """Clear reconnaissance results"""
        self.recon_results.delete(1.0, tk.END)
    
    def build_exploits(self):
        """Build exploits"""
        if not self.engine:
            messagebox.showerror("Error", "Engine not initialized")
            return
        
        self.update_status("Building exploits...")
        # Implementation would go here
    
    def run_selected_exploit(self):
        """Run selected exploit"""
        selection = self.exploit_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an exploit")
            return
        
        # Implementation would go here
        self.update_status("Running exploit...")
    
    def generate_payload(self):
        """Generate payload"""
        if not self.engine:
            messagebox.showerror("Error", "Engine not initialized")
            return
        
        payload_type = self.payload_type.get()
        platform = self.payload_platform.get()
        lhost = self.lhost.get()
        lport = self.lport.get()
        
        if not all([payload_type, platform, lhost, lport]):
            messagebox.showwarning("Warning", "Please fill all payload fields")
            return
        
        self.update_status("Generating payload...")
        
        try:
            payload_generator = self.engine.get_module('payload_generator')
            if payload_generator:
                options = {'lhost': lhost, 'lport': int(lport)}
                result = payload_generator.generate_payload(payload_type, platform, options)
                
                self.payload_results.delete(1.0, tk.END)
                output = f"=== Payload Generation Result ===\\n"
                output += f"ID: {result['id']}\\n"
                output += f"Type: {result['type']}\\n"
                output += f"Platform: {result['platform']}\\n"
                output += f"Success: {result['success']}\\n"
                if result.get('file_path'):
                    output += f"Saved to: {result['file_path']}\\n"
                
                self.payload_results.insert(tk.END, output)
                self.update_status("Payload generated successfully")
            else:
                messagebox.showerror("Error", "Payload generator not available")
                
        except Exception as e:
            messagebox.showerror("Error", f"Payload generation failed: {e}")
    
    def start_listener(self):
        """Start C2 listener"""
        if not self.engine:
            messagebox.showerror("Error", "Engine not initialized")
            return
        
        listener_type = self.listener_type.get()
        port = self.listener_port.get()
        
        if not listener_type or not port:
            messagebox.showwarning("Warning", "Please specify listener type and port")
            return
        
        try:
            c2_handler = self.engine.get_module('c2_handler')
            if c2_handler:
                result = c2_handler.start_listener(listener_type, int(port))
                if result['success']:
                    self.update_status(f"Listener started: {result['message']}")
                else:
                    messagebox.showerror("Error", result['error'])
            else:
                messagebox.showerror("Error", "C2 handler not available")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start listener: {e}")
    
    def start_monitoring(self):
        """Start monitoring"""
        if not self.engine:
            messagebox.showerror("Error", "Engine not initialized")
            return
        
        try:
            self.engine.start_monitoring()
            self.update_status("Monitoring started")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start monitoring: {e}")
    
    def stop_monitoring(self):
        """Stop monitoring"""
        if not self.engine:
            return
        
        try:
            self.engine.stop_monitoring()
            self.update_status("Monitoring stopped")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop monitoring: {e}")
    
    def refresh_alerts(self):
        """Refresh alerts"""
        if not self.engine:
            return
        
        try:
            logger_defender = self.engine.get_module('logger_defender')
            if logger_defender:
                alerts = logger_defender.get_recent_alerts(hours=24)
                
                # Clear existing items
                for item in self.alerts_tree.get_children():
                    self.alerts_tree.delete(item)
                
                # Add alerts
                for alert in alerts[:50]:  # Show latest 50
                    self.alerts_tree.insert("", tk.END, 
                                          text=alert['description'][:50] + "...",
                                          values=(alert['timestamp'], alert['event_type'], alert['severity']))
                
                self.update_status(f"Refreshed {len(alerts)} alerts")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh alerts: {e}")
    
    def refresh_logs(self):
        """Refresh logs"""
        self.log_viewer.delete(1.0, tk.END)
        self.log_viewer.insert(tk.END, "Log refreshing not implemented yet")
    
    def clear_logs(self):
        """Clear logs"""
        self.log_viewer.delete(1.0, tk.END)
    
    def export_logs(self):
        """Export logs"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.log_viewer.get(1.0, tk.END))
                messagebox.showinfo("Success", f"Logs exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export logs: {e}")
    
    def run_killchain(self):
        """Run kill chain"""
        if not self.engine:
            messagebox.showerror("Error", "Engine not initialized")
            return
        
        target = self.current_target.get()
        if not target:
            messagebox.showwarning("Warning", "Please set a target first")
            return
        
        if self.engine.mode == 'blue':
            messagebox.showerror("Error", "Kill chain not available in blue mode")
            return
        
        result = messagebox.askyesno("Confirm", f"Run kill chain against {target}?")
        if result:
            self.update_status(f"Running kill chain against {target}...")
            # Implementation would go here
    
    def open_killchain_window(self):
        """Open kill chain configuration window"""
        # Implementation for kill chain window
        messagebox.showinfo("Info", "Kill chain window not implemented yet")
    
    def open_threat_hunter(self):
        """Open threat hunter window"""
        # Implementation for threat hunter window
        messagebox.showinfo("Info", "Threat hunter window not implemented yet")
    
    def save_session(self):
        """Save session"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                session_data = {
                    'target': self.current_target.get(),
                    'mode': self.mode_var.get(),
                    'timestamp': datetime.now().isoformat()
                }
                with open(filename, 'w') as f:
                    json.dump(session_data, f, indent=2)
                messagebox.showinfo("Success", f"Session saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save session: {e}")
    
    def load_session(self):
        """Load session"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    session_data = json.load(f)
                
                self.current_target.set(session_data.get('target', ''))
                self.mode_var.set(session_data.get('mode', 'dual'))
                
                messagebox.showinfo("Success", f"Session loaded from {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load session: {e}")
    
    def export_report(self):
        """Export report"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                report = f"""C-KEEPER SESSION REPORT
=======================

Target: {self.current_target.get()}
Mode: {self.mode_var.get()}
Generated: {datetime.now().isoformat()}

Session Information:
{self.session_info.get(1.0, tk.END)}
"""
                with open(filename, 'w') as f:
                    f.write(report)
                messagebox.showinfo("Success", f"Report exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export report: {e}")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """C-Keeper v1.0
Dual-Use Cyber Kill Chain Engine

A comprehensive framework for both red team (offensive) 
and blue team (defensive) operations.

Modules:
• Reconnaissance
• Exploit Builder  
• Payload Generator
• Delivery Engine
• Command & Control
• Logger/Defender

⚠️ For authorized testing only!
"""
        messagebox.showinfo("About C-Keeper", about_text)
    
    def update_status(self, message):
        """Update status bar"""
        self.status_bar.config(text=message)
    
    def update_session_info(self):
        """Update session information"""
        if self.engine:
            session_info = self.engine.get_session_info()
            
            info_text = f"""Session Information:
Session ID: {session_info['session_id']}
Mode: {session_info['mode']}
Start Time: {session_info['start_time']}

Available Modules:
{chr(10).join(f"• {module}" for module in session_info['modules'])}

Current Target: {self.current_target.get() or 'None'}
"""
            
            self.session_info.delete(1.0, tk.END)
            self.session_info.insert(tk.END, info_text)
    
    def run(self):
        """Run the GUI application"""
        self.root.mainloop()

def start_gui(engine=None):
    """Start the GUI interface"""
    try:
        if GUI_TYPE == "modern":
            return start_modern_gui(engine)
        else:
            app = CKeeperGUI()
            if engine:
                app.engine = engine
                app.update_session_info()
            app.run()
            return 0
    except Exception as e:
        print(f"GUI Error: {e}")
        return 1
