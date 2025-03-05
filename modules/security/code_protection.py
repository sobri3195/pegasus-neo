#!/usr/bin/env python3

import hashlib
import os
import sys
import base64
from cryptography.fernet import Fernet
from rich.console import Console
from datetime import datetime

console = Console()

class CodeProtection:
    def __init__(self):
        self.key = b'YOUR_SECRET_KEY_HERE'  # Ganti dengan key yang aman
        self.checksum_file = ".checksums"
        self.cipher = Fernet(base64.b64encode(hashlib.sha256(self.key).digest()))
        
    def calculate_file_hash(self, filepath):
        """Calculate SHA-256 hash of a file"""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def encrypt_file(self, filepath):
        """Encrypt Python source files"""
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            encrypted_data = self.cipher.encrypt(data)
            with open(filepath + '.enc', 'wb') as f:
                f.write(encrypted_data)
            os.remove(filepath)  # Remove original file
            return True
        except Exception as e:
            console.print(f"[red]Error encrypting {filepath}: {str(e)}[/red]")
            return False
            
    def decrypt_file(self, filepath):
        """Decrypt Python source files"""
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            decrypted_data = self.cipher.decrypt(data)
            with open(filepath[:-4], 'wb') as f:
                f.write(decrypted_data)
            return True
        except Exception as e:
            console.print(f"[red]Error decrypting {filepath}: {str(e)}[/red]")
            return False
            
    def store_checksums(self, files):
        """Store checksums of all source files"""
        checksums = {}
        for file in files:
            if file.endswith('.py'):
                checksums[file] = self.calculate_file_hash(file)
                
        encrypted_checksums = self.cipher.encrypt(str(checksums).encode())
        with open(self.checksum_file, 'wb') as f:
            f.write(encrypted_checksums)
            
    def verify_integrity(self, files):
        """Verify file integrity using stored checksums"""
        try:
            with open(self.checksum_file, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = self.cipher.decrypt(encrypted_data)
            stored_checksums = eval(decrypted_data.decode())
            
            for file in files:
                if file.endswith('.py'):
                    current_hash = self.calculate_file_hash(file)
                    if file in stored_checksums:
                        if current_hash != stored_checksums[file]:
                            console.print(f"[bold red]Warning: {file} has been modified![/bold red]")
                            return False
            return True
        except Exception as e:
            console.print(f"[bold red]Error verifying integrity: {str(e)}[/bold red]")
            return False
            
    def protect_source_code(self):
        """Implement multiple layers of protection"""
        try:
            # Get all Python source files
            python_files = []
            for root, dirs, files in os.walk('.'):
                for file in files:
                    if file.endswith('.py'):
                        python_files.append(os.path.join(root, file))
            
            # Store original checksums
            self.store_checksums(python_files)
            
            # Add integrity check code to each file
            for file in python_files:
                with open(file, 'r') as f:
                    content = f.read()
                
                # Add integrity check
                protection_code = f"""
import hashlib
import sys
from datetime import datetime

def _verify_integrity():
    with open(__file__, 'rb') as f:
        content = f.read()
    current_hash = hashlib.sha256(content).hexdigest()
    if current_hash != '{self.calculate_file_hash(file)}':
        print("\\n[!] Critical: Source code has been modified!")
        sys.exit(1)

_verify_integrity()
"""
                
                with open(file, 'w') as f:
                    f.write(protection_code + content)
                
            console.print("[green]Source code protection applied successfully[/green]")
            return True
            
        except Exception as e:
            console.print(f"[bold red]Error protecting source code: {str(e)}[/bold red]")
            return False 