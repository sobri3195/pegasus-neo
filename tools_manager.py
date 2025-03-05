#!/usr/bin/env python3

import json
import os

class ToolsManager:
    def __init__(self):
        self.tools_file = "config/tools.json"
        self.load_tools()

    def load_tools(self):
        if not os.path.exists("config"):
            os.makedirs("config")
            
        if not os.path.exists(self.tools_file):
            self.create_default_tools()
        
        with open(self.tools_file, 'r') as f:
            self.tools = json.load(f)

    def create_default_tools(self):
        default_tools = {
            "Wireless Hacking": {
                "1": {"name": "Aircrack-ng", "cmd": "aircrack-ng", "desc": "Complete suite for wireless hacking"},
                "2": {"name": "Kismet", "cmd": "kismet", "desc": "Wireless network detector and sniffer"},
                "3": {"name": "Reaver", "cmd": "reaver", "desc": "WPS brute force attack tool"},
                "4": {"name": "Wifite", "cmd": "wifite", "desc": "Automated wireless attack tool"},
                "5": {"name": "Fern Wifi Cracker", "cmd": "fern-wifi-cracker", "desc": "Wireless security auditing tool"}
            },
            "Web Hacking": {
                "1": {"name": "Burp Suite", "cmd": "burpsuite", "desc": "Web vulnerability scanner"},
                "2": {"name": "OWASP ZAP", "cmd": "zaproxy", "desc": "Web app security scanner"},
                "3": {"name": "Nikto", "cmd": "nikto", "desc": "Web server scanner"},
                "4": {"name": "WPScan", "cmd": "wpscan", "desc": "WordPress vulnerability scanner"},
                "5": {"name": "Dirbuster", "cmd": "dirbuster", "desc": "Directory brute forcing tool"}
            },
            "MITM & Sniffing": {
                "1": {"name": "Bettercap", "cmd": "bettercap", "desc": "Swiss army knife for network attacks"},
                "2": {"name": "Ettercap", "cmd": "ettercap", "desc": "Network protocol analyzer"},
                "3": {"name": "Wireshark", "cmd": "wireshark", "desc": "Network protocol analyzer"},
                "4": {"name": "Evilginx", "cmd": "evilginx", "desc": "MITM attack framework"},
                "5": {"name": "MITMproxy", "cmd": "mitmproxy", "desc": "Interactive MITM proxy"}
            }
        }
        
        with open(self.tools_file, 'w') as f:
            json.dump(default_tools, f, indent=4)
        
        self.tools = default_tools

    def get_tools(self):
        return self.tools

    def add_tool(self, category, name, cmd, desc):
        if category not in self.tools:
            self.tools[category] = {}
            
        tool_number = str(len(self.tools[category]) + 1)
        self.tools[category][tool_number] = {
            "name": name,
            "cmd": cmd,
            "desc": desc
        }
        
        self.save_tools()

    def save_tools(self):
        with open(self.tools_file, 'w') as f:
            json.dump(self.tools, f, indent=4) 