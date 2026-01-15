#!/usr/bin/env python3

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from cryptography.fernet import Fernet
import hashlib
import os
import json
from datetime import datetime

console = Console()

class EncryptionTool:
    def __init__(self):
        self.output_dir = "output/encryption"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_key(self):
        """Generate encryption key"""
        try:
            key = Fernet.generate_key()
            
            table = Table(title="Generated Encryption Key")
            table.add_row("Key", key.decode())
            table.add_row("Store securely!", "This key is needed for decryption")
            
            console.print(table)
            return key
            
        except Exception as e:
            console.print(f"[bold red]Error generating key: {str(e)}[/bold red]")
            return None
    
    def encrypt_message(self, message, key):
        """Encrypt message with Fernet"""
        try:
            f = Fernet(key)
            encrypted = f.encrypt(message.encode())
            
            table = Table(title="Message Encryption")
            table.add_row("Original", message)
            table.add_row("Encrypted", encrypted.decode())
            
            console.print(table)
            return encrypted
            
        except Exception as e:
            console.print(f"[bold red]Error encrypting: {str(e)}[/bold red]")
            return None
    
    def decrypt_message(self, encrypted, key):
        """Decrypt message with Fernet"""
        try:
            f = Fernet(key)
            decrypted = f.decrypt(encrypted).decode()
            
            table = Table(title="Message Decryption")
            table.add_row("Encrypted", encrypted.decode())
            table.add_row("Decrypted", decrypted)
            
            console.print(table)
            return decrypted
            
        except Exception as e:
            console.print(f"[bold red]Error decrypting: {str(e)}[/bold red]")
            return None
    
    def encrypt_file(self, filepath, key):
        """Encrypt file"""
        try:
            f = Fernet(key)
            
            with open(filepath, 'rb') as file:
                file_data = file.read()
            
            encrypted_data = f.encrypt(file_data)
            
            output_path = filepath + '.enc'
            with open(output_path, 'wb') as file:
                file.write(encrypted_data)
            
            table = Table(title="File Encryption")
            table.add_row("Original File", filepath)
            table.add_row("Encrypted File", output_path)
            
            console.print(table)
            return output_path
            
        except Exception as e:
            console.print(f"[bold red]Error encrypting file: {str(e)}[/bold red]")
            return None
    
    def decrypt_file(self, filepath, key):
        """Decrypt file"""
        try:
            f = Fernet(key)
            
            with open(filepath, 'rb') as file:
                encrypted_data = file.read()
            
            decrypted_data = f.decrypt(encrypted_data)
            
            output_path = filepath[:-4]  # Remove .enc extension
            with open(output_path, 'wb') as file:
                file.write(decrypted_data)
            
            table = Table(title="File Decryption")
            table.add_row("Encrypted File", filepath)
            table.add_row("Decrypted File", output_path)
            
            console.print(table)
            return output_path
            
        except Exception as e:
            console.print(f"[bold red]Error decrypting file: {str(e)}[/bold red]")
            return None
    
    def hash_file(self, filepath, algorithm="sha256"):
        """Calculate file hash"""
        try:
            hash_obj = hashlib.new(algorithm)
            
            with open(filepath, 'rb') as file:
                for chunk in iter(lambda: file.read(4096), b''):
                    hash_obj.update(chunk)
            
            file_hash = hash_obj.hexdigest()
            
            table = Table(title=f"File Hash ({algorithm.upper()})")
            table.add_row("File", filepath)
            table.add_row("Hash", file_hash)
            
            console.print(table)
            return file_hash
            
        except Exception as e:
            console.print(f"[bold red]Error hashing file: {str(e)}[/bold red]")
            return None
    
    def verify_hash(self, filepath, expected_hash, algorithm="sha256"):
        """Verify file hash"""
        try:
            current_hash = self.hash_file(filepath, algorithm)
            
            if current_hash == expected_hash:
                console.print("[green]✓ Hash matches![/green]")
                return True
            else:
                console.print("[red]✗ Hash does not match![/red]")
                console.print(f"[yellow]Expected: {expected_hash}[/yellow]")
                console.print(f"[yellow]Got: {current_hash}[/yellow]")
                return False
                
        except Exception as e:
            console.print(f"[bold red]Error verifying hash: {str(e)}[/bold red]")
            return False
    
    def create_password_hash(self, password, salt=None):
        """Create salted password hash"""
        try:
            if salt is None:
                salt = os.urandom(32)
            
            key = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt,
                100000
            )
            
            table = Table(title="Password Hash")
            table.add_row("Algorithm", "PBKDF2-HMAC-SHA256")
            table.add_row("Iterations", "100,000")
            table.add_row("Salt (hex)", salt.hex())
            table.add_row("Hash (hex)", key.hex())
            
            console.print(table)
            
            return {
                "salt": salt.hex(),
                "hash": key.hex(),
                "algorithm": "pbkdf2_hmac_sha256"
            }
            
        except Exception as e:
            console.print(f"[bold red]Error creating hash: {str(e)}[/bold red]")
            return None
