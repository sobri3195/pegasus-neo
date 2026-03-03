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
from modules.vulnerability_scanner import VulnerabilityScanner
from modules.password_generator import PasswordGenerator
from modules.honeytoken import HoneytokenGenerator
from modules.network_sniffer import NetworkSniffer
from modules.code_scanner import CodeScanner
from modules.forensic_analyzer import ForensicAnalyzer
from modules.steganography import SteganographyTool
from modules.encryption_tool import EncryptionTool
from modules.log_analyzer import LogAnalyzer
from modules.port_scanner import PortScanner
from cryptography.fernet import Fernet

# Setup logging
logging.basicConfig(
    filename='pegasus_neo.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

console = Console()


def ask_int(prompt, default=None, min_value=None, max_value=None):
    """Ask for integer input with retry and bounds validation."""
    while True:
        value = Prompt.ask(prompt, default=str(default) if default is not None else None)
        try:
            num = int(value)
        except ValueError:
            console.print("[red]Input harus berupa angka.[/red]")
            continue

        if min_value is not None and num < min_value:
            console.print(f"[red]Nilai minimum adalah {min_value}.[/red]")
            continue
        if max_value is not None and num > max_value:
            console.print(f"[red]Nilai maksimum adalah {max_value}.[/red]")
            continue

        return num


def ask_fernet_key(prompt="Enter encryption key"):
    """Get and validate Fernet key input before operation."""
    while True:
        key = Prompt.ask(prompt).strip().encode()
        try:
            Fernet(key)
            return key
        except Exception:
            console.print("[red]Kunci tidak valid. Gunakan key dari menu Generate Encryption Key.[/red]")

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
    console.print("[bold green]Version: 2.0[/bold green]\n")

def authenticate():
    password = Prompt.ask("🔒 Enter password", password=True).strip()
    if password.lower() != "sobri":
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
    table.add_row(str(module_start + 5), "Vulnerability Scanner", "Security vulnerability scanning")
    table.add_row(str(module_start + 6), "Password Generator", "Generate secure passwords")
    table.add_row(str(module_start + 7), "Honeytoken Generator", "Create decoy credentials")
    table.add_row(str(module_start + 8), "Network Sniffer", "Packet capture & analysis")
    table.add_row(str(module_start + 9), "Code Scanner", "Security code analysis")
    table.add_row(str(module_start + 10), "Forensic Analyzer", "File & directory forensics")
    table.add_row(str(module_start + 11), "Steganography Tool", "Encoding & decoding tools")
    table.add_row(str(module_start + 12), "Encryption Tool", "File & message encryption")
    table.add_row(str(module_start + 13), "Log Analyzer", "Parse and analyze logs")
    table.add_row(str(module_start + 14), "Port Scanner", "Advanced port scanning")
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
        "phone_tracker": PhoneTracker(),
        "vulnerability_scanner": VulnerabilityScanner(),
        "password_generator": PasswordGenerator(),
        "honeytoken": HoneytokenGenerator(),
        "network_sniffer": NetworkSniffer(),
        "code_scanner": CodeScanner(),
        "forensic_analyzer": ForensicAnalyzer(),
        "steganography": SteganographyTool(),
        "encryption_tool": EncryptionTool(),
        "log_analyzer": LogAnalyzer(),
        "port_scanner": PortScanner()
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

        elif module_name == "Vulnerability Scanner":
            console.print("\n[cyan]Vulnerability Scanner Options:[/cyan]")
            console.print("1. Scan Open Ports")
            console.print("2. Check SSL Certificate")
            console.print("3. Check HTTP Security Headers")
            choice = Prompt.ask("Select option", choices=["1", "2", "3"])

            if choice == "1":
                target = Prompt.ask("Enter target IP or hostname")
                modules["vulnerability_scanner"].scan_open_ports(target)
            elif choice == "2":
                hostname = Prompt.ask("Enter hostname")
                modules["vulnerability_scanner"].check_ssl_cert(hostname)
            elif choice == "3":
                url = Prompt.ask("Enter target URL (e.g., https://example.com)")
                modules["vulnerability_scanner"].check_http_headers(url)

        elif module_name == "Password Generator":
            console.print("\n[cyan]Password Generator Options:[/cyan]")
            console.print("1. Generate Secure Password")
            console.print("2. Generate Passphrase")
            console.print("3. Check Password Strength")
            choice = Prompt.ask("Select option", choices=["1", "2", "3"])

            if choice == "1":
                length = ask_int("Enter password length", default=16, min_value=4, max_value=256)
                modules["password_generator"].generate_password(length=length)
            elif choice == "2":
                word_count = ask_int("Enter word count", default=5, min_value=2, max_value=20)
                modules["password_generator"].generate_passphrase(word_count=word_count)
            elif choice == "3":
                password = Prompt.ask("Enter password to check")
                modules["password_generator"].check_password_strength(password)

        elif module_name == "Honeytoken Generator":
            console.print("\n[cyan]Honeytoken Generator Options:[/cyan]")
            console.print("1. Generate AWS Key")
            console.print("2. Generate Database URL")
            console.print("3. Generate API Key")
            console.print("4. Generate Canary Token")
            console.print("5. Generate SSH Key")
            choice = Prompt.ask("Select option", choices=["1", "2", "3", "4", "5"])

            token_map = {
                "1": ("generate_aws_key", "AWS Key"),
                "2": ("generate_database_url", "Database URL"),
                "3": ("generate_api_key", "API Key"),
                "4": ("generate_canary_token", "Canary Token"),
                "5": ("generate_ssh_key", "SSH Key")
            }
            method, name = token_map[choice]
            token = getattr(modules["honeytoken"], method)()
            modules["honeytoken"].display_honeytoken(token)
            modules["honeytoken"].save_honeytoken(token)

        elif module_name == "Network Sniffer":
            console.print("\n[cyan]Network Sniffer Options:[/cyan]")
            console.print("1. Start Packet Sniffing")
            console.print("2. Analyze Captured Traffic")
            console.print("3. Save Capture")
            choice = Prompt.ask("Select option", choices=["1", "2", "3"])

            if choice == "1":
                interface = Prompt.ask("Enter network interface (e.g., eth0)")
                count = ask_int("Enter number of packets to capture", default=100, min_value=1, max_value=100000)
                modules["network_sniffer"].start_sniffing(interface, count)
            elif choice == "2":
                modules["network_sniffer"].analyze_traffic()
            elif choice == "3":
                modules["network_sniffer"].save_capture()

        elif module_name == "Code Scanner":
            console.print("\n[cyan]Code Scanner Options:[/cyan]")
            console.print("1. Scan Directory for Security Issues")
            console.print("2. Scan for Secrets")
            choice = Prompt.ask("Select option", choices=["1", "2"])

            directory = Prompt.ask("Enter directory path")
            if choice == "1":
                findings = modules["code_scanner"].scan_directory(directory)
                if findings:
                    modules["code_scanner"].save_results(findings)
            elif choice == "2":
                modules["code_scanner"].scan_for_secrets(directory)

        elif module_name == "Forensic Analyzer":
            console.print("\n[cyan]Forensic Analyzer Options:[/cyan]")
            console.print("1. Analyze File")
            console.print("2. Scan Directory")
            console.print("3. Find Duplicate Files")
            console.print("4. Create File Timeline")
            choice = Prompt.ask("Select option", choices=["1", "2", "3", "4"])

            if choice == "1":
                filepath = Prompt.ask("Enter file path")
                modules["forensic_analyzer"].analyze_file(filepath)
            elif choice == "2":
                directory = Prompt.ask("Enter directory path")
                modules["forensic_analyzer"].scan_directory(directory)
            elif choice == "3":
                directory = Prompt.ask("Enter directory path")
                modules["forensic_analyzer"].find_duplicates(directory)
            elif choice == "4":
                directory = Prompt.ask("Enter directory path")
                modules["forensic_analyzer"].create_timeline(directory)

        elif module_name == "Steganography Tool":
            console.print("\n[cyan]Steganography Tool Options:[/cyan]")
            console.print("1. Base64 Encode")
            console.print("2. Base64 Decode")
            console.print("3. Hex Encode")
            console.print("4. Hex Decode")
            console.print("5. ROT13 Encode/Decode")
            console.print("6. Caesar Cipher")
            console.print("7. Reverse String")
            console.print("8. Binary Encode")
            console.print("9. Binary Decode")
            choice = Prompt.ask("Select option", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9"])

            message = Prompt.ask("Enter message/text")
            if choice == "1":
                modules["steganography"].encode_base64(message)
            elif choice == "2":
                modules["steganography"].decode_base64(message)
            elif choice == "3":
                modules["steganography"].encode_hex(message)
            elif choice == "4":
                modules["steganography"].decode_hex(message)
            elif choice == "5":
                modules["steganography"].rot13_encode(message)
            elif choice == "6":
                shift = ask_int("Enter shift amount", default=3, min_value=-1000, max_value=1000)
                modules["steganography"].caesar_cipher(message, shift)
            elif choice == "7":
                modules["steganography"].reverse_string(message)
            elif choice == "8":
                modules["steganography"].binary_encode(message)
            elif choice == "9":
                modules["steganography"].binary_decode(message)

        elif module_name == "Encryption Tool":
            console.print("\n[cyan]Encryption Tool Options:[/cyan]")
            console.print("1. Generate Encryption Key")
            console.print("2. Encrypt Message")
            console.print("3. Decrypt Message")
            console.print("4. Encrypt File")
            console.print("5. Decrypt File")
            console.print("6. Hash File")
            console.print("7. Create Password Hash")
            choice = Prompt.ask("Select option", choices=["1", "2", "3", "4", "5", "6", "7"])

            if choice == "1":
                modules["encryption_tool"].generate_key()
            elif choice in ["2", "3"]:
                message = Prompt.ask("Enter message")
                key = ask_fernet_key("Enter encryption key")
                if choice == "2":
                    modules["encryption_tool"].encrypt_message(message, key)
                else:
                    modules["encryption_tool"].decrypt_message(message.encode(), key)
            elif choice in ["4", "5"]:
                filepath = Prompt.ask("Enter file path")
                key = ask_fernet_key("Enter encryption key")
                if choice == "4":
                    modules["encryption_tool"].encrypt_file(filepath, key)
                else:
                    modules["encryption_tool"].decrypt_file(filepath, key)
            elif choice == "6":
                filepath = Prompt.ask("Enter file path")
                modules["encryption_tool"].hash_file(filepath)
            elif choice == "7":
                password = Prompt.ask("Enter password")
                modules["encryption_tool"].create_password_hash(password)

        elif module_name == "Log Analyzer":
            console.print("\n[cyan]Log Analyzer Options:[/cyan]")
            console.print("1. Parse Log File")
            console.print("2. Analyze Apache Logs")
            console.print("3. Analyze Errors")
            console.print("4. Find IP Activity")
            choice = Prompt.ask("Select option", choices=["1", "2", "3", "4"])

            logfile = Prompt.ask("Enter log file path")
            if choice == "1":
                modules["log_analyzer"].parse_log_file(logfile)
            elif choice == "2":
                modules["log_analyzer"].analyze_apache_logs(logfile)
            elif choice == "3":
                modules["log_analyzer"].analyze_errors(logfile)
            elif choice == "4":
                ip = Prompt.ask("Enter IP address to search")
                modules["log_analyzer"].find_ip_activity(logfile, ip)

        elif module_name == "Port Scanner":
            console.print("\n[cyan]Port Scanner Options:[/cyan]")
            console.print("1. Quick Scan (Common Ports)")
            console.print("2. Full Scan (All Ports)")
            console.print("3. Detect Service Versions")
            console.print("4. Save Results")
            choice = Prompt.ask("Select option", choices=["1", "2", "3", "4"])

            target = Prompt.ask("Enter target IP or hostname")
            if choice == "1":
                modules["port_scanner"].quick_scan(target)
            elif choice == "2":
                console.print("[red]This may take a while...[/red]")
                start = ask_int("Start port", default=1, min_value=1, max_value=65535)
                end = ask_int("End port", default=65535, min_value=start, max_value=65535)
                modules["port_scanner"].full_scan(target, start, end)
            elif choice == "3":
                modules["port_scanner"].detect_service_versions(target)
            elif choice == "4":
                modules["port_scanner"].save_results(target)
                
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
        console.print("[bold yellow]Missing external tools detected. Advanced external commands may be unavailable:[/bold yellow]")
        for tool in missing_tools:
            console.print(f"[yellow]- {tool}[/yellow]")
        logging.warning(f"Missing tools: {', '.join(missing_tools)}")
    
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
                module_names = ["Social Engineering", "Exploitation", "Post Exploitation", "Tracking", "Install Tools",
                              "Vulnerability Scanner", "Password Generator", "Honeytoken Generator", "Network Sniffer",
                              "Code Scanner", "Forensic Analyzer", "Steganography Tool", "Encryption Tool",
                              "Log Analyzer", "Port Scanner"]
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
