#!/usr/bin/env python3

import re
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.progress import track
import json
import os

console = Console()

class LogAnalyzer:
    def __init__(self):
        self.output_dir = "output/logs"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Common log patterns
        self.patterns = {
            "IP Address": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
            "Timestamp": r'\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}',
            "HTTP Method": r'\b(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\b',
            "HTTP Status": r'\s[1-5]\d{2}\s',
            "Error": r'\b(404|500|502|503)\b',
            "User Agent": r'[uU]ser-[aA]gent:[^\n]*',
            "URL": r'https?://[^\s<>"]+',
            "Email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        }
    
    def parse_log_file(self, filepath):
        """Parse and analyze log file"""
        try:
            console.print(f"[yellow]Parsing log file: {filepath}[/yellow]")
            
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            results = {
                "total_lines": len(lines),
                "patterns_found": {},
                "statistics": {}
            }
            
            # Find all patterns
            for pattern_name, pattern in self.patterns.items():
                matches = []
                for line_num, line in enumerate(lines, 1):
                    found = re.findall(pattern, line)
                    if found:
                        matches.extend([(line_num, match) for match in found])
                
                if matches:
                    results["patterns_found"][pattern_name] = {
                        "count": len(matches),
                        "samples": matches[:10]
                    }
            
            self.display_results(results)
            return results
            
        except Exception as e:
            console.print(f"[bold red]Error parsing log file: {str(e)}[/bold red]")
            return None
    
    def analyze_apache_logs(self, filepath):
        """Analyze Apache access logs"""
        try:
            console.print(f"[yellow]Analyzing Apache log: {filepath}[/yellow]")
            
            # Apache Combined Log Format pattern
            apache_pattern = r'(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+) (\S+)" (\d{3}) (\d+|-) "([^"]*)" "([^"]*)"'
            
            stats = {
                "total_requests": 0,
                "methods": {},
                "status_codes": {},
                "top_ips": {},
                "top_urls": {},
                "errors": 0
            }
            
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    match = re.match(apache_pattern, line)
                    if match:
                        stats["total_requests"] += 1
                        
                        ip = match.group(1)
                        method = match.group(5)
                        status = int(match.group(8))
                        url = match.group(6)
                        
                        # Count methods
                        stats["methods"][method] = stats["methods"].get(method, 0) + 1
                        
                        # Count status codes
                        stats["status_codes"][status] = stats["status_codes"].get(status, 0) + 1
                        
                        # Track top IPs
                        stats["top_ips"][ip] = stats["top_ips"].get(ip, 0) + 1
                        
                        # Track top URLs
                        stats["top_urls"][url] = stats["top_urls"].get(url, 0) + 1
                        
                        # Count errors (4xx and 5xx)
                        if status >= 400:
                            stats["errors"] += 1
            
            self.display_apache_stats(stats)
            return stats
            
        except Exception as e:
            console.print(f"[bold red]Error analyzing Apache logs: {str(e)}[/bold red]")
            return None
    
    def analyze_errors(self, filepath):
        """Extract and analyze error messages"""
        try:
            console.print(f"[yellow]Analyzing errors in: {filepath}[/yellow]")
            
            error_patterns = [
                r'\b(error|Error|ERROR|exception|Exception|EXCEPTION)\b',
                r'\b(failed|Failed|FAILED|failure|Failure)\b',
                r'\b(critical|Critical|CRITICAL)\b',
                r'\b(warning|Warning|WARNING)\b'
            ]
            
            errors = []
            
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    for pattern in error_patterns:
                        if re.search(pattern, line):
                            errors.append({
                                "line": line_num,
                                "content": line.strip()[:100]
                            })
                            break
            
            if errors:
                table = Table(title=f"Errors Found ({len(errors)})")
                table.add_column("Line", style="cyan")
                table.add_column("Content", style="yellow")
                
                for error in errors[:20]:
                    table.add_row(str(error["line"]), error["content"])
                
                console.print(table)
            else:
                console.print("[green]No errors found[/green]")
            
            return errors
            
        except Exception as e:
            console.print(f"[bold red]Error analyzing: {str(e)}[/bold red]")
            return []
    
    def find_ip_activity(self, filepath, ip_address):
        """Find all activity from specific IP"""
        try:
            console.print(f"[yellow]Searching for IP: {ip_address}[/yellow]")
            
            activities = []
            
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    if ip_address in line:
                        activities.append({
                            "line": line_num,
                            "content": line.strip()
                        })
            
            if activities:
                table = Table(title=f"Activity from {ip_address} ({len(activities)} entries)")
                table.add_column("Line", style="cyan")
                table.add_column("Activity", style="yellow")
                
                for activity in activities[:20]:
                    table.add_row(str(activity["line"]), activity["content"])
                
                console.print(table)
            else:
                console.print("[yellow]No activity found for this IP[/yellow]")
            
            return activities
            
        except Exception as e:
            console.print(f"[bold red]Error searching IP: {str(e)}[/bold red]")
            return []
    
    def display_results(self, results):
        """Display analysis results"""
        table = Table(title="Log Analysis Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="yellow")
        
        table.add_row("Total Lines", str(results["total_lines"]))
        table.add_row("Patterns Found", str(len(results["patterns_found"])))
        
        console.print(table)
        
        if results["patterns_found"]:
            console.print("\n[cyan]Pattern Matches:[/cyan]")
            for pattern_name, data in results["patterns_found"].items():
                console.print(f"  [green]{pattern_name}[/green]: {data['count']} matches")
    
    def display_apache_stats(self, stats):
        """Display Apache statistics"""
        table = Table(title="Apache Log Statistics")
        table.add_column("Metric", style="cyan")
        table.add_row("Total Requests", str(stats["total_requests"]))
        table.add_row("Total Errors", f"[red]{stats['errors']}[/red]")
        
        console.print(table)
        
        # Show top IPs
        if stats["top_ips"]:
            console.print("\n[cyan]Top IP Addresses:[/cyan]")
            top_table = Table()
            top_table.add_column("IP", style="yellow")
            top_table.add_column("Requests", style="green")
            
            for ip, count in sorted(stats["top_ips"].items(), key=lambda x: x[1], reverse=True)[:10]:
                top_table.add_row(ip, str(count))
            
            console.print(top_table)
        
        # Show status codes
        if stats["status_codes"]:
            console.print("\n[cyan]Status Code Distribution:[/cyan]")
            status_table = Table()
            status_table.add_column("Status", style="yellow")
            status_table.add_column("Count", style="green")
            
            for status, count in sorted(stats["status_codes"].items()):
                color = "red" if status >= 400 else "green"
                status_table.add_row(f"[{color}]{status}[/{color}]", str(count))
            
            console.print(status_table)
    
    def save_report(self, report, report_type):
        """Save analysis report"""
        output_file = f"{self.output_dir}/{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=4)
        
        console.print(f"[green]Report saved to: {output_file}[/green]")
