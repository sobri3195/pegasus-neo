#!/usr/bin/env python3

# Application settings
APP_NAME = "Pegasus-Neo"
VERSION = "1.0"
AUTHOR = "Letda Kes dr. Sobri"

# Default paths
OUTPUT_DIR = "output"
WORDLISTS_DIR = "wordlists"
LOG_FILE = "pegasus_neo.log"

# Tool configurations
TOOL_SETTINGS = {
    "network_scan": {
        "default_ports": "1-1000",
        "timeout": 60,
        "aggressive_mode": False
    },
    "wireless": {
        "default_interface": "wlan0",
        "channel_hop_time": 2,
        "capture_time": 300
    },
    "web": {
        "timeout": 30,
        "max_retries": 3,
        "user_agent": "Pegasus-Neo/1.0"
    }
}

# Color schemes
COLORS = {
    "primary": "cyan",
    "secondary": "green",
    "warning": "yellow",
    "error": "red",
    "success": "green",
    "info": "blue"
} 