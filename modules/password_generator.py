#!/usr/bin/env python3

import secrets
import string
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

class PasswordGenerator:
    def __init__(self):
        pass
        
    def generate_password(self, length=16, use_uppercase=True, use_lowercase=True,
                         use_digits=True, use_special=True):
        """Generate secure random password"""
        try:
            charset = ''
            
            if use_lowercase:
                charset += string.ascii_lowercase
            if use_uppercase:
                charset += string.ascii_uppercase
            if use_digits:
                charset += string.digits
            if use_special:
                charset += '!@#$%^&*()_+-=[]{}|;:,.<>?'
            
            if not charset:
                console.print("[red]At least one character type must be selected[/red]")
                return None
            
            password = ''.join(secrets.choice(charset) for _ in range(length))
            
            table = Table(title="Generated Password")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="yellow")
            
            table.add_row("Password", f"[bold green]{password}[/bold green]")
            table.add_row("Length", str(length))
            table.add_row("Uppercase", "✓" if use_uppercase else "✗")
            table.add_row("Lowercase", "✓" if use_lowercase else "✗")
            table.add_row("Digits", "✓" if use_digits else "✗")
            table.add_row("Special", "✓" if use_special else "✗")
            
            console.print(table)
            return password
            
        except Exception as e:
            console.print(f"[bold red]Error generating password: {str(e)}[/bold red]")
            return None
    
    def generate_passphrase(self, word_count=5):
        """Generate memorable passphrase"""
        try:
            word_list = [
                "correct", "horse", "battery", "staple", "apple", "brave",
                "cloud", "delta", "eagle", "forest", "guitar", "harbor",
                "island", "jungle", "kite", "lemon", "mountain", "night",
                "ocean", "planet", "quiet", "river", "stone", "tiger",
                "urban", "violet", "whale", "xray", "yellow", "zebra"
            ]
            
            words = [secrets.choice(word_list) for _ in range(word_count)]
            passphrase = '-'.join(words)
            
            table = Table(title="Generated Passphrase")
            table.add_row("Passphrase", f"[bold green]{passphrase}[/bold green]")
            table.add_row("Word Count", str(word_count))
            table.add_row("Entropy", f"~{word_count * 12.9} bits")
            
            console.print(table)
            return passphrase
            
        except Exception as e:
            console.print(f"[bold red]Error generating passphrase: {str(e)}[/bold red]")
            return None
    
    def check_password_strength(self, password):
        """Check password strength"""
        try:
            score = 0
            feedback = []
            
            if len(password) >= 12:
                score += 1
            else:
                feedback.append("Password should be at least 12 characters")
            
            if any(c.islower() for c in password):
                score += 1
            else:
                feedback.append("Add lowercase letters")
            
            if any(c.isupper() for c in password):
                score += 1
            else:
                feedback.append("Add uppercase letters")
            
            if any(c.isdigit() for c in password):
                score += 1
            else:
                feedback.append("Add numbers")
            
            if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
                score += 1
            else:
                feedback.append("Add special characters")
            
            table = Table(title="Password Strength Analysis")
            table.add_column("Metric", style="cyan")
            table.add_column("Result", style="yellow")
            
            strength_levels = ["Very Weak", "Weak", "Fair", "Good", "Strong", "Very Strong"]
            strength = strength_levels[score] if score < len(strength_levels) else "Very Strong"
            
            table.add_row("Score", f"{score}/5")
            table.add_row("Strength", f"[{self._get_strength_color(score)}]{strength}[/{self._get_strength_color(score)}]")
            table.add_row("Length", str(len(password)))
            
            console.print(table)
            
            if feedback:
                console.print("\n[cyan]Suggestions:[/cyan]")
                for item in feedback:
                    console.print(f"  [yellow]- {item}[/yellow]")
            
            return score
            
        except Exception as e:
            console.print(f"[bold red]Error checking strength: {str(e)}[/bold red]")
            return 0
    
    def _get_strength_color(self, score):
        if score <= 2:
            return "red"
        elif score == 3:
            return "yellow"
        else:
            return "green"
