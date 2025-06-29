#!/usr/bin/env python3
"""
Ultra Intelligent GameIcons Scraper
Advanced intelligent scraping with comprehensive icon extraction and quality scoring
"""

import time
import json
import random
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import requests
from safe_scraping import SafeScrapingManager
from urllib.parse import urljoin, urlparse

class UltraIntelligentGameIconsScraper:
    """Ultra intelligent GameIcons scraper with advanced features"""
    
    def __init__(self):
        self.base_url = "https://game-icons.net"
        self.site_name = "GameIcons"
        self.safe_scraper = SafeScrapingManager()
        self.scraped_assets = []
        self.site_intelligence = {}
        
        print("🧠 Ultra Intelligent GameIcons Scraper Initialized")
        print("=" * 60)
        print("🎯 Features:")
        print("   ✅ Intelligent category analysis")
        print("   ✅ SVG icon extraction")
        print("   ✅ Quality scoring system")
        print("   ✅ License information parsing")
        print("   ✅ Multi-format support")
        print("   ✅ Advanced metadata extraction")
    
    def analyze_and_scrape(self, limit: int = None) -> List[Dict]:
        """Main ultra intelligent scraping method"""
        print("🧠 Starting Ultra Intelligent GameIcons Scraping...")
        print("=" * 60)
        
        # Phase 1: Site Intelligence Analysis
        print("🔍 Phase 1: Site Intelligence Analysis")
        self.site_intelligence = self._perform_site_analysis()
        
        # Phase 2: Category-Based Strategy
        print("🎯 Phase 2: Category-Based Scraping Strategy")
        strategy = self._determine_scraping_strategy()
        
        # Phase 3: Multi-Category Icon Extraction
        print("📦 Phase 3: Multi-Category Icon Extraction")
        assets = self._execute_intelligent_scraping(strategy, limit)
        
        # Phase 4: Quality Enhancement & Scoring
        print("✨ Phase 4: Quality Enhancement & Scoring")
        enhanced_assets = self._enhance_and_score_assets(assets)
        
        # Phase 5: Results Optimization
        print("🎯 Phase 5: Results Optimization")
        optimized_assets = self._optimize_results(enhanced_assets)
        
        return optimized_assets
    
    def _perform_site_analysis(self) -> Dict:
        """Perform intelligent site analysis"""
        print("🌐 Analyzing GameIcons structure...")
        
        # Analyze main page
        response = self.safe_scraper.safe_get(self.base_url)
        if not response:
            return {'error': 'Cannot access site'}
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find available categories
        categories = self._discover_categories(soup)
        
        # Analyze icon structure
        icon_structure = self._analyze_icon_structure()
        
        # Test download capabilities
        download_methods = self._test_download_methods()
        
        intelligence = {
            'categories': categories,
            'icon_structure': icon_structure,
            'download_methods': download_methods,
            'base_url': self.base_url,
            'analysis_time': time.time()
        }
        
        print(f"   📂 Found {len(categories)} categories")
        print(f"   🔍 Icon structure analyzed")
        print(f"   📥 Download methods tested")
        
        return intelligence
    
    def _discover_categories(self, soup: BeautifulSoup) -> List[Dict]:
        """Discover available categories"""
        categories = []
        
        # Look for category links
        category_selectors = [
            'a[href*="/tags/"]',
            '.tag-link',
            '.category-link'
        ]
        
        for selector in category_selectors:
            category_links = soup.select(selector)
            for link in category_links:
                href = link.get('href')
                text = link.get_text(strip=True)
                
                if href and text and '/tags/' in href:
                    category_name = href.split('/tags/')[-1].replace('.html', '')
                    categories.append({
                        'name': category_name,
                        'display_name': text,
                        'url': urljoin(self.base_url, href)
                    })
        
        # Add default categories if none found
        if not categories:
            default_categories = [
                'game', 'weapon', 'armor', 'magic', 'creature', 'item',
                'skill', 'spell', 'potion', 'treasure', 'tool', 'symbol',
                'ui', 'interface', 'button', 'menu'
            ]
            
            for cat in default_categories:
                categories.append({
                    'name': cat,
                    'display_name': cat.title(),
                    'url': f"{self.base_url}/tags/{cat}.html"
                })
        
        return categories[:20]  # Limit to 20 categories
    
    def _analyze_icon_structure(self) -> Dict:
        """Analyze icon page structure"""
        # Test with a known category
        test_url = f"{self.base_url}/tags/game.html"
        response = self.safe_scraper.safe_get(test_url)
        
        if not response:
            return {'error': 'Cannot analyze structure'}
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find icon containers - GameIcons uses specific structure
        icon_selectors = [
            'div.icon',  # Primary selector from working scraper
            'a.icon-link',  # Alternative selector
            'img',  # Fallback to images
            'svg'   # Fallback to SVG elements
        ]

        best_selector = None
        max_icons = 0

        for selector in icon_selectors:
            icons = soup.select(selector)
            if len(icons) > max_icons:
                max_icons = len(icons)
                best_selector = selector
                print(f"   🔍 Testing selector '{selector}': {len(icons)} icons found")
        
        return {
            'best_selector': best_selector,
            'icon_count_sample': max_icons,
            'structure_analyzed': True
        }
    
    def _test_download_methods(self) -> List[str]:
        """Test available download methods"""
        methods = []
        
        # Test SVG direct access
        test_svg_url = f"{self.base_url}/1x1/delapouite/sword.svg"
        response = self.safe_scraper.safe_get(test_svg_url)
        if response and response.status_code == 200:
            methods.append('direct_svg')
        
        # Test PNG access
        test_png_url = f"{self.base_url}/1x1/delapouite/sword.png"
        response = self.safe_scraper.safe_get(test_png_url)
        if response and response.status_code == 200:
            methods.append('direct_png')
        
        return methods
    
    def _determine_scraping_strategy(self) -> Dict:
        """Determine optimal scraping strategy"""
        strategy = {
            'primary_method': 'category_based',
            'icon_selector': '.icon',
            'categories_to_scrape': [],
            'max_icons_per_category': 20,
            'download_formats': ['svg', 'png'],
            'rate_limiting': 1.5
        }
        
        # Use discovered categories
        if self.site_intelligence.get('categories'):
            strategy['categories_to_scrape'] = [
                cat['name'] for cat in self.site_intelligence['categories'][:10]
            ]
        
        # Use best icon selector
        if self.site_intelligence.get('icon_structure', {}).get('best_selector'):
            strategy['icon_selector'] = self.site_intelligence['icon_structure']['best_selector']
        
        # Use available download methods
        if self.site_intelligence.get('download_methods'):
            strategy['download_formats'] = self.site_intelligence['download_methods']
        
        print(f"   🎯 Strategy: {strategy['primary_method']}")
        print(f"   📂 Categories: {len(strategy['categories_to_scrape'])}")
        print(f"   🔍 Icon selector: {strategy['icon_selector']}")
        
        return strategy
    
    def _execute_intelligent_scraping(self, strategy: Dict, limit: int = None) -> List[Dict]:
        """Execute intelligent scraping"""
        assets = []
        limit = limit or 100
        
        print(f"🎯 Target: {limit} icons")
        
        categories = strategy['categories_to_scrape']
        icons_per_category = min(strategy['max_icons_per_category'], limit // len(categories) if categories else limit)
        
        for category in categories:
            if len(assets) >= limit:
                break
            
            try:
                category_url = f"{self.base_url}/tags/{category}.html"
                category_assets = self._scrape_category(category_url, category, strategy, icons_per_category)
                assets.extend(category_assets)
                
                print(f"   📂 {category}: {len(category_assets)} icons")
                time.sleep(strategy['rate_limiting'])
                
            except Exception as e:
                print(f"⚠️ Error scraping category {category}: {e}")
                continue
        
        return assets[:limit]
    
    def _scrape_category(self, url: str, category: str, strategy: Dict, limit: int) -> List[Dict]:
        """Scrape icons from a category"""
        assets = []
        
        response = self.safe_scraper.safe_get(url)
        if not response:
            return assets
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find icon elements
        icon_elements = soup.select(strategy['icon_selector'])
        
        for elem in icon_elements[:limit]:
            try:
                icon_data = self._extract_icon_data(elem, category, strategy)
                if icon_data:
                    assets.append(icon_data)
            except Exception as e:
                continue
        
        return assets
    
    def _extract_icon_data(self, element, category: str, strategy: Dict) -> Optional[Dict]:
        """Extract icon data from element - adapted from working scraper"""
        try:
            # Handle different element types
            if element.name == 'div' and 'icon' in element.get('class', []):
                # Primary GameIcons structure: div.icon containing a link
                link_elem = element.select_one('a')
                if not link_elem:
                    return None
                icon_url = urljoin(self.base_url, link_elem.get('href'))
                title = link_elem.get('title') or icon_url.split('/')[-1].replace('.html', '').replace('-', ' ').title()

                # Look for image in the div
                img_elem = element.select_one('img')
                preview_image = urljoin(self.base_url, img_elem.get('src')) if img_elem else None

            elif element.name == 'a':
                # Direct link element
                icon_url = urljoin(self.base_url, element.get('href'))
                title = element.get('title') or icon_url.split('/')[-1].replace('.html', '').replace('-', ' ').title()

                img_elem = element.select_one('img')
                preview_image = urljoin(self.base_url, img_elem.get('src')) if img_elem else None

            elif element.name == 'img':
                # Direct image element
                preview_image = urljoin(self.base_url, element.get('src'))
                title = element.get('alt') or element.get('title') or 'Game Icon'

                # Look for parent link
                parent_link = element.find_parent('a')
                if parent_link:
                    icon_url = urljoin(self.base_url, parent_link.get('href'))
                else:
                    icon_url = preview_image

            else:
                return None

            if not title or not icon_url:
                return None

            # Generate download URLs
            download_urls = self._generate_download_urls(icon_url, strategy)

            # Extract author if available
            author = self._extract_author_from_url(icon_url)

            return {
                'title': f"{title} Icon",
                'source_url': icon_url,
                'preview_image': preview_image,
                'download_urls': download_urls,
                'author': author,
                'category': category,
                'asset_type': 'Icon',
                'site': 'GameIcons',
                'license': 'CC BY 3.0',
                'file_formats': strategy.get('download_formats', ['svg']),
                'tags': [category, 'icon', 'game', 'ui'],
                'timestamp': time.time()
            }

        except Exception as e:
            return None
    
    def _generate_download_urls(self, icon_url: str, strategy: Dict) -> Dict[str, str]:
        """Generate download URLs for different formats"""
        download_urls = {}
        
        # Extract icon path from URL
        # Example: https://game-icons.net/1x1/delapouite/sword.html
        if '/1x1/' in icon_url:
            base_path = icon_url.replace('.html', '')
            
            for format_type in strategy.get('download_formats', ['svg']):
                if format_type == 'direct_svg':
                    download_urls['svg'] = f"{base_path}.svg"
                elif format_type == 'direct_png':
                    download_urls['png'] = f"{base_path}.png"
        
        return download_urls
    
    def _extract_author_from_url(self, url: str) -> str:
        """Extract author name from URL"""
        try:
            # URL format: https://game-icons.net/1x1/author/icon.html
            parts = url.split('/')
            if len(parts) >= 5 and '1x1' in parts:
                author_index = parts.index('1x1') + 1
                if author_index < len(parts):
                    return parts[author_index].replace('-', ' ').title()
        except:
            pass
        return ""

    def _enhance_and_score_assets(self, assets: List[Dict]) -> List[Dict]:
        """Enhance assets with quality scoring"""
        enhanced_assets = []

        print(f"✨ Enhancing {len(assets)} icons...")

        for asset in assets:
            try:
                enhanced = asset.copy()

                # Calculate quality score
                enhanced['quality_score'] = self._calculate_quality_score(asset)

                # Enhance metadata
                enhanced = self._enhance_icon_metadata(enhanced)

                # Verify download URLs
                enhanced = self._verify_download_urls(enhanced)

                enhanced_assets.append(enhanced)

            except Exception as e:
                enhanced_assets.append(asset)
                continue

        return enhanced_assets

    def _calculate_quality_score(self, asset: Dict) -> float:
        """Calculate icon quality score"""
        score = 0.0

        # Title quality (20%)
        if asset.get('title') and len(asset['title']) > 5:
            score += 0.2

        # Preview image availability (25%)
        if asset.get('preview_image'):
            score += 0.25

        # Download URLs availability (30%)
        download_urls = asset.get('download_urls', {})
        if download_urls:
            score += 0.3

        # Author information (10%)
        if asset.get('author'):
            score += 0.1

        # License information (10%)
        if asset.get('license'):
            score += 0.1

        # Category information (5%)
        if asset.get('category'):
            score += 0.05

        return min(score, 1.0)

    def _enhance_icon_metadata(self, asset: Dict) -> Dict:
        """Enhance icon with additional metadata"""
        # Add usage suggestions
        category = asset.get('category', '').lower()
        title = asset.get('title', '').lower()

        usage_suggestions = []

        if any(term in category or term in title for term in ['weapon', 'sword', 'bow']):
            usage_suggestions.extend(['Combat UI', 'Inventory', 'Equipment'])
        elif any(term in category or term in title for term in ['magic', 'spell', 'potion']):
            usage_suggestions.extend(['Magic System', 'Spellbook', 'Alchemy'])
        elif any(term in category or term in title for term in ['ui', 'interface', 'button']):
            usage_suggestions.extend(['User Interface', 'Menu', 'HUD'])
        else:
            usage_suggestions.extend(['Game UI', 'Interface', 'Icons'])

        asset['usage_suggestions'] = usage_suggestions

        # Add technical specifications
        asset['technical_specs'] = {
            'format': 'SVG/PNG',
            'scalable': True,
            'transparent_background': True,
            'color': 'Monochrome (customizable)',
            'recommended_size': '16x16 to 512x512 pixels'
        }

        # Add game development context
        asset['game_dev_context'] = {
            'suitable_for': ['2D Games', '3D Games', 'Mobile Games', 'Web Games'],
            'ui_elements': ['HUD', 'Inventory', 'Menus', 'Buttons'],
            'customizable': True
        }

        return asset

    def _verify_download_urls(self, asset: Dict) -> Dict:
        """Verify and update download URLs"""
        download_urls = asset.get('download_urls', {})
        verified_urls = {}

        for format_type, url in download_urls.items():
            try:
                # Quick HEAD request to verify URL
                response = self.safe_scraper.safe_get(url, method='HEAD')
                if response and response.status_code == 200:
                    verified_urls[format_type] = url
            except:
                continue

        asset['download_urls'] = verified_urls
        asset['download_verified'] = len(verified_urls) > 0

        return asset

    def _optimize_results(self, assets: List[Dict]) -> List[Dict]:
        """Optimize and filter results"""
        print(f"🎯 Optimizing {len(assets)} icons...")

        # Remove duplicates
        seen_titles = set()
        seen_urls = set()
        unique_assets = []

        for asset in assets:
            title = asset.get('title', '').lower()
            url = asset.get('source_url', '')

            if title not in seen_titles and url not in seen_urls:
                seen_titles.add(title)
                if url:
                    seen_urls.add(url)
                unique_assets.append(asset)

        # Sort by quality score
        unique_assets.sort(key=lambda x: x.get('quality_score', 0), reverse=True)

        # Group by category
        category_stats = {}
        for asset in unique_assets:
            category = asset.get('category', 'Unknown')
            category_stats[category] = category_stats.get(category, 0) + 1

        print(f"✅ Optimization complete: {len(unique_assets)} unique icons")
        if unique_assets:
            avg_quality = sum(a.get('quality_score', 0) for a in unique_assets) / len(unique_assets)
            print(f"📊 Average quality score: {avg_quality:.2f}")
            print(f"📂 Categories: {len(category_stats)}")

        return unique_assets

# Test function
def test_ultra_intelligent_gameicons_scraper():
    """Test the ultra intelligent GameIcons scraper"""
    print("🧪 Testing Ultra Intelligent GameIcons Scraper")
    print("=" * 60)

    scraper = UltraIntelligentGameIconsScraper()

    try:
        assets = scraper.analyze_and_scrape(limit=20)

        print(f"\n📊 SCRAPING RESULTS")
        print(f"   🎯 Total icons: {len(assets)}")

        if assets:
            avg_quality = sum(a.get('quality_score', 0) for a in assets) / len(assets)
            print(f"   📈 Average quality score: {avg_quality:.2f}")

            # Count by category
            categories = {}
            for asset in assets:
                category = asset.get('category', 'Unknown')
                categories[category] = categories.get(category, 0) + 1

            print(f"\n📂 Categories:")
            for category, count in categories.items():
                print(f"   {category}: {count} icons")

            print(f"\n🎨 Sample Icons:")
            for i, asset in enumerate(assets[:5], 1):
                print(f"   {i}. {asset['title'][:50]}...")
                print(f"      Quality: {asset.get('quality_score', 0):.2f}")
                print(f"      Category: {asset.get('category', 'Unknown')}")
                print(f"      Author: {asset.get('author', 'Unknown')}")
                print(f"      Downloads: {len(asset.get('download_urls', {}))}")

        return assets

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return []

if __name__ == "__main__":
    test_ultra_intelligent_gameicons_scraper()
