#!/usr/bin/env python3
"""
Intelligent Itch.io Scraper
Advanced intelligent scraper for Itch.io game assets with site analysis and adaptive strategies
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json
import re
from typing import List, Dict, Optional
from intelligent_site_analyzer import IntelligentSiteAnalyzer

class IntelligentItchScraper:
    """Intelligent Itch.io scraper with advanced site analysis"""
    
    def __init__(self):
        self.base_url = 'https://itch.io'
        self.game_assets_url = 'https://itch.io/game-assets'
        self.session = self._create_intelligent_session()
        self.site_analyzer = IntelligentSiteAnalyzer(self.base_url)
        
        # Itch.io-specific patterns discovered from analysis
        self.asset_patterns = [
            '/game-assets',
            'free',
            'assets',
            'sprites',
            'music',
            'sound-effects',
            'fonts',
            'tools'
        ]
        
        self.search_terms = [
            'free sprites', 'free assets', 'pixel art', 'game music',
            'sound effects', 'ui elements', 'characters', 'backgrounds',
            'tilesets', 'icons', 'fonts', 'tools'
        ]
        
        # Intelligence data
        self.site_structure = None
        self.scraping_strategy = None
        
    def _create_intelligent_session(self):
        """Create intelligent session with Itch.io optimized headers"""
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
            'DNT': '1',
            'Referer': 'https://itch.io'
        })
        return session
    
    def analyze_and_scrape(self, limit: int = None) -> List[Dict]:
        """Main intelligent scraping method with site analysis"""
        print("🧠 Starting Intelligent Itch.io Scraping...")
        print("=" * 60)
        
        # Phase 1: Site Intelligence Analysis
        print("🔍 Phase 1: Intelligent Site Analysis")
        self.site_structure = self._perform_site_analysis()
        
        # Phase 2: Adaptive Scraping Strategy
        print("🎯 Phase 2: Adaptive Scraping Strategy")
        self.scraping_strategy = self._determine_scraping_strategy()
        
        # Phase 3: Multi-Strategy Asset Extraction
        print("📦 Phase 3: Multi-Strategy Asset Extraction")
        assets = self._execute_intelligent_scraping(limit)
        
        # Phase 4: Results Optimization
        print("✨ Phase 4: Results Optimization")
        optimized_assets = self._optimize_results(assets)
        
        return optimized_assets
    
    def _perform_site_analysis(self) -> Dict:
        """Perform intelligent site structure analysis"""
        print("   🔍 Analyzing Itch.io site structure...")
        
        structure = {
            'asset_containers': [],
            'pagination_indicators': [],
            'search_capabilities': [],
            'category_navigation': [],
            'free_asset_indicators': []
        }
        
        try:
            # Analyze game assets page
            response = self.session.get(self.game_assets_url, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find asset containers (Itch.io specific)
                potential_containers = [
                    '.game_cell', '.game_link', '.game_thumb',
                    '.asset_row', '.browse_game', '[data-game_id]',
                    '.game_grid_widget', '.game_summary'
                ]
                
                for selector in potential_containers:
                    elements = soup.select(selector)
                    if elements and len(elements) > 2:
                        structure['asset_containers'].append({
                            'selector': selector,
                            'count': len(elements),
                            'confidence': min(len(elements) / 5, 1.0)
                        })
                
                # Find pagination patterns
                pagination_selectors = [
                    '.pager', '.pager_links', '.page_link',
                    'a[href*="page="]', '.next_page', '.prev_page'
                ]
                
                for selector in pagination_selectors:
                    if soup.select(selector):
                        structure['pagination_indicators'].append(selector)
                
                # Check for free asset indicators
                free_indicators = [
                    '.price_value:contains("Free")',
                    '.game_price:contains("Free")',
                    '[data-price="0"]',
                    '.free_game'
                ]
                
                for indicator in free_indicators:
                    if soup.select(indicator):
                        structure['free_asset_indicators'].append(indicator)
                        
        except Exception as e:
            print(f"   ⚠️ Site analysis warning: {e}")
        
        print(f"   ✅ Found {len(structure['asset_containers'])} container patterns")
        print(f"   ✅ Found {len(structure['pagination_indicators'])} pagination patterns")
        
        return structure
    
    def _determine_scraping_strategy(self) -> Dict:
        """Determine optimal scraping strategy"""
        strategy = {
            'primary_method': 'category_browsing',
            'secondary_method': 'search_based',
            'asset_selector': None,
            'pagination_method': 'url_parameter',
            'rate_limiting': 3.0,  # Itch.io prefers slower requests
            'max_pages_per_category': 10,
            'categories_to_scrape': [
                'game-assets', 'game-assets/free', 'game-assets/sprites',
                'game-assets/music', 'game-assets/sound-effects'
            ]
        }
        
        # Choose best asset container
        if self.site_structure['asset_containers']:
            best_container = max(
                self.site_structure['asset_containers'],
                key=lambda x: x['confidence']
            )
            strategy['asset_selector'] = best_container['selector']
            print(f"   🎯 Selected container: {best_container['selector']}")
        
        return strategy
    
    def _execute_intelligent_scraping(self, limit: int = None) -> List[Dict]:
        """Execute intelligent multi-strategy scraping"""
        all_assets = []
        
        # Strategy 1: Category browsing
        print("   📂 Strategy 1: Category Browsing")
        category_assets = self._scrape_categories(limit)
        all_assets.extend(category_assets)
        
        # Strategy 2: Search-based scraping (if we need more assets)
        if not limit or len(all_assets) < limit:
            remaining_limit = (limit - len(all_assets)) if limit else None
            print("   🔍 Strategy 2: Search-Based Scraping")
            search_assets = self._scrape_search_terms(remaining_limit)
            all_assets.extend(search_assets)
        
        return all_assets
    
    def _scrape_categories(self, limit: int = None) -> List[Dict]:
        """Scrape assets from different categories"""
        assets = []
        categories = self.scraping_strategy['categories_to_scrape']
        
        for category in categories:
            if limit and len(assets) >= limit:
                break
                
            print(f"     📂 Scraping category: {category}")
            category_url = f"{self.base_url}/{category}"
            
            # Scrape multiple pages for each category
            for page in range(1, self.scraping_strategy['max_pages_per_category'] + 1):
                if limit and len(assets) >= limit:
                    break
                
                page_url = f"{category_url}?page={page}"
                page_assets = self._scrape_page(page_url)
                
                if not page_assets:
                    break  # No more assets in this category
                
                assets.extend(page_assets)
                print(f"       📄 Page {page}: {len(page_assets)} assets")
                
                # Rate limiting
                time.sleep(self.scraping_strategy['rate_limiting'])
        
        return assets
    
    def _scrape_search_terms(self, limit: int = None) -> List[Dict]:
        """Scrape assets using search terms"""
        assets = []
        
        for term in self.search_terms:
            if limit and len(assets) >= limit:
                break
                
            print(f"     🔍 Searching for: {term}")
            search_url = f"{self.base_url}/search?q={term.replace(' ', '+')}&classification=assets"
            
            page_assets = self._scrape_page(search_url)
            assets.extend(page_assets)
            
            # Rate limiting
            time.sleep(self.scraping_strategy['rate_limiting'])
        
        return assets
    
    def _scrape_page(self, url: str) -> List[Dict]:
        """Scrape assets from a single page"""
        try:
            response = self.session.get(url, timeout=15)
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            return self._extract_page_assets(soup)
            
        except Exception as e:
            print(f"       ❌ Error scraping {url}: {e}")
            return []
    
    def _extract_page_assets(self, soup) -> List[Dict]:
        """Extract assets from page using intelligent selectors"""
        assets = []
        
        # Use intelligent asset selector
        asset_selector = self.scraping_strategy.get('asset_selector', '.game_cell')
        asset_elements = soup.select(asset_selector)
        
        # Fallback selectors for Itch.io
        if not asset_elements:
            fallback_selectors = ['.game_link', '.browse_game', '.game_thumb']
            for selector in fallback_selectors:
                asset_elements = soup.select(selector)
                if asset_elements:
                    break
        
        for element in asset_elements:
            try:
                asset_data = self._extract_asset_details(element)
                if asset_data and self._is_free_asset(element):
                    assets.append(asset_data)
            except Exception as e:
                continue
        
        return assets
    
    def _extract_asset_details(self, element) -> Optional[Dict]:
        """Extract detailed asset information"""
        try:
            # Extract title
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
            author = self._extract_author(element)
            tags = self._extract_tags(title, description)
            category = self._determine_category(title, description, asset_url)
            asset_type = self._determine_asset_type(title, description, asset_url)
            
            return {
                'title': title,
                'description': description,
                'source_url': asset_url,
                'preview_image': preview_image,
                'author': author,
                'site': 'itch_io',
                'category': category,
                'asset_type': asset_type,
                'tags': tags,
                'license': 'Varies (check individual asset)',
                'is_free': True,
                'download_url': None  # Will be populated if needed
            }
            
        except Exception as e:
            return None
    
    def _extract_title(self, element):
        """Extract title using multiple strategies"""
        title_selectors = [
            '.game_title', '.title', 'h3', 'h2', 'a[title]', '.game_link'
        ]
        
        for selector in title_selectors:
            title_elem = element.select_one(selector)
            if title_elem:
                title = title_elem.get_text(strip=True) or title_elem.get('title', '')
                if title and len(title) > 2:
                    return title
        return None
    
    def _extract_asset_url(self, element):
        """Extract asset URL"""
        link_elem = element.select_one('a[href]')
        if not link_elem:
            link_elem = element if element.name == 'a' else None
            
        if link_elem:
            href = link_elem.get('href')
            if href:
                return urljoin(self.base_url, href)
        return None
    
    def _extract_description(self, element):
        """Extract description"""
        desc_selectors = ['.game_summary', '.game_text', '.description', '.excerpt']
        
        for selector in desc_selectors:
            desc_elem = element.select_one(selector)
            if desc_elem:
                desc = desc_elem.get_text(strip=True)
                if desc and len(desc) > 5:
                    return desc[:250]
        return ''
    
    def _extract_preview_image(self, element):
        """Extract preview image URL"""
        img_elem = element.select_one('img')
        if img_elem:
            src = img_elem.get('src') or img_elem.get('data-src')
            if src:
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    src = urljoin(self.base_url, src)
                return src
        return None
    
    def _extract_author(self, element):
        """Extract author information"""
        author_selectors = ['.game_author', '.by_author', '.creator']
        
        for selector in author_selectors:
            author_elem = element.select_one(selector)
            if author_elem:
                author = author_elem.get_text(strip=True)
                if author:
                    return author.replace('by ', '')
        return 'Unknown'
    
    def _is_free_asset(self, element) -> bool:
        """Check if asset is free"""
        # Look for free indicators
        free_indicators = [
            '.price_value', '.game_price', '[data-price]'
        ]
        
        for indicator in free_indicators:
            price_elem = element.select_one(indicator)
            if price_elem:
                price_text = price_elem.get_text(strip=True).lower()
                if 'free' in price_text or '$0' in price_text:
                    return True
                # Check data attribute
                price_data = price_elem.get('data-price')
                if price_data == '0':
                    return True
        
        # If no price indicator found, assume it might be free (Itch.io has many free assets)
        return True
    
    def _extract_tags(self, title: str, description: str) -> List[str]:
        """Extract intelligent tags"""
        tags = []
        text = f"{title} {description}".lower()
        
        tag_keywords = [
            'sprite', 'pixel', 'art', 'character', 'background', 'ui', 'music',
            'sound', 'effect', 'font', 'tool', 'free', 'game', 'asset',
            '2d', '3d', 'animation', 'tileset', 'icon', 'platformer', 'rpg'
        ]
        
        for keyword in tag_keywords:
            if keyword in text:
                tags.append(keyword)
        
        return list(set(tags))[:8]
    
    def _determine_category(self, title: str, description: str, url: str) -> str:
        """Determine asset category intelligently"""
        text = f"{title} {description} {url}".lower()
        
        if any(word in text for word in ['music', 'audio', 'sound', 'sfx']):
            return 'audio'
        elif any(word in text for word in ['sprite', 'character', 'player']):
            return 'characters'
        elif any(word in text for word in ['background', 'scene', 'environment']):
            return 'backgrounds'
        elif any(word in text for word in ['ui', 'interface', 'button', 'menu']):
            return 'ui'
        elif any(word in text for word in ['tile', 'tileset', 'terrain']):
            return 'tiles'
        elif any(word in text for word in ['font', 'text', 'typography']):
            return 'fonts'
        elif any(word in text for word in ['tool', 'utility', 'software']):
            return 'tools'
        else:
            return 'misc'
    
    def _determine_asset_type(self, title: str, description: str, url: str) -> str:
        """Determine asset type"""
        text = f"{title} {description} {url}".lower()
        
        if any(word in text for word in ['music', 'audio', 'sound', 'sfx', 'wav', 'mp3']):
            return 'audio'
        elif any(word in text for word in ['3d', 'model', 'mesh', 'obj', 'fbx']):
            return '3d'
        elif any(word in text for word in ['tool', 'software', 'utility', 'editor']):
            return 'tool'
        else:
            return '2d'
    
    def _optimize_results(self, assets: List[Dict]) -> List[Dict]:
        """Optimize and filter results"""
        print(f"   🔍 Optimizing {len(assets)} assets...")
        
        # Remove duplicates based on URL
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
            bool(x.get('preview_image')),
            x.get('author', '') != 'Unknown'
        ), reverse=True)
        
        return unique_assets
    
    def save_results(self, assets, filename='itch_intelligent_assets.json'):
        """Save results to file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(assets, f, indent=2, ensure_ascii=False)
        print(f"💾 Results saved to {filename}")


# Test the intelligent Itch.io scraper
if __name__ == "__main__":
    scraper = IntelligentItchScraper()
    assets = scraper.analyze_and_scrape(limit=15)
    
    print(f"\n🎯 ITCH.IO INTELLIGENT SCRAPING RESULTS")
    print(f"=" * 60)
    print(f"Total assets found: {len(assets)}")
    
    for i, asset in enumerate(assets, 1):
        print(f"\n{i}. {asset['title']}")
        print(f"   Category: {asset['category']}")
        print(f"   Type: {asset['asset_type']}")
        print(f"   Author: {asset['author']}")
        print(f"   Tags: {', '.join(asset['tags'][:5])}")
        print(f"   URL: {asset['source_url']}")
    
    if assets:
        scraper.save_results(assets)
        print(f"\n✅ Itch.io intelligent scraping completed successfully!")
    else:
        print(f"\n❌ No assets found. Check site structure or patterns.")
