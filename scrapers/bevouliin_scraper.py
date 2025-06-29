"""
Enhanced secure scraper for Bevouliin.com free game assets with advanced bot protection
"""

import re
import time
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from .enhanced_base_scraper import EnhancedBaseScraper
import config

class BevouliinScraper(EnhancedBaseScraper):
    """Enhanced secure scraper for Bevouliin.com free game assets"""

    def __init__(self):
        super().__init__('bevouliin', enable_advanced_security=True)
        self.base_url = 'https://bevouliin.com'
        self.assets_url = 'https://bevouliin.com'

        # Real URL patterns discovered from site analysis
        self.game_asset_base = 'https://bevouliin.com/game-asset'
        self.asset_detail_pattern = '/game-asset/'

        # Categories discovered from site analysis (screenshots)
        self.game_categories = [
            'characters', 'backgrounds', 'particles', 'enemies',
            'trading-card-game', 'game-illustration', 'obstacles',
            'ornaments', 'tower-defense-game'
        ]

        self.design_categories = [
            'logo-templates', 'vector-illustration'
        ]

        # All categories combined
        self.all_categories = self.game_categories + self.design_categories

        # Asset card selectors based on real site structure analysis
        self.asset_card_selectors = [
            'article.fusion-post-grid',  # Main asset containers
            'article.post',
            'div.fusion-post-wrapper',
            '.fusion-rollover-link',
            'h2.fusion-post-title a',
            'a[href*="-game-"]',  # Asset links contain "-game-"
            'a[href*="-asset"]',
            'a[href*="-sprites"]'
        ]

        # Real asset URL patterns discovered from working test
        self.asset_url_patterns = [
            '-game-asset-sprites',  # 7 matches
            '-game-background',     # 4 matches
            '-game-sprites',        # 7 matches
            '-game-characters',
            'winter-cat',
            'halloween',
            'pirate-fish',
            'steampunk',
            'blaster',
            'beetle',
            'pets-game',
            'bee-fish',
            'rpg-',
            'trading-card'
        ]

        # Exclude category URLs (not actual assets)
        self.exclude_patterns = [
            '/category/',
            '/wp-content/',
            '/tag/',
            '/page/',
            'illustration-game-asset',
            'exclusive-2d-game-asset'
        ]

        # Site-specific patterns
        self.asset_patterns = {
            'title': r'<h[1-6][^>]*class="[^"]*title[^"]*"[^>]*>([^<]+)</h[1-6]>',
            'download_link': r'href="([^"]*download[^"]*)"',
            'image': r'<img[^>]*src="([^"]*\.(jpg|jpeg|png|gif|webp))"[^>]*>',
            'description': r'<p[^>]*class="[^"]*description[^"]*"[^>]*>([^<]+)</p>'
        }
    
    def scrape_assets(self, limit: int = None) -> List[Dict]:
        """Scrape free game assets from Bevouliin with comprehensive deep scraping"""
        assets = []
        start_time = time.time()

        try:
            print(f"🎯 Starting Bevouliin.com deep scraping (target: {limit or 'unlimited'} assets)")
            self.enable_deep_scraping()

            # Phase 1: Main page scraping
            print("📄 Phase 1: Scraping main page...")
            main_assets = self._scrape_main_page_enhanced(limit)
            assets.extend(main_assets)
            print(f"   ✅ Found {len(main_assets)} assets from main page")

            if limit and len(assets) >= limit:
                return self._finalize_results(assets[:limit], start_time)

            # Phase 2: Category-based deep scraping
            print("🎯 Phase 2: Category-based deep scraping...")
            category_assets = self._scrape_all_categories(limit - len(assets) if limit else None)

            # Filter duplicates
            new_assets = [a for a in category_assets if a['source_url'] not in [existing['source_url'] for existing in assets]]
            assets.extend(new_assets)
            print(f"   ✅ Found {len(new_assets)} new assets from categories")

            if limit and len(assets) >= limit:
                return self._finalize_results(assets[:limit], start_time)

            # Phase 3: Search-based discovery
            print("🔍 Phase 3: Search-based asset discovery...")
            search_assets = self._scrape_search_enhanced(limit - len(assets) if limit else None)

            # Filter duplicates
            new_search_assets = [a for a in search_assets if a['source_url'] not in [existing['source_url'] for existing in assets]]
            assets.extend(new_search_assets)
            print(f"   ✅ Found {len(new_search_assets)} new assets from search")

            # Phase 4: Deep pagination scraping
            if not limit or len(assets) < limit:
                print("📄 Phase 4: Deep pagination scraping...")
                pagination_assets = self._scrape_deep_pagination(limit - len(assets) if limit else 100)

                # Filter duplicates
                new_pagination_assets = [a for a in pagination_assets if a['source_url'] not in [existing['source_url'] for existing in assets]]
                assets.extend(new_pagination_assets)
                print(f"   ✅ Found {len(new_pagination_assets)} new assets from pagination")

            return self._finalize_results(assets[:limit] if limit else assets, start_time)

        except Exception as e:
            print(f"💥 Bevouliin scraping failed: {e}")
            import traceback
            traceback.print_exc()

        return assets[:limit] if limit else assets

    def _finalize_results(self, assets: List[Dict], start_time: float) -> List[Dict]:
        """Finalize scraping results with statistics"""
        duration = time.time() - start_time

        # Log security statistics
        stats = self.get_stats()
        if stats.get('bot_detections', 0) > 0:
            print(f"⚠️ Bot protection encountered {stats['bot_detections']} times")

        success_rate = stats.get('success_rate', 0)
        successful_requests = stats.get('successful_requests', 0)
        total_requests = stats.get('requests_made', 0)

        print(f"📊 Success rate: {success_rate:.1%} ({successful_requests}/{total_requests} requests)")
        print(f"⏱️ Scraping duration: {duration:.1f} seconds")
        print(f"✅ Bevouliin deep scraping completed: {len(assets)} assets found")

        return assets

    def _scrape_main_page_enhanced(self, limit: int = None) -> List[Dict]:
        """Enhanced main page scraping with direct requests"""
        assets = []

        # Use direct requests instead of safe_scraping for better compatibility
        import requests

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        try:
            print(f"🔍 Fetching main page: {self.base_url}")
            response = requests.get(self.base_url, headers=headers, timeout=15)
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')

                # Intelligent multi-strategy asset link detection
                real_asset_links = self._extract_asset_links_intelligent(soup)

                print(f"📦 Found {len(real_asset_links)} real asset links")

                # Extract asset data from each link
                for i, asset_url in enumerate(real_asset_links):
                    if limit and len(assets) >= limit:
                        break

                    try:
                        asset_data = self._extract_asset_data(asset_url)
                        if asset_data:
                            assets.append(asset_data)
                            print(f"✅ Extracted: {asset_data['title'][:50]}...")

                    except Exception as e:
                        print(f"⚠️ Error extracting asset {i+1}: {e}")
                        continue
            else:
                print(f"❌ Failed to load main page: {response.status_code}")

        except Exception as e:
            print(f"💥 Error fetching main page: {e}")

        return assets

    def _extract_asset_links_intelligent(self, soup) -> List[str]:
        """Intelligent asset link extraction with multiple strategies"""
        asset_links = []

        # Strategy 1: Pattern-based detection (primary)
        pattern_links = self._extract_links_by_patterns(soup)
        asset_links.extend(pattern_links)
        print(f"   Strategy 1 (Patterns): {len(pattern_links)} links")

        # Strategy 2: Article-based detection (fallback)
        if len(asset_links) < 5:  # If pattern detection fails
            article_links = self._extract_links_from_articles(soup)
            new_links = [link for link in article_links if link not in asset_links]
            asset_links.extend(new_links)
            print(f"   Strategy 2 (Articles): {len(new_links)} additional links")

        # Strategy 3: Semantic detection (advanced fallback)
        if len(asset_links) < 3:  # If still not enough
            semantic_links = self._extract_links_semantic(soup)
            new_links = [link for link in semantic_links if link not in asset_links]
            asset_links.extend(new_links)
            print(f"   Strategy 3 (Semantic): {len(new_links)} additional links")

        # Strategy 4: Brute force detection (last resort)
        if len(asset_links) == 0:
            brute_links = self._extract_links_brute_force(soup)
            asset_links.extend(brute_links)
            print(f"   Strategy 4 (Brute Force): {len(brute_links)} links")

        return asset_links[:50]  # Limit to prevent overwhelming

    def _extract_links_by_patterns(self, soup) -> List[str]:
        """Extract links using known asset patterns"""
        links = []
        all_links = soup.find_all('a', href=True)

        for link in all_links:
            href = link.get('href', '')
            # Enhanced pattern matching
            if (any(pattern in href for pattern in self.asset_url_patterns) and
                not any(exclude in href for exclude in self.exclude_patterns)):
                full_url = urljoin(self.base_url, href)
                if full_url not in links and self.base_url in full_url:
                    links.append(full_url)

        return links

    def _extract_links_from_articles(self, soup) -> List[str]:
        """Extract asset links from article elements"""
        links = []
        articles = soup.find_all('article')

        for article in articles:
            # Look for main asset link in article
            article_links = article.find_all('a', href=True)
            for link in article_links:
                href = link.get('href', '')
                # Check if it's a potential asset link
                if (href and self.base_url in href and
                    not any(exclude in href for exclude in self.exclude_patterns) and
                    href.endswith('/')):  # Asset pages typically end with /
                    if href not in links:
                        links.append(href)

        return links

    def _extract_links_semantic(self, soup) -> List[str]:
        """Extract links using semantic analysis"""
        links = []

        # Look for links with game/asset-related text
        asset_keywords = [
            'game', 'asset', 'sprite', 'character', 'background',
            'texture', 'animation', 'pixel', 'art', 'graphics'
        ]

        all_links = soup.find_all('a', href=True)
        for link in all_links:
            href = link.get('href', '')
            text = link.get_text(strip=True).lower()

            # Check if link text contains asset keywords
            if (any(keyword in text for keyword in asset_keywords) and
                self.base_url in href and
                not any(exclude in href for exclude in self.exclude_patterns)):
                if href not in links:
                    links.append(href)

        return links

    def _extract_links_brute_force(self, soup) -> List[str]:
        """Brute force link extraction as last resort"""
        links = []
        all_links = soup.find_all('a', href=True)

        for link in all_links:
            href = link.get('href', '')
            # Very permissive matching - any internal link that's not obviously a category/page
            if (self.base_url in href and
                href.count('/') >= 3 and  # Has some depth
                not any(exclude in href for exclude in ['/category/', '/tag/', '/page/', '/wp-content/'])):
                if href not in links:
                    links.append(href)

        return links[:20]  # Limit brute force results

    def _scrape_all_categories(self, limit: int = None) -> List[Dict]:
        """Scrape all discovered categories systematically"""
        all_assets = []

        for category in self.all_categories:
            if limit and len(all_assets) >= limit:
                break

            print(f"🎯 Scraping category: {category}")
            category_assets = self._scrape_category_enhanced(category,
                                                           limit - len(all_assets) if limit else 50)

            if category_assets:
                all_assets.extend(category_assets)
                print(f"   ✅ Found {len(category_assets)} assets in {category}")
            else:
                print(f"   ⚠️ No assets found in {category}")

        return all_assets

    def _scrape_search_enhanced(self, limit: int = None) -> List[Dict]:
        """Enhanced search-based scraping with game-specific terms"""
        search_terms = [
            # Game development terms
            'game assets', 'sprite', 'character', 'background', 'ui',
            'particle', 'enemy', 'obstacle', 'ornament', 'illustration',

            # Design terms
            'logo', 'vector', 'template', 'icon', 'graphic',

            # Asset types
            '2d', 'pixel art', 'cartoon', 'fantasy', 'sci-fi'
        ]

        all_assets = []

        for term in search_terms:
            if limit and len(all_assets) >= limit:
                break

            print(f"🔍 Searching for: '{term}'")
            search_assets = self._scrape_search_term_enhanced(term,
                                                            limit - len(all_assets) if limit else 20)

            if search_assets:
                all_assets.extend(search_assets)
                print(f"   ✅ Found {len(search_assets)} assets for '{term}'")

        return all_assets

    def _scrape_deep_pagination(self, limit: int = 100) -> List[Dict]:
        """Deep pagination scraping across multiple pages"""
        assets = []

        # Try different pagination patterns
        pagination_urls = [
            f"{self.base_url}?page=",
            f"{self.base_url}/page/",
            f"{self.base_url}/assets?page=",
            f"{self.base_url}/gallery?page="
        ]

        for base_url in pagination_urls:
            if limit and len(assets) >= limit:
                break

            page_assets = self.scrape_with_pagination(base_url.rstrip('='),
                                                    max_pages=10,
                                                    limit=limit - len(assets) if limit else None)
            if page_assets:
                assets.extend(page_assets)
                print(f"   ✅ Found {len(page_assets)} assets from pagination")
                break  # Use first working pagination pattern

        return assets

    def _find_asset_links(self, soup) -> List[str]:
        """Find asset page links based on real site structure"""
        asset_links = []

        # Primary: look for real asset URL patterns
        all_links = soup.find_all('a', href=True)
        for link in all_links:
            href = link.get('href', '')
            # Check if link matches real asset patterns and exclude categories
            if (any(pattern in href for pattern in self.asset_url_patterns) and
                not any(exclude in href for exclude in self.exclude_patterns)):
                full_url = urljoin(self.base_url, href)
                if full_url not in asset_links and self.base_url in full_url:
                    asset_links.append(full_url)

        # Secondary: look for article-based links
        if not asset_links:
            # Look for links within article elements
            articles = soup.find_all('article')
            for article in articles:
                article_links = article.find_all('a', href=True)
                for link in article_links:
                    href = link.get('href', '')
                    if href and self.base_url in href:
                        full_url = urljoin(self.base_url, href)
                        if full_url not in asset_links:
                            asset_links.append(full_url)

        print(f"🔗 Found {len(asset_links)} asset links (real patterns)")
        return asset_links[:50]  # Limit to first 50 to avoid overwhelming

    def _extract_asset_from_element(self, element) -> Optional[Dict]:
        """Extract asset data directly from HTML element"""
        try:
            # Try to find asset link
            asset_link = None

            # Check if element itself is a link
            if element.name == 'a' and element.get('href'):
                asset_link = urljoin(self.base_url, element.get('href'))
            else:
                # Look for link within element
                link_elem = element.find('a', href=True)
                if link_elem:
                    asset_link = urljoin(self.base_url, link_elem.get('href'))

            if not asset_link:
                return None

            # Extract title from element
            title = self._extract_title_from_element(element)
            if not title:
                return None

            # Extract other data from element
            description = self._extract_description_from_element(element)
            preview_image = self._extract_image_from_element(element)

            # Determine category and type
            category = self._determine_category_from_title(title)
            asset_type = self._determine_asset_type_from_title(title)

            return {
                'title': title,
                'description': description or '',
                'download_url': None,  # Will be extracted from detail page
                'preview_image': preview_image,
                'source_url': asset_link,
                'site': 'bevouliin',
                'license': 'CC0',
                'tags': self._extract_tags_from_title(title),
                'asset_type': asset_type,
                'category': category,
                'file_size': 'unknown',
                'format': 'unknown'
            }

        except Exception as e:
            print(f"⚠️ Error extracting from element: {e}")
            return None

    def _extract_title_from_element(self, element) -> Optional[str]:
        """Extract title from HTML element"""
        # Try different title selectors
        title_selectors = ['h1', 'h2', 'h3', '.title', '.name', 'img[alt]']

        for selector in title_selectors:
            title_elem = element.select_one(selector)
            if title_elem:
                if title_elem.name == 'img':
                    title = title_elem.get('alt', '').strip()
                else:
                    title = title_elem.get_text(strip=True)

                if title and len(title) > 3:
                    return title

        # Fallback to element text
        text = element.get_text(strip=True)
        if text and len(text) > 3 and len(text) < 100:
            return text

        return None

    def _extract_description_from_element(self, element) -> Optional[str]:
        """Extract description from HTML element"""
        desc_selectors = ['.description', '.content', 'p', '.excerpt']

        for selector in desc_selectors:
            desc_elem = element.select_one(selector)
            if desc_elem:
                desc = desc_elem.get_text(strip=True)
                if desc and len(desc) > 10:
                    return desc[:300]

        return None

    def _extract_image_from_element(self, element) -> Optional[str]:
        """Extract preview image from HTML element"""
        img_elem = element.find('img')
        if img_elem:
            src = img_elem.get('src') or img_elem.get('data-src')
            if src:
                return urljoin(self.base_url, src)

        return None

    def _determine_category_from_title(self, title: str) -> str:
        """Determine category from title"""
        title_lower = title.lower()

        # Game categories
        if any(word in title_lower for word in ['character', 'hero', 'player', 'npc']):
            return 'characters'
        elif any(word in title_lower for word in ['background', 'scene', 'environment']):
            return 'backgrounds'
        elif any(word in title_lower for word in ['particle', 'effect', 'explosion', 'magic']):
            return 'particles'
        elif any(word in title_lower for word in ['enemy', 'monster', 'boss', 'villain']):
            return 'enemies'
        elif any(word in title_lower for word in ['card', 'trading', 'deck']):
            return 'trading-card-game'
        elif any(word in title_lower for word in ['obstacle', 'barrier', 'wall']):
            return 'obstacles'
        elif any(word in title_lower for word in ['ornament', 'decoration', 'border']):
            return 'ornaments'
        elif any(word in title_lower for word in ['tower', 'defense', 'turret']):
            return 'tower-defense-game'
        elif any(word in title_lower for word in ['logo', 'brand', 'identity']):
            return 'logo-templates'
        elif any(word in title_lower for word in ['vector', 'illustration', 'graphic']):
            return 'vector-illustration'
        else:
            return 'game-illustration'

    def _determine_asset_type_from_title(self, title: str) -> str:
        """Determine asset type from title"""
        title_lower = title.lower()

        if any(word in title_lower for word in ['sprite', 'character', 'animation']):
            return 'sprite'
        elif any(word in title_lower for word in ['background', 'scene', 'environment']):
            return 'background'
        elif any(word in title_lower for word in ['ui', 'button', 'interface', 'menu']):
            return 'ui'
        elif any(word in title_lower for word in ['texture', 'material', 'surface']):
            return 'texture'
        elif any(word in title_lower for word in ['icon', 'symbol', 'badge']):
            return 'icon'
        elif any(word in title_lower for word in ['logo', 'brand']):
            return 'logo'
        elif any(word in title_lower for word in ['vector', 'illustration']):
            return 'vector'
        else:
            return '2d_asset'

    def _extract_tags_from_title(self, title: str) -> List[str]:
        """Extract tags from title"""
        tags = []
        title_lower = title.lower()

        # Common game asset tags
        tag_keywords = [
            'pixel', 'cartoon', 'fantasy', 'sci-fi', 'medieval', 'modern',
            'cute', 'dark', 'colorful', 'minimalist', 'retro', 'futuristic',
            'free', 'game', 'asset', '2d', '3d', 'vector', 'sprite'
        ]

        for keyword in tag_keywords:
            if keyword in title_lower:
                tags.append(keyword)

        return tags[:5]  # Limit to 5 tags

    def _scrape_category_enhanced(self, category: str, limit: int = None) -> List[Dict]:
        """Enhanced category scraping with real URL patterns"""
        # Try different category URL patterns based on actual site structure
        category_urls = [
            f"{self.base_url}/game-asset?category={category}",
            f"{self.base_url}/game-asset/{category}",
            f"{self.base_url}/category/{category}",
            f"{self.base_url}/{category}",
            f"{self.base_url}/assets/{category}",
            f"{self.base_url}/free/{category}",
            f"{self.base_url}/game-assets/{category}",
            f"{self.base_url}/downloads/{category}"
        ]

        for category_url in category_urls:
            print(f"   🔍 Trying: {category_url}")

            # Get the page and look for game-asset links
            soup = self.get_soup(category_url)
            if soup:
                # Look for game-asset links
                asset_links = soup.find_all('a', href=True)
                game_asset_links = []

                for link in asset_links:
                    href = link.get('href', '')
                    if '/game-asset/' in href:
                        full_url = urljoin(self.base_url, href)
                        if full_url not in game_asset_links:
                            game_asset_links.append(full_url)

                if game_asset_links:
                    print(f"   ✅ Found {len(game_asset_links)} assets at: {category_url}")

                    # Extract asset data
                    assets = []
                    for asset_url in game_asset_links[:limit] if limit else game_asset_links:
                        try:
                            asset_data = self._extract_asset_data(asset_url)
                            if asset_data:
                                assets.append(asset_data)
                        except Exception as e:
                            print(f"⚠️ Error extracting asset: {e}")
                            continue

                    return assets
                else:
                    print(f"   ❌ No game-asset links found at: {category_url}")
            else:
                print(f"   ❌ Failed to load: {category_url}")

        return []

    def _scrape_search_term_enhanced(self, term: str, limit: int = None) -> List[Dict]:
        """Enhanced search term scraping"""
        # Try different search URL patterns
        search_urls = [
            f"{self.base_url}/search?q={term}",
            f"{self.base_url}/?s={term}",
            f"{self.base_url}/search/{term}",
            f"{self.base_url}/?search={term}",
            f"{self.base_url}/assets?search={term}"
        ]

        for search_url in search_urls:
            assets = self.scrape_with_pagination(search_url, max_pages=3, limit=limit)
            if assets:
                return assets

        return []

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
        
        return {
            'title': title,
            'description': description or '',
            'download_url': download_url,
            'preview_image': preview_image,
            'source_url': asset_url,
            'site': 'bevouliin',
            'license': 'CC0',  # Bevouliin uses CC0 license
            'tags': tags,
            'asset_type': asset_type,
            'category': category,
            'file_size': 'unknown',
            'format': self._guess_format_from_url(download_url or asset_url)
        }
    
    def _extract_title(self, soup) -> Optional[str]:
        """Extract asset title"""
        # Try multiple selectors for title
        title_selectors = [
            'h1',
            'h2',
            '.title',
            '.asset-title',
            '.post-title',
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
            title = re.sub(r'\s*[-|]\s*Bevouliin.*$', '', title, flags=re.IGNORECASE)
            if title and len(title) > 3:
                return title
        
        return None
    
    def _extract_description(self, soup) -> Optional[str]:
        """Extract asset description"""
        desc_selectors = [
            '.description',
            '.content',
            '.post-content',
            'p',
            '.asset-description'
        ]
        
        for selector in desc_selectors:
            element = soup.select_one(selector)
            if element:
                desc = element.get_text(strip=True)
                if desc and len(desc) > 10:
                    return desc[:500]  # Limit description length
        
        return None
    
    def _extract_download_url(self, soup, asset_url: str) -> Optional[str]:
        """Extract download URL"""
        # Look for download links
        download_selectors = [
            'a[href*="download"]',
            'a[href*=".zip"]',
            'a[href*=".rar"]',
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
        
        # Look for direct file links
        file_extensions = ['.zip', '.rar', '.7z', '.tar.gz', '.png', '.jpg', '.gif']
        all_links = soup.find_all('a', href=True)
        
        for link in all_links:
            href = link.get('href')
            if href and any(ext in href.lower() for ext in file_extensions):
                return urljoin(asset_url, href)
        
        return None
    
    def _extract_preview_image(self, soup, asset_url: str) -> Optional[str]:
        """Extract preview image URL"""
        # Look for images
        img_selectors = [
            'img[src*="preview"]',
            'img[src*="thumb"]',
            '.preview-image img',
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
        
        # Look for tag elements
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
        
        return tags[:10]  # Limit to 10 tags
    
    def _guess_format_from_url(self, url: str) -> str:
        """Guess file format from URL"""
        if not url:
            return 'unknown'
        
        url_lower = url.lower()
        
        if '.zip' in url_lower:
            return 'zip'
        elif '.rar' in url_lower:
            return 'rar'
        elif '.png' in url_lower:
            return 'png'
        elif '.jpg' in url_lower or '.jpeg' in url_lower:
            return 'jpeg'
        elif '.gif' in url_lower:
            return 'gif'
        elif '.svg' in url_lower:
            return 'svg'
        else:
            return 'unknown'
    
    def get_download_url(self, asset_url: str) -> Optional[str]:
        """Get direct download URL for an asset"""
        soup = self.get_soup(asset_url)
        if soup:
            return self._extract_download_url(soup, asset_url)
        return None

    # ===== DEEP SCRAPING IMPLEMENTATION =====

    def _build_page_url(self, base_url: str, page: int) -> str:
        """Build URL for specific page number"""
        if '?' in base_url:
            return f"{base_url}&page={page}"
        else:
            return f"{base_url}?page={page}"

    def _extract_page_assets(self, soup) -> List[Dict]:
        """Extract assets from a page soup"""
        assets = []

        # Look for asset links and categories
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
            f"{self.base_url}/assets/{category}",
            f"{self.base_url}/free/{category}"
        ]

        for category_url in category_urls:
            assets = self.scrape_with_pagination(category_url, max_pages=8, limit=limit)
            if assets:
                return assets

        return []

    def _scrape_search_term(self, term: str, max_pages: int = 10) -> List[Dict]:
        """Scrape search results for a term"""
        # Try different search URL patterns
        search_urls = [
            f"{self.base_url}/search?q={term}",
            f"{self.base_url}/?s={term}",
            f"{self.base_url}/search/{term}"
        ]

        for search_url in search_urls:
            assets = self.scrape_with_pagination(search_url, max_pages=max_pages, limit=None)
            if assets:
                return assets

        return []
