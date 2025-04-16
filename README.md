# Linux Firewall System

A robust Linux-based firewall system that provides network security through packet filtering and traffic control.

## Features

- Packet filtering using iptables/nftables
- Stateful inspection
- Port forwarding capabilities
- Logging and monitoring
- Rule management system
- Easy configuration through YAML files

## Requirements

- Linux operating system (Ubuntu/Debian recommended)
- iptables or nftables
- Python 3.6 or higher
- Root privileges for firewall operations

## Installation

1. Clone this repository:
```bash
git clone [repository-url]
cd linux-firewall
```

2. Install dependencies:
```bash
sudo apt-get update
sudo apt-get install iptables python3-yaml
```

3. Make the firewall script executable:
```bash
chmod +x firewall.py
```

## Usage

To start the firewall:
```bash
sudo ./firewall.py start
```

To stop the firewall:
```bash
sudo ./firewall.py stop
```

To reload rules:
```bash
sudo ./firewall.py reload
```

## Configuration

The firewall rules are configured in `config/rules.yaml`. Edit this file to customize your firewall settings.

## Security Considerations

- Always test rules in a non-production environment first
- Keep the system updated with security patches
- Regularly review and update firewall rules
- Monitor logs for suspicious activity

## License

MIT License 