#!/usr/bin/env python3

import os
import re
from rich.console import Console
from rich.table import Table
from rich.progress import track
import json
from datetime import datetime

console = Console()

class CodeScanner:
    def __init__(self):
        self.output_dir = "output/scan_results"
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.security_patterns = {
            "SQL Injection": [
                r"SELECT.*FROM.*WHERE",
                r"execute\(['\"].*SELECT",
                r"query\(['\"].*'",
                r"format.*%.*s"
            ],
            "XSS": [
                r"innerHTML\s*=",
                r"document\.write",
                r"eval\(",
                r"dangerouslySetInnerHTML"
            ],
            "Hardcoded Credentials": [
                r"[pP]assword\s*=\s*['\"][^'\"]+['\"]",
                r"[aA]pi[_-]?[kK]ey\s*=\s*['\"][^'\"]+['\"]",
                r"[sS]ecret[_-]?[kK]ey\s*=\s*['\"][^'\"]+['\"]",
                r"token\s*=\s*['\"][^'\"]+['\"]"
            ],
            "Weak Encryption": [
                r"md5\(",
                r"sha1\(",
                r"base64\.encode",
                r"rot13"
            ],
            "Command Injection": [
                r"os\.system\(",
                r"subprocess\.call\(.*shell=True",
                r"exec\(",
                r"popen\("
            ]
        }
        
        self.file_extensions = ['.py', '.js', '.php', '.java', '.rb', '.go', '.ts', '.jsx']
    
    def scan_directory(self, directory):
        """Scan directory for security issues"""
        try:
            console.print(f"[yellow]Scanning directory: {directory}[/yellow]")
            
            findings = {}
            
            for root, dirs, files in track(list(os.walk(directory)), description="Scanning files..."):
                for file in files:
                    if any(file.endswith(ext) for ext in self.file_extensions):
                        filepath = os.path.join(root, file)
                        file_findings = self.scan_file(filepath)
                        
                        if file_findings:
                            findings[filepath] = file_findings
            
            self.display_findings(findings)
            return findings
            
        except Exception as e:
            console.print(f"[bold red]Error scanning directory: {str(e)}[/bold red]")
            return {}
    
    def scan_file(self, filepath):
        """Scan individual file for security issues"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            file_findings = []
            
            for category, patterns in self.security_patterns.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        lines = content[:match.start()].split('\n')
                        line_num = len(lines)
                        line_content = lines[-1].strip()
                        
                        file_findings.append({
                            "category": category,
                            "pattern": pattern,
                            "line": line_num,
                            "content": line_content[:100]
                        })
            
            return file_findings
            
        except Exception as e:
            console.print(f"[red]Error scanning {filepath}: {str(e)}[/red]")
            return []
    
    def display_findings(self, findings):
        """Display scan findings"""
        if not findings:
            console.print("[green]No security issues found![/green]")
            return
        
        total_issues = sum(len(issues) for issues in findings.values())
        console.print(f"[yellow]Found {total_issues} potential security issues[/yellow]\n")
        
        for filepath, issues in findings.items():
            console.print(f"[cyan]File: {filepath}[/cyan]")
            
            table = Table()
            table.add_column("Type", style="red")
            table.add_column("Line", style="cyan")
            table.add_column("Content", style="yellow")
            
            for issue in issues[:5]:  # Show first 5 per file
                table.add_row(
                    issue["category"],
                    str(issue["line"]),
                    issue["content"]
                )
            
            console.print(table)
    
    def scan_for_secrets(self, directory):
        """Scan for secrets and sensitive data"""
        try:
            secret_patterns = {
                "AWS Keys": r"AKIA[0-9A-Z]{16}",
                "Private Keys": r"-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----",
                "API Keys": r"[aA][pP][iI][_ -]?[kK][eE][yY]\s*[:=]\s*['\"][^'\"]+['\"]",
                "Database URLs": r"[a-z]+://[^\s:]+:[^\s@]+@[^\s]+",
                "JWT Tokens": r"eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+"
            }
            
            secrets_found = {}
            
            for root, dirs, files in os.walk(directory):
                for file in files:
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    for secret_type, pattern in secret_patterns.items():
                        matches = re.finditer(pattern, content)
                        for match in matches:
                            lines = content[:match.start()].split('\n')
                            line_num = len(lines)
                            
                            if secret_type not in secrets_found:
                                secrets_found[secret_type] = []
                            
                            secrets_found[secret_type].append({
                                "file": filepath,
                                "line": line_num,
                                "match": match.group()[:50]
                            })
            
            if secrets_found:
                table = Table(title="Secrets Found")
                table.add_column("Type", style="red")
                table.add_column("File", style="cyan")
                table.add_column("Line", style="yellow")
                
                for secret_type, matches in secrets_found.items():
                    for match in matches[:3]:
                        table.add_row(secret_type, match["file"], str(match["line"]))
                
                console.print(table)
            
            return secrets_found
            
        except Exception as e:
            console.print(f"[bold red]Error scanning for secrets: {str(e)}[/bold red]")
            return {}
    
    def save_results(self, findings):
        """Save scan results"""
        output_file = f"{self.output_dir}/scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, 'w') as f:
            json.dump(findings, f, indent=4)
        
        console.print(f"[green]Scan results saved to: {output_file}[/green]")
