#!/usr/bin/env python3

import socket
import concurrent.futures
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from datetime import datetime
import json
import os

console = Console()

class PortScanner:
    def __init__(self):
        self.output_dir = "output/scan_results"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Common ports with services
        self.common_ports = {
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            445: "SMB",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            5900: "VNC",
            6379: "Redis",
            8080: "HTTP-Alt",
            8443: "HTTPS-Alt"
        }
        
        self.open_ports = []
    
    def scan_port(self, target, port, timeout=1):
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            
            if result == 0:
                service = self.common_ports.get(port, "Unknown")
                banner = self._grab_banner(target, port)
                
                port_info = {
                    "port": port,
                    "service": service,
                    "banner": banner
                }
                self.open_ports.append(port_info)
                
            sock.close()
            return result == 0
            
        except Exception:
            return False
    
    def _grab_banner(self, target, port):
        """Grab service banner"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((target, port))
            
            if port in [80, 8080, 443, 8443]:
                sock.send(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
            else:
                sock.send(b"\r\n")
            
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            sock.close()
            
            return banner[:100] if banner else None
            
        except:
            return None
    
    def quick_scan(self, target, ports=None):
        """Quick scan of common ports"""
        if ports is None:
            ports = list(self.common_ports.keys())
        
        console.print(f"[yellow]Starting quick scan on {target}...[/yellow]")
        console.print(f"[yellow]Scanning {len(ports)} ports...[/yellow]")
        
        self.open_ports = []
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Scanning ports...", total=len(ports))
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                futures = {
                    executor.submit(self.scan_port, target, port): port
                    for port in ports
                }
                
                for future in concurrent.futures.as_completed(futures):
                    progress.update(task, advance=1)
        
        self.display_results(target)
        return self.open_ports
    
    def full_scan(self, target, start_port=1, end_port=65535):
        """Full port scan (1-65535)"""
        console.print(f"[yellow]Starting full scan on {target}...[/yellow]")
        console.print(f"[yellow]Scanning ports {start_port}-{end_port}...[/yellow]")
        console.print("[red]This may take a while...[/red]")
        
        self.open_ports = []
        ports = range(start_port, end_port + 1)
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Scanning ports...", total=len(ports))
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                futures = {
                    executor.submit(self.scan_port, target, port): port
                    for port in ports
                }
                
                for future in concurrent.futures.as_completed(futures):
                    progress.update(task, advance=1)
        
        self.display_results(target)
        return self.open_ports
    
    def display_results(self, target):
        """Display scan results"""
        if not self.open_ports:
            console.print("[yellow]No open ports found[/yellow]")
            return
        
        self.open_ports.sort(key=lambda x: x['port'])
        
        table = Table(title=f"Scan Results for {target}")
        table.add_column("Port", style="cyan")
        table.add_column("Service", style="yellow")
        table.add_column("Banner", style="green")
        
        for port_info in self.open_ports:
            banner = port_info['banner'][:30] if port_info['banner'] else "N/A"
            table.add_row(
                str(port_info['port']),
                port_info['service'],
                banner
            )
        
        console.print(table)
        console.print(f"\n[green]Found {len(self.open_ports)} open ports[/green]")
    
    def detect_service_versions(self, target):
        """Try to detect service versions"""
        console.print(f"[yellow]Detecting service versions on {target}...[/yellow]")
        
        if not self.open_ports:
            self.quick_scan(target)
        
        version_info = {}
        
        for port_info in self.open_ports:
            port = port_info['port']
            banner = port_info['banner']
            
            if banner:
                version_info[port] = {
                    "service": port_info['service'],
                    "banner": banner,
                    "version": self._extract_version(banner)
                }
        
        if version_info:
            table = Table(title="Service Version Detection")
            table.add_column("Port", style="cyan")
            table.add_column("Service", style="yellow")
            table.add_column("Version", style="green")
            
            for port, info in version_info.items():
                version = info['version'] or "Unknown"
                table.add_row(str(port), info['service'], version[:50])
            
            console.print(table)
        
        return version_info
    
    def _extract_version(self, banner):
        """Extract version from banner"""
        try:
            import re
            # Look for version patterns like X.X.X
            version_pattern = r'\d+\.\d+(?:\.\d+)?(?:\.\d+)?'
            match = re.search(version_pattern, banner)
            return match.group() if match else banner[:30]
        except:
            return None
    
    def save_results(self, target):
        """Save scan results"""
        if not self.open_ports:
            console.print("[yellow]No results to save[/yellow]")
            return
        
        output_file = f"{self.output_dir}/port_scan_{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        results = {
            "target": target,
            "scan_date": datetime.now().isoformat(),
            "open_ports": self.open_ports
        }
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
        
        console.print(f"[green]Results saved to: {output_file}[/green]")
        return output_file
