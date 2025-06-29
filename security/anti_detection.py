"""
Advanced Anti-Detection System
Handles User-Agent rotation, browser fingerprinting, and request patterns
"""

import random
import time
import json
import hashlib
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import logging

@dataclass
class BrowserProfile:
    """Browser profile for fingerprint simulation"""
    user_agent: str
    accept: str
    accept_language: str
    accept_encoding: str
    platform: str
    screen_resolution: str
    timezone: str
    plugins: List[str]
    webgl_vendor: str
    webgl_renderer: str

class AntiDetectionManager:
    """Advanced anti-detection system for web scraping"""
    
    def __init__(self, profiles_file: str = "security/browser_profiles.json"):
        self.profiles_file = Path(profiles_file)
        self.browser_profiles: List[BrowserProfile] = []
        self.current_profile: Optional[BrowserProfile] = None
        self.request_history: List[Dict] = []
        self.max_history = 1000
        
        # Load browser profiles
        self.load_browser_profiles()
        
        # Request timing patterns
        self.min_delay = 1.0
        self.max_delay = 5.0
        self.burst_protection = True
        self.max_requests_per_minute = 30
        
        logging.info("AntiDetectionManager initialized")
    
    def load_browser_profiles(self):
        """Load realistic browser profiles"""
        if not self.profiles_file.exists():
            self._create_default_profiles()
            return
        
        try:
            with open(self.profiles_file, 'r') as f:
                profiles_data = json.load(f)
            
            self.browser_profiles = []
            for profile_data in profiles_data.get('profiles', []):
                profile = BrowserProfile(
                    user_agent=profile_data['user_agent'],
                    accept=profile_data['accept'],
                    accept_language=profile_data['accept_language'],
                    accept_encoding=profile_data['accept_encoding'],
                    platform=profile_data['platform'],
                    screen_resolution=profile_data['screen_resolution'],
                    timezone=profile_data['timezone'],
                    plugins=profile_data['plugins'],
                    webgl_vendor=profile_data['webgl_vendor'],
                    webgl_renderer=profile_data['webgl_renderer']
                )
                self.browser_profiles.append(profile)
                
        except Exception as e:
            logging.error(f"Error loading browser profiles: {e}")
            self._create_default_profiles()
    
    def _create_default_profiles(self):
        """Create default browser profiles"""
        self.profiles_file.parent.mkdir(exist_ok=True)
        
        default_profiles = {
            "profiles": [
                {
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                    "accept_language": "en-US,en;q=0.9",
                    "accept_encoding": "gzip, deflate, br",
                    "platform": "Win32",
                    "screen_resolution": "1920x1080",
                    "timezone": "America/New_York",
                    "plugins": ["Chrome PDF Plugin", "Chrome PDF Viewer", "Native Client"],
                    "webgl_vendor": "Google Inc. (Intel)",
                    "webgl_renderer": "ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)"
                },
                {
                    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                    "accept_language": "en-US,en;q=0.9",
                    "accept_encoding": "gzip, deflate, br",
                    "platform": "MacIntel",
                    "screen_resolution": "2560x1440",
                    "timezone": "America/Los_Angeles",
                    "plugins": ["Chrome PDF Plugin", "Chrome PDF Viewer", "Native Client"],
                    "webgl_vendor": "Google Inc. (Apple)",
                    "webgl_renderer": "ANGLE (Apple, Apple M1 Pro, OpenGL 4.1)"
                },
                {
                    "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                    "accept_language": "en-US,en;q=0.9",
                    "accept_encoding": "gzip, deflate, br",
                    "platform": "Linux x86_64",
                    "screen_resolution": "1920x1080",
                    "timezone": "Europe/London",
                    "plugins": ["Chrome PDF Plugin", "Chrome PDF Viewer", "Native Client"],
                    "webgl_vendor": "Google Inc. (NVIDIA Corporation)",
                    "webgl_renderer": "ANGLE (NVIDIA Corporation, NVIDIA GeForce GTX 1060/PCIe/SSE2, OpenGL 4.5.0)"
                },
                {
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                    "accept_language": "en-US,en;q=0.5",
                    "accept_encoding": "gzip, deflate, br",
                    "platform": "Win32",
                    "screen_resolution": "1920x1080",
                    "timezone": "America/Chicago",
                    "plugins": ["PDF.js", "OpenH264 Video Codec"],
                    "webgl_vendor": "Mozilla",
                    "webgl_renderer": "Mozilla -- ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)"
                },
                {
                    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "accept_language": "en-US,en;q=0.9",
                    "accept_encoding": "gzip, deflate, br",
                    "platform": "MacIntel",
                    "screen_resolution": "2880x1800",
                    "timezone": "America/Denver",
                    "plugins": ["PDF", "QuickTime Plugin"],
                    "webgl_vendor": "Apple Inc.",
                    "webgl_renderer": "Apple GPU"
                }
            ]
        }
        
        with open(self.profiles_file, 'w') as f:
            json.dump(default_profiles, f, indent=2)
        
        # Load the created profiles
        self.load_browser_profiles()
    
    def get_random_profile(self) -> BrowserProfile:
        """Get a random browser profile"""
        if not self.browser_profiles:
            raise ValueError("No browser profiles available")
        
        profile = random.choice(self.browser_profiles)
        self.current_profile = profile
        return profile
    
    def get_headers(self, url: str = None, referer: str = None) -> Dict[str, str]:
        """Generate realistic headers for a request"""
        if not self.current_profile:
            self.get_random_profile()
        
        headers = {
            'User-Agent': self.current_profile.user_agent,
            'Accept': self.current_profile.accept,
            'Accept-Language': self.current_profile.accept_language,
            'Accept-Encoding': self.current_profile.accept_encoding,
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
        
        # Add referer if provided
        if referer:
            headers['Referer'] = referer
        
        # Add random variations
        if random.random() < 0.3:  # 30% chance
            headers['DNT'] = '1'
        
        if random.random() < 0.2:  # 20% chance
            headers['Sec-GPC'] = '1'
        
        # Randomize header order
        header_items = list(headers.items())
        random.shuffle(header_items)
        return dict(header_items)
    
    def calculate_delay(self, url: str = None) -> float:
        """Calculate intelligent delay between requests"""
        base_delay = random.uniform(self.min_delay, self.max_delay)
        
        # Check request frequency
        current_time = time.time()
        recent_requests = [r for r in self.request_history if current_time - r['timestamp'] < 60]
        
        if len(recent_requests) >= self.max_requests_per_minute:
            # Add extra delay if too many requests
            base_delay += random.uniform(5, 15)
        
        # Add domain-specific delays
        if url:
            domain = self._extract_domain(url)
            domain_requests = [r for r in recent_requests if r.get('domain') == domain]
            
            if len(domain_requests) > 10:  # More than 10 requests to same domain in last minute
                base_delay += random.uniform(2, 8)
        
        # Human-like patterns: occasionally longer delays
        if random.random() < 0.1:  # 10% chance of longer delay
            base_delay += random.uniform(10, 30)
        
        return base_delay
    
    def record_request(self, url: str, success: bool, response_time: float):
        """Record request for pattern analysis"""
        request_record = {
            'timestamp': time.time(),
            'url': url,
            'domain': self._extract_domain(url),
            'success': success,
            'response_time': response_time,
            'profile_hash': self._get_profile_hash()
        }
        
        self.request_history.append(request_record)
        
        # Keep history size manageable
        if len(self.request_history) > self.max_history:
            self.request_history = self.request_history[-self.max_history//2:]
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc
        except:
            return url
    
    def _get_profile_hash(self) -> str:
        """Get hash of current profile for tracking"""
        if not self.current_profile:
            return "no_profile"
        
        profile_str = f"{self.current_profile.user_agent}{self.current_profile.platform}"
        return hashlib.md5(profile_str.encode()).hexdigest()[:8]
    
    def should_rotate_profile(self) -> bool:
        """Determine if profile should be rotated"""
        if not self.current_profile:
            return True
        
        # Rotate after certain number of requests
        current_profile_hash = self._get_profile_hash()
        profile_requests = [r for r in self.request_history if r.get('profile_hash') == current_profile_hash]
        
        if len(profile_requests) > 50:  # Rotate after 50 requests
            return True
        
        # Rotate after certain time
        if profile_requests:
            first_request_time = min(r['timestamp'] for r in profile_requests)
            if time.time() - first_request_time > 3600:  # 1 hour
                return True
        
        # Random rotation
        if random.random() < 0.05:  # 5% chance
            return True
        
        return False
    
    def get_request_stats(self) -> Dict:
        """Get statistics about request patterns"""
        current_time = time.time()
        recent_requests = [r for r in self.request_history if current_time - r['timestamp'] < 3600]  # Last hour
        
        if not recent_requests:
            return {'total_requests': 0}
        
        success_rate = sum(1 for r in recent_requests if r['success']) / len(recent_requests)
        avg_response_time = sum(r['response_time'] for r in recent_requests) / len(recent_requests)
        
        domains = {}
        for request in recent_requests:
            domain = request['domain']
            domains[domain] = domains.get(domain, 0) + 1
        
        return {
            'total_requests': len(recent_requests),
            'success_rate': success_rate,
            'average_response_time': avg_response_time,
            'domains_accessed': len(domains),
            'top_domains': sorted(domains.items(), key=lambda x: x[1], reverse=True)[:5]
        }
    
    def simulate_human_behavior(self):
        """Simulate human-like browsing behavior"""
        # Random mouse movements, scrolling, etc. could be added here
        # For now, just add a small random delay
        time.sleep(random.uniform(0.1, 0.5))
    
    def get_realistic_viewport(self) -> Tuple[int, int]:
        """Get realistic viewport dimensions"""
        if not self.current_profile:
            self.get_random_profile()
        
        resolution = self.current_profile.screen_resolution
        width, height = map(int, resolution.split('x'))
        
        # Subtract browser chrome
        viewport_width = width - random.randint(0, 50)
        viewport_height = height - random.randint(100, 200)
        
        return viewport_width, viewport_height
