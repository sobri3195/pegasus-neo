#!/usr/bin/env python3

import requests
from rich.console import Console
from rich.progress import track
from urllib.parse import urljoin

console = Console()

class WebAttacks:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def directory_scan(self, target_url, wordlist_file):
        """Perform directory bruteforce scan"""
        try:
            console.print(f"[yellow]Starting directory scan on {target_url}...[/yellow]")
            found_dirs = []
            
            with open(wordlist_file) as f:
                directories = f.read().splitlines()
            
            for directory in track(directories, description="Scanning directories..."):
                url = urljoin(target_url, directory)
                response = self.session.get(url, headers=self.headers)
                
                if response.status_code == 200:
                    found_dirs.append(url)
                    console.print(f"[green]Found: {url} (Status: {response.status_code})[/green]")
            
            return found_dirs
            
        except Exception as e:
            console.print(f"[bold red]Error during scan: {str(e)}[/bold red]")
            return [] 