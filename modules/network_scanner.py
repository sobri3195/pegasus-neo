#!/usr/bin/env python3

import nmap
import socket
from rich.console import Console
from rich.table import Table

console = Console()

class NetworkScanner:
    def __init__(self):
        self.scanner = nmap.PortScanner()
    
    def quick_scan(self, target):
        """Perform quick network scan"""
        try:
            console.print(f"[yellow]Starting quick scan on {target}...[/yellow]")
            self.scanner.scan(target, arguments='-sV --version-intensity 5')
            
            table = Table(title=f"Scan Results for {target}")
            table.add_column("Port", style="cyan")
            table.add_column("State", style="green")
            table.add_column("Service", style="yellow")
            table.add_column("Version", style="magenta")
            
            for host in self.scanner.all_hosts():
                for proto in self.scanner[host].all_protocols():
                    ports = self.scanner[host][proto].keys()
                    for port in ports:
                        service = self.scanner[host][proto][port]
                        table.add_row(
                            str(port),
                            service['state'],
                            service['name'],
                            service['version']
                        )
            
            console.print(table)
            return True
            
        except Exception as e:
            console.print(f"[bold red]Error during scan: {str(e)}[/bold red]")
            return False 