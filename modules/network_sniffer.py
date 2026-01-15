#!/usr/bin/env python3

import socket
import struct
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.live import Live
import os

console = Console()

class NetworkSniffer:
    def __init__(self):
        self.output_dir = "output/sniffer"
        os.makedirs(self.output_dir, exist_ok=True)
        self.captured_packets = []
        
    def parse_ethernet_header(self, data):
        """Parse Ethernet header"""
        try:
            eth_header = struct.unpack('!6s6sH', data[:14])
            dest_mac = ':'.join(f'{b:02x}' for b in eth_header[0])
            src_mac = ':'.join(f'{b:02x}' for b in eth_header[1])
            eth_protocol = socket.ntohs(eth_header[2])
            return {
                "dest_mac": dest_mac,
                "src_mac": src_mac,
                "protocol": eth_protocol
            }
        except:
            return None
    
    def parse_ip_header(self, data):
        """Parse IP header"""
        try:
            ip_header = struct.unpack('!BBHHHBBH4s4s', data[:20])
            version = ip_header[0] >> 4
            ihl = (ip_header[0] & 0xF) * 4
            ttl = ip_header[5]
            protocol = ip_header[6]
            src_addr = socket.inet_ntoa(ip_header[8])
            dest_addr = socket.inet_ntoa(ip_header[9])
            
            return {
                "version": version,
                "header_length": ihl,
                "ttl": ttl,
                "protocol": protocol,
                "src_addr": src_addr,
                "dest_addr": dest_addr
            }
        except:
            return None
    
    def parse_tcp_header(self, data):
        """Parse TCP header"""
        try:
            tcp_header = struct.unpack('!HHLLBBHHH', data[:20])
            src_port = tcp_header[0]
            dest_port = tcp_header[1]
            sequence = tcp_header[2]
            acknowledgement = tcp_header[3]
            flags = tcp_header[5]
            
            return {
                "src_port": src_port,
                "dest_port": dest_port,
                "sequence": sequence,
                "acknowledgement": acknowledgement,
                "flags": flags
            }
        except:
            return None
    
    def parse_udp_header(self, data):
        """Parse UDP header"""
        try:
            udp_header = struct.unpack('!HHHH', data[:8])
            src_port = udp_header[0]
            dest_port = udp_header[1]
            length = udp_header[2]
            checksum = udp_header[3]
            
            return {
                "src_port": src_port,
                "dest_port": dest_port,
                "length": length,
                "checksum": checksum
            }
        except:
            return None
    
    def start_sniffing(self, interface, packet_count=100):
        """Start packet sniffing"""
        try:
            console.print(f"[yellow]Starting packet sniffing on {interface}...[/yellow]")
            console.print(f"[yellow]Capturing {packet_count} packets...[/yellow]")
            
            # Create raw socket
            try:
                s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
            except:
                console.print("[red]Raw socket requires root privileges![/red]")
                console.print("[yellow]Run with sudo to capture packets[/yellow]")
                return False
            
            captured = 0
            
            table = Table(title="Captured Packets")
            table.add_column("#", style="cyan")
            table.add_column("Source", style="green")
            table.add_column("Destination", style="yellow")
            table.add_column("Protocol", style="magenta")
            
            console.print(table)
            
            while captured < packet_count:
                try:
                    raw_packet, addr = s.recvfrom(65535)
                    
                    eth_data = self.parse_ethernet_header(raw_packet)
                    if not eth_data:
                        continue
                    
                    if eth_data['protocol'] == 8:  # IP
                        ip_data = self.parse_ip_header(raw_packet[14:])
                        if not ip_data:
                            continue
                        
                        protocol_num = ip_data['protocol']
                        protocol = "IP"
                        
                        if protocol_num == 6:  # TCP
                            tcp_data = self.parse_tcp_header(raw_packet[14+ip_data['header_length']:])
                            protocol = f"TCP:{tcp_data['dest_port']}"
                        elif protocol_num == 17:  # UDP
                            udp_data = self.parse_udp_header(raw_packet[14+ip_data['header_length']:])
                            protocol = f"UDP:{udp_data['dest_port']}"
                        
                        packet_info = {
                            "timestamp": datetime.now().isoformat(),
                            "src": ip_data['src_addr'],
                            "dest": ip_data['dest_addr'],
                            "protocol": protocol
                        }
                        
                        self.captured_packets.append(packet_info)
                        captured += 1
                        
                        if captured <= 20:
                            console.print(f"[cyan]{captured}[/cyan] - [green]{ip_data['src_addr']}[/green] -> [yellow]{ip_data['dest_addr']}[/yellow] - [magenta]{protocol}[/magenta]")
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    continue
            
            s.close()
            console.print(f"\n[green]Captured {captured} packets[/green]")
            return True
            
        except Exception as e:
            console.print(f"[bold red]Error sniffing: {str(e)}[/bold red]")
            return False
    
    def analyze_traffic(self):
        """Analyze captured traffic"""
        if not self.captured_packets:
            console.print("[yellow]No packets captured to analyze[/yellow]")
            return
        
        protocols = {}
        top_sources = {}
        top_destinations = {}
        
        for packet in self.captured_packets:
            protocol = packet['protocol']
            protocols[protocol] = protocols.get(protocol, 0) + 1
            
            src = packet['src']
            top_sources[src] = top_sources.get(src, 0) + 1
            
            dest = packet['dest']
            top_destinations[dest] = top_destinations.get(dest, 0) + 1
        
        table = Table(title="Traffic Analysis")
        table.add_column("Metric", style="cyan")
        table.add_column("Result", style="yellow")
        
        table.add_row("Total Packets", str(len(self.captured_packets)))
        table.add_row("Unique Protocols", str(len(protocols)))
        table.add_row("Unique Sources", str(len(top_sources)))
        table.add_row("Unique Destinations", str(len(top_destinations)))
        
        console.print(table)
        
        return {
            "protocols": protocols,
            "sources": top_sources,
            "destinations": top_destinations
        }
    
    def save_capture(self):
        """Save captured packets"""
        if not self.captured_packets:
            console.print("[yellow]No packets to save[/yellow]")
            return
        
        output_file = f"{self.output_dir}/capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, 'w') as f:
            json.dump(self.captured_packets, f, indent=4)
        
        console.print(f"[green]Capture saved to: {output_file}[/green]")
