#!/usr/bin/env python3

import os
import hashlib
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.progress import track

console = Console()

class ForensicAnalyzer:
    def __init__(self):
        self.output_dir = "output/forensic"
        os.makedirs(self.output_dir, exist_ok=True)
        self.file_hashes = {}
        
    def calculate_hashes(self, filepath):
        """Calculate multiple hash values"""
        hashes = {
            "md5": hashlib.md5(),
            "sha1": hashlib.sha1(),
            "sha256": hashlib.sha256()
        }
        
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                for hash_obj in hashes.values():
                    hash_obj.update(chunk)
        
        return {name: hash_obj.hexdigest() for name, hash_obj in hashes.items()}
    
    def analyze_file(self, filepath):
        """Perform forensic analysis on file"""
        try:
            if not os.path.exists(filepath):
                console.print(f"[red]File not found: {filepath}[/red]")
                return None
            
            stat_info = os.stat(filepath)
            hashes = self.calculate_hashes(filepath)
            
            analysis = {
                "filepath": filepath,
                "size": stat_info.st_size,
                "modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                "accessed": datetime.fromtimestamp(stat_info.st_atime).isoformat(),
                "created": datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
                "mode": oct(stat_info.st_mode),
                "md5": hashes['md5'],
                "sha1": hashes['sha1'],
                "sha256": hashes['sha256']
            }
            
            table = Table(title=f"File Analysis: {os.path.basename(filepath)}")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="yellow")
            
            table.add_row("Size", f"{stat_info.st_size:,} bytes")
            table.add_row("Modified", analysis['modified'])
            table.add_row("MD5", hashes['md5'])
            table.add_row("SHA256", hashes['sha256'])
            
            console.print(table)
            
            return analysis
            
        except Exception as e:
            console.print(f"[bold red]Error analyzing file: {str(e)}[/bold red]")
            return None
    
    def scan_directory(self, directory):
        """Scan directory and hash all files"""
        try:
            console.print(f"[yellow]Scanning directory: {directory}[/yellow]")
            
            all_files = []
            for root, dirs, files in track(list(os.walk(directory)), description="Finding files..."):
                for file in files:
                    filepath = os.path.join(root, file)
                    all_files.append(filepath)
            
            results = {}
            
            for filepath in track(all_files, description="Calculating hashes..."):
                try:
                    hashes = self.calculate_hashes(filepath)
                    stat_info = os.stat(filepath)
                    
                    results[filepath] = {
                        "size": stat_info.st_size,
                        "md5": hashes['md5'],
                        "sha256": hashes['sha256']
                    }
                except:
                    pass
            
            console.print(f"[green]Analyzed {len(results)} files[/green]")
            return results
            
        except Exception as e:
            console.print(f"[bold red]Error scanning directory: {str(e)}[/bold red]")
            return {}
    
    def find_duplicates(self, directory):
        """Find duplicate files by hash"""
        try:
            console.print(f"[yellow]Finding duplicates in: {directory}[/yellow]")
            
            hash_map = {}
            for root, dirs, files in os.walk(directory):
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        hashes = self.calculate_hashes(filepath)
                        md5_hash = hashes['md5']
                        
                        if md5_hash not in hash_map:
                            hash_map[md5_hash] = []
                        hash_map[md5_hash].append(filepath)
                    except:
                        pass
            
            duplicates = {h: files for h, files in hash_map.items() if len(files) > 1}
            
            if duplicates:
                table = Table(title="Duplicate Files Found")
                table.add_column("Hash", style="cyan")
                table.add_column("Files", style="yellow")
                
                for h, files in list(duplicates.items())[:5]:
                    table.add_row(h[:16] + "...", "\n".join([f for f in files]))
                
                console.print(table)
                console.print(f"[red]Found {len(duplicates)} sets of duplicates[/red]")
            else:
                console.print("[green]No duplicate files found[/green]")
            
            return duplicates
            
        except Exception as e:
            console.print(f"[bold red]Error finding duplicates: {str(e)}[/bold red]")
            return {}
    
    def create_timeline(self, directory):
        """Create timeline of file modifications"""
        try:
            console.print(f"[yellow]Creating timeline for: {directory}[/yellow]")
            
            timeline = []
            
            for root, dirs, files in os.walk(directory):
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        stat_info = os.stat(filepath)
                        timeline.append({
                            "filepath": filepath,
                            "modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                            "size": stat_info.st_size
                        })
                    except:
                        pass
            
            timeline.sort(key=lambda x: x['modified'])
            
            table = Table(title="File Modification Timeline")
            table.add_column("Time", style="cyan")
            table.add_column("Size", style="yellow")
            table.add_column("File", style="green")
            
            for entry in timeline[-20:]:  # Show last 20
                table.add_row(
                    entry['modified'][:19],
                    f"{entry['size']:,}",
                    os.path.basename(entry['filepath'])
                )
            
            console.print(table)
            
            return timeline
            
        except Exception as e:
            console.print(f"[bold red]Error creating timeline: {str(e)}[/bold red]")
            return []
    
    def save_report(self, data, report_type):
        """Save forensic report"""
        output_file = f"{self.output_dir}/{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
        
        console.print(f"[green]Report saved to: {output_file}[/green]")
