#!/usr/bin/env python3
"""
Intelligent OpenGameArt Scraper
Advanced intelligent scraper for OpenGameArt.org with site analysis and adaptive strategies
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json
import re
from typing import List, Dict, Optional
from intelligent_site_analyzer import IntelligentSiteAnalyzer

class IntelligentOpenGameArtScraper:
    """Intelligent OpenGameArt scraper with advanced site analysis"""
    
    def __init__(self):
        self.base_url = 'https://opengameart.org'
        self.browse_url = 'https://opengameart.org/art-search-advanced'
        self.session = self._create_intelligent_session()
        self.site_analyzer = IntelligentSiteAnalyzer(self.base_url)
        
        # OpenGameArt-specific patterns
        self.asset_categories = [
            '2D Art', '3D Art', 'Music', 'Sound Effect', 'Document', 'Concept Art'
        ]
        
        self.search_terms = [
            'sprite', 'character', 'background', 'tileset', 'ui', 'icon',
            'music', 'sound', 'effect', 'texture', 'model', 'animation'
        ]
        
        # Intelligence data
        self.site_structure = None
        self.scraping_strategy = None
        
    def _create_intelligent_session(self):
        """Create intelligent session optimized for OpenGameArt"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'Referer': 'https://opengameart.org'
        })
        return session
    
    def analyze_and_scrape(self, limit: int = None) -> List[Dict]:
        """Main intelligent scraping method with site analysis"""
        print("🧠 Starting Intelligent OpenGameArt Scraping...")
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
        print("   🔍 Analyzing OpenGameArt site structure...")
        
        structure = {
            'asset_containers': [],
            'pagination_indicators': [],
            'search_capabilities': [],
            'category_filters': [],
            'license_indicators': []
        }
        
        try:
            # Analyze browse page
            response = self.session.get(self.browse_url, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find asset containers
                potential_containers = [
                    '.view-art-search', '.views-row', '.node-art',
                    '.art-preview', '.search-result', 'article'
                ]
                
                for selector in potential_containers:
                    elements = soup.select(selector)
                    if elements and len(elements) > 2:
                        structure['asset_containers'].append({
                            'selector': selector,
                            'count': len(elements),
                            'confidence': min(len(elements) / 8, 1.0)
                        })
                
                # Find pagination
                pagination_selectors = [
                    '.pager', '.pager-item', '.page-link',
                    'a[href*="page="]', '.next', '.previous'
                ]
                
                for selector in pagination_selectors:
                    if soup.select(selector):
                        structure['pagination_indicators'].append(selector)
                
                # Find license indicators
                license_selectors = [
                    '.license', '.copyright', '.cc-license',
                    '[class*="license"]', '.field-name-field-art-licenses'
                ]
                
                for selector in license_selectors:
                    if soup.select(selector):
                        structure['license_indicators'].append(selector)
                        
        except Exception as e:
            print(f"   ⚠️ Site analysis warning: {e}")
        
        print(f"   ✅ Found {len(structure['asset_containers'])} container patterns")
        print(f"   ✅ Found {len(structure['pagination_indicators'])} pagination patterns")
        
        return structure
    
    def _determine_scraping_strategy(self) -> Dict:
        """Determine optimal scraping strategy"""
        strategy = {
            'primary_method': 'advanced_search',
            'secondary_method': 'category_browsing',
            'asset_selector': None,
            'pagination_method': 'url_parameter',
            'rate_limiting': 2.5,  # OpenGameArt is community-friendly
            'max_pages_per_search': 15,
            'search_parameters': {
                'sort_by': 'created',
                'sort_order': 'DESC',
                'items_per_page': 12
            }
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
        
        # Strategy 1: Advanced search with different parameters
        print("   🔍 Strategy 1: Advanced Search")
        search_assets = self._scrape_advanced_search(limit)
        all_assets.extend(search_assets)
        
        # Strategy 2: Category-based browsing (if we need more assets)
        if not limit or len(all_assets) < limit:
            remaining_limit = (limit - len(all_assets)) if limit else None
            print("   📂 Strategy 2: Category Browsing")
            category_assets = self._scrape_categories(remaining_limit)
            all_assets.extend(category_assets)
        
        return all_assets
    
    def _scrape_advanced_search(self, limit: int = None) -> List[Dict]:
        """Scrape using advanced search functionality"""
        assets = []
        
        # Different search configurations
        search_configs = [
            {'field_art_type': '9', 'title': '2D Art'},  # 2D Art
            {'field_art_type': '10', 'title': '3D Art'}, # 3D Art
            {'field_art_type': '12', 'title': 'Music'},  # Music
            {'field_art_type': '13', 'title': 'Sound Effect'}, # Sound Effect
        ]
        
        for config in search_configs:
            if limit and len(assets) >= limit:
                break
                
            print(f"     🎯 Searching {config['title']}...")
            
            # Scrape multiple pages for each search
            for page in range(0, self.scraping_strategy['max_pages_per_search']):
                if limit and len(assets) >= limit:
                    break
                
                search_url = self._build_search_url(config, page)
                page_assets = self._scrape_page(search_url)
                
                if not page_assets:
                    break
                
                assets.extend(page_assets)
                print(f"       📄 Page {page + 1}: {len(page_assets)} assets")
                
                # Rate limiting
                time.sleep(self.scraping_strategy['rate_limiting'])
        
        return assets
    
    def _build_search_url(self, config: Dict, page: int = 0) -> str:
        """Build advanced search URL"""
        base_params = {
            'page': page,
            'sort_by': 'created',
            'sort_order': 'DESC'
        }
        base_params.update(config)
        
        # Remove title from params
        if 'title' in base_params:
            del base_params['title']
        
        param_string = '&'.join([f"{k}={v}" for k, v in base_params.items()])
        return f"{self.browse_url}?{param_string}"
    
    def _scrape_categories(self, limit: int = None) -> List[Dict]:
        """Scrape assets from different categories"""
        assets = []
        
        for term in self.search_terms:
            if limit and len(assets) >= limit:
                break
                
            print(f"     🔍 Searching for: {term}")
            search_url = f"{self.browse_url}?keys={term}"
            
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
        asset_selector = self.scraping_strategy.get('asset_selector', '.views-row')
        asset_elements = soup.select(asset_selector)
        
        # Fallback selectors for OpenGameArt
        if not asset_elements:
            fallback_selectors = ['.node-art', '.art-preview', 'article']
            for selector in fallback_selectors:
                asset_elements = soup.select(selector)
                if asset_elements:
                    break
        
        for element in asset_elements:
            try:
                asset_data = self._extract_asset_details(element)
                if asset_data:
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
            license_info = self._extract_license(element)
            tags = self._extract_tags(title, description)
            category = self._determine_category(title, description, asset_url)
            asset_type = self._determine_asset_type(title, description, asset_url)
            
            return {
                'title': title,
                'description': description,
                'source_url': asset_url,
                'preview_image': preview_image,
                'author': author,
                'license': license_info,
                'site': 'opengameart',
                'category': category,
                'asset_type': asset_type,
                'tags': tags,
                'is_free': True,  # OpenGameArt is all free/open
                'download_url': None  # Will be populated if needed
            }
            
        except Exception as e:
            return None
    
    def _extract_title(self, element):
        """Extract title using multiple strategies"""
        title_selectors = [
            'h2 a', 'h3 a', '.node-title a', '.title a', 'a[href*="/content/"]'
        ]
        
        for selector in title_selectors:
            title_elem = element.select_one(selector)
            if title_elem:
                title = title_elem.get_text(strip=True)
                if title and len(title) > 2:
                    return title
        return None
    
    def _extract_asset_url(self, element):
        """Extract asset URL"""
        link_selectors = [
            'h2 a', 'h3 a', '.node-title a', 'a[href*="/content/"]'
        ]
        
        for selector in link_selectors:
            link_elem = element.select_one(selector)
            if link_elem:
                href = link_elem.get('href')
                if href:
                    return urljoin(self.base_url, href)
        return None
    
    def _extract_description(self, element):
        """Extract description"""
        desc_selectors = [
            '.field-name-body', '.content', '.node-content', 'p'
        ]
        
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
    
    def _extract_author(self, element):
        """Extract author information"""
        author_selectors = [
            '.username', '.field-name-name', '.submitted a', '.author'
        ]
        
        for selector in author_selectors:
            author_elem = element.select_one(selector)
            if author_elem:
                author = author_elem.get_text(strip=True)
                if author:
                    return author
        return 'Unknown'
    
    def _extract_license(self, element):
        """Extract license information"""
        license_selectors = [
            '.field-name-field-art-licenses', '.license', '.copyright'
        ]
        
        for selector in license_selectors:
            license_elem = element.select_one(selector)
            if license_elem:
                license_text = license_elem.get_text(strip=True)
                if license_text:
                    return license_text
        
        return 'CC0/GPL/OGA-BY (check individual asset)'
    
    def _extract_tags(self, title: str, description: str) -> List[str]:
        """Extract intelligent tags"""
        tags = []
        text = f"{title} {description}".lower()
        
        tag_keywords = [
            'sprite', 'character', 'background', 'tileset', 'ui', 'icon',
            'music', 'sound', 'effect', 'texture', 'model', 'animation',
            '2d', '3d', 'pixel', 'art', 'game', 'free', 'open', 'cc0'
        ]
        
        for keyword in tag_keywords:
            if keyword in text:
                tags.append(keyword)
        
        return list(set(tags))[:8]
    
    def _determine_category(self, title: str, description: str, url: str) -> str:
        """Determine asset category intelligently"""
        text = f"{title} {description} {url}".lower()
        
        if any(word in text for word in ['music', 'audio', 'sound', 'ogg', 'wav']):
            return 'audio'
        elif any(word in text for word in ['3d', 'model', 'mesh', 'obj', 'blend']):
            return '3d'
        elif any(word in text for word in ['sprite', 'character', 'player']):
            return 'characters'
        elif any(word in text for word in ['background', 'scene', 'environment']):
            return 'backgrounds'
        elif any(word in text for word in ['ui', 'interface', 'button', 'menu']):
            return 'ui'
        elif any(word in text for word in ['tile', 'tileset', 'terrain']):
            return 'tiles'
        elif any(word in text for word in ['icon', 'symbol']):
            return 'icons'
        elif any(word in text for word in ['texture', 'material']):
            return 'textures'
        else:
            return 'misc'
    
    def _determine_asset_type(self, title: str, description: str, url: str) -> str:
        """Determine asset type"""
        text = f"{title} {description} {url}".lower()
        
        if any(word in text for word in ['music', 'audio', 'sound', 'ogg', 'wav', 'mp3']):
            return 'audio'
        elif any(word in text for word in ['3d', 'model', 'mesh', 'obj', 'blend', 'fbx']):
            return '3d'
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
    
    def save_results(self, assets, filename='opengameart_intelligent_assets.json'):
        """Save results to file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(assets, f, indent=2, ensure_ascii=False)
        print(f"💾 Results saved to {filename}")


# Test the intelligent OpenGameArt scraper
if __name__ == "__main__":
    scraper = IntelligentOpenGameArtScraper()
    assets = scraper.analyze_and_scrape(limit=12)
    
    print(f"\n🎯 OPENGAMEART INTELLIGENT SCRAPING RESULTS")
    print(f"=" * 60)
    print(f"Total assets found: {len(assets)}")
    
    for i, asset in enumerate(assets, 1):
        print(f"\n{i}. {asset['title']}")
        print(f"   Category: {asset['category']}")
        print(f"   Type: {asset['asset_type']}")
        print(f"   Author: {asset['author']}")
        print(f"   License: {asset['license']}")
        print(f"   Tags: {', '.join(asset['tags'][:5])}")
        print(f"   URL: {asset['source_url']}")
    
    if assets:
        scraper.save_results(assets)
        print(f"\n✅ OpenGameArt intelligent scraping completed successfully!")
    else:
        print(f"\n❌ No assets found. Check site structure or patterns.")
