"""
Enhanced Base Scraper with Advanced Security
All new scrapers should inherit from this class for maximum protection
"""

import time
import random
import requests
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sys
from pathlib import Path

# Add security module to path
sys.path.append(str(Path(__file__).parent.parent))

try:
    from security.secure_scraper import SecureScraper
    from security.advanced_bot_bypass import AdvancedBotBypass
    SECURITY_AVAILABLE = True
except ImportError:
    SECURITY_AVAILABLE = False
    logging.warning("Security modules not available - using basic scraping")

import config

class EnhancedBaseScraper(ABC):
    """Enhanced base class for all site scrapers with maximum security"""

    def __init__(self, site_name: str, enable_advanced_security: bool = True):
        self.site_name = site_name
        self.enable_advanced_security = enable_advanced_security and SECURITY_AVAILABLE
        
        # Initialize security components
        if self.enable_advanced_security:
            self.secure_scraper = SecureScraper(site_name)
            self.bot_bypass = AdvancedBotBypass()
            logging.info(f"Enhanced security enabled for {site_name}")
        else:
            # Fallback to basic session with enhanced headers
            self.session = self._create_enhanced_session()
            logging.warning(f"Using basic security for {site_name}")
        
        # Scraping statistics
        self.stats = {
            'requests_made': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'bot_detections': 0,
            'bypasses_attempted': 0,
            'bypasses_successful': 0
        }
        
        # Rate limiting
        self.last_request_time = 0
        self.min_delay = 1.0
        self.max_delay = 5.0
        
    def _create_enhanced_session(self) -> requests.Session:
        """Create enhanced session with security headers"""
        session = requests.Session()
        
        # Enhanced headers for better stealth
        session.headers.update({
            'User-Agent': self._get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        })
        
        return session
    
    def _get_random_user_agent(self) -> str:
        """Get random user agent for better anonymity"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0'
        ]
        return random.choice(user_agents)
    
    def make_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
        """Make HTTP request with advanced security and bot protection"""
        self.stats['requests_made'] += 1

        # Intelligent delay
        self._apply_intelligent_delay()

        try:
            if self.enable_advanced_security and hasattr(self, 'secure_scraper'):
                # Use secure scraper with all protections
                response = self.secure_scraper.make_request(url, method, **kwargs)
            else:
                # Enhanced basic request
                if not hasattr(self, 'session'):
                    self.session = self._create_enhanced_session()
                response = self._make_basic_request(url, method, **kwargs)
            
            if response and response.status_code == 200:
                self.stats['successful_requests'] += 1
                return response
            else:
                self.stats['failed_requests'] += 1
                return response
                
        except Exception as e:
            logging.error(f"Request failed for {url}: {e}")
            self.stats['failed_requests'] += 1
            return None
    
    def _make_basic_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
        """Make basic request with enhanced protection"""
        # Rotate User-Agent occasionally
        if random.random() < 0.1:  # 10% chance
            self.session.headers['User-Agent'] = self._get_random_user_agent()
        
        # Add referer if not provided
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        
        if 'Referer' not in kwargs['headers']:
            kwargs['headers']['Referer'] = self._get_realistic_referer(url)
        
        # Make request with timeout
        kwargs.setdefault('timeout', 30)
        
        response = self.session.request(method, url, **kwargs)
        
        # Check for bot protection and attempt basic bypass
        if self._detect_basic_bot_protection(response):
            self.stats['bot_detections'] += 1
            logging.warning(f"Basic bot protection detected for {url}")
            
            # Try simple bypass
            bypassed_response = self._attempt_basic_bypass(url, method, **kwargs)
            if bypassed_response:
                self.stats['bypasses_successful'] += 1
                return bypassed_response
            else:
                self.stats['bypasses_attempted'] += 1
        
        return response
    
    def _detect_basic_bot_protection(self, response: requests.Response) -> bool:
        """Detect basic bot protection"""
        if not response:
            return False
        
        # Check status codes
        if response.status_code in [403, 429, 503]:
            return True
        
        # Check content for protection indicators
        content = response.text.lower()
        protection_indicators = [
            'captcha', 'robot', 'automated', 'blocked',
            'access denied', 'cloudflare', 'checking your browser',
            'verify you are human', 'suspicious activity'
        ]
        
        return any(indicator in content for indicator in protection_indicators)
    
    def _attempt_basic_bypass(self, url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
        """Attempt basic bot protection bypass"""
        self.stats['bypasses_attempted'] += 1
        
        # Wait longer
        time.sleep(random.uniform(10, 30))
        
        # Change User-Agent
        self.session.headers['User-Agent'] = self._get_random_user_agent()
        
        # Add more realistic headers
        enhanced_headers = kwargs.get('headers', {})
        enhanced_headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        })
        kwargs['headers'] = enhanced_headers
        
        try:
            response = self.session.request(method, url, **kwargs)
            if response.status_code == 200 and not self._detect_basic_bot_protection(response):
                return response
        except Exception as e:
            logging.error(f"Basic bypass failed: {e}")
        
        return None
    
    def _get_realistic_referer(self, url: str) -> str:
        """Get realistic referer for the URL"""
        domain = urlparse(url).netloc
        referers = [
            'https://www.google.com/',
            'https://www.bing.com/',
            f'https://{domain}/',
            'https://github.com/',
            'https://stackoverflow.com/'
        ]
        return random.choice(referers)
    
    def _apply_intelligent_delay(self):
        """Apply intelligent delay between requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        # Calculate delay based on success rate
        success_rate = self.stats['successful_requests'] / max(1, self.stats['requests_made'])
        
        if success_rate < 0.5:
            # Low success rate - increase delay
            delay = random.uniform(self.max_delay, self.max_delay * 2)
        elif success_rate > 0.9:
            # High success rate - can be more aggressive
            delay = random.uniform(self.min_delay * 0.5, self.min_delay)
        else:
            # Normal delay
            delay = random.uniform(self.min_delay, self.max_delay)
        
        # Ensure minimum time between requests
        if time_since_last < delay:
            sleep_time = delay - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def get_soup(self, url: str, **kwargs) -> Optional[BeautifulSoup]:
        """Get BeautifulSoup object with security"""
        response = self.make_request(url, **kwargs)
        if response and response.status_code == 200:
            return BeautifulSoup(response.content, 'html.parser')
        return None
    
    def determine_asset_type(self, url: str, title: str = "", description: str = "") -> str:
        """Determine asset type based on URL and content"""
        url_lower = url.lower()
        title_lower = title.lower()
        desc_lower = description.lower()

        # Check for 3D keywords
        if any(keyword in url_lower or keyword in title_lower or keyword in desc_lower
               for keyword in ['3d', 'model', 'obj', 'fbx', 'blend', 'mesh', 'character model']):
            return '3d'

        # Check for audio keywords
        if any(keyword in url_lower or keyword in title_lower or keyword in desc_lower
               for keyword in ['audio', 'sound', 'music', 'sfx', 'mp3', 'wav', 'ogg']):
            return 'audio'

        # Default to 2D for sprites, textures, etc.
        return '2d'

    # ===== DEEP SCRAPING INTERFACE =====

    def enable_deep_scraping(self) -> None:
        """Enable deep scraping capabilities"""
        self.deep_scraping_enabled = True
        self.visited_urls = set()
        self.discovered_categories = set()
        self.pagination_urls = []

    def scrape_with_pagination(self, base_url: str, max_pages: int = 50, limit: int = None) -> List[Dict]:
        """Scrape with pagination support"""
        assets = []
        page = 1

        while page <= max_pages:
            if limit and len(assets) >= limit:
                break

            # Build page URL
            page_url = self._build_page_url(base_url, page)

            print(f"🔍 Scraping page {page}: {page_url}")
            soup = self.get_soup(page_url)
            if not soup:
                break

            # Extract assets from current page
            page_assets = self._extract_page_assets(soup)

            if not page_assets:
                print(f"📄 No more assets found on page {page}")
                break

            assets.extend(page_assets[:limit - len(assets) if limit else len(page_assets)])
            page += 1

        return assets

    def scrape_categories(self, categories: List[str], limit_per_category: int = None) -> List[Dict]:
        """Scrape multiple categories"""
        all_assets = []

        for category in categories:
            print(f"🎯 Scraping category: {category}")
            category_assets = self._scrape_category(category, limit_per_category)
            all_assets.extend(category_assets)
            self.discovered_categories.add(category)

        return all_assets

    def scrape_with_search(self, search_terms: List[str], max_pages_per_term: int = 10) -> List[Dict]:
        """Scrape using search functionality"""
        all_assets = []

        for term in search_terms:
            print(f"🔍 Searching for: {term}")
            search_assets = self._scrape_search_term(term, max_pages_per_term)
            all_assets.extend(search_assets)

        return all_assets

    # Abstract methods for deep scraping - to be implemented by subclasses
    def _build_page_url(self, base_url: str, page: int) -> str:
        """Build URL for specific page number"""
        return f"{base_url}?page={page}"

    def _extract_page_assets(self, soup) -> List[Dict]:
        """Extract assets from a page soup"""
        return []

    def _scrape_category(self, category: str, limit: int = None) -> List[Dict]:
        """Scrape specific category"""
        return []

    def _scrape_search_term(self, term: str, max_pages: int = 10) -> List[Dict]:
        """Scrape search results for a term"""
        return []

    def determine_category(self, title: str, description: str = "", tags: List[str] = None) -> str:
        """Determine asset category"""
        text = f"{title} {description} {' '.join(tags)}".lower()
        
        categories = {
            'characters': ['character', 'hero', 'player', 'npc', 'enemy', 'monster'],
            'ui': ['ui', 'interface', 'button', 'menu', 'hud', 'gui'],
            'backgrounds': ['background', 'scene', 'environment', 'landscape'],
            'icons': ['icon', 'symbol', 'logo', 'badge'],
            'tiles': ['tile', 'tileset', 'platform', 'ground'],
            'effects': ['effect', 'particle', 'explosion', 'magic', 'fire'],
            'weapons': ['weapon', 'sword', 'gun', 'bow', 'staff'],
            'vehicles': ['car', 'ship', 'plane', 'vehicle', 'transport']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return 'misc'
    
    def get_stats(self) -> Dict[str, Any]:
        """Get scraping statistics"""
        total_requests = self.stats['requests_made']
        if total_requests > 0:
            success_rate = self.stats['successful_requests'] / total_requests
            failure_rate = self.stats['failed_requests'] / total_requests
            bot_detection_rate = self.stats['bot_detections'] / total_requests
        else:
            success_rate = failure_rate = bot_detection_rate = 0
        
        return {
            **self.stats,
            'success_rate': success_rate,
            'failure_rate': failure_rate,
            'bot_detection_rate': bot_detection_rate,
            'security_enabled': self.enable_advanced_security
        }
    
    def cleanup(self):
        """Cleanup resources"""
        if hasattr(self, 'bot_bypass'):
            self.bot_bypass.cleanup()
        
        if hasattr(self, 'secure_scraper') and hasattr(self.secure_scraper, 'bot_bypass'):
            self.secure_scraper.bot_bypass.cleanup()
    
    @abstractmethod
    def scrape_assets(self, limit: int = None) -> List[Dict]:
        """Scrape assets from the site - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def get_download_url(self, asset_url: str) -> Optional[str]:
        """Get direct download URL - must be implemented by subclasses"""
        pass
