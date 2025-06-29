import re
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from .enhanced_base_scraper import EnhancedBaseScraper
import config

class ItchScraper(EnhancedBaseScraper):
    """Enhanced secure scraper for Itch.io game assets with advanced bot protection"""
    
    def __init__(self):
        super().__init__('itch_io', enable_advanced_security=True)
        self.base_url = 'https://itch.io'
        self.game_assets_url = 'https://itch.io/game-assets'
        self.free_assets_url = 'https://itch.io/game-assets/free'
    
    def scrape_assets(self, limit: int = None) -> List[Dict]:
        """Scrape free assets from Itch.io"""
        assets = []
        page = 1
        
        while True:
            if limit and len(assets) >= limit:
                break
                
            page_url = f"{self.free_assets_url}?page={page}"
            print(f"Scraping Itch.io page {page}...")
            
            soup = self.get_soup(page_url)
            if not soup:
                break
            
            # Find asset cards - Itch.io uses game_cell class
            asset_cards = soup.find_all('div', class_=['game_cell', 'game_link'])
            
            if not asset_cards:
                # Try alternative selectors
                asset_cards = soup.find_all('a', class_='game_link') or soup.find_all('div', class_='game_thumb')
            
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
            # Safety break
            if page > 50:
                break
        
        return assets
    
    def _extract_asset_data(self, card) -> Optional[Dict]:
        """Extract asset data from a card element"""
        try:
            # Find title and URL
            if card.name == 'a':
                asset_url = urljoin(self.base_url, card.get('href'))
                title_elem = card.find('div', class_='game_title') or card.find('div', class_='title')
            else:
                link_elem = card.find('a', class_='game_link') or card.find('a')
                if not link_elem:
                    return None
                asset_url = urljoin(self.base_url, link_elem.get('href'))
                title_elem = card.find('div', class_='game_title') or card.find('div', class_='title')
            
            if not title_elem:
                # Try to get title from link text
                title_elem = card.find('a')
                if title_elem:
                    title = title_elem.get_text(strip=True)
                else:
                    return None
            else:
                title = title_elem.get_text(strip=True)
            
            if not title:
                return None
            
            # Find description
            desc_elem = card.find('div', class_='game_text') or card.find('div', class_='game_short_text')
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # Find preview image
            img_elem = card.find('img')
            preview_url = None
            if img_elem:
                img_src = img_elem.get('src') or img_elem.get('data-src')
                if img_src:
                    preview_url = urljoin(self.base_url, img_src)
            
            # Find author
            author_elem = card.find('div', class_='game_author') or card.find('a', class_='user_link')
            author = author_elem.get_text(strip=True) if author_elem else ""
            
            # Extract tags
            tags = self._extract_tags(title, description, card)
            
            # Check if it's free
            price_elem = card.find('div', class_='price_value') or card.find('span', class_='price')
            is_free = True
            if price_elem:
                price_text = price_elem.get_text(strip=True).lower()
                is_free = 'free' in price_text or '$0' in price_text or price_text == ''
            
            return {
                'title': title,
                'description': f"{description} (by {author})" if author else description,
                'url': asset_url,
                'source_site': self.site_name,
                'asset_type': self.determine_asset_type(asset_url, title, description),
                'category': self.determine_category(title, description, tags),
                'tags': tags,
                'preview_url': preview_url,
                'is_free': is_free,
                'license_info': 'Check individual asset page for license details'
            }
            
        except Exception as e:
            print(f"Error extracting asset data: {e}")
            return None
    
    def _extract_tags(self, title: str, description: str, card) -> List[str]:
        """Extract tags from title, description, and card element"""
        tags = []
        text = f"{title} {description}".lower()
        
        # Look for tag elements
        tag_elements = card.find_all('span', class_='tag') or card.find_all('a', class_='tag')
        for tag_elem in tag_elements:
            tag_text = tag_elem.get_text(strip=True)
            if tag_text:
                tags.append(tag_text.lower())
        
        # Common Itch.io game asset tags
        tag_keywords = [
            '2d', '3d', 'sprite', 'pixel art', 'vector', 'tileset', 'character',
            'background', 'ui', 'icon', 'sound', 'music', 'sfx', 'texture',
            'animation', 'platformer', 'rpg', 'puzzle', 'shooter', 'horror',
            'fantasy', 'sci-fi', 'medieval', 'modern', 'cartoon', 'realistic'
        ]
        
        for keyword in tag_keywords:
            if keyword in text and keyword not in tags:
                tags.append(keyword)
        
        return tags
    
    def get_download_url(self, asset_url: str) -> Optional[str]:
        """Get direct download URL for an Itch.io asset"""
        soup = self.get_soup(asset_url)
        if not soup:
            return None
        
        # Itch.io has different download patterns
        download_selectors = [
            'a.button.download_btn',
            'a[href*="/download/"]',
            '.download_btn',
            'a.download_link',
            '.game_download_btn a',
            'a[href*=".zip"]',
            'a[href*=".rar"]'
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
        
        # Look for file attachments or direct links
        file_links = soup.find_all('a', href=re.compile(r'\.(zip|rar|7z|tar\.gz|png|jpg|wav|mp3)$', re.I))
        if file_links:
            return urljoin(self.base_url, file_links[0].get('href'))
        
        return None
