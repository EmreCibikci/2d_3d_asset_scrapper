import re
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from .enhanced_base_scraper import EnhancedBaseScraper
import config

class CraftPixScraper(EnhancedBaseScraper):
    """Enhanced secure scraper for CraftPix.net freebies with advanced bot protection"""
    
    def __init__(self):
        super().__init__('craftpix', enable_advanced_security=True)
        self.base_url = config.SITES_CONFIG['craftpix']['base_url']
        self.freebies_url = config.SITES_CONFIG['craftpix']['freebies_url']
    
    def scrape_assets(self, limit: int = None) -> List[Dict]:
        """Scrape free assets from CraftPix"""
        assets = []
        page = 1
        
        while True:
            if limit and len(assets) >= limit:
                break
                
            page_url = f"{self.freebies_url}?page={page}"
            print(f"Scraping CraftPix page {page}...")
            
            soup = self.get_soup(page_url)
            if not soup:
                break
            
            # Find asset cards
            asset_cards = soup.find_all('div', class_=['product-item', 'item-product'])
            
            if not asset_cards:
                # Try alternative selectors
                asset_cards = soup.find_all('article') or soup.find_all('div', class_='post')
            
            if not asset_cards:
                print(f"No more assets found on page {page}")
                break
            
            for card in asset_cards:
                if limit and len(assets) >= limit:
                    break
                
                try:
                    asset_data = self._extract_asset_data(card)
                    if asset_data:
                        assets.append(asset_data)
                        print(f"Found asset: {asset_data['title']}")
                except Exception as e:
                    print(f"Error extracting asset data: {e}")
                    continue
            
            page += 1
            # Enhanced base scraper handles delays automatically
            # Safety break to avoid infinite loops
            if page > 50:
                break
        
        return assets
    
    def _extract_asset_data(self, card) -> Optional[Dict]:
        """Extract asset data from a card element"""
        try:
            # Find title
            title_elem = (card.find('h3') or 
                         card.find('h2') or 
                         card.find('a', class_='title') or
                         card.find('a'))
            
            if not title_elem:
                return None
            
            title = title_elem.get_text(strip=True)
            
            # Find asset URL
            link_elem = title_elem if title_elem.name == 'a' else title_elem.find('a')
            if not link_elem:
                link_elem = card.find('a')
            
            if not link_elem:
                return None
            
            asset_url = urljoin(self.base_url, link_elem.get('href'))
            
            # Find description
            desc_elem = card.find('p') or card.find('div', class_='description')
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # Find preview image
            img_elem = card.find('img')
            preview_url = None
            if img_elem:
                img_src = img_elem.get('src') or img_elem.get('data-src')
                if img_src:
                    preview_url = urljoin(self.base_url, img_src)
            
            # Extract tags from title and description
            tags = self._extract_tags(title, description)
            
            return {
                'title': title,
                'description': description,
                'url': asset_url,
                'source_site': self.site_name,
                'asset_type': self.determine_asset_type(asset_url, title, description),
                'category': self.determine_category(title, description, tags),
                'tags': tags,
                'preview_url': preview_url,
                'is_free': True,
                'license_info': 'Free for commercial use'
            }
            
        except Exception as e:
            print(f"Error extracting asset data: {e}")
            return None
    
    def _extract_tags(self, title: str, description: str) -> List[str]:
        """Extract tags from title and description"""
        tags = []
        text = f"{title} {description}".lower()
        
        # Common game asset tags
        tag_keywords = [
            '2d', '3d', 'sprite', 'character', 'background', 'ui', 'icon',
            'pixel art', 'cartoon', 'fantasy', 'sci-fi', 'medieval', 'modern',
            'animation', 'tileset', 'platformer', 'rpg', 'shooter', 'puzzle'
        ]
        
        for keyword in tag_keywords:
            if keyword in text:
                tags.append(keyword)
        
        return tags
    
    def get_download_url(self, asset_url: str) -> Optional[str]:
        """Get direct download URL for a CraftPix asset"""
        soup = self.get_soup(asset_url)
        if not soup:
            return None

        # CraftPix often requires registration, look for direct file links first
        # Look for meta tags with file info
        meta_download = soup.find('meta', {'property': 'og:url'})
        if meta_download:
            # Sometimes the download is in a different format
            pass

        # Look for download button or link with more specific selectors
        download_selectors = [
            'a.btn.btn-primary[href*="download"]',
            'a.download-btn',
            'a.btn-download',
            '.download-link a',
            'a[href*="/download/"]',
            'a[href*=".zip"]',
            'a[href*=".rar"]',
            '.btn-group a[href*="download"]'
        ]

        for selector in download_selectors:
            download_elem = soup.select_one(selector)
            if download_elem:
                download_url = download_elem.get('href')
                if download_url:
                    full_url = urljoin(self.base_url, download_url)
                    print(f"Found download URL: {full_url}")
                    return full_url

        # Look for JavaScript-based download links
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                # Look for download URLs in JavaScript
                if 'download' in script.string and ('.zip' in script.string or '.rar' in script.string):
                    # Extract URL from JavaScript (basic pattern matching)
                    import re
                    url_pattern = r'["\']([^"\']*(?:\.zip|\.rar)[^"\']*)["\']'
                    matches = re.findall(url_pattern, script.string)
                    if matches:
                        download_url = matches[0]
                        if download_url.startswith('http'):
                            return download_url
                        else:
                            return urljoin(self.base_url, download_url)

        # Look for direct file links in the page
        file_links = soup.find_all('a', href=re.compile(r'\.(zip|rar|7z|tar\.gz)$', re.I))
        if file_links:
            return urljoin(self.base_url, file_links[0].get('href'))

        # If no direct download found, return None (site may require login)
        print(f"No download URL found for: {asset_url}")
        return None
