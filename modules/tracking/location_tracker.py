#!/usr/bin/env python3

import os
import requests
import json
import folium
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from datetime import datetime

console = Console()

class LocationTracker:
    def __init__(self):
        self.api_key = None  # IP Geolocation API key
        self.output_dir = "output/tracking"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def setup_api(self):
        """Setup API credentials"""
        self.api_key = Prompt.ask("[cyan]Enter IP Geolocation API key")
        
    def track_ip(self, target_ip):
        """Track IP address location"""
        try:
            url = f"http://ip-api.com/json/{target_ip}"
            response = requests.get(url)
            data = response.json()
            
            if data['status'] == 'success':
                table = Table(title=f"Location Data for {target_ip}")
                table.add_column("Field", style="cyan")
                table.add_column("Value", style="yellow")
                
                fields = ['country', 'regionName', 'city', 'lat', 'lon', 'isp', 'org']
                for field in fields:
                    if field in data:
                        table.add_row(field.capitalize(), str(data[field]))
                
                console.print(table)
                
                # Generate map
                map_file = f"{self.output_dir}/ip_location_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                m = folium.Map(location=[data['lat'], data['lon']], zoom_start=12)
                folium.Marker(
                    [data['lat'], data['lon']],
                    popup=f"IP: {target_ip}\nISP: {data['isp']}",
                    icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(m)
                m.save(map_file)
                
                console.print(f"[green]Map saved to: {map_file}[/green]")
                return data
                
            else:
                console.print("[red]Failed to get location data[/red]")
                return None
                
        except Exception as e:
            console.print(f"[bold red]Error tracking IP: {str(e)}[/bold red]")
            return None 