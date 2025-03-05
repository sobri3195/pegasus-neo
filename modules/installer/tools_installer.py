#!/usr/bin/env python3

import os
import subprocess
from rich.console import Console
from rich.progress import track
import sys
import logging

console = Console()

class ToolsInstaller:
    def __init__(self):
        self.tools = {
            "Reconnaissance & OSINT": {
                "nmap": "apt-get install nmap -y",
                "wireshark": "apt-get install wireshark -y",
                "maltego": "apt-get install maltego -y",
                "shodan": "pip3 install shodan",
                "theharvester": "apt-get install theharvester -y",
                "recon-ng": "apt-get install recon-ng -y",
                "spiderfoot": "git clone https://github.com/smicallef/spiderfoot.git && cd spiderfoot && pip3 install -r requirements.txt",
                "foca": "apt-get install foca -y",
                "metagoofil": "apt-get install metagoofil -y"
            },
            "Exploitation & Pentesting": {
                "metasploit": "apt-get install metasploit-framework -y",
                "sqlmap": "apt-get install sqlmap -y",
                "commix": "apt-get install commix -y",
                "beef": "apt-get install beef-xss -y",
                "set": "apt-get install set -y",
                "hydra": "apt-get install hydra -y",
                "john": "apt-get install john -y",
                "hashcat": "apt-get install hashcat -y",
                "exploitdb": "apt-get install exploitdb -y",
                "powersploit": "git clone https://github.com/PowerShellMafia/PowerSploit.git"
            },
            "Wireless Hacking": {
                "aircrack-ng": "apt-get install aircrack-ng -y",
                "kismet": "apt-get install kismet -y",
                "wifite": "apt-get install wifite -y",
                "fern-wifi-cracker": "apt-get install fern-wifi-cracker -y",
                "reaver": "apt-get install reaver -y",
                "wifiphisher": "apt-get install wifiphisher -y",
                "cowpatty": "apt-get install cowpatty -y",
                "fluxion": "git clone https://github.com/FluxionNetwork/fluxion.git"
            },
            "Web Hacking": {
                "burpsuite": "apt-get install burpsuite -y",
                "zaproxy": "apt-get install zaproxy -y",
                "nikto": "apt-get install nikto -y",
                "xsstrike": "git clone https://github.com/s0md3v/XSStrike.git",
                "wapiti": "apt-get install wapiti -y",
                "sublist3r": "git clone https://github.com/aboul3la/Sublist3r.git && cd Sublist3r && pip3 install -r requirements.txt",
                "dirbuster": "apt-get install dirbuster -y",
                "wpscan": "apt-get install wpscan -y"
            },
            "MITM & Sniffing": {
                "bettercap": "apt-get install bettercap -y",
                "ettercap": "apt-get install ettercap-graphical -y",
                "mitmf": "git clone https://github.com/byt3bl33d3r/MITMf.git && cd MITMf && pip3 install -r requirements.txt",
                "evilginx2": "apt-get install golang-go && go get -u github.com/kgretzky/evilginx2"
            },
            "Anonymity & Privacy": {
                "tor": "apt-get install tor -y",
                "proxychains": "apt-get install proxychains -y",
                "tails": "echo 'Tails OS needs to be downloaded from https://tails.boum.org/'",
                "i2p": "apt-get install i2p -y"
            },
            "Exploit Development": {
                "ida-free": "wget https://out7.hex-rays.com/files/idafree70_linux.run && chmod +x idafree70_linux.run",
                "ghidra": "apt-get install ghidra -y",
                "radare2": "apt-get install radare2 -y",
                "immunity": "echo 'Immunity Debugger is Windows-only'",
                "pwntools": "pip3 install pwntools",
                "frida": "pip3 install frida-tools"
            }
        }
        
    def update_system(self):
        """Update system and package lists"""
        try:
            console.print("[yellow]Updating system...[/yellow]")
            subprocess.run("apt-get update && apt-get upgrade -y", shell=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error updating system: {str(e)}[/red]")
            return False
            
    def install_dependencies(self):
        """Install basic dependencies"""
        dependencies = [
            "python3-pip",
            "git",
            "curl",
            "wget",
            "build-essential"
        ]
        
        try:
            for dep in dependencies:
                console.print(f"[yellow]Installing {dep}...[/yellow]")
                subprocess.run(f"apt-get install {dep} -y", shell=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error installing dependencies: {str(e)}[/red]")
            return False
            
    def install_tool(self, category, tool_name):
        """Install specific tool"""
        try:
            if category in self.tools and tool_name in self.tools[category]:
                command = self.tools[category][tool_name]
                console.print(f"[yellow]Installing {tool_name}...[/yellow]")
                subprocess.run(command, shell=True, check=True)
                console.print(f"[green]{tool_name} installed successfully![/green]")
                return True
            else:
                console.print(f"[red]Tool {tool_name} not found in category {category}[/red]")
                return False
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error installing {tool_name}: {str(e)}[/red]")
            return False
            
    def install_category(self, category):
        """Install all tools in a category"""
        if category not in self.tools:
            console.print(f"[red]Category {category} not found![/red]")
            return False
            
        success = True
        for tool_name in track(self.tools[category].keys(), description=f"Installing {category} tools..."):
            if not self.install_tool(category, tool_name):
                success = False
                
        return success
        
    def install_all(self):
        """Install all tools"""
        if not self.update_system():
            return False
            
        if not self.install_dependencies():
            return False
            
        for category in self.tools.keys():
            console.print(f"\n[cyan]Installing {category} tools...[/cyan]")
            self.install_category(category)
            
        console.print("\n[green]Installation complete![/green]")
        return True 