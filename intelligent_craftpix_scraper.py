#!/usr/bin/env python3
"""
Intelligent CraftPix Scraper
Advanced intelligent scraper for CraftPix.net with site analysis and adaptive strategies
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json
import re
from typing import List, Dict, Optional
from intelligent_site_analyzer import IntelligentSiteAnalyzer

class IntelligentCraftPixScraper:
    """Intelligent CraftPix scraper with advanced site analysis"""
    
    def __init__(self):
        self.base_url = 'https://craftpix.net'
        self.freebies_url = 'https://craftpix.net/freebies/'
        self.session = self._create_intelligent_session()
        self.site_analyzer = IntelligentSiteAnalyzer(self.base_url)
        
        # CraftPix-specific patterns discovered from analysis
        self.asset_patterns = [
            '/freebies/',
            'game-assets',
            'sprites',
            'characters',
            'backgrounds',
            'ui-elements',
            'icons',
            'tilesets'
        ]
        
        self.exclude_patterns = [
            '/blog/',
            '/about/',
            '/contact/',
            '/login/',
            '/register/',
            '/cart/',
            '/checkout/'
        ]
        
        # Intelligence data
        self.site_structure = None
        self.scraping_strategy = None
        
    def _create_intelligent_session(self):
        """Create intelligent session with advanced headers"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
            'DNT': '1'
        })
        return session
    
    def analyze_and_scrape(self, limit: int = None) -> List[Dict]:
        """Main intelligent scraping method with site analysis"""
        print("🧠 Starting Intelligent CraftPix Scraping...")
        print("=" * 60)
        
        # Phase 1: Site Intelligence Analysis
        print("🔍 Phase 1: Intelligent Site Analysis")
        self.site_structure = self._perform_site_analysis()
        
        # Phase 2: Adaptive Scraping Strategy
        print("🎯 Phase 2: Adaptive Scraping Strategy")
        self.scraping_strategy = self._determine_scraping_strategy()
        
        # Phase 3: Intelligent Asset Extraction
        print("📦 Phase 3: Intelligent Asset Extraction")
        assets = self._execute_intelligent_scraping(limit)
        
        # Phase 4: Results Optimization
        print("✨ Phase 4: Results Optimization")
        optimized_assets = self._optimize_results(assets)
        
        return optimized_assets
    
    def _perform_site_analysis(self) -> Dict:
        """Perform intelligent site structure analysis"""
        print("   🔍 Analyzing CraftPix site structure...")
        
        structure = {
            'navigation_patterns': [],
            'asset_containers': [],
            'pagination_indicators': [],
            'content_selectors': [],
            'download_patterns': []
        }
        
        try:
            # Analyze main freebies page
            response = self.session.get(self.freebies_url, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find asset containers
                potential_containers = [
                    '.product-item', '.item-product', '.asset-card',
                    '.freebie-item', '.game-asset', 'article',
                    '[class*="product"]', '[class*="item"]'
                ]
                
                for selector in potential_containers:
                    elements = soup.select(selector)
                    if elements and len(elements) > 3:  # Likely asset containers
                        structure['asset_containers'].append({
                            'selector': selector,
                            'count': len(elements),
                            'confidence': len(elements) / 10  # Simple confidence score
                        })
                
                # Find pagination patterns
                pagination_selectors = [
                    '.pagination', '.page-numbers', '.pager',
                    '[class*="page"]', 'nav[aria-label*="page"]'
                ]
                
                for selector in pagination_selectors:
                    if soup.select(selector):
                        structure['pagination_indicators'].append(selector)
                
                # Analyze download patterns
                download_patterns = [
                    'a[href*="download"]', '.download-btn', '.btn-download',
                    'a[href*=".zip"]', '.free-download'
                ]
                
                for pattern in download_patterns:
                    if soup.select(pattern):
                        structure['download_patterns'].append(pattern)
                        
        except Exception as e:
            print(f"   ⚠️ Site analysis warning: {e}")
        
        print(f"   ✅ Found {len(structure['asset_containers'])} container patterns")
        print(f"   ✅ Found {len(structure['pagination_indicators'])} pagination patterns")
        
        return structure
    
    def _determine_scraping_strategy(self) -> Dict:
        """Determine optimal scraping strategy based on site analysis"""
        strategy = {
            'primary_method': 'container_based',
            'fallback_methods': ['link_crawling', 'pattern_matching'],
            'asset_selector': None,
            'pagination_method': 'url_parameter',
            'rate_limiting': 2.0,  # seconds between requests
            'max_pages': 20
        }
        
        # Choose best asset container
        if self.site_structure['asset_containers']:
            best_container = max(
                self.site_structure['asset_containers'],
                key=lambda x: x['confidence']
            )
            strategy['asset_selector'] = best_container['selector']
            print(f"   🎯 Selected container: {best_container['selector']}")
        
        # Determine pagination method
        if self.site_structure['pagination_indicators']:
            strategy['pagination_method'] = 'navigation_links'
            print(f"   📄 Pagination method: navigation_links")
        
        return strategy
    
    def _execute_intelligent_scraping(self, limit: int = None) -> List[Dict]:
        """Execute intelligent scraping based on strategy"""
        assets = []
        page = 1

        while True:
            if limit and len(assets) >= limit:
                break

            # Build page URL - CraftPix doesn't use ?page= format
            if page == 1:
                page_url = self.freebies_url
            else:
                page_url = f"{self.freebies_url}page/{page}/"
            print(f"   📄 Scraping page {page}: {page_url}")

            try:
                response = self.session.get(page_url, timeout=15)
                if response.status_code != 200:
                    print(f"   ❌ Failed to fetch page {page}")
                    break

                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract assets using intelligent strategy
                page_assets = self._extract_page_assets(soup)

                if not page_assets:
                    print(f"   ⚠️ No assets found on page {page}")
                    break

                assets.extend(page_assets)
                print(f"   ✅ Found {len(page_assets)} assets on page {page}")

                # Intelligent rate limiting
                time.sleep(self.scraping_strategy['rate_limiting'])

                page += 1
                if page > self.scraping_strategy['max_pages']:
                    break

            except Exception as e:
                print(f"   ❌ Error on page {page}: {e}")
                import traceback
                traceback.print_exc()
                break

        return assets
    
    def _extract_page_assets(self, soup) -> List[Dict]:
        """Extract assets from page using intelligent selectors"""
        assets = []

        # Use intelligent asset selector with fallback
        asset_selector = self.scraping_strategy.get('asset_selector') or '.product-item'

        try:
            asset_elements = soup.select(asset_selector)
        except Exception as e:
            print(f"   ⚠️ Error with selector {asset_selector}: {e}")
            asset_elements = []

        # Fallback to alternative selectors - CraftPix specific
        if not asset_elements:
            fallback_selectors = [
                'article.product.freebie',  # CraftPix specific
                'article.product',          # CraftPix general
                'article',                  # Generic articles
                '.product.freebie',         # Class-based
                '.product',                 # Product class
                '.freebie'                  # Freebie class
            ]
            for selector in fallback_selectors:
                try:
                    asset_elements = soup.select(selector)
                    print(f"   🔍 Trying selector: {selector} -> {len(asset_elements)} elements")
                    if asset_elements:
                        print(f"   🔄 Using fallback selector: {selector} ({len(asset_elements)} elements)")
                        break
                except Exception as e:
                    print(f"   ❌ Error with selector {selector}: {e}")
                    continue

        for element in asset_elements:
            try:
                asset_data = self._extract_asset_details(element)
                if asset_data:
                    assets.append(asset_data)
            except Exception as e:
                print(f"   ⚠️ Error extracting asset: {e}")
                continue

        return assets
    
    def _extract_asset_details(self, element) -> Optional[Dict]:
        """Extract detailed asset information"""
        try:
            # Extract title with multiple strategies
            title = self._extract_title(element)
            if not title:
                return None
            
            # Extract URL
            asset_url = self._extract_asset_url(element)
            if not asset_url:
                return None
            
            # Extract other details
            description = self._extract_description(element)
            preview_image = self._extract_preview_image(element)
            tags = self._extract_tags(title, description)
            category = self._determine_category(title, description)
            asset_type = self._determine_asset_type(title, description)
            
            return {
                'title': title,
                'description': description,
                'source_url': asset_url,
                'preview_image': preview_image,
                'site': 'craftpix',
                'category': category,
                'asset_type': asset_type,
                'tags': tags,
                'license': 'Free for commercial use',
                'is_free': True,
                'download_url': None  # Will be populated later if needed
            }
            
        except Exception as e:
            print(f"     Error extracting asset details: {e}")
            return None
    
    def _extract_title(self, element):
        """Extract title using multiple strategies"""
        title_selectors = ['h3', 'h2', 'h4', '.title', '.product-title', 'a']

        for selector in title_selectors:
            try:
                title_elem = element.select_one(selector)
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    if title and len(title) > 3:
                        # Clean title
                        title = title.replace('\n', ' ').replace('\t', ' ')
                        title = ' '.join(title.split())  # Remove extra spaces
                        return title
            except Exception as e:
                continue
        return None
    
    def _extract_asset_url(self, element):
        """Extract asset URL"""
        link_elem = element.select_one('a[href]')
        if link_elem:
            href = link_elem.get('href')
            if href:
                return urljoin(self.base_url, href)
        return None
    
    def _extract_description(self, element):
        """Extract description"""
        desc_selectors = ['.description', '.excerpt', 'p', '.content']
        
        for selector in desc_selectors:
            desc_elem = element.select_one(selector)
            if desc_elem:
                desc = desc_elem.get_text(strip=True)
                if desc and len(desc) > 10:
                    return desc[:300]
        return ''
    
    def _extract_preview_image(self, element):
        """Extract preview image URL"""
        img_elem = element.select_one('img')
        if img_elem:
            src = img_elem.get('src') or img_elem.get('data-src')
            if src:
                return urljoin(self.base_url, src)
        return None
    
    def _extract_tags(self, title: str, description: str) -> List[str]:
        """Extract intelligent tags"""
        tags = []
        text = f"{title} {description}".lower()
        
        tag_keywords = [
            '2d', '3d', 'sprite', 'character', 'background', 'ui', 'icon',
            'pixel', 'cartoon', 'fantasy', 'sci-fi', 'medieval', 'modern',
            'animation', 'tileset', 'platformer', 'rpg', 'shooter', 'puzzle',
            'free', 'game', 'asset'
        ]
        
        for keyword in tag_keywords:
            if keyword in text:
                tags.append(keyword)
        
        return list(set(tags))[:8]
    
    def _determine_category(self, title: str, description: str) -> str:
        """Determine asset category intelligently"""
        text = f"{title} {description}".lower()
        
        if any(word in text for word in ['character', 'player', 'hero', 'enemy']):
            return 'characters'
        elif any(word in text for word in ['background', 'scene', 'environment']):
            return 'backgrounds'
        elif any(word in text for word in ['ui', 'interface', 'button', 'menu']):
            return 'ui'
        elif any(word in text for word in ['icon', 'symbol']):
            return 'icons'
        elif any(word in text for word in ['tile', 'tileset', 'terrain']):
            return 'tiles'
        elif any(word in text for word in ['effect', 'particle', 'explosion']):
            return 'effects'
        else:
            return 'misc'
    
    def _determine_asset_type(self, title: str, description: str) -> str:
        """Determine asset type"""
        text = f"{title} {description}".lower()
        
        if any(word in text for word in ['3d', 'model', 'mesh']):
            return '3d'
        elif any(word in text for word in ['sound', 'audio', 'music']):
            return 'audio'
        else:
            return '2d'
    
    def _optimize_results(self, assets: List[Dict]) -> List[Dict]:
        """Optimize and filter results"""
        print(f"   🔍 Optimizing {len(assets)} assets...")
        
        # Remove duplicates
        seen_urls = set()
        unique_assets = []
        
        for asset in assets:
            if asset['source_url'] not in seen_urls:
                seen_urls.add(asset['source_url'])
                unique_assets.append(asset)
        
        print(f"   ✅ Removed {len(assets) - len(unique_assets)} duplicates")
        
        # Sort by quality indicators
        unique_assets.sort(key=lambda x: (
            len(x.get('description', '')),
            len(x.get('tags', [])),
            bool(x.get('preview_image'))
        ), reverse=True)
        
        return unique_assets
    
    def save_results(self, assets, filename='craftpix_intelligent_assets.json'):
        """Save results to file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(assets, f, indent=2, ensure_ascii=False)
        print(f"💾 Results saved to {filename}")


# Test the intelligent CraftPix scraper
if __name__ == "__main__":
    scraper = IntelligentCraftPixScraper()
    assets = scraper.analyze_and_scrape(limit=10)
    
    print(f"\n🎯 CRAFTPIX INTELLIGENT SCRAPING RESULTS")
    print(f"=" * 60)
    print(f"Total assets found: {len(assets)}")
    
    for i, asset in enumerate(assets, 1):
        print(f"\n{i}. {asset['title']}")
        print(f"   Category: {asset['category']}")
        print(f"   Type: {asset['asset_type']}")
        print(f"   Tags: {', '.join(asset['tags'][:5])}")
        print(f"   URL: {asset['source_url']}")
    
    if assets:
        scraper.save_results(assets)
        print(f"\n✅ CraftPix intelligent scraping completed successfully!")
    else:
        print(f"\n❌ No assets found. Check site structure or patterns.")
