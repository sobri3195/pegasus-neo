#!/usr/bin/env python3

import dns.resolver
from rich.console import Console
from rich.table import Table
import requests
import json
from datetime import datetime

console = Console()

class EmailTracker:
    def __init__(self):
        self.output_dir = "output/tracking"
        
    def verify_email(self, email):
        """Verify email existence and gather information"""
        try:
            domain = email.split('@')[1]
            results = {
                "email": email,
                "domain": domain,
                "mx_records": [],
                "disposable": False,
                "breached": False
            }
            
            # Check MX records
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                for mx in mx_records:
                    results["mx_records"].append(str(mx.exchange))
            except:
                results["mx_records"] = ["No MX records found"]
            
            # Check if domain is disposable
            disposable_domains = ["tempmail.com", "10minutemail.com"]  # Add more
            if domain in disposable_domains:
                results["disposable"] = True
            
            # Check for breaches (simulated - you'd need an actual API for this)
            breach_check_url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            try:
                response = requests.get(breach_check_url)
                if response.status_code == 200:
                    results["breached"] = True
            except:
                pass
            
            # Display results
            table = Table(title=f"Email Analysis Results for {email}")
            table.add_column("Check", style="cyan")
            table.add_column("Result", style="yellow")
            
            table.add_row("Domain", domain)
            table.add_row("MX Records", "\n".join(results["mx_records"]))
            table.add_row("Disposable", "Yes" if results["disposable"] else "No")
            table.add_row("Found in Breaches", "Yes" if results["breached"] else "No")
            
            console.print(table)
            
            # Save results
            output_file = f"{self.output_dir}/email_analysis_{email}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=4)
                
            console.print(f"[green]Results saved to: {output_file}[/green]")
            return results
            
        except Exception as e:
            console.print(f"[bold red]Error analyzing email: {str(e)}[/bold red]")
            return None 