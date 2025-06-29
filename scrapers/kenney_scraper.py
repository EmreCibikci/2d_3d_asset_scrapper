import re
import time
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse, parse_qs
from .enhanced_base_scraper import EnhancedBaseScraper
import config

class KenneyScraper(EnhancedBaseScraper):
    """Enhanced secure scraper for Kenney.nl assets with deep scraping support"""

    def __init__(self):
        super().__init__('kenney', enable_advanced_security=True)
        self.base_url = config.SITES_CONFIG['kenney']['base_url']
        self.assets_url = config.SITES_CONFIG['kenney']['assets_url']

        # Initialize visited URLs tracking
        self.visited_urls = set()

        # Kenney-specific selectors based on site analysis
        self.asset_card_selectors = [
            'div.asset-card',
            'div.asset-item',
            'a[href*="/assets/"]',
            '.grid-item',
            '.asset'
        ]

        # Category filters from the site
        self.categories = ['2d', '3d', 'ui', 'audio', 'pixel', 'textures']

        # Search terms for comprehensive scraping
        self.search_terms = [
            'sprite', 'character', 'tileset', 'ui', 'button', 'icon',
            'background', 'texture', 'building', 'vehicle', 'weapon',
            'nature', 'food', 'animal', 'space', 'platformer'
        ]
    
    def scrape_assets(self, limit: int = None) -> List[Dict]:
        """Scrape assets from Kenney.nl with comprehensive deep scraping strategy"""
        assets = []
        start_time = time.time()

        print(f"🎯 Starting Kenney.nl deep scraping (target: {limit or 'unlimited'} assets)")
        self.enable_deep_scraping()

        try:
            # Phase 1: Main assets page with pagination
            print("📄 Phase 1: Scraping main assets page...")
            main_assets = self._scrape_main_assets_with_pagination(limit)
            assets.extend(main_assets)
            print(f"   ✅ Found {len(main_assets)} assets from main page")

            if limit and len(assets) >= limit:
                return self._finalize_results(assets[:limit], start_time)

            # Phase 2: Category-based scraping
            print("🎯 Phase 2: Category-based deep scraping...")
            category_assets = self._scrape_all_categories(limit - len(assets) if limit else None)
            new_category_assets = self._filter_duplicates(category_assets, assets)
            assets.extend(new_category_assets)
            print(f"   ✅ Found {len(new_category_assets)} new assets from categories")

            if limit and len(assets) >= limit:
                return self._finalize_results(assets[:limit], start_time)

            # Phase 3: Search-based discovery
            print("🔍 Phase 3: Search-based asset discovery...")
            search_assets = self._scrape_with_search_terms(limit - len(assets) if limit else None)
            new_search_assets = self._filter_duplicates(search_assets, assets)
            assets.extend(new_search_assets)
            print(f"   ✅ Found {len(new_search_assets)} new assets from search")

            return self._finalize_results(assets[:limit] if limit else assets, start_time)

        except Exception as e:
            print(f"❌ Error during Kenney scraping: {e}")
            return self._finalize_results(assets, start_time)
    
    def _scrape_main_assets_with_pagination(self, limit: int = None) -> List[Dict]:
        """Scrape main assets page with pagination support"""
        assets = []
        page = 1
        max_pages = 50  # Reasonable limit

        while page <= max_pages:
            if limit and len(assets) >= limit:
                break

            page_url = self._build_assets_page_url(page)
            print(f"   📄 Scraping page {page}: {page_url}")

            soup = self.get_soup(page_url)
            if not soup:
                print(f"   ⚠️ Failed to load page {page}")
                break

            page_assets = self._extract_assets_from_page(soup)
            if not page_assets:
                print(f"   ℹ️ No assets found on page {page}, stopping pagination")
                break

            assets.extend(page_assets)
            print(f"   ✅ Found {len(page_assets)} assets on page {page}")

            page += 1
            self._random_delay()

        return assets

    def _build_assets_page_url(self, page: int) -> str:
        """Build URL for assets page with pagination"""
        if page == 1:
            return self.assets_url
        return f"{self.assets_url}?page={page}"

    def _scrape_all_categories(self, limit: int = None) -> List[Dict]:
        """Scrape all categories with deep pagination"""
        all_assets = []

        for category in self.categories:
            if limit and len(all_assets) >= limit:
                break

            print(f"   🎯 Scraping category: {category}")
            category_assets = self._scrape_category_deep(category, limit - len(all_assets) if limit else None)
            all_assets.extend(category_assets)
            print(f"   ✅ Category '{category}': {len(category_assets)} assets")

        return all_assets

    def _scrape_category_deep(self, category: str, limit: int = None) -> List[Dict]:
        """Deep scrape a specific category with pagination"""
        assets = []

        # Try different category URL patterns for Kenney
        category_urls = [
            f"{self.assets_url}?{category}=1",  # Original pattern
            f"{self.assets_url}?category={category}",  # Alternative pattern
            f"{self.base_url}/assets/category:{category.upper()}",  # Kenney's actual pattern
            f"{self.assets_url}?tag={category}",  # Tag-based pattern
        ]

        for category_url in category_urls:
            print(f"   🔍 Trying category URL: {category_url}")

            page = 1
            max_pages = 10  # Reduced for efficiency

            while page <= max_pages:
                if limit and len(assets) >= limit:
                    break

                # Build paginated URL
                if page == 1:
                    url = category_url
                else:
                    separator = '&' if '?' in category_url else '?'
                    url = f"{category_url}{separator}page={page}"

                soup = self.get_soup(url)
                if not soup:
                    break

                page_assets = self._extract_assets_from_page(soup)
                if not page_assets:
                    break

                # Filter out duplicates
                new_assets = [a for a in page_assets if a['url'] not in [existing['url'] for existing in assets]]
                assets.extend(new_assets)

                if not new_assets:  # No new assets found
                    break

                page += 1
                self._random_delay()

            # If we found assets with this URL pattern, use it
            if assets:
                break

        return assets
    
    def _scrape_with_search_terms(self, limit: int = None) -> List[Dict]:
        """Scrape using search terms for comprehensive discovery"""
        all_assets = []

        for term in self.search_terms:
            if limit and len(all_assets) >= limit:
                break

            print(f"   🔍 Searching for: {term}")
            search_assets = self._scrape_search_term(term, limit - len(all_assets) if limit else None)
            all_assets.extend(search_assets)
            print(f"   ✅ Search '{term}': {len(search_assets)} assets")

        return all_assets

    def _scrape_search_term(self, term: str, limit: int = None) -> List[Dict]:
        """Scrape search results for a specific term"""
        assets = []
        page = 1
        max_pages = 10

        while page <= max_pages:
            if limit and len(assets) >= limit:
                break

            search_url = f"{self.assets_url}?search={term}&page={page}"

            soup = self.get_soup(search_url)
            if not soup:
                break

            page_assets = self._extract_assets_from_page(soup)
            if not page_assets:
                break

            assets.extend(page_assets)
            page += 1
            self._random_delay()

        return assets

    def _extract_assets_from_page(self, soup) -> List[Dict]:
        """Extract all assets from a page using multiple selectors"""
        assets = []

        # Try different selectors to find asset cards/links
        for selector in self.asset_card_selectors:
            elements = soup.select(selector)
            if elements:
                print(f"   📋 Found {len(elements)} elements with selector: {selector}")
                for element in elements:
                    asset_data = self._extract_asset_from_element(element)
                    if asset_data and self._is_valid_asset(asset_data):
                        assets.append(asset_data)
                break  # Use first successful selector

        # Fallback: Look for specific asset links (not category/filter links)
        if not assets:
            # More specific pattern to avoid category/filter links
            asset_links = soup.find_all('a', href=re.compile(r'/assets/[a-zA-Z0-9\-]+/?$'))
            filtered_links = []

            for link in asset_links:
                href = link.get('href', '')
                # Filter out category and filter links
                if not any(exclude in href.lower() for exclude in ['category:', 'tag:', 'sort=', '?']):
                    filtered_links.append(link)

            print(f"   🔗 Fallback: Found {len(filtered_links)} valid asset links (filtered from {len(asset_links)})")
            for link in filtered_links:
                asset_data = self._extract_asset_from_link(link)
                if asset_data and self._is_valid_asset(asset_data):
                    assets.append(asset_data)

        return assets

    def _is_valid_asset(self, asset_data: Dict) -> bool:
        """Check if asset data represents a valid individual asset"""
        if not asset_data:
            return False

        url = asset_data.get('url', '')
        title = asset_data.get('title', '')

        # Filter out category/filter pages
        invalid_patterns = [
            'category:', 'tag:', 'sort=', '?',
            'Category:', 'Tag:', 'Sort=',
            'Audio', 'Pixel'  # These seem to be category pages
        ]

        for pattern in invalid_patterns:
            if pattern in url or pattern in title:
                return False

        return True
    
    def _extract_asset_from_element(self, element) -> Optional[Dict]:
        """Extract asset data from a card/element"""
        try:
            # Get asset URL
            if element.name == 'a':
                asset_url = urljoin(self.base_url, element.get('href', ''))
                title_elem = element
            else:
                link_elem = element.find('a', href=re.compile(r'/assets/'))
                if not link_elem:
                    return None
                asset_url = urljoin(self.base_url, link_elem.get('href', ''))
                title_elem = link_elem

            # Skip if already visited
            if asset_url in self.visited_urls:
                return None
            self.visited_urls.add(asset_url)

            # Extract title
            title = self._extract_title_from_element(element, asset_url)

            # Extract preview image
            preview_url = self._extract_preview_from_element(element)

            # Get detailed data from asset page (optional for performance)
            detailed_data = self._get_basic_asset_details(asset_url)

            # Extract category and tags
            category_info = self._extract_category_info(element, title, asset_url)

            return {
                'title': title,
                'description': detailed_data.get('description', ''),
                'url': asset_url,
                'source_site': self.site_name,
                'asset_type': category_info['asset_type'],
                'category': category_info['category'],
                'tags': category_info['tags'],
                'preview_url': preview_url,
                'download_url': detailed_data.get('download_url'),
                'is_free': True,
                'license_info': 'CC0 1.0 Universal (Public Domain)',
                'file_count': detailed_data.get('file_count', 'unknown'),
                'scraped_at': time.time()
            }

        except Exception as e:
            print(f"   ⚠️ Error extracting asset from element: {e}")
            return None

    def _extract_asset_from_link(self, link) -> Optional[Dict]:
        """Extract asset data from a simple link element"""
        try:
            asset_url = urljoin(self.base_url, link.get('href', ''))

            if asset_url in self.visited_urls:
                return None
            self.visited_urls.add(asset_url)

            # Extract title from link text or URL
            title = link.get_text(strip=True)
            if not title:
                title = asset_url.split('/')[-1].replace('-', ' ').title()

            # Basic category detection from URL
            category_info = self._extract_category_info(link, title, asset_url)

            return {
                'title': title,
                'description': '',
                'url': asset_url,
                'source_site': self.site_name,
                'asset_type': category_info['asset_type'],
                'category': category_info['category'],
                'tags': category_info['tags'],
                'preview_url': None,
                'download_url': None,
                'is_free': True,
                'license_info': 'CC0 1.0 Universal (Public Domain)',
                'scraped_at': time.time()
            }

        except Exception as e:
            print(f"   ⚠️ Error extracting asset from link: {e}")
            return None
    
    def _extract_title_from_element(self, element, asset_url: str) -> str:
        """Extract title from element or URL"""
        # Try to get title from element text
        title = element.get_text(strip=True)

        # Clean up title (remove extra whitespace, etc.)
        if title:
            title = ' '.join(title.split())

        # Fallback to URL-based title
        if not title or len(title) < 3:
            title = asset_url.split('/')[-1].replace('-', ' ').title()

        return title

    def _extract_preview_from_element(self, element) -> Optional[str]:
        """Extract preview image URL from element"""
        img_elem = element.find('img')
        if img_elem:
            img_src = img_elem.get('src') or img_elem.get('data-src') or img_elem.get('data-lazy')
            if img_src:
                return urljoin(self.base_url, img_src)
        return None

    def _extract_category_info(self, element, title: str, asset_url: str) -> Dict:
        """Extract category, asset type, and tags"""
        text = f"{title} {asset_url}".lower()

        # Determine asset type
        asset_type = '2d'  # Default
        if any(keyword in text for keyword in ['3d', 'isometric', 'model']):
            asset_type = '3d'
        elif any(keyword in text for keyword in ['audio', 'sound', 'music']):
            asset_type = 'audio'
        elif any(keyword in text for keyword in ['ui', 'interface', 'button']):
            asset_type = 'ui'

        # Determine category
        category = 'general'
        if 'character' in text:
            category = 'character'
        elif any(keyword in text for keyword in ['ui', 'interface', 'button']):
            category = 'ui'
        elif any(keyword in text for keyword in ['building', 'house', 'city']):
            category = 'building'
        elif any(keyword in text for keyword in ['vehicle', 'car', 'ship']):
            category = 'vehicle'
        elif any(keyword in text for keyword in ['nature', 'tree', 'plant']):
            category = 'nature'
        elif any(keyword in text for keyword in ['weapon', 'sword', 'gun']):
            category = 'weapon'

        # Extract tags
        tags = []
        tag_keywords = [
            'ui', 'interface', 'platformer', 'space', 'racing', 'puzzle',
            'pixel', 'vector', '3d', '2d', 'isometric', 'top-down',
            'character', 'vehicle', 'building', 'nature', 'weapon',
            'food', 'animal', 'robot', 'medieval', 'modern', 'fantasy'
        ]

        for keyword in tag_keywords:
            if keyword in text:
                tags.append(keyword)

        return {
            'asset_type': asset_type,
            'category': category,
            'tags': tags
        }

    def _get_basic_asset_details(self, asset_url: str) -> Dict:
        """Get basic details from asset page (optimized for performance)"""
        details = {}

        # For performance, we might skip detailed page scraping for some assets
        # and only get essential info
        soup = self.get_soup(asset_url)
        if not soup:
            return details

        # Extract description
        desc_selectors = [
            '.asset-description',
            '.description',
            'meta[name="description"]',
            'p'
        ]

        for selector in desc_selectors:
            if selector.startswith('meta'):
                desc_elem = soup.select_one(selector)
                if desc_elem:
                    details['description'] = desc_elem.get('content', '')
                    break
            else:
                desc_elem = soup.select_one(selector)
                if desc_elem:
                    details['description'] = desc_elem.get_text(strip=True)
                    break

        # Extract file count if visible
        file_count_text = soup.get_text()
        file_match = re.search(r'(\d+)\s*files?', file_count_text, re.IGNORECASE)
        if file_match:
            details['file_count'] = file_match.group(1)

        # Get download URL
        details['download_url'] = self._get_download_url(asset_url, soup)

        return details

    def _get_download_url(self, asset_url: str, soup=None) -> Optional[str]:
        """Get direct download URL for a Kenney asset"""
        if not soup:
            soup = self.get_soup(asset_url)
            if not soup:
                return None

        # Kenney download button selectors
        download_selectors = [
            'a[href*=".zip"]',
            'a.download',
            'a[href*="download"]',
            '.download-btn',
            'button[onclick*="download"]',
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

        return None

    def _filter_duplicates(self, new_assets: List[Dict], existing_assets: List[Dict]) -> List[Dict]:
        """Filter out duplicate assets based on URL"""
        existing_urls = {asset['url'] for asset in existing_assets}
        return [asset for asset in new_assets if asset['url'] not in existing_urls]

    def _finalize_results(self, assets: List[Dict], start_time: float) -> List[Dict]:
        """Finalize scraping results with statistics"""
        duration = time.time() - start_time

        print(f"\n🎯 Kenney.nl Scraping Complete!")
        print(f"   ✅ Total assets found: {len(assets)}")
        print(f"   ⏱️ Duration: {duration:.2f} seconds")
        print(f"   🚀 Rate: {len(assets)/duration:.2f} assets/second")

        # Add scraping metadata
        for asset in assets:
            asset['scraping_duration'] = duration
            asset['scraping_method'] = 'deep_scraping'

        return assets

    def _random_delay(self):
        """Add random delay between requests for politeness and bot protection avoidance"""
        import random
        # Longer delays to avoid bot protection
        delay = random.uniform(1.0, 3.0)
        time.sleep(delay)

    def get_site_statistics(self) -> Dict:
        """Get statistics about the scraping session"""
        return {
            'visited_urls_count': len(self.visited_urls),
            'base_url': self.base_url,
            'assets_url': self.assets_url,
            'categories': self.categories,
            'search_terms': self.search_terms
        }

    # ===== LEGACY COMPATIBILITY METHODS =====

    def get_download_url(self, asset_url: str) -> Optional[str]:
        """Legacy method for backward compatibility"""
        return self._get_download_url(asset_url)

    def _extract_tags(self, title: str, description: str) -> List[str]:
        """Legacy method for backward compatibility"""
        category_info = self._extract_category_info(None, title, "")
        return category_info['tags']
