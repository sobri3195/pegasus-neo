#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.progress import track
import json
import os
from datetime import datetime

console = Console()

class SocialTracker:
    def __init__(self):
        self.output_dir = "output/tracking"
        os.makedirs(self.output_dir, exist_ok=True)
        self.platforms = {
            "twitter": "https://twitter.com/{}",
            "instagram": "https://instagram.com/{}",
            "facebook": "https://facebook.com/{}",
            "github": "https://github.com/{}",
            "linkedin": "https://linkedin.com/in/{}"
        }
        
    def search_username(self, username):
        """Search username across social platforms"""
        try:
            results = {}
            
            for platform, url in track(self.platforms.items(), description="Searching platforms..."):
                try:
                    response = requests.get(url.format(username))
                    if response.status_code == 200:
                        results[platform] = {"found": True, "url": url.format(username)}
                    else:
                        results[platform] = {"found": False, "url": None}
                except:
                    results[platform] = {"found": False, "url": None}
            
            # Display results
            table = Table(title=f"Social Media Search Results for {username}")
            table.add_column("Platform", style="cyan")
            table.add_column("Found", style="green")
            table.add_column("URL", style="yellow")
            
            for platform, data in results.items():
                table.add_row(
                    platform.capitalize(),
                    "✓" if data["found"] else "✗",
                    data["url"] if data["found"] else "Not found"
                )
            
            console.print(table)
            
            # Save results
            output_file = f"{self.output_dir}/social_search_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=4)
                
            console.print(f"[green]Results saved to: {output_file}[/green]")
            return results
            
        except Exception as e:
            console.print(f"[bold red]Error searching username: {str(e)}[/bold red]")
            return None 