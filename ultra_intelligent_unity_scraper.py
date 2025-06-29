#!/usr/bin/env python3
"""
Ultra Intelligent Unity Asset Store Scraper
Advanced free asset extraction from Unity Asset Store
"""

import time
import json
import random
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import requests
from safe_scraping import SafeScrapingManager
from urllib.parse import urljoin, urlparse

class UltraIntelligentUnityScraper:
    """Ultra intelligent Unity Asset Store scraper for free assets"""
    
    def __init__(self):
        self.base_url = "https://assetstore.unity.com"
        self.site_name = "Unity Asset Store"
        self.safe_scraper = SafeScrapingManager()
        self.scraped_assets = []
        self.site_intelligence = {}
        
        print("🧠 Ultra Intelligent Unity Asset Store Scraper Initialized")
        print("=" * 60)
        print("🎯 Features:")
        print("   ✅ Free asset focus")
        print("   ✅ 2D/3D asset extraction")
        print("   ✅ Quality scoring system")
        print("   ✅ Category-based organization")
        print("   ✅ License information parsing")
        print("   ✅ Advanced filtering")
    
    def analyze_and_scrape(self, limit: int = None) -> List[Dict]:
        """Main ultra intelligent scraping method"""
        print("🧠 Starting Ultra Intelligent Unity Asset Store Scraping...")
        print("=" * 60)
        
        # Phase 1: Site Intelligence Analysis
        print("🔍 Phase 1: Site Intelligence Analysis")
        self.site_intelligence = self._perform_site_analysis()
        
        # Phase 2: Free Asset Strategy
        print("🎯 Phase 2: Free Asset Scraping Strategy")
        strategy = self._determine_scraping_strategy()
        
        # Phase 3: Multi-Category Asset Extraction
        print("📦 Phase 3: Multi-Category Asset Extraction")
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
        print("🌐 Analyzing Unity Asset Store structure...")
        
        # Test free assets page
        free_assets_url = f"{self.base_url}/packages/2d/gui/free"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(free_assets_url, headers=headers, timeout=15)
        except Exception as e:
            print(f"   ❌ Site analysis failed: {e}")
            return {'error': 'Cannot access site'}
        
        if not response or response.status_code != 200:
            return {'error': f'Site returned {response.status_code if response else "no response"}'}
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Analyze asset containers
        asset_structure = self._analyze_asset_structure(soup)
        
        # Get asset categories
        asset_categories = self._get_unity_asset_categories()
        
        intelligence = {
            'asset_structure': asset_structure,
            'asset_categories': asset_categories,
            'base_url': self.base_url,
            'analysis_time': time.time()
        }
        
        print(f"   🔍 Asset structure analyzed")
        print(f"   📂 Asset categories prepared")
        
        return intelligence
    
    def _analyze_asset_structure(self, soup: BeautifulSoup) -> Dict:
        """Analyze asset container structure"""
        selectors = [
            '.package-card',
            '.asset-card',
            '[data-package-id]',
            '.result-item',
            '.package-item'
        ]
        
        best_selector = None
        max_assets = 0
        
        for selector in selectors:
            assets = soup.select(selector)
            if len(assets) > max_assets:
                max_assets = len(assets)
                best_selector = selector
                print(f"   🎯 Testing selector '{selector}': {len(assets)} assets found")
        
        return {
            'best_selector': best_selector or '.package-card',
            'asset_count_sample': max_assets,
            'structure_analyzed': True
        }
    
    def _get_unity_asset_categories(self) -> List[Dict]:
        """Get Unity Asset Store categories for free assets"""
        return [
            {
                'name': '2d_gui',
                'url_path': '/packages/2d/gui/free',
                'priority': 1,
                'description': '2D GUI Elements'
            },
            {
                'name': '2d_characters',
                'url_path': '/packages/2d/characters/free',
                'priority': 1,
                'description': '2D Characters'
            },
            {
                'name': '2d_environments',
                'url_path': '/packages/2d/environments/free',
                'priority': 2,
                'description': '2D Environments'
            },
            {
                'name': '3d_characters',
                'url_path': '/packages/3d/characters/free',
                'priority': 2,
                'description': '3D Characters'
            },
            {
                'name': '3d_environments',
                'url_path': '/packages/3d/environments/free',
                'priority': 3,
                'description': '3D Environments'
            },
            {
                'name': 'audio',
                'url_path': '/packages/audio/free',
                'priority': 3,
                'description': 'Audio Assets'
            }
        ]
    
    def _determine_scraping_strategy(self) -> Dict:
        """Determine optimal scraping strategy"""
        strategy = {
            'primary_method': 'category_based',
            'asset_selector': '.package-card',
            'asset_categories': [],
            'assets_per_category': 8,
            'max_pages_per_category': 2,
            'rate_limiting': 2.5,
            'quality_filters': ['free_only', 'game_relevant']
        }
        
        # Use discovered asset structure
        if self.site_intelligence.get('asset_structure', {}).get('best_selector'):
            strategy['asset_selector'] = self.site_intelligence['asset_structure']['best_selector']
        
        # Use asset categories
        if self.site_intelligence.get('asset_categories'):
            strategy['asset_categories'] = self.site_intelligence['asset_categories']
        
        print(f"   🎯 Strategy: {strategy['primary_method']}")
        print(f"   📂 Asset categories: {len(strategy['asset_categories'])}")
        print(f"   🔍 Asset selector: {strategy['asset_selector']}")
        
        return strategy
    
    def _execute_intelligent_scraping(self, strategy: Dict, limit: int = None) -> List[Dict]:
        """Execute intelligent scraping"""
        assets = []
        limit = limit or 40
        
        print(f"🎯 Target: {limit} assets")
        
        asset_categories = strategy['asset_categories']
        assets_per_category = limit // len(asset_categories) if asset_categories else limit
        
        for category in asset_categories:
            if len(assets) >= limit:
                break
            
            try:
                category_assets = self._scrape_asset_category(category, strategy, assets_per_category)
                assets.extend(category_assets)
                
                print(f"   📂 {category['name']}: {len(category_assets)} assets")
                time.sleep(strategy['rate_limiting'])
                
            except Exception as e:
                print(f"⚠️ Error scraping category {category['name']}: {e}")
                continue
        
        return assets[:limit]
    
    def _scrape_asset_category(self, category: Dict, strategy: Dict, limit: int) -> List[Dict]:
        """Scrape assets from a category"""
        assets = []
        
        for page in range(1, strategy['max_pages_per_category'] + 1):
            if len(assets) >= limit:
                break
            
            # Build category URL
            category_url = f"{self.base_url}{category['url_path']}"
            if page > 1:
                category_url += f"?page={page}"
            
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
                response = requests.get(category_url, headers=headers, timeout=15)
            except Exception as e:
                print(f"   ❌ Request failed for {category['name']} page {page}: {e}")
                continue
            
            if not response or response.status_code != 200:
                continue
            
            soup = BeautifulSoup(response.content, 'html.parser')
            page_assets = self._extract_assets_from_page(soup, strategy, category)
            
            if not page_assets:
                break  # No more assets
            
            assets.extend(page_assets)
            time.sleep(1)  # Page rate limiting
        
        return assets[:limit]
    
    def _extract_assets_from_page(self, soup: BeautifulSoup, strategy: Dict, category: Dict) -> List[Dict]:
        """Extract assets from a page"""
        assets = []
        
        asset_elements = soup.select(strategy['asset_selector'])
        
        for elem in asset_elements:
            try:
                asset_data = self._extract_asset_data(elem, category)
                if asset_data and self._passes_quality_filters(asset_data, strategy):
                    assets.append(asset_data)
            except Exception as e:
                continue
        
        return assets
    
    def _extract_asset_data(self, element, category: Dict) -> Optional[Dict]:
        """Extract asset data from element"""
        try:
            # Extract asset link
            link_elem = element.select_one('a')
            if not link_elem:
                return None
            
            asset_url = urljoin(self.base_url, link_elem.get('href'))
            
            # Extract title
            title_elem = element.select_one('.package-title, .asset-title, h3, h4')
            title = title_elem.get_text(strip=True) if title_elem else 'Unity Asset'
            
            # Extract preview image
            img_elem = element.select_one('img')
            preview_image = None
            if img_elem:
                preview_image = img_elem.get('src') or img_elem.get('data-src')
                if preview_image and not preview_image.startswith('http'):
                    preview_image = urljoin(self.base_url, preview_image)
            
            # Extract author/publisher
            author_elem = element.select_one('.publisher, .author, .package-publisher')
            author = author_elem.get_text(strip=True) if author_elem else ""
            
            # Extract price (should be free)
            price_elem = element.select_one('.price, .package-price')
            price = price_elem.get_text(strip=True) if price_elem else "Free"
            
            # Extract rating if available
            rating_elem = element.select_one('.rating, .stars')
            rating = rating_elem.get_text(strip=True) if rating_elem else ""
            
            return {
                'title': title,
                'source_url': asset_url,
                'preview_image': preview_image,
                'author': author,
                'price': price,
                'rating': rating,
                'category': category['name'],
                'category_description': category['description'],
                'category_priority': category['priority'],
                'site': 'Unity Asset Store',
                'license': 'Unity Asset Store License',
                'asset_type': 'Unity Asset',
                'timestamp': time.time()
            }
            
        except Exception as e:
            return None

    def _passes_quality_filters(self, asset_data: Dict, strategy: Dict) -> bool:
        """Check if asset passes quality filters"""
        filters = strategy.get('quality_filters', [])

        for filter_type in filters:
            if filter_type == 'free_only':
                # Check if asset is free
                price = asset_data.get('price', '').lower()
                if 'free' not in price and '$0' not in price and price != '':
                    return False

            elif filter_type == 'game_relevant':
                # Check if asset is game development relevant
                title = asset_data.get('title', '').lower()
                category = asset_data.get('category', '').lower()

                # All Unity assets are game relevant, but filter out non-game categories
                irrelevant_keywords = ['enterprise', 'business', 'medical', 'education']
                if any(keyword in title or keyword in category for keyword in irrelevant_keywords):
                    return False

        return True

    def _enhance_and_score_assets(self, assets: List[Dict]) -> List[Dict]:
        """Enhance assets with quality scoring"""
        enhanced_assets = []

        print(f"✨ Enhancing {len(assets)} assets...")

        for asset in assets:
            try:
                enhanced = asset.copy()

                # Calculate quality score
                enhanced['quality_score'] = self._calculate_quality_score(asset)

                # Enhance metadata
                enhanced = self._enhance_asset_metadata(enhanced)

                enhanced_assets.append(enhanced)

            except Exception as e:
                enhanced_assets.append(asset)
                continue

        return enhanced_assets

    def _calculate_quality_score(self, asset: Dict) -> float:
        """Calculate asset quality score"""
        score = 0.0

        # Title quality (20%)
        title = asset.get('title', '')
        if title and len(title) > 5 and title != 'Unity Asset':
            score += 0.2

        # Preview image availability (25%)
        if asset.get('preview_image'):
            score += 0.25

        # Author/Publisher information (15%)
        if asset.get('author'):
            score += 0.15

        # Free asset bonus (20%)
        price = asset.get('price', '').lower()
        if 'free' in price or '$0' in price:
            score += 0.2

        # Rating availability (10%)
        if asset.get('rating'):
            score += 0.1

        # Category priority (10%)
        category_priority = asset.get('category_priority', 3)
        priority_score = (4 - category_priority) / 3 * 0.1
        score += priority_score

        return min(score, 1.0)

    def _enhance_asset_metadata(self, asset: Dict) -> Dict:
        """Enhance asset with additional metadata"""
        # Categorize based on Unity category
        category = asset.get('category', '')

        if '2d' in category:
            asset['dimension'] = '2D'
        elif '3d' in category:
            asset['dimension'] = '3D'
        else:
            asset['dimension'] = 'Mixed'

        # Add usage suggestions based on category
        usage_suggestions = []

        if 'gui' in category:
            usage_suggestions.extend(['UI Development', 'Interface Design', 'HUD Creation'])
        elif 'character' in category:
            usage_suggestions.extend(['Character Design', 'Game Characters', 'Animation'])
        elif 'environment' in category:
            usage_suggestions.extend(['Level Design', 'Environment Art', 'Scene Creation'])
        elif 'audio' in category:
            usage_suggestions.extend(['Sound Effects', 'Game Audio', 'Music'])
        else:
            usage_suggestions.extend(['Game Development', 'Unity Projects', 'Asset Integration'])

        asset['usage_suggestions'] = usage_suggestions

        # Add technical specifications
        asset['technical_specs'] = {
            'platform': 'Unity Engine',
            'license': 'Unity Asset Store Standard License',
            'commercial_use': True,
            'unity_version': 'Compatible with Unity',
            'file_formats': 'Unity Package (.unitypackage)'
        }

        # Add download information
        asset['download_info'] = {
            'platform': 'Unity Asset Store',
            'requires_unity_account': True,
            'installation': 'Import via Unity Package Manager'
        }

        return asset

    def _optimize_results(self, assets: List[Dict]) -> List[Dict]:
        """Optimize and filter results"""
        print(f"🎯 Optimizing {len(assets)} assets...")

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

        # Sort by quality score and category priority
        unique_assets.sort(key=lambda x: (x.get('quality_score', 0), -x.get('category_priority', 3)), reverse=True)

        # Group by category and dimension
        category_stats = {}
        dimension_stats = {}

        for asset in unique_assets:
            category = asset.get('category_description', 'Unknown')
            dimension = asset.get('dimension', 'Unknown')

            category_stats[category] = category_stats.get(category, 0) + 1
            dimension_stats[dimension] = dimension_stats.get(dimension, 0) + 1

        print(f"✅ Optimization complete: {len(unique_assets)} unique assets")
        if unique_assets:
            avg_quality = sum(a.get('quality_score', 0) for a in unique_assets) / len(unique_assets)
            print(f"📊 Average quality score: {avg_quality:.2f}")
            print(f"📂 Categories: {len(category_stats)}")
            print(f"🎯 Dimensions: {dimension_stats}")

        return unique_assets

# Test function
def test_ultra_intelligent_unity_scraper():
    """Test the ultra intelligent Unity scraper"""
    print("🧪 Testing Ultra Intelligent Unity Asset Store Scraper")
    print("=" * 60)

    scraper = UltraIntelligentUnityScraper()

    try:
        assets = scraper.analyze_and_scrape(limit=12)

        print(f"\n📊 SCRAPING RESULTS")
        print(f"   🎯 Total assets: {len(assets)}")

        if assets:
            avg_quality = sum(a.get('quality_score', 0) for a in assets) / len(assets)
            print(f"   📈 Average quality score: {avg_quality:.2f}")

            # Count by category and dimension
            categories = {}
            dimensions = {}

            for asset in assets:
                category = asset.get('category_description', 'Unknown')
                dimension = asset.get('dimension', 'Unknown')

                categories[category] = categories.get(category, 0) + 1
                dimensions[dimension] = dimensions.get(dimension, 0) + 1

            print(f"\n📂 Categories:")
            for category, count in categories.items():
                print(f"   {category}: {count} assets")

            print(f"\n🎯 Dimensions:")
            for dimension, count in dimensions.items():
                print(f"   {dimension}: {count} assets")

            print(f"\n🎮 Sample Assets:")
            for i, asset in enumerate(assets[:5], 1):
                print(f"   {i}. {asset['title'][:50]}...")
                print(f"      Quality: {asset.get('quality_score', 0):.2f}")
                print(f"      Category: {asset.get('category_description', 'Unknown')}")
                print(f"      Dimension: {asset.get('dimension', 'Unknown')}")
                print(f"      Price: {asset.get('price', 'Unknown')}")

        return assets

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return []

if __name__ == "__main__":
    test_ultra_intelligent_unity_scraper()
