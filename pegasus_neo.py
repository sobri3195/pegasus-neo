#!/usr/bin/env python3

import os
import sys
import time
import logging
from datetime import datetime
from pyfiglet import Figlet
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
import subprocess
from ascii_art import get_pegasus_art
from tools_manager import ToolsManager
from utils import check_root, check_dependencies, show_loading_animation
from modules.network_scanner import NetworkScanner
from modules.wireless_attacks import WirelessAttacks
from modules.web_attacks import WebAttacks
from modules.password_attacks import PasswordAttacks
from config.settings import *
from modules.social_engineering.phishing import PhishingServer
from modules.social_engineering.spear_phishing import SpearPhishing
from modules.exploitation.payload_generator import PayloadGenerator
from modules.post_exploitation.persistence import Persistence
from modules.tracking.location_tracker import LocationTracker
from modules.tracking.social_tracker import SocialTracker
from modules.tracking.email_tracker import EmailTracker
from modules.tracking.phone_tracker import PhoneTracker
from modules.security.code_protection import CodeProtection
from modules.installer.tools_installer import ToolsInstaller

# Setup logging
logging.basicConfig(
    filename='pegasus_neo.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

console = Console()

# Tools dictionary
TOOLS = {
    "Reconnaissance & OSINT": {
        "1": {"name": "Nmap", "cmd": "nmap", "desc": "Network scanning tool"},
        "2": {"name": "theHarvester", "cmd": "theHarvester", "desc": "E-mail and subdomain harvesting"},
        "3": {"name": "Shodan", "cmd": "shodan", "desc": "Search engine for Internet-connected devices"},
        "4": {"name": "Recon-ng", "cmd": "recon-ng", "desc": "Web reconnaissance framework"},
        "5": {"name": "Maltego", "cmd": "maltego", "desc": "Open source intelligence tool"},
    },
    "Exploitation & Pentesting": {
        "1": {"name": "Metasploit", "cmd": "msfconsole", "desc": "Penetration testing framework"},
        "2": {"name": "SQLMap", "cmd": "sqlmap", "desc": "SQL injection tool"},
        "3": {"name": "Hydra", "cmd": "hydra", "desc": "Password cracking tool"},
        "4": {"name": "Hashcat", "cmd": "hashcat", "desc": "Password recovery tool"},
        "5": {"name": "BeEF", "cmd": "beef-xss", "desc": "Browser exploitation framework"},
    },
    "Tracking Tools": {
        "1": {"name": "Trape", "cmd": "trape", "desc": "OSINT Analysis and tracking tool"},
        "2": {"name": "Sherlock", "cmd": "sherlock", "desc": "Social media username tracker"},
        "3": {"name": "UserRecon", "cmd": "userrecon", "desc": "Username reconnaissance tool"},
        "4": {"name": "Holehe", "cmd": "holehe", "desc": "Email OSINT tool"},
        "5": {"name": "GeoSpy", "cmd": "geospy", "desc": "Geolocation tracking tool"},
    }
}

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def display_banner():
    clear_screen()
    f = Figlet(font='slant')
    banner = f.renderText('PEGASUS-NEO')
    console.print(Panel(banner, style="bold cyan"))
    console.print(Panel.fit(get_pegasus_art(), style="bold blue"))
    console.print("\n[bold yellow]Developed by: Letda Kes dr. Sobri[/bold yellow]")
    console.print("[bold green]Version: 1.0[/bold green]\n")

def authenticate():
    password = Prompt.ask("🔒 Enter password", password=True)
    if password != "sobri":
        console.print("[bold red]❌ Authentication failed! Access denied.[/bold red]")
        logging.warning("Failed authentication attempt")
        sys.exit(1)
    console.print("[bold green]✅ Authentication successful![/bold green]")
    logging.info("Successful authentication")

def display_menu():
    table = Table(title="[bold cyan]PEGASUS-NEO MENU[/bold cyan]")
    table.add_column("Option", style="cyan")
    table.add_column("Category", style="green")
    table.add_column("Description", style="yellow")
    
    # Tools categories
    for i, category in enumerate(TOOLS.keys(), 1):
        table.add_row(str(i), category, "Standard tools")
    
    # Advanced modules
    module_start = len(TOOLS) + 1
    table.add_row(str(module_start), "Social Engineering", "Phishing & Email attacks")
    table.add_row(str(module_start + 1), "Exploitation", "Payload generation")
    table.add_row(str(module_start + 2), "Post Exploitation", "Persistence & more")
    table.add_row(str(module_start + 3), "Tracking", "IP Location, Username Search, Email Analysis")
    table.add_row(str(module_start + 4), "Install Tools", "Install hacking tools")
    table.add_row("0", "Exit", "Exit program")
    
    console.print(table)

def execute_tool(category, tool_number):
    try:
        tool = TOOLS[category][tool_number]
        console.print(f"\n[bold cyan]Executing {tool['name']}...[/bold cyan]")
        console.print(f"[yellow]Description: {tool['desc']}[/yellow]\n")
        
        # Create output directory if it doesn't exist
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Execute the tool and log the activity
        cmd = f"{tool['cmd']} 2>&1 | tee {output_dir}/{tool['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        subprocess.run(cmd, shell=True)
        
        logging.info(f"Executed tool: {tool['name']}")
        
    except KeyError:
        console.print("[bold red]Invalid tool selection![/bold red]")
        logging.error(f"Invalid tool selection: {category} - {tool_number}")
    except Exception as e:
        console.print(f"[bold red]Error executing tool: {str(e)}[/bold red]")
        logging.error(f"Tool execution error: {str(e)}")

def initialize_modules():
    """Initialize all attack modules"""
    modules = {
        "network": NetworkScanner(),
        "wireless": WirelessAttacks(),
        "web": WebAttacks(),
        "password": PasswordAttacks(),
        "phishing": PhishingServer(),
        "spear_phishing": SpearPhishing(),
        "payload_gen": PayloadGenerator(),
        "persistence": Persistence(),
        "location_tracker": LocationTracker(),
        "social_tracker": SocialTracker(),
        "email_tracker": EmailTracker(),
        "phone_tracker": PhoneTracker()
    }
    return modules

def handle_module(modules, module_name):
    """Handle advanced module execution"""
    try:
        if module_name == "Social Engineering":
            console.print("\n[cyan]Social Engineering Options:[/cyan]")
            console.print("1. Start Phishing Server")
            console.print("2. Send Spear Phishing Email")
            choice = Prompt.ask("Select option", choices=["1", "2"])
            
            if choice == "1":
                template = Prompt.ask("Enter template name (e.g. login)")
                target = Prompt.ask("Enter target site name")
                if modules["phishing"].create_template(template, target):
                    modules["phishing"].start_server()
            else:
                modules["spear_phishing"].setup_sender()
                target = Prompt.ask("Enter target email")
                subject = Prompt.ask("Enter email subject")
                template = Prompt.ask("Enter template file path")
                modules["spear_phishing"].send_email(target, subject, template)
                
        elif module_name == "Exploitation":
            modules["payload_gen"].list_payloads()
            platform = Prompt.ask("Enter target platform", choices=["windows", "linux", "android"])
            payload_type = Prompt.ask("Enter payload type", choices=["reverse_tcp", "reverse_https", "bind_tcp"])
            lhost = Prompt.ask("Enter LHOST")
            lport = Prompt.ask("Enter LPORT")
            modules["payload_gen"].generate_payload(platform, payload_type, lhost, lport)
            
        elif module_name == "Post Exploitation":
            payload_path = Prompt.ask("Enter payload path")
            platform = Prompt.ask("Enter target platform", choices=["windows", "linux"])
            modules["persistence"].install_persistence(payload_path, platform)
            
        elif module_name == "Tracking":
            console.print("\n[cyan]Tracking Options:[/cyan]")
            console.print("1. Track IP Location")
            console.print("2. Search Username")
            console.print("3. Analyze Email")
            console.print("4. Track Phone Number")
            console.print("5. Bulk Phone Tracking")
            choice = Prompt.ask("Select option", choices=["1", "2", "3", "4", "5"])
            
            if choice == "1":
                target_ip = Prompt.ask("Enter target IP")
                modules["location_tracker"].track_ip(target_ip)
            elif choice == "2":
                username = Prompt.ask("Enter username to search")
                modules["social_tracker"].search_username(username)
            elif choice == "3":
                email = Prompt.ask("Enter email to analyze")
                modules["email_tracker"].verify_email(email)
            elif choice == "4":
                phone = Prompt.ask("Enter phone number (e.g., 0812xxxxxxxx or +62812xxxxxxxx)")
                modules["phone_tracker"].track_phone(phone)
            else:
                phones = []
                console.print("[yellow]Enter phone numbers (one per line, empty line to finish):[/yellow]")
                while True:
                    phone = input()
                    if not phone:
                        break
                    phones.append(phone)
                if phones:
                    modules["phone_tracker"].bulk_track(phones)
                
        elif module_name == "Install Tools":
            installer = ToolsInstaller()
            console.print("\n[cyan]Install Tools Options:[/cyan]")
            console.print("1. Install All Tools")
            console.print("2. Install Reconnaissance & OSINT Tools")
            console.print("3. Install Exploitation Tools")
            console.print("4. Install Wireless Hacking Tools")
            console.print("5. Install Web Hacking Tools")
            console.print("6. Install MITM & Sniffing Tools")
            console.print("7. Install Anonymity Tools")
            console.print("8. Install Exploit Development Tools")
            
            choice = Prompt.ask("Select option", choices=["1", "2", "3", "4", "5", "6", "7", "8"])
            
            if choice == "1":
                installer.install_all()
            else:
                categories = {
                    "2": "Reconnaissance & OSINT",
                    "3": "Exploitation & Pentesting",
                    "4": "Wireless Hacking",
                    "5": "Web Hacking",
                    "6": "MITM & Sniffing",
                    "7": "Anonymity & Privacy",
                    "8": "Exploit Development"
                }
                installer.install_category(categories[choice])
                
    except Exception as e:
        console.print(f"[bold red]Error in module execution: {str(e)}[/bold red]")

def main():
    # Initialize code protection
    protector = CodeProtection()
    
    # Verify code integrity
    if not protector.verify_integrity([__file__]):
        console.print("[bold red]Critical: Source code integrity check failed![/bold red]")
        console.print("[red]The program may have been tampered with.[/red]")
        sys.exit(1)
    
    # Check if running as root
    check_root()
    
    # Check dependencies
    missing_tools = check_dependencies()
    if missing_tools:
        console.print("[bold red]Missing required tools:[/bold red]")
        for tool in missing_tools:
            console.print(f"[red]- {tool}[/red]")
        sys.exit(1)
    
    # Show loading animation
    show_loading_animation()
    
    # Load additional tools
    tools_manager = ToolsManager()
    TOOLS.update(tools_manager.get_tools())
    
    # Initialize modules
    modules = initialize_modules()
    
    display_banner()
    authenticate()
    
    while True:
        display_menu()
        choice = Prompt.ask("\n[bold cyan]Select category[/bold cyan]", default="0")
        
        if choice == "0":
            console.print("[bold yellow]Thank you for using Pegasus-Neo![/bold yellow]")
            logging.info("Program terminated normally")
            break
            
        try:
            choice_num = int(choice)
            if choice_num <= len(TOOLS):
                category = list(TOOLS.keys())[choice_num-1]
                console.print(f"\n[bold cyan]{category} Tools:[/bold cyan]")
                
                # Display tools in the selected category
                tools_table = Table()
                tools_table.add_column("Number", style="cyan")
                tools_table.add_column("Tool", style="green")
                tools_table.add_column("Description", style="yellow")
                
                for num, tool in TOOLS[category].items():
                    tools_table.add_row(num, tool["name"], tool["desc"])
                
                console.print(tools_table)
                
                tool_choice = Prompt.ask("[bold cyan]Select tool number[/bold cyan]")
                execute_tool(category, tool_choice)
            else:
                # Handle advanced modules
                module_num = choice_num - len(TOOLS)
                module_names = ["Social Engineering", "Exploitation", "Post Exploitation", "Tracking", "Install Tools"]
                if module_num <= len(module_names):
                    handle_module(modules, module_names[module_num-1])
                else:
                    raise ValueError("Invalid selection")
                
        except (ValueError, IndexError):
            console.print("[bold red]Invalid selection![/bold red]")
            logging.error(f"Invalid menu selection: {choice}")
            
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Program terminated by user.[/bold red]")
        logging.info("Program terminated by user (KeyboardInterrupt)")
        sys.exit(0) 