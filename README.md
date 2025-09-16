# 0x403 - HTTP 403 Forbidden Bypass Testing Tool

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Security](https://img.shields.io/badge/security-pentesting-red.svg)

A comprehensive Python tool designed for security researchers, penetration testers, and bug bounty hunters to test various HTTP 403 Forbidden bypass techniques.

## 🚀 Features

### HTTP Method Testing
- Tests multiple HTTP methods: GET, POST, PUT, DELETE, OPTIONS, HEAD, PATCH, TRACE, CONNECT
- Identifies methods that bypass access restrictions

### Header-Based Bypasses
- **IP Spoofing Headers**: X-Forwarded-For, X-Real-IP, X-Originating-IP, X-Remote-IP
- **Protocol Headers**: X-Forwarded-Proto, X-Forwarded-Protocol, X-Forwarded-Ssl
- **User-Agent Variations**: Googlebot, mobile browsers, custom agents
- **Custom Authorization Headers**: X-Custom-IP-Authorization and more

### URL Path Manipulations
- Trailing slash variations (`/admin` vs `/admin/`)
- Case sensitivity tests (`/Admin`, `/ADMIN`)
- URL encoding (single and double encoding)
- Path traversal attempts (`/./admin`, `/../admin`)
- Unicode character substitution
- HTTP Parameter Pollution

### Protocol & Port Testing
- HTTP/HTTPS protocol switching
- Common port variations (80, 443, 8080, 8443, etc.)

### Combined Techniques
- Tests combinations of headers + URL variations
- Method + header combinations for maximum coverage

## 📦 Installation

### Prerequisites
```bash
pip install requests colorama
```

### Clone the Repository
```bash
git clone https://github.com/yourusername/0x403.git
cd 0x403
```

## 🛠️ Usage

### Basic Usage
```bash
python 0x403.py https://target.com/admin
```

### Advanced Options
```bash
# Custom delay between requests (default: 0.5 seconds)
python 0x403.py https://target.com/admin --delay 1.0

# Custom timeout (default: 10 seconds)
python 0x403.py https://target.com/admin --timeout 15

# Combined options
python 0x403.py https://target.com/admin --delay 0.8 --timeout 20
```

### Example Output
```
============================================================
0x403 - HTTP 403 Forbidden Bypass Testing Tool
Target: https://example.com/admin
============================================================

[i] Testing original request...
[i] Testing HTTP methods...
[✓] HTTP Method: POST | Status: 200 | Method: POST | URL: https://example.com/admin
[i] Testing header-based bypasses...
[✓] Headers: X-Forwarded-For: 127.0.0.1 | Status: 200 | Method: GET | URL: https://example.com/admin
[i] Testing URL variations...
[✓] URL Variation: /admin/ | Status: 302 | Method: GET

============================================================
SUMMARY
============================================================
[✓] Found 3 successful bypasses:
  → HTTP Method: POST
  → Headers: X-Forwarded-For: 127.0.0.1
  → URL Variation: /admin/
```

## 🔧 Technical Details

### Bypass Techniques Implemented

1. **HTTP Method Bypass**
   - Some applications only restrict GET requests
   - Tests all common HTTP methods

2. **IP-based Header Bypass**
   - Spoofs client IP using various headers
   - Useful when IP-based access control is implemented

3. **Protocol Manipulation**
   - Tests HTTP vs HTTPS access
   - Some applications have different rules for different protocols

4. **Path Normalization Issues**
   - Exploits how web servers handle path normalization
   - URL encoding and case sensitivity variations

5. **Combined Attack Vectors**
   - Real-world scenarios often require multiple techniques
   - Tests logical combinations of bypass methods

## ⚡ Performance Features

- **Configurable Delays**: Prevent overwhelming target servers
- **Timeout Controls**: Handle slow responses gracefully
- **Session Management**: Efficient connection reuse
- **Colored Output**: Easy-to-read results with status indicators
- **Detailed Reporting**: Comprehensive summary of successful bypasses

## 🎯 Use Cases

- **Bug Bounty Hunting**: Identify access control vulnerabilities
- **Penetration Testing**: Assess application security controls
- **Security Research**: Study HTTP 403 bypass techniques
- **DevSecOps**: Test your own applications for access control issues

## ⚖️ Legal Disclaimer

**🚨 IMPORTANT: For Authorized Testing Only**

This tool is designed for:
- Systems you own
- Authorized penetration testing engagements
- Bug bounty programs with explicit permission
- Educational purposes in controlled environments

**Unauthorized testing may be illegal in your jurisdiction. Always ensure you have proper authorization before testing any system.**

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-bypass`)
3. **Commit your changes** (`git commit -m 'Add amazing bypass technique'`)
4. **Push to the branch** (`git push origin feature/amazing-bypass`)
5. **Open a Pull Request**

### Ideas for Contributions
- Additional bypass techniques
- Output format options (JSON, XML)
- Proxy support
- Multi-threading capabilities
- Integration with security frameworks

## 📋 Roadmap

- [ ] Proxy support for testing through Burp Suite/OWASP ZAP
- [ ] JSON/CSV output formats
- [ ] Multi-threading for faster testing
- [ ] Custom wordlist support
- [ ] Integration with popular security tools
- [ ] Docker containerization
- [ ] Web interface version

## 🐛 Bug Reports

Found a bug? Please open an issue with:
- Target URL (if safe to share)
- Command used
- Expected vs actual behavior
- Error messages (if any)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to the bug bounty and penetration testing community
- Inspired by various 403 bypass techniques shared by security researchers
- Built with Python and love for the cybersecurity community

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/0x403)
![GitHub forks](https://img.shields.io/github/forks/yourusername/0x403)
![GitHub issues](https://img.shields.io/github/issues/yourusername/0x403)

---

**Made with ❤️ for the cybersecurity community**

**Happy Bug Hunting! 🐛🔍**
