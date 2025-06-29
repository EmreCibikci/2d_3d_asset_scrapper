import requests
import time
import sys
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import config

# Add safe scraping module to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from safe_scraping import SafeScrapingManager, safe_request

class BaseScraper(ABC):
    """Base class for all site scrapers with safe and ethical scraping"""

    def __init__(self, site_name: str):
        self.site_name = site_name
        # Initialize safe scraping manager
        self.safe_scraper = SafeScrapingManager()

        print(f"🔒 {site_name} scraper initialized with safe scraping protocols")
        print(f"   ✅ Rate limiting enabled")
        print(f"   ✅ Robots.txt compliance enabled")
        print(f"   ✅ User-Agent rotation enabled")
        print(f"   ❌ Proxy usage disabled for security")
    
    def make_request(self, url: str, retries: int = None) -> Optional[requests.Response]:
        """Make HTTP request with safe scraping protocols"""
        print(f"🌐 Making safe request to: {url}")

        # Use safe scraping manager
        response = self.safe_scraper.safe_get(url)

        if response:
            print(f"✅ Request successful: {response.status_code}")
            return response
        else:
            print(f"❌ Request failed: {url}")
            return None
    
    def get_soup(self, url: str) -> Optional[BeautifulSoup]:
        """Get BeautifulSoup object from URL with safe scraping"""
        response = self.make_request(url)
        if response:
            return BeautifulSoup(response.content, 'html.parser')
        return None
    
    def delay(self):
        """Add intelligent delay between requests"""
        # Safe scraper handles delays automatically
        print("⏱️  Safe scraper handles delays automatically")
        pass

    def get_scraping_stats(self) -> Dict:
        """Get scraping statistics"""
        if hasattr(self.safe_scraper, 'request_times'):
            total_requests = sum(len(times) for times in self.safe_scraper.request_times.values())
            return {
                'total_requests': total_requests,
                'domains_accessed': len(self.safe_scraper.request_times),
                'site_name': self.site_name
            }
        return {'site_name': self.site_name}
    
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
    
    def determine_category(self, title: str, description: str = "", tags: List[str] = None) -> str:
        """Determine asset category"""
        text = f"{title} {description}".lower()
        tags = tags or []
        tag_text = " ".join(tags).lower()
        combined_text = f"{text} {tag_text}"
        
        categories = {
            'character': ['character', 'hero', 'enemy', 'npc', 'player', 'avatar', 'sprite'],
            'environment': ['environment', 'background', 'landscape', 'terrain', 'building', 'architecture'],
            'ui': ['ui', 'interface', 'button', 'menu', 'hud', 'icon', 'gui'],
            'effect': ['effect', 'particle', 'explosion', 'magic', 'fire', 'smoke', 'vfx'],
            'weapon': ['weapon', 'sword', 'gun', 'bow', 'staff', 'blade'],
            'item': ['item', 'collectible', 'pickup', 'treasure', 'coin', 'gem'],
            'tile': ['tile', 'tileset', 'platform', 'ground', 'wall'],
            'animation': ['animation', 'animated', 'sequence', 'frames']
        }
        
        for category, keywords in categories.items():
            if any(keyword in combined_text for keyword in keywords):
                return category
        
        return 'other'
    
    @abstractmethod
    def scrape_assets(self, limit: int = None) -> List[Dict]:
        """Scrape assets from the site. Must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def get_download_url(self, asset_url: str) -> Optional[str]:
        """Get direct download URL for an asset. Must be implemented by subclasses"""
        pass
