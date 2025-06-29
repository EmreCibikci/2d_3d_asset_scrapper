import re
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse, parse_qs
from .enhanced_base_scraper import EnhancedBaseScraper
import config

class OpenGameArtScraper(EnhancedBaseScraper):
    """Enhanced secure scraper for OpenGameArt.org with advanced bot protection"""
    
    def __init__(self):
        super().__init__('opengameart', enable_advanced_security=True)
        self.base_url = config.SITES_CONFIG['opengameart']['base_url']
        self.search_url = f"{self.base_url}/art-search-advanced"
    
    def scrape_assets(self, limit: int = None) -> List[Dict]:
        """Scrape assets from OpenGameArt.org"""
        assets = []
        page = 0
        
        while True:
            if limit and len(assets) >= limit:
                break
            
            page_url = f"{self.search_url}?page={page}"
            print(f"Scraping OpenGameArt page {page}...")
            
            soup = self.get_soup(page_url)
            if not soup:
                break
            
            asset_entries = soup.find_all('div', class_=['art-preview', 'view-art-search'])
            
            if not asset_entries:
                asset_entries = soup.find_all('div', class_='views-row') or soup.find_all('article')
            
            if not asset_entries:
                print(f"No more assets found on page {page}")
                break
            
            for entry in asset_entries:
                if limit and len(assets) >= limit:
                    break
                
                try:
                    asset_data = self._extract_asset_data(entry)
                    if asset_data:
                        assets.append(asset_data)
                        print(f"Found asset: {asset_data['title']}")
                except Exception as e:
                    print(f"Error extracting asset data: {e}")
                    continue
            
            page += 1
            # Enhanced base scraper handles delays automatically
            if page > 100:
                break
        
        return assets
    
    def _extract_asset_data(self, entry) -> Optional[Dict]:
        """Extract asset data from an entry element"""
        try:
            title_elem = (entry.find('h3') or entry.find('h2') or entry.find('a', class_='title'))
            
            if not title_elem:
                title_elem = entry.find('a')
            
            if not title_elem:
                return None
            
            title = title_elem.get_text(strip=True)
            
            link_elem = title_elem if title_elem.name == 'a' else title_elem.find('a')
            if not link_elem:
                return None
            
            asset_url = urljoin(self.base_url, link_elem.get('href'))
            
            desc_elem = entry.find('div', class_='description') or entry.find('p')
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            img_elem = entry.find('img')
            preview_url = None
            if img_elem:
                img_src = img_elem.get('src') or img_elem.get('data-src')
                if img_src:
                    preview_url = urljoin(self.base_url, img_src)
            
            license_elem = entry.find('div', class_='license') or entry.find('span', class_='license')
            license_info = license_elem.get_text(strip=True) if license_elem else "Check asset page for license"
            
            tags = self._extract_tags(title, description, entry)
            
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
                'license_info': license_info
            }
            
        except Exception as e:
            print(f"Error extracting asset data: {e}")
            return None
    
    def _extract_tags(self, title: str, description: str, entry) -> List[str]:
        """Extract tags from title, description, and entry element"""
        tags = []
        text = f"{title} {description}".lower()
        
        tag_elements = entry.find_all('span', class_='tag') or entry.find_all('a', class_='tag')
        for tag_elem in tag_elements:
            tag_text = tag_elem.get_text(strip=True)
            if tag_text:
                tags.append(tag_text.lower())
        
        tag_keywords = [
            '2d', '3d', 'sprite', 'texture', 'model', 'sound', 'music',
            'character', 'background', 'tile', 'ui', 'icon', 'weapon',
            'fantasy', 'sci-fi', 'medieval', 'modern', 'cartoon', 'realistic',
            'pixel art', 'vector', 'low poly', 'high poly'
        ]
        
        for keyword in tag_keywords:
            if keyword in text and keyword not in tags:
                tags.append(keyword)
        
        return tags
    
    def get_download_url(self, asset_url: str) -> Optional[str]:
        """Get direct download URL for an OpenGameArt asset"""
        soup = self.get_soup(asset_url)
        if not soup:
            return None
        
        download_selectors = [
            'a[href*="/sites/default/files/"]',
            '.file a',
            '.attachment a',
            'a[href*=".zip"]',
            'a[href*=".rar"]',
            'a[href*=".tar"]',
            'a[href*=".7z"]'
        ]
        
        for selector in download_selectors:
            download_elem = soup.select_one(selector)
            if download_elem:
                download_url = download_elem.get('href')
                if download_url:
                    return urljoin(self.base_url, download_url)
        
        file_links = soup.find_all('a', href=re.compile(r'\.(zip|rar|7z|tar\.gz|png|jpg|ogg|wav|mp3)$', re.I))
        if file_links:
            return urljoin(self.base_url, file_links[0].get('href'))
        
        return None
