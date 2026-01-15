#!/usr/bin/env python3

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import base64

console = Console()

class SteganographyTool:
    def __init__(self):
        pass
        
    def encode_base64(self, message):
        """Encode message using Base64"""
        try:
            encoded = base64.b64encode(message.encode()).decode()
            
            table = Table(title="Base64 Encoding")
            table.add_row("Original", message)
            table.add_row("Encoded", encoded)
            
            console.print(table)
            return encoded
            
        except Exception as e:
            console.print(f"[bold red]Error encoding: {str(e)}[/bold red]")
            return None
    
    def decode_base64(self, encoded):
        """Decode Base64 message"""
        try:
            decoded = base64.b64decode(encoded).decode()
            
            table = Table(title="Base64 Decoding")
            table.add_row("Encoded", encoded)
            table.add_row("Decoded", decoded)
            
            console.print(table)
            return decoded
            
        except Exception as e:
            console.print(f"[bold red]Error decoding: {str(e)}[/bold red]")
            return None
    
    def encode_hex(self, message):
        """Encode message using hexadecimal"""
        try:
            encoded = message.encode().hex()
            
            table = Table(title="Hexadecimal Encoding")
            table.add_row("Original", message)
            table.add_row("Encoded", encoded)
            
            console.print(table)
            return encoded
            
        except Exception as e:
            console.print(f"[bold red]Error encoding: {str(e)}[/bold red]")
            return None
    
    def decode_hex(self, encoded):
        """Decode hexadecimal message"""
        try:
            decoded = bytes.fromhex(encoded).decode()
            
            table = Table(title="Hexadecimal Decoding")
            table.add_row("Encoded", encoded)
            table.add_row("Decoded", decoded)
            
            console.print(table)
            return decoded
            
        except Exception as e:
            console.print(f"[bold red]Error decoding: {str(e)}[/bold red]")
            return None
    
    def rot13_encode(self, message):
        """Encode using ROT13 cipher"""
        try:
            result = []
            for char in message:
                if 'a' <= char <= 'z':
                    result.append(chr((ord(char) - ord('a') + 13) % 26 + ord('a')))
                elif 'A' <= char <= 'Z':
                    result.append(chr((ord(char) - ord('A') + 13) % 26 + ord('A')))
                else:
                    result.append(char)
            
            encoded = ''.join(result)
            
            table = Table(title="ROT13 Encoding")
            table.add_row("Original", message)
            table.add_row("Encoded", encoded)
            
            console.print(table)
            return encoded
            
        except Exception as e:
            console.print(f"[bold red]Error encoding: {str(e)}[/bold red]")
            return None
    
    def caesar_cipher(self, message, shift=3):
        """Encode/Decode using Caesar cipher"""
        try:
            result = []
            for char in message:
                if 'a' <= char <= 'z':
                    result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
                elif 'A' <= char <= 'Z':
                    result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
                else:
                    result.append(char)
            
            encoded = ''.join(result)
            
            table = Table(title=f"Caesar Cipher (Shift: {shift})")
            table.add_row("Original", message)
            table.add_row("Encoded", encoded)
            
            console.print(table)
            return encoded
            
        except Exception as e:
            console.print(f"[bold red]Error encoding: {str(e)}[/bold red]")
            return None
    
    def reverse_string(self, message):
        """Reverse string"""
        try:
            reversed_msg = message[::-1]
            
            table = Table(title="String Reversal")
            table.add_row("Original", message)
            table.add_row("Reversed", reversed_msg)
            
            console.print(table)
            return reversed_msg
            
        except Exception as e:
            console.print(f"[bold red]Error reversing: {str(e)}[/bold red]")
            return None
    
    def binary_encode(self, message):
        """Encode message to binary"""
        try:
            binary = ' '.join(format(ord(char), '08b') for char in message)
            
            table = Table(title="Binary Encoding")
            table.add_row("Original", message)
            table.add_row("Binary", binary)
            
            console.print(table)
            return binary
            
        except Exception as e:
            console.print(f"[bold red]Error encoding: {str(e)}[/bold red]")
            return None
    
    def binary_decode(self, binary):
        """Decode binary message"""
        try:
            decoded = ''.join(chr(int(byte, 2)) for byte in binary.split())
            
            table = Table(title="Binary Decoding")
            table.add_row("Binary", binary)
            table.add_row("Decoded", decoded)
            
            console.print(table)
            return decoded
            
        except Exception as e:
            console.print(f"[bold red]Error decoding: {str(e)}[/bold red]")
            return None
