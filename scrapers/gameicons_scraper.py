import re
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from .enhanced_base_scraper import EnhancedBaseScraper
import config

class GameIconsScraper(EnhancedBaseScraper):
    """Enhanced secure scraper for Game-Icons.net with advanced bot protection"""
    
    def __init__(self):
        super().__init__('game_icons', enable_advanced_security=True)
        self.base_url = 'https://game-icons.net'
        self.icons_url = 'https://game-icons.net/tags/game.html'
    
    def scrape_assets(self, limit: int = None) -> List[Dict]:
        """Scrape icons from Game-Icons.net"""
        assets = []
        
        # Game-Icons.net has different categories
        categories = [
            'game', 'weapon', 'armor', 'magic', 'creature', 'item',
            'skill', 'spell', 'potion', 'treasure', 'tool', 'symbol'
        ]
        
        for category in categories:
            if limit and len(assets) >= limit:
                break
                
            category_url = f"{self.base_url}/tags/{category}.html"
            print(f"Scraping Game-Icons category: {category}")
            
            category_assets = self._scrape_category(category_url, category, limit - len(assets) if limit else None)
            assets.extend(category_assets)
            # Enhanced base scraper handles delays automatically
        return assets
    
    def _scrape_category(self, category_url: str, category: str, limit: int = None) -> List[Dict]:
        """Scrape icons from a specific category"""
        assets = []
        
        soup = self.get_soup(category_url)
        if not soup:
            return assets
        
        # Find icon elements
        icon_elements = soup.find_all('div', class_='icon') or soup.find_all('a', class_='icon-link')
        
        if not icon_elements:
            # Try alternative selectors
            icon_elements = soup.find_all('img') or soup.find_all('svg')
        
        for icon_elem in icon_elements:
            if limit and len(assets) >= limit:
                break
            
            try:
                asset_data = self._extract_icon_data(icon_elem, category)
                if asset_data:
                    assets.append(asset_data)
                    print(f"Found icon: {asset_data['title']}")
            except Exception as e:
                print(f"Error extracting icon data: {e}")
                continue
        
        return assets
    
    def _extract_icon_data(self, icon_elem, category: str) -> Optional[Dict]:
        """Extract icon data from an icon element"""
        try:
            # Find icon URL and title
            if icon_elem.name == 'a':
                icon_url = urljoin(self.base_url, icon_elem.get('href'))
                title_elem = icon_elem.find('img') or icon_elem
            else:
                # Look for parent link
                parent_link = icon_elem.find_parent('a')
                if parent_link:
                    icon_url = urljoin(self.base_url, parent_link.get('href'))
                else:
                    icon_url = self.base_url
                title_elem = icon_elem
            
            # Get title from alt text, title attribute, or filename
            title = ""
            if icon_elem.name == 'img':
                title = icon_elem.get('alt', '') or icon_elem.get('title', '')
            elif icon_elem.name == 'svg':
                title_tag = icon_elem.find('title')
                title = title_tag.get_text(strip=True) if title_tag else ""
            
            if not title:
                # Try to extract from URL
                parsed_url = urlparse(icon_url)
                title = parsed_url.path.split('/')[-1].replace('.html', '').replace('-', ' ').title()
            
            if not title:
                title = f"Game Icon ({category})"
            
            # Find preview/download URL
            preview_url = None
            download_url = None
            
            if icon_elem.name == 'img':
                img_src = icon_elem.get('src')
                if img_src:
                    preview_url = urljoin(self.base_url, img_src)
                    # Game-Icons.net usually has SVG versions
                    if img_src.endswith('.png'):
                        download_url = img_src.replace('.png', '.svg')
                    else:
                        download_url = img_src
            
            # Generate description
            description = f"Game icon from {category} category. High-quality SVG icon suitable for games and applications."
            
            # Extract tags
            tags = self._extract_tags(title, category)
            
            return {
                'title': title,
                'description': description,
                'url': icon_url,
                'source_site': self.site_name,
                'asset_type': '2d',
                'category': 'ui',
                'tags': tags,
                'preview_url': preview_url,
                'download_url': download_url,
                'is_free': True,
                'license_info': 'CC BY 3.0 (Creative Commons Attribution)'
            }
            
        except Exception as e:
            print(f"Error extracting icon data: {e}")
            return None
    
    def _extract_tags(self, title: str, category: str) -> List[str]:
        """Extract tags from title and category"""
        tags = [category, 'icon', 'svg', 'game', 'ui']
        
        title_lower = title.lower()
        
        # Add specific tags based on title content
        tag_keywords = {
            'weapon': ['sword', 'gun', 'bow', 'axe', 'knife', 'blade'],
            'magic': ['spell', 'wand', 'crystal', 'potion', 'scroll'],
            'creature': ['monster', 'dragon', 'beast', 'animal'],
            'armor': ['shield', 'helmet', 'chest', 'boot'],
            'item': ['treasure', 'coin', 'gem', 'key', 'tool'],
            'skill': ['ability', 'power', 'talent', 'expertise']
        }
        
        for tag_category, keywords in tag_keywords.items():
            for keyword in keywords:
                if keyword in title_lower:
                    tags.append(tag_category)
                    break
        
        return list(set(tags))  # Remove duplicates
    
    def get_download_url(self, asset_url: str) -> Optional[str]:
        """Get direct download URL for a Game-Icons asset"""
        soup = self.get_soup(asset_url)
        if not soup:
            return None
        
        # Game-Icons.net has direct SVG downloads
        download_selectors = [
            'a[href*=".svg"]',
            'a[download]',
            '.download-link',
            'a[href*="/download/"]'
        ]
        
        for selector in download_selectors:
            download_elem = soup.select_one(selector)
            if download_elem:
                download_url = download_elem.get('href')
                if download_url:
                    return urljoin(self.base_url, download_url)
        
        # Look for SVG elements that can be downloaded
        svg_elem = soup.find('svg')
        if svg_elem:
            # We could potentially extract the SVG content here
            # For now, return the page URL as download might be available there
            return asset_url
        
        return None
