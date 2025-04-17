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

## 💻 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/luna-osint-tool.git
cd luna-osint-tool
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the tool:
```bash
python main.py
```

### Windows-Specific Requirements
For certain functionality on Windows, you may need to install npcap:
- Download from [npcap.org](https://npcap.org/#download)
- Install with WinPcap compatibility mode

## 🛠️ Usage

Luna OSINT Tool provides an intuitive menu-driven interface:

1. Launch the application:
```bash
python main.py
```

2. Navigate through the menu by selecting the desired option.
3. Follow the on-screen prompts to access various features.

### Example: Domain Reconnaissance
```
[1] OSINT Search
  > Select Domain Information
  > Enter domain: example.com
```

### Example: Custom HTTP Request
```
[5] Custom HTTP Requests
  > Select Request Builder
  > Enter URL, headers, and custom parameters
```

## 🤝 Pro Tips

- Save scan results to files for easier analysis
- Use proxy capabilities when performing sensitive searches
- Combine multiple modules for comprehensive intelligence gathering
- Use the custom request builder for tailored reconnaissance
- Metadata extraction can reveal hidden information in files

## 🔒 Legal Disclaimer

This tool is provided for educational and legitimate security research purposes only. Users are responsible for complying with applicable laws and should only use this tool on systems they own or have explicit permission to test. The developers assume no liability for misuse or damage caused by this tool.

## 🔄 Updates

This tool is actively maintained. Check for updates regularly using:
```bash
git pull
```

## 🐛 Troubleshooting

### Common Issues:
- **Network module errors**: Ensure you have administrator privileges
- **Python module not found**: Verify all dependencies are installed from requirements.txt
- **Permission denied**: Run with elevated privileges for certain network operations
- **Connection errors**: Check your network connectivity and firewall settings

## 📞 Contact & Support

For bug reports, feature requests, or other inquiries:
- Telegram: https://t.me/luna_intelligence

## 🌟 Acknowledgements

Special thanks to the open-source community and the developers of the libraries this tool depends on.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details. 