import re
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from .enhanced_base_scraper import EnhancedBaseScraper
import config

class PixabayScraper(EnhancedBaseScraper):
    """Enhanced secure scraper for Pixabay free images and vectors with advanced bot protection"""
    
    def __init__(self):
        super().__init__('pixabay', enable_advanced_security=True)
        self.base_url = 'https://pixabay.com'
        self.search_url = 'https://pixabay.com/images/search'
    
    def scrape_assets(self, limit: int = None) -> List[Dict]:
        """Scrape game-related images from Pixabay"""
        assets = []
        
        # Search terms for game development
        search_terms = [
            'game+background', 'game+texture', 'pixel+art', 'game+sprite',
            'game+character', 'game+ui', 'game+icon', 'fantasy+background',
            'sci-fi+texture', 'medieval+background', 'space+background',
            'forest+background', 'castle+background', 'dungeon+texture'
        ]
        
        for search_term in search_terms:
            if limit and len(assets) >= limit:
                break
                
            print(f"Searching Pixabay for: {search_term.replace('+', ' ')}")
            search_assets = self._scrape_search_term(search_term, limit - len(assets) if limit else None)
            assets.extend(search_assets)
            # Enhanced base scraper handles delays automatically
        return assets
    
    def _scrape_search_term(self, search_term: str, limit: int = None) -> List[Dict]:
        """Scrape search results for a specific term"""
        assets = []
        page = 1
        
        while True:
            if limit and len(assets) >= limit:
                break
                
            # Pixabay search URL format
            page_url = f"{self.search_url}/{search_term}/?pagi={page}"
            print(f"Scraping Pixabay page {page} for {search_term}")
            
            soup = self.get_soup(page_url)
            if not soup:
                break
            
            # Find image containers
            image_containers = soup.find_all('div', class_=['item', 'image-container'])
            
            if not image_containers:
                # Try alternative selectors
                image_containers = soup.find_all('a', href=re.compile(r'/photos/'))
            
            if not image_containers:
                print(f"No more images found on page {page}")
                break
            
            for container in image_containers:
                if limit and len(assets) >= limit:
                    break
                
                try:
                    asset_data = self._extract_image_data(container)
                    if asset_data:
                        assets.append(asset_data)
                        print(f"Found image: {asset_data['title']}")
                except Exception as e:
                    print(f"Error extracting image data: {e}")
                    continue
            
            page += 1
            # Enhanced base scraper handles delays automatically
            # Safety break
            if page > 5:  # Limit pages for each search term
                break
        
        return assets
    
    def _extract_image_data(self, container) -> Optional[Dict]:
        """Extract image data from a container element"""
        try:
            # Find image URL
            if container.name == 'a':
                image_url = urljoin(self.base_url, container.get('href'))
                img_elem = container.find('img')
            else:
                link_elem = container.find('a')
                if not link_elem:
                    return None
                image_url = urljoin(self.base_url, link_elem.get('href'))
                img_elem = container.find('img')
            
            if not img_elem:
                return None
            
            # Get title from alt text or data attributes
            title = (img_elem.get('alt', '') or 
                    img_elem.get('data-alt', '') or 
                    img_elem.get('title', '') or
                    "Pixabay Image")
            
            # Get preview image URL
            preview_url = img_elem.get('src') or img_elem.get('data-src')
            if preview_url:
                preview_url = urljoin(self.base_url, preview_url)
            
            # Get image dimensions if available
            width = img_elem.get('data-width', '')
            height = img_elem.get('data-height', '')
            dimensions = f"{width}x{height}" if width and height else ""
            
            # Generate description
            description = f"High-quality image from Pixabay. {dimensions}".strip()
            
            # Extract tags from title and URL
            tags = self._extract_tags(title, image_url)
            
            # Determine category based on content
            category = self._determine_image_category(title, tags)
            
            return {
                'title': title,
                'description': description,
                'url': image_url,
                'source_site': self.site_name,
                'asset_type': '2d',
                'category': category,
                'tags': tags,
                'preview_url': preview_url,
                'is_free': True,
                'license_info': 'Pixabay License (free for commercial use, no attribution required)'
            }
            
        except Exception as e:
            print(f"Error extracting image data: {e}")
            return None
    
    def _extract_tags(self, title: str, url: str) -> List[str]:
        """Extract tags from title and URL"""
        tags = []
        text = f"{title} {url}".lower()
        
        # Game development related tags
        tag_keywords = [
            'background', 'texture', 'pattern', 'abstract', 'fantasy',
            'sci-fi', 'medieval', 'space', 'forest', 'castle', 'dungeon',
            'pixel', 'art', 'game', 'digital', 'illustration', 'graphic',
            'nature', 'landscape', 'sky', 'water', 'fire', 'ice', 'stone',
            'metal', 'wood', 'fabric', 'paper', 'grunge', 'vintage'
        ]
        
        for keyword in tag_keywords:
            if keyword in text:
                tags.append(keyword)
        
        return tags
    
    def _determine_image_category(self, title: str, tags: List[str]) -> str:
        """Determine image category based on title and tags"""
        title_lower = title.lower()
        tags_text = ' '.join(tags).lower()
        combined_text = f"{title_lower} {tags_text}"
        
        if any(word in combined_text for word in ['background', 'landscape', 'sky', 'forest', 'castle']):
            return 'environment'
        elif any(word in combined_text for word in ['texture', 'pattern', 'material', 'surface']):
            return 'texture'
        elif any(word in combined_text for word in ['character', 'person', 'creature', 'monster']):
            return 'character'
        elif any(word in combined_text for word in ['ui', 'interface', 'button', 'icon']):
            return 'ui'
        else:
            return 'other'
    
    def get_download_url(self, asset_url: str) -> Optional[str]:
        """Get direct download URL for a Pixabay image"""
        soup = self.get_soup(asset_url)
        if not soup:
            return None
        
        # Pixabay has download buttons for different sizes
        download_selectors = [
            'a[href*="/download/"]',
            '.download',
            'a[download]',
            '.btn-download',
            'a[href*=".jpg"]',
            'a[href*=".png"]'
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
        
        # Look for the largest image size available
        img_elem = soup.find('img', {'id': 'image'})
        if img_elem:
            img_src = img_elem.get('src')
            if img_src:
                return urljoin(self.base_url, img_src)
        
        return None
