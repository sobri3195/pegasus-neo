#!/usr/bin/env python3

import hashlib
import itertools
from rich.console import Console
from rich.progress import track
import time

console = Console()

class PasswordAttacks:
    def __init__(self):
        self.common_passwords = [
            "password", "123456", "admin", "root", "letmein",
            "monkey", "dragon", "baseball", "football", "abc123"
        ]
    
    def dictionary_attack(self, hash_to_crack, hash_type="md5"):
        """Perform dictionary attack on hash"""
        try:
            console.print(f"[yellow]Starting dictionary attack on {hash_type} hash...[/yellow]")
            
            for password in track(self.common_passwords, description="Testing passwords..."):
                if hash_type == "md5":
                    test_hash = hashlib.md5(password.encode()).hexdigest()
                elif hash_type == "sha256":
                    test_hash = hashlib.sha256(password.encode()).hexdigest()
                else:
                    raise ValueError("Unsupported hash type")
                
                if test_hash == hash_to_crack:
                    console.print(f"[green]Password found: {password}[/green]")
                    return password
                    
                time.sleep(0.1)  # Simulate work
            
            console.print("[red]Password not found in dictionary[/red]")
            return None
            
        except Exception as e:
            console.print(f"[bold red]Error during attack: {str(e)}[/bold red]")
            return None 