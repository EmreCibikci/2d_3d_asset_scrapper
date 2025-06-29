"""
Enhanced secure scraper for Quaternius.com low poly assets with advanced bot protection
"""

import re
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from .enhanced_base_scraper import EnhancedBaseScraper
import config

class QuaterniusScraper(EnhancedBaseScraper):
    """Enhanced secure scraper for Quaternius.com low poly assets"""
    
    def __init__(self):
        super().__init__('quaternius', enable_advanced_security=True)
        self.base_url = 'https://quaternius.com'
        self.assets_url = 'https://quaternius.com'
        
    def scrape_assets(self, limit: int = None) -> List[Dict]:
        """Scrape low poly assets from Quaternius with deep scraping"""
        assets = []

        try:
            print(f"🔍 Starting Quaternius deep scraping (limit: {limit or 'unlimited'})")
            self.enable_deep_scraping()

            # 1. Scrape main page and discover categories
            print("📄 Scraping main page...")
            main_assets = self._scrape_main_page(limit)
            assets.extend(main_assets)

            if limit and len(assets) >= limit:
                return assets[:limit]

            # 2. Scrape discovered categories
            print("🎯 Scraping categories...")
            categories = ['characters', 'vehicles', 'buildings', 'nature', 'props', 'weapons', 'animals']
            category_assets = self.scrape_categories(categories, limit_per_category=30)

            # Filter out duplicates
            new_assets = [a for a in category_assets if a['source_url'] not in [existing['source_url'] for existing in assets]]
            assets.extend(new_assets[:limit - len(assets) if limit else len(new_assets)])

            if limit and len(assets) >= limit:
                return assets[:limit]

            # 3. Search-based scraping
            print("🔍 Performing search-based scraping...")
            search_terms = ['low poly', '3d model', 'character', 'vehicle', 'building', 'prop']
            search_assets = self.scrape_with_search(search_terms, max_pages_per_term=3)

            # Filter out duplicates
            new_search_assets = [a for a in search_assets if a['source_url'] not in [existing['source_url'] for existing in assets]]
            assets.extend(new_search_assets[:limit - len(assets) if limit else len(new_search_assets)])

            # Log security statistics
            stats = self.get_stats()
            if stats['bot_detections'] > 0:
                print(f"⚠️ Bot protection encountered {stats['bot_detections']} times")
            print(f"📊 Success rate: {stats['success_rate']:.1%} ({stats['successful_requests']}/{stats['requests_made']} requests)")
            print(f"✅ Quaternius deep scraping completed: {len(assets)} assets found")

        except Exception as e:
            print(f"💥 Quaternius scraping failed: {e}")

        return assets[:limit] if limit else assets
    
    def _find_asset_links(self, soup) -> List[str]:
        """Find asset page links"""
        asset_links = []
        
        # Look for asset cards, galleries, or download sections
        link_selectors = [
            'a[href*="asset"]',
            'a[href*="model"]',
            'a[href*="pack"]',
            '.asset-card a',
            '.model-card a',
            '.gallery a',
            '.download a'
        ]
        
        for selector in link_selectors:
            links = soup.select(selector)
            for link in links:
                href = link.get('href')
                if href:
                    full_url = urljoin(self.base_url, href)
                    if full_url not in asset_links:
                        asset_links.append(full_url)
        
        # Look for direct download links or asset pages
        all_links = soup.find_all('a', href=True)
        for link in all_links:
            href = link.get('href')
            if href:
                # Check if link contains asset-related keywords
                if any(keyword in href.lower() for keyword in ['asset', 'model', 'pack', 'download', 'free']):
                    full_url = urljoin(self.base_url, href)
                    if full_url not in asset_links and self.base_url in full_url:
                        asset_links.append(full_url)
        
        return asset_links[:30]  # Limit to avoid overwhelming
    
    def _extract_asset_data(self, asset_url: str) -> Optional[Dict]:
        """Extract asset data from individual asset page"""
        soup = self.get_soup(asset_url)
        if not soup:
            return None
        
        # Extract title
        title = self._extract_title(soup)
        if not title:
            return None
        
        # Extract other data
        description = self._extract_description(soup)
        download_url = self._extract_download_url(soup, asset_url)
        preview_image = self._extract_preview_image(soup, asset_url)
        tags = self._extract_tags(soup)
        
        # Determine asset type and category
        asset_type = self.determine_asset_type(asset_url, title, description)
        category = self.determine_category(title, description, tags)
        
        # Quaternius specializes in low poly 3D models
        if asset_type == '2d':
            asset_type = '3d'  # Override since Quaternius is primarily 3D
        
        return {
            'title': title,
            'description': description or '',
            'download_url': download_url,
            'preview_image': preview_image,
            'source_url': asset_url,
            'site': 'quaternius',
            'license': 'CC0',  # Quaternius uses CC0 license
            'tags': tags + ['low-poly', '3d'],  # Add characteristic tags
            'asset_type': asset_type,
            'category': category,
            'file_size': 'unknown',
            'format': self._guess_format_from_url(download_url or asset_url)
        }
    
    def _extract_title(self, soup) -> Optional[str]:
        """Extract asset title"""
        title_selectors = [
            'h1',
            'h2',
            '.title',
            '.asset-title',
            '.model-title',
            '[class*="title"]'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                title = element.get_text(strip=True)
                if title and len(title) > 3:
                    return title
        
        # Fallback to page title
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text(strip=True)
            # Clean up common title suffixes
            title = re.sub(r'\s*[-|]\s*Quaternius.*$', '', title, flags=re.IGNORECASE)
            if title and len(title) > 3:
                return title
        
        return None
    
    def _extract_description(self, soup) -> Optional[str]:
        """Extract asset description"""
        desc_selectors = [
            '.description',
            '.content',
            '.model-description',
            '.asset-description',
            'p'
        ]
        
        for selector in desc_selectors:
            element = soup.select_one(selector)
            if element:
                desc = element.get_text(strip=True)
                if desc and len(desc) > 10:
                    return desc[:500]
        
        return None
    
    def _extract_download_url(self, soup, asset_url: str) -> Optional[str]:
        """Extract download URL"""
        download_selectors = [
            'a[href*="download"]',
            'a[href*=".zip"]',
            'a[href*=".blend"]',
            'a[href*=".fbx"]',
            'a[href*=".obj"]',
            '.download-button',
            '.download-link',
            '[class*="download"]'
        ]
        
        for selector in download_selectors:
            element = soup.select_one(selector)
            if element:
                href = element.get('href')
                if href:
                    return urljoin(asset_url, href)
        
        # Look for 3D model file extensions
        file_extensions = ['.zip', '.blend', '.fbx', '.obj', '.dae', '.3ds', '.max']
        all_links = soup.find_all('a', href=True)
        
        for link in all_links:
            href = link.get('href')
            if href and any(ext in href.lower() for ext in file_extensions):
                return urljoin(asset_url, href)
        
        return None
    
    def _extract_preview_image(self, soup, asset_url: str) -> Optional[str]:
        """Extract preview image URL"""
        img_selectors = [
            'img[src*="preview"]',
            'img[src*="thumb"]',
            '.preview img',
            '.model-preview img',
            '.asset-image img',
            'img'
        ]
        
        for selector in img_selectors:
            element = soup.select_one(selector)
            if element:
                src = element.get('src')
                if src and any(ext in src.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                    return urljoin(asset_url, src)
        
        return None
    
    def _extract_tags(self, soup) -> List[str]:
        """Extract tags/keywords"""
        tags = []
        
        tag_selectors = [
            '.tags a',
            '.categories a',
            '.keywords',
            '[class*="tag"]'
        ]
        
        for selector in tag_selectors:
            elements = soup.select(selector)
            for element in elements:
                tag = element.get_text(strip=True)
                if tag and tag not in tags:
                    tags.append(tag)
        
        # Extract from meta keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            keywords = meta_keywords.get('content', '')
            for keyword in keywords.split(','):
                keyword = keyword.strip()
                if keyword and keyword not in tags:
                    tags.append(keyword)
        
        return tags[:10]
    
    def _guess_format_from_url(self, url: str) -> str:
        """Guess file format from URL"""
        if not url:
            return 'unknown'
        
        url_lower = url.lower()
        
        if '.zip' in url_lower:
            return 'zip'
        elif '.blend' in url_lower:
            return 'blend'
        elif '.fbx' in url_lower:
            return 'fbx'
        elif '.obj' in url_lower:
            return 'obj'
        elif '.dae' in url_lower:
            return 'dae'
        elif '.3ds' in url_lower:
            return '3ds'
        elif '.max' in url_lower:
            return 'max'
        else:
            return 'unknown'
    
    def get_download_url(self, asset_url: str) -> Optional[str]:
        """Get direct download URL for an asset"""
        soup = self.get_soup(asset_url)
        if soup:
            return self._extract_download_url(soup, asset_url)
        return None

    # ===== DEEP SCRAPING IMPLEMENTATION =====

    def _scrape_main_page(self, limit: int = None) -> List[Dict]:
        """Scrape main page for assets"""
        assets = []

        soup = self.get_soup(self.assets_url)
        if not soup:
            return assets

        # Look for asset sections and links
        asset_links = self._find_asset_links(soup)

        print(f"📦 Found {len(asset_links)} potential asset links")

        for i, asset_link in enumerate(asset_links):
            if limit and len(assets) >= limit:
                break

            try:
                asset_data = self._extract_asset_data(asset_link)
                if asset_data:
                    assets.append(asset_data)
                    print(f"✅ Extracted: {asset_data['title'][:50]}...")

            except Exception as e:
                print(f"⚠️ Error extracting asset {i+1}: {e}")
                continue

        return assets

    def _build_page_url(self, base_url: str, page: int) -> str:
        """Build URL for specific page number"""
        if '?' in base_url:
            return f"{base_url}&page={page}"
        else:
            return f"{base_url}?page={page}"

    def _extract_page_assets(self, soup) -> List[Dict]:
        """Extract assets from a page soup"""
        assets = []

        # Find asset links
        asset_links = self._find_asset_links(soup)

        for asset_link in asset_links:
            try:
                asset_data = self._extract_asset_data(asset_link)
                if asset_data:
                    assets.append(asset_data)
            except Exception as e:
                print(f"⚠️ Error extracting asset data: {e}")
                continue

        return assets

    def _scrape_category(self, category: str, limit: int = None) -> List[Dict]:
        """Scrape specific category"""
        # Try different category URL patterns
        category_urls = [
            f"{self.base_url}/category/{category}",
            f"{self.base_url}/{category}",
            f"{self.base_url}/models/{category}",
            f"{self.base_url}/assets/{category}"
        ]

        for category_url in category_urls:
            assets = self.scrape_with_pagination(category_url, max_pages=5, limit=limit)
            if assets:
                return assets

        return []

    def _scrape_search_term(self, term: str, max_pages: int = 10) -> List[Dict]:
        """Scrape search results for a term"""
        # Try different search URL patterns
        search_urls = [
            f"{self.base_url}/search?q={term}",
            f"{self.base_url}/?s={term}",
            f"{self.base_url}/models?search={term}"
        ]

        for search_url in search_urls:
            assets = self.scrape_with_pagination(search_url, max_pages=max_pages, limit=None)
            if assets:
                return assets

        return []
