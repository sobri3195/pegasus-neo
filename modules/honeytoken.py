#!/usr/bin/env python3

import json
import uuid
from datetime import datetime
from rich.console import Console
from rich.table import Table
import os

console = Console()

class HoneytokenGenerator:
    def __init__(self):
        self.output_dir = "output/honeytokens"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_aws_key(self):
        """Generate fake AWS access key"""
        fake_key = {
            "type": "AWS Key",
            "access_key_id": f"AKIA{self._random_string(16)}",
            "secret_access_key": self._random_string(40),
            "token_id": str(uuid.uuid4()),
            "created": datetime.now().isoformat(),
            "canary": "This is a honeytoken - Alert if accessed!"
        }
        return fake_key
    
    def generate_database_url(self):
        """Generate fake database connection string"""
        db_types = ["mysql", "postgresql", "mongodb", "redis"]
        db_type = db_types[hash(str(uuid.uuid4())) % len(db_types)]
        
        fake_url = {
            "type": "Database URL",
            "url": f"{db_type}://user:{self._random_string(20)}@localhost:5432/{self._random_string(10)}",
            "token_id": str(uuid.uuid4()),
            "created": datetime.now().isoformat(),
            "canary": "This is a honeytoken - Alert if connected!"
        }
        return fake_url
    
    def generate_api_key(self):
        """Generate fake API key"""
        fake_key = {
            "type": "API Key",
            "key": f"sk-{self._random_string(32)}",
            "token_id": str(uuid.uuid4()),
            "created": datetime.now().isoformat(),
            "canary": "This is a honeytoken - Alert if used!"
        }
        return fake_key
    
    def generate_canary_token(self):
        """Generate canary token for files"""
        token = {
            "type": "Canary Token",
            "token": self._random_string(32),
            "token_id": str(uuid.uuid4()),
            "created": datetime.now().isoformat(),
            "canary": "This is a canary token - Alert if accessed!"
        }
        return token
    
    def generate_ssh_key(self):
        """Generate fake SSH private key"""
        fake_key = {
            "type": "SSH Key",
            "key_type": "RSA",
            "private_key": f"""-----BEGIN RSA PRIVATE KEY-----
{self._random_string(64)}
{self._random_string(64)}
{self._random_string(64)}
-----END RSA PRIVATE KEY-----""",
            "token_id": str(uuid.uuid4()),
            "created": datetime.now().isoformat(),
            "canary": "This is a honeytoken - Alert if used!"
        }
        return fake_key
    
    def create_honeytoken_file(self, filename, content):
        """Create file with honeytoken"""
        try:
            output_path = f"{self.output_dir}/{filename}"
            with open(output_path, 'w') as f:
                f.write(content)
            
            console.print(f"[green]Honeytoken file created: {output_path}[/green]")
            return output_path
            
        except Exception as e:
            console.print(f"[bold red]Error creating honeytoken file: {str(e)}[/bold red]")
            return None
    
    def display_honeytoken(self, token):
        """Display honeytoken details"""
        table = Table(title=f"Honeytoken: {token['type']}")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="yellow")
        
        for key, value in token.items():
            if key != "canary":
                table.add_row(key.replace('_', ' ').title(), str(value)[:50])
        
        table.add_row("Canary", "[bold red]" + token['canary'] + "[/bold red]")
        console.print(table)
    
    def save_honeytoken(self, token):
        """Save honeytoken to file"""
        filename = f"honeytoken_{token['type'].lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output_path = f"{self.output_dir}/{filename}"
        
        with open(output_path, 'w') as f:
            json.dump(token, f, indent=4)
        
        console.print(f"[green]Honeytoken saved to: {output_path}[/green]")
        return output_path
    
    def _random_string(self, length):
        """Generate random alphanumeric string"""
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
