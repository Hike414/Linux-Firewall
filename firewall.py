#!/usr/bin/env python3

import os
import sys
import yaml
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('firewall.log'),
        logging.StreamHandler()
    ]
)

class Firewall:
    def __init__(self):
        self.config_path = Path('config/rules.yaml')
        self.rules = self._load_rules()
        
    def _load_rules(self):
        """Load firewall rules from YAML configuration file."""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logging.error(f"Configuration file not found: {self.config_path}")
            sys.exit(1)
        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML configuration: {e}")
            sys.exit(1)

    def _execute_command(self, command):
        """Execute a shell command and return the result."""
        try:
            result = subprocess.run(command, shell=True, check=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            logging.error(f"Command failed: {e.stderr}")
            return None

    def start(self):
        """Start the firewall and apply rules."""
        logging.info("Starting firewall...")
        
        # Flush existing rules
        self._execute_command("iptables -F")
        self._execute_command("iptables -X")
        
        # Set default policies
        self._execute_command("iptables -P INPUT DROP")
        self._execute_command("iptables -P FORWARD DROP")
        self._execute_command("iptables -P OUTPUT ACCEPT")
        
        # Allow localhost traffic
        self._execute_command("iptables -A INPUT -i lo -j ACCEPT")
        
        # Allow established connections
        self._execute_command("iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT")
        
        # Apply custom rules from configuration
        self._apply_custom_rules()
        
        logging.info("Firewall started successfully")

    def stop(self):
        """Stop the firewall and flush all rules."""
        logging.info("Stopping firewall...")
        self._execute_command("iptables -F")
        self._execute_command("iptables -X")
        self._execute_command("iptables -P INPUT ACCEPT")
        self._execute_command("iptables -P FORWARD ACCEPT")
        self._execute_command("iptables -P OUTPUT ACCEPT")
        logging.info("Firewall stopped successfully")

    def reload(self):
        """Reload firewall rules."""
        logging.info("Reloading firewall rules...")
        self.stop()
        self.start()
        logging.info("Firewall rules reloaded successfully")

    def _apply_custom_rules(self):
        """Apply custom rules from the configuration file."""
        if not self.rules:
            return

        for rule in self.rules.get('rules', []):
            chain = rule.get('chain', 'INPUT')
            protocol = rule.get('protocol')
            port = rule.get('port')
            source = rule.get('source')
            action = rule.get('action', 'ACCEPT')
            
            cmd = f"iptables -A {chain}"
            
            if protocol:
                cmd += f" -p {protocol}"
            if port:
                cmd += f" --dport {port}"
            if source:
                cmd += f" -s {source}"
            
            cmd += f" -j {action}"
            
            self._execute_command(cmd)
            logging.info(f"Applied rule: {cmd}")

def main():
    if os.geteuid() != 0:
        logging.error("This script must be run as root")
        sys.exit(1)

    firewall = Firewall()
    
    if len(sys.argv) < 2:
        print("Usage: ./firewall.py [start|stop|reload]")
        sys.exit(1)
    
    action = sys.argv[1].lower()
    
    if action == 'start':
        firewall.start()
    elif action == 'stop':
        firewall.stop()
    elif action == 'reload':
        firewall.reload()
    else:
        print("Invalid action. Use: start, stop, or reload")
        sys.exit(1)

if __name__ == "__main__":
    main() 