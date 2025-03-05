#!/usr/bin/env python3

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from rich.console import Console
from rich.prompt import Prompt

console = Console()

class SpearPhishing:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = None
        self.sender_password = None
        
    def setup_sender(self):
        """Setup sender email credentials"""
        self.sender_email = Prompt.ask("[cyan]Enter sender email")
        self.sender_password = Prompt.ask("[cyan]Enter email password", password=True)
        
    def create_email(self, target_email, subject, template_file):
        """Create spear phishing email"""
        try:
            with open(template_file) as f:
                template = f.read()
                
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = target_email
            msg['Subject'] = subject
            
            body = template
            msg.attach(MIMEText(body, 'html'))
            
            return msg
            
        except Exception as e:
            console.print(f"[red]Error creating email: {str(e)}[/red]")
            return None
            
    def send_email(self, target_email, subject, template_file):
        """Send spear phishing email"""
        if not self.sender_email or not self.sender_password:
            console.print("[red]Sender credentials not set![/red]")
            return False
            
        try:
            msg = self.create_email(target_email, subject, template_file)
            if not msg:
                return False
                
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            
            server.send_message(msg)
            server.quit()
            
            console.print(f"[green]Email sent successfully to {target_email}[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]Error sending email: {str(e)}[/red]")
            return False 