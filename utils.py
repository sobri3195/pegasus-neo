#!/usr/bin/env python3

import os
import sys
import hashlib
from rich.progress import Progress
from time import sleep

def check_root():
    """Check if script is running as root"""
    if os.geteuid() != 0:
        print("This script must be run as root!")
        sys.exit(1)

def check_dependencies():
    """Check if required tools are installed"""
    required_tools = [
        "nmap", "theHarvester", "metasploit-framework",
        "sqlmap", "aircrack-ng", "kismet", "wireshark",
        "burpsuite", "hydra", "hashcat"
    ]

    missing_tools = []
    for tool in required_tools:
        if os.system(f"which {tool} > /dev/null 2>&1") != 0:
            missing_tools.append(tool)

    # Optional: show warning if tools missing but continue
    if missing_tools:
        from rich.console import Console
        console = Console()
        console.print(f"[yellow]Warning: Some tools may not be installed: {', '.join(missing_tools)}[/yellow]")
        console.print("[yellow]Some features may not work properly. Install tools from the Install Tools menu.[/yellow]")

    return missing_tools

def hash_password(password):
    """Create SHA-256 hash of password"""
    return hashlib.sha256(password.encode()).hexdigest()

def show_loading_animation():
    """Show a loading progress bar"""
    with Progress() as progress:
        task = progress.add_task("[cyan]Loading...", total=100)
        while not progress.finished:
            progress.update(task, advance=0.5)
            sleep(0.02) 