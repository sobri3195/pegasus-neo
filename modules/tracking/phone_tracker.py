#!/usr/bin/env python3

import os
import requests
import json
import re
from rich.console import Console
from rich.table import Table
from rich.progress import track
from datetime import datetime
from bs4 import BeautifulSoup

console = Console()

class PhoneTracker:
    def __init__(self):
        self.output_dir = "output/tracking"
        os.makedirs(self.output_dir, exist_ok=True)
        self.providers = {
            "0811": "Telkomsel", "0812": "Telkomsel", "0813": "Telkomsel", "0821": "Telkomsel", "0822": "Telkomsel",
            "0851": "Telkomsel", "0852": "Telkomsel", "0853": "Telkomsel",
            "0814": "Indosat", "0815": "Indosat", "0816": "Indosat", "0855": "Indosat", "0856": "Indosat", "0857": "Indosat", "0858": "Indosat",
            "0817": "XL", "0818": "XL", "0819": "XL", "0859": "XL", "0877": "XL", "0878": "XL",
            "0831": "Axis", "0832": "Axis", "0833": "Axis", "0838": "Axis",
            "0895": "Three", "0896": "Three", "0897": "Three", "0898": "Three", "0899": "Three"
        }
        
    def normalize_number(self, phone):
        """Normalize phone number format"""
        # Remove any non-digit characters
        phone = re.sub(r'\D', '', phone)
        
        # Convert common Indonesia formats
        if phone.startswith('62'):
            phone = '0' + phone[2:]
        elif phone.startswith('+62'):
            phone = '0' + phone[3:]
            
        return phone
        
    def get_provider_info(self, phone):
        """Get provider information"""
        prefix = phone[:4]
        return self.providers.get(prefix, "Unknown Provider")
        
    def check_whatsapp(self, phone):
        """Check if number is registered on WhatsApp"""
        try:
            # Using wa.me API to check number
            phone = phone.replace('+', '').replace('-', '')
            if phone.startswith('0'):
                phone = '62' + phone[1:]
                
            url = f"https://api.whatsapp.com/send/?phone={phone}"
            response = requests.get(url)
            
            # If redirects to chat, number exists
            return 'chat' in response.url
            
        except Exception:
            return False
            
    def track_location(self, phone):
        """Track approximate location based on provider and prefix"""
        provider = self.get_provider_info(phone)
        prefix = phone[:4]
        
        # Simplified location mapping (could be expanded)
        location_map = {
            "0811": "Jakarta/Jabodetabek",
            "0812": "Jawa/Sumatera",
            "0813": "Jawa/Kalimantan",
            "0821": "Nasional",
            "0822": "Nasional",
            "0851": "Nasional",
            "0852": "Nasional",
            "0853": "Nasional",
            "0814": "Sumatera",
            "0815": "Jawa Barat",
            "0816": "Jakarta/Jabodetabek",
            "0855": "Nasional",
            "0856": "Nasional",
            "0857": "Nasional",
            "0858": "Nasional",
            "0817": "Jakarta/Jabodetabek",
            "0818": "Jakarta/Jabodetabek",
            "0819": "Jakarta/Jabodetabek",
            "0859": "Nasional",
            "0877": "Nasional",
            "0878": "Nasional",
            "0831": "Jawa/Sumatera",
            "0832": "Nasional",
            "0833": "Nasional",
            "0838": "Nasional",
            "0895": "Nasional",
            "0896": "Nasional",
            "0897": "Nasional",
            "0898": "Nasional",
            "0899": "Nasional"
        }
        
        return location_map.get(prefix, "Unknown Location")
        
    def track_phone(self, phone_number):
        """Track Indonesian phone number"""
        try:
            # Normalize number format
            phone = self.normalize_number(phone_number)
            
            if not phone.startswith('0') or len(phone) < 10:
                console.print("[red]Invalid Indonesian phone number format![/red]")
                return None
                
            results = {
                "phone": phone,
                "provider": self.get_provider_info(phone),
                "location": self.track_location(phone),
                "whatsapp": self.check_whatsapp(phone),
                "type": "Mobile",
                "country": "Indonesia",
                "prefix": phone[:4]
            }
            
            # Display results
            table = Table(title=f"Phone Number Analysis Results for {phone}")
            table.add_column("Information", style="cyan")
            table.add_column("Details", style="yellow")
            
            table.add_row("Phone Number", phone)
            table.add_row("Provider", results["provider"])
            table.add_row("Region", results["location"])
            table.add_row("WhatsApp", "✓ Registered" if results["whatsapp"] else "✗ Not Found")
            table.add_row("Type", results["type"])
            table.add_row("Country", results["country"])
            table.add_row("Prefix", results["prefix"])
            
            console.print(table)
            
            # Additional WhatsApp info if available
            if results["whatsapp"]:
                console.print("\n[green]WhatsApp Link:[/green]")
                console.print(f"https://wa.me/{phone.replace('0', '62', 1)}")
            
            # Save results
            output_file = f"{self.output_dir}/phone_analysis_{phone}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=4)
                
            console.print(f"\n[green]Results saved to: {output_file}[/green]")
            return results
            
        except Exception as e:
            console.print(f"[bold red]Error analyzing phone number: {str(e)}[/bold red]")
            return None
            
    def bulk_track(self, phone_list):
        """Track multiple phone numbers"""
        results = []
        for phone in track(phone_list, description="Analyzing phone numbers..."):
            result = self.track_phone(phone)
            if result:
                results.append(result)
                
        # Save bulk results
        if results:
            output_file = f"{self.output_dir}/bulk_phone_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=4)
            console.print(f"\n[green]Bulk results saved to: {output_file}[/green]") 