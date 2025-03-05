#!/usr/bin/env python3

import os
import subprocess
from rich.console import Console
from rich.prompt import Prompt

console = Console()

class WirelessAttacks:
    def __init__(self):
        self.interface = None
        self.target_bssid = None
        
    def setup_monitor_mode(self, interface):
        """Put wireless interface in monitor mode"""
        try:
            console.print(f"[yellow]Setting {interface} to monitor mode...[/yellow]")
            subprocess.run(['airmon-ng', 'start', interface], check=True)
            self.interface = f"{interface}mon"
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]Error setting monitor mode: {str(e)}[/bold red]")
            return False
            
    def scan_networks(self):
        """Scan for wireless networks"""
        if not self.interface:
            console.print("[bold red]Interface not in monitor mode![/bold red]")
            return False
            
        try:
            console.print("[yellow]Starting wireless network scan...[/yellow]")
            subprocess.run(['airodump-ng', self.interface], check=True)
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]Error scanning networks: {str(e)}[/bold red]")
            return False 