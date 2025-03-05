#!/usr/bin/env python3

import os
import sys
from modules.security.code_protection import CodeProtection

def encrypt_source_files():
    protector = CodeProtection()
    
    # Apply source code protection
    protector.protect_source_code()
    
    # Get all Python files
    python_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    # Encrypt each file
    for file in python_files:
        print(f"Encrypting {file}...")
        protector.encrypt_file(file)
    
    print("\nSource code encryption complete!")

if __name__ == "__main__":
    encrypt_source_files() 