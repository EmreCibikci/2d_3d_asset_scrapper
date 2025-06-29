import re
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from .enhanced_base_scraper import EnhancedBaseScraper
import config

class FreepikScraper(EnhancedBaseScraper):
    """Enhanced secure scraper for Freepik free resources with advanced bot protection"""
    
    def __init__(self):
        super().__init__('freepik', enable_advanced_security=True)
        self.base_url = 'https://www.freepik.com'
        self.free_vectors_url = 'https://www.freepik.com/free-vectors'
        self.game_graphics_url = 'https://www.freepik.com/search?format=search&query=game+graphics&type=vector'
    
    def scrape_assets(self, limit: int = None) -> List[Dict]:
        """Scrape free vectors from Freepik"""
        assets = []
        page = 1
        
        # Search for game-related graphics
        search_terms = [
            'game+sprites', 'game+characters', 'game+ui', 'game+icons',
            'pixel+art', 'game+backgrounds', 'game+tiles', 'game+assets'
        ]
        
        for search_term in search_terms:
            if limit and len(assets) >= limit:
                break
                
            search_url = f"{self.base_url}/search?format=search&query={search_term}&type=vector"
            page_assets = self._scrape_search_results(search_url, limit - len(assets) if limit else None)
            assets.extend(page_assets)
            # Enhanced base scraper handles delays automatically
        return assets
    
    def _scrape_search_results(self, search_url: str, limit: int = None) -> List[Dict]:
        """Scrape search results from a specific URL"""
        assets = []
        page = 1
        
        while True:
            if limit and len(assets) >= limit:
                break
                
            page_url = f"{search_url}&page={page}"
            print(f"Scraping Freepik search page {page}...")
            
            soup = self.get_soup(page_url)
            if not soup:
                break
            
            # Find asset cards
            asset_cards = soup.find_all('figure', class_=['showcase__item', 'grid-item'])
            
            if not asset_cards:
                # Try alternative selectors
                asset_cards = soup.find_all('div', class_='resource') or soup.find_all('article')
            
            if not asset_cards:
                print(f"No more assets found on page {page}")
                break
            
            for card in asset_cards:
                if limit and len(assets) >= limit:
                    break
                
                try:
                    asset_data = self._extract_asset_data(card)
                    if asset_data and asset_data.get('is_free', False):
                        assets.append(asset_data)
                        print(f"Found free asset: {asset_data['title']}")
                except Exception as e:
                    print(f"Error extracting asset data: {e}")
                    continue
            
            page += 1
            # Enhanced base scraper handles delays automatically
            # Safety break
            if page > 10:  # Freepik has many pages, limit for free content
                break
        
        return assets
    
    def _extract_asset_data(self, card) -> Optional[Dict]:
        """Extract asset data from a card element"""
        try:
            # Find title and URL
            link_elem = card.find('a') or card.find('a', href=True)
            if not link_elem:
                return None
            
            asset_url = urljoin(self.base_url, link_elem.get('href'))
            
            # Find title
            title_elem = (card.find('h3') or 
                         card.find('h2') or 
                         card.find('span', class_='title') or
                         link_elem)
            
            title = title_elem.get_text(strip=True) if title_elem else "Freepik Asset"
            
            # Find description (usually in alt text or title attribute)
            img_elem = card.find('img')
            description = ""
            if img_elem:
                description = img_elem.get('alt', '') or img_elem.get('title', '')
            
            # Find preview image
            preview_url = None
            if img_elem:
                img_src = img_elem.get('src') or img_elem.get('data-src') or img_elem.get('data-lazy-src')
                if img_src:
                    preview_url = urljoin(self.base_url, img_src)
            
            # Check if it's free (Freepik has premium and free content)
            is_free = self._check_if_free(card)
            
            # Extract tags
            tags = self._extract_tags(title, description, card)
            
            return {
                'title': title,
                'description': description,
                'url': asset_url,
                'source_site': self.site_name,
                'asset_type': self.determine_asset_type(asset_url, title, description),
                'category': self.determine_category(title, description, tags),
                'tags': tags,
                'preview_url': preview_url,
                'is_free': is_free,
                'license_info': 'Freepik License (attribution required for free use)'
            }
            
        except Exception as e:
            print(f"Error extracting asset data: {e}")
            return None
    
    def _check_if_free(self, card) -> bool:
        """Check if the asset is free"""
        # Look for premium indicators
        premium_indicators = card.find_all(['span', 'div'], class_=re.compile(r'premium|pro|paid', re.I))
        if premium_indicators:
            return False
        
        # Look for free indicators
        free_indicators = card.find_all(['span', 'div'], class_=re.compile(r'free', re.I))
        if free_indicators:
            return True
        
        # If no clear indicator, assume it might be free (will be filtered later)
        return True
    
    def _extract_tags(self, title: str, description: str, card) -> List[str]:
        """Extract tags from title, description, and card element"""
        tags = []
        text = f"{title} {description}".lower()
        
        # Freepik-specific tags
        tag_keywords = [
            'vector', 'illustration', 'graphic', 'design', 'icon', 'logo',
            'character', 'cartoon', 'flat', 'minimal', 'modern', 'vintage',
            'game', 'gaming', 'pixel', 'sprite', 'ui', 'interface',
            'background', 'pattern', 'texture', 'abstract'
        ]
        
        for keyword in tag_keywords:
            if keyword in text and keyword not in tags:
                tags.append(keyword)
        
        return tags
    
    def get_download_url(self, asset_url: str) -> Optional[str]:
        """Get direct download URL for a Freepik asset"""
        soup = self.get_soup(asset_url)
        if not soup:
            return None
        
        # Freepik requires login for downloads, but we can try to find direct links
        download_selectors = [
            'a[href*="/download"]',
            '.download-button',
            'a.download',
            '.btn-download',
            'a[href*=".svg"]',
            'a[href*=".eps"]',
            'a[href*=".ai"]'
        ]
        
        for selector in download_selectors:
            download_elem = soup.select_one(selector)
            if download_elem:
                download_url = download_elem.get('href')
                if download_url:
                    if download_url.startswith('http'):
                        return download_url
                    else:
                        return urljoin(self.base_url, download_url)
        
        # Note: Freepik usually requires account login for downloads
        return None
