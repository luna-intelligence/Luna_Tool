# Luna OSINT Tool

Luna OSINT is a comprehensive open-source intelligence gathering and cybersecurity toolkit designed for security researchers, penetration testers, and threat intelligence analysts.

## 🌟 Features

Luna OSINT provides a wide array of capabilities divided into several modules:

### 🔍 OSINT Search
- Domain reconnaissance
- IP address intelligence
- DNS record analysis
- Whois lookup
- Website technology fingerprinting
- Metadata extraction from various file types
- Phone number lookup

### 🌐 Network Reconnaissance
- Port scanning
- Network mapping
- DNS enumeration
- Packet analysis using Scapy
- Network traffic monitoring
- Host discovery

### ⚡ DDoS Tools
- Various stress-testing methods
- Protocol-specific flood options
- Anti-DDoS bypass techniques
- Connection flooding
- Traffic generation capabilities

### 🕸️ Web Intelligence
- Web application analysis
- Header inspection
- Certificate information
- Security posture assessment
- Site structure mapping

### 🔄 Custom HTTP Requests
- Custom request builder
- Support for all HTTP methods
- Header manipulation
- Payload customization
- Response analysis with HTML parsing

### 💾 Database Search
- Search across multiple database formats
- CSV file analysis
- SQLite database exploration
- Pattern matching across structured data

## 📋 Requirements

- Python 3.8+
- Required Python packages (see requirements.txt)
- Administrative privileges for some network operations
- Supported Operating Systems:
  - Windows 10/11
  - Linux (Debian, Kali, Fedora, CentOS)
  - Ubuntu (18.04+)

## 💻 Installation

### Windows

```bash
# Clone the repository
git clone https://github.com/yourusername/luna-osint-tool.git

# Navigate to the project directory
cd luna-osint-tool

# Install required dependencies
pip install -r requirements.txt

# Run the tool
python main.py
```

### Ubuntu/Debian

```bash
# Install Python if not already installed
sudo apt-get update
sudo apt-get install python3 python3-pip git -y

# Clone the repository
git clone https://github.com/yourusername/luna-osint-tool.git

# Navigate to the project directory
cd luna-osint-tool

# Install required dependencies
pip3 install -r requirements.txt

# Install additional system dependencies
sudo apt-get install nmap libpcap-dev -y

# Run the tool
python3 main.py
```

### Other Linux Distributions

```bash
# For Fedora/RHEL/CentOS
sudo dnf install python3 python3-pip git nmap libpcap-devel -y
# OR for Arch-based
sudo pacman -S python python-pip git nmap libpcap

# Clone the repository
git clone https://github.com/yourusername/luna-osint-tool.git

# Navigate to the project directory
cd luna-osint-tool

# Install required dependencies
pip3 install -r requirements.txt

# Run the tool
python3 main.py
```

## ⚠️ Legal Disclaimer

Luna OSINT is designed for legitimate security research, penetration testing with proper authorization, and educational purposes only. The developers assume no liability and are not responsible for any misuse or damage caused by this program. Users are responsible for ensuring compliance with local, state, and federal laws while using this tool.

## 🛠️ Troubleshooting

- **Permission Issues**: Ensure you're running with administrative privileges for network operations
- **Dependencies Errors**: Verify that all requirements are installed with `pip install -r requirements.txt`
- **Connection Timeouts**: Check your network settings and firewall configurations
- **Rate Limiting**: Some modules implement delays to prevent API rate limiting

## 📞 Contact & Support

- Telegram : [Luna Intelligence](https://t.me/luna_intelligence)

## 🙏 Acknowledgements

- Thanks to all contributors and the open-source community
- Special thanks to the developers of the libraries used in this project
- Inspired by various OSINT frameworks and security tools

## 📄 License

Luna OSINT is released under the MIT License. See the LICENSE file for details.