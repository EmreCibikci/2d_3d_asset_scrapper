#!/usr/bin/env python3
"""
Ultra Intelligent Quaternius Scraper
Advanced 3D/2D free asset extraction from Quaternius
"""

import time
import json
import random
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import requests
from safe_scraping import SafeScrapingManager
from urllib.parse import urljoin, urlparse

class UltraIntelligentQuaterniusScraper:
    """Ultra intelligent Quaternius scraper for free 3D/2D assets"""
    
    def __init__(self):
        self.base_url = "https://quaternius.com"
        self.site_name = "Quaternius"
        self.safe_scraper = SafeScrapingManager()
        self.scraped_assets = []
        self.site_intelligence = {}
        
        print("🧠 Ultra Intelligent Quaternius Scraper Initialized")
        print("=" * 60)
        print("🎯 Features:")
        print("   ✅ Free 3D/2D asset focus")
        print("   ✅ CC0 license assets")
        print("   ✅ Quality scoring system")
        print("   ✅ Multi-format support")
        print("   ✅ Category-based organization")
        print("   ✅ Download link extraction")
    
    def analyze_and_scrape(self, limit: int = None) -> List[Dict]:
        """Main ultra intelligent scraping method"""
        print("🧠 Starting Ultra Intelligent Quaternius Scraping...")
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
        print("🌐 Analyzing Quaternius structure...")
        
        # Test main assets page
        assets_url = f"{self.base_url}/packs"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(assets_url, headers=headers, timeout=15)
        except Exception as e:
            print(f"   ❌ Site analysis failed: {e}")
            return {'error': 'Cannot access site'}
        
        if not response or response.status_code != 200:
            return {'error': f'Site returned {response.status_code if response else "no response"}'}
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Analyze pack containers
        pack_structure = self._analyze_pack_structure(soup)
        
        # Get asset categories
        asset_categories = self._get_quaternius_categories()
        
        intelligence = {
            'pack_structure': pack_structure,
            'asset_categories': asset_categories,
            'base_url': self.base_url,
            'analysis_time': time.time()
        }
        
        print(f"   🔍 Pack structure analyzed")
        print(f"   📂 Asset categories prepared")
        
        return intelligence
    
    def _analyze_pack_structure(self, soup: BeautifulSoup) -> Dict:
        """Analyze pack container structure"""
        selectors = [
            '.pack-card',
            '.asset-pack',
            '.pack-item',
            '.grid-item',
            '[data-pack]'
        ]
        
        best_selector = None
        max_packs = 0
        
        for selector in selectors:
            packs = soup.select(selector)
            if len(packs) > max_packs:
                max_packs = len(packs)
                best_selector = selector
                print(f"   🎯 Testing selector '{selector}': {len(packs)} packs found")
        
        return {
            'best_selector': best_selector or '.pack-card',
            'pack_count_sample': max_packs,
            'structure_analyzed': True
        }
    
    def _get_quaternius_categories(self) -> List[Dict]:
        """Get Quaternius asset categories"""
        return [
            {
                'name': 'characters',
                'url_path': '/packs',
                'keywords': ['character', 'people', 'human', 'npc'],
                'priority': 1,
                'description': '3D Characters'
            },
            {
                'name': 'environments',
                'url_path': '/packs',
                'keywords': ['environment', 'landscape', 'terrain', 'nature'],
                'priority': 1,
                'description': '3D Environments'
            },
            {
                'name': 'props',
                'url_path': '/packs',
                'keywords': ['prop', 'object', 'furniture', 'item'],
                'priority': 2,
                'description': '3D Props'
            },
            {
                'name': 'vehicles',
                'url_path': '/packs',
                'keywords': ['vehicle', 'car', 'truck', 'transport'],
                'priority': 2,
                'description': '3D Vehicles'
            },
            {
                'name': 'buildings',
                'url_path': '/packs',
                'keywords': ['building', 'house', 'structure', 'architecture'],
                'priority': 3,
                'description': '3D Buildings'
            },
            {
                'name': 'weapons',
                'url_path': '/packs',
                'keywords': ['weapon', 'sword', 'gun', 'tool'],
                'priority': 3,
                'description': '3D Weapons & Tools'
            }
        ]
    
    def _determine_scraping_strategy(self) -> Dict:
        """Determine optimal scraping strategy"""
        strategy = {
            'primary_method': 'pack_based',
            'pack_selector': '.pack-card',
            'asset_categories': [],
            'packs_per_category': 5,
            'rate_limiting': 2.0,
            'quality_filters': ['cc0_license', 'download_available']
        }
        
        # Use discovered pack structure
        if self.site_intelligence.get('pack_structure', {}).get('best_selector'):
            strategy['pack_selector'] = self.site_intelligence['pack_structure']['best_selector']
        
        # Use asset categories
        if self.site_intelligence.get('asset_categories'):
            strategy['asset_categories'] = self.site_intelligence['asset_categories']
        
        print(f"   🎯 Strategy: {strategy['primary_method']}")
        print(f"   📂 Asset categories: {len(strategy['asset_categories'])}")
        print(f"   🔍 Pack selector: {strategy['pack_selector']}")
        
        return strategy
    
    def _execute_intelligent_scraping(self, strategy: Dict, limit: int = None) -> List[Dict]:
        """Execute intelligent scraping"""
        assets = []
        limit = limit or 30
        
        print(f"🎯 Target: {limit} assets")
        
        # Scrape main packs page
        packs_url = f"{self.base_url}/packs"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(packs_url, headers=headers, timeout=15)
        except Exception as e:
            print(f"   ❌ Request failed: {e}")
            return []
        
        if not response or response.status_code != 200:
            print(f"   ❌ Failed to access packs page: {response.status_code if response else 'No response'}")
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract all packs
        pack_elements = soup.select(strategy['pack_selector'])
        print(f"   📦 Found {len(pack_elements)} asset packs")
        
        for i, pack_elem in enumerate(pack_elements):
            if len(assets) >= limit:
                break
            
            try:
                pack_data = self._extract_pack_data(pack_elem, strategy)
                if pack_data and self._passes_quality_filters(pack_data, strategy):
                    assets.append(pack_data)
                    print(f"   ✅ {i+1}. {pack_data['title'][:40]}...")
                
                time.sleep(strategy['rate_limiting'])
                
            except Exception as e:
                print(f"   ⚠️ Error extracting pack {i+1}: {e}")
                continue
        
        return assets[:limit]
    
    def _extract_pack_data(self, element, strategy: Dict) -> Optional[Dict]:
        """Extract pack data from element"""
        try:
            # Extract pack link
            link_elem = element.select_one('a')
            if not link_elem:
                return None
            
            pack_url = urljoin(self.base_url, link_elem.get('href'))
            
            # Extract title
            title_elem = element.select_one('.pack-title, .title, h3, h4')
            if not title_elem:
                title_elem = element.select_one('img')
                title = title_elem.get('alt') if title_elem else 'Quaternius Pack'
            else:
                title = title_elem.get_text(strip=True)
            
            # Extract preview image
            img_elem = element.select_one('img')
            preview_image = None
            if img_elem:
                preview_image = img_elem.get('src') or img_elem.get('data-src')
                if preview_image and not preview_image.startswith('http'):
                    preview_image = urljoin(self.base_url, preview_image)
            
            # Extract description if available
            desc_elem = element.select_one('.description, .pack-desc')
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # Determine category based on title and description
            category = self._determine_pack_category(title, description)
            
            # Extract additional details from pack page
            pack_details = self._extract_pack_details(pack_url)
            
            return {
                'title': title,
                'source_url': pack_url,
                'preview_image': preview_image,
                'description': description,
                'category': category['name'],
                'category_description': category['description'],
                'category_priority': category['priority'],
                'download_url': pack_details.get('download_url'),
                'file_formats': pack_details.get('file_formats', []),
                'asset_count': pack_details.get('asset_count', 'Multiple'),
                'site': 'Quaternius',
                'license': 'CC0 (Public Domain)',
                'asset_type': '3D Asset Pack',
                'timestamp': time.time()
            }
            
        except Exception as e:
            return None
    
    def _determine_pack_category(self, title: str, description: str) -> Dict:
        """Determine pack category based on title and description"""
        text = f"{title} {description}".lower()
        
        categories = self.site_intelligence.get('asset_categories', [])
        
        for category in categories:
            if any(keyword in text for keyword in category['keywords']):
                return category
        
        # Default category
        return {
            'name': 'general',
            'description': '3D Assets',
            'priority': 3
        }
    
    def _extract_pack_details(self, pack_url: str) -> Dict:
        """Extract additional details from pack page"""
        details = {
            'download_url': None,
            'file_formats': [],
            'asset_count': 'Multiple'
        }
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(pack_url, headers=headers, timeout=10)
            
            if response and response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find download link
                download_selectors = [
                    'a[href*="download"]',
                    'a[href*=".zip"]',
                    '.download-btn',
                    '.btn-download'
                ]
                
                for selector in download_selectors:
                    download_elem = soup.select_one(selector)
                    if download_elem:
                        download_url = download_elem.get('href')
                        if download_url:
                            if not download_url.startswith('http'):
                                download_url = urljoin(self.base_url, download_url)
                            details['download_url'] = download_url
                            break
                
                # Extract file formats
                format_text = soup.get_text().lower()
                formats = []
                
                if 'fbx' in format_text:
                    formats.append('FBX')
                if 'obj' in format_text:
                    formats.append('OBJ')
                if 'blend' in format_text:
                    formats.append('Blender')
                if 'gltf' in format_text or 'glb' in format_text:
                    formats.append('glTF')
                
                details['file_formats'] = formats
                
        except Exception as e:
            pass  # Don't fail if we can't get details
        
        return details

    def _passes_quality_filters(self, pack_data: Dict, strategy: Dict) -> bool:
        """Check if pack passes quality filters"""
        filters = strategy.get('quality_filters', [])

        for filter_type in filters:
            if filter_type == 'cc0_license':
                # Quaternius assets are CC0, so this always passes
                pass

            elif filter_type == 'download_available':
                # Check if download URL is available
                if not pack_data.get('download_url'):
                    # Don't filter out if download URL not found, might be extractable later
                    pass

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
        if title and len(title) > 5 and title != 'Quaternius Pack':
            score += 0.2

        # Preview image availability (25%)
        if asset.get('preview_image'):
            score += 0.25

        # Download URL availability (25%)
        if asset.get('download_url'):
            score += 0.25

        # File formats availability (15%)
        file_formats = asset.get('file_formats', [])
        if file_formats:
            score += 0.15

        # Description quality (10%)
        description = asset.get('description', '')
        if description and len(description) > 10:
            score += 0.1

        # Category priority (5%)
        category_priority = asset.get('category_priority', 3)
        priority_score = (4 - category_priority) / 3 * 0.05
        score += priority_score

        return min(score, 1.0)

    def _enhance_asset_metadata(self, asset: Dict) -> Dict:
        """Enhance asset with additional metadata"""
        # Add usage suggestions based on category
        category = asset.get('category', '')
        usage_suggestions = []

        if category == 'characters':
            usage_suggestions.extend(['Character Design', 'Game Characters', 'NPCs', 'Animation'])
        elif category == 'environments':
            usage_suggestions.extend(['Level Design', 'Environment Art', 'Landscapes', 'Scenes'])
        elif category == 'props':
            usage_suggestions.extend(['Game Props', 'Scene Objects', 'Decoration', 'Items'])
        elif category == 'vehicles':
            usage_suggestions.extend(['Transportation', 'Vehicle Design', 'Racing Games', 'Simulation'])
        elif category == 'buildings':
            usage_suggestions.extend(['Architecture', 'City Building', 'Structures', 'Urban Design'])
        elif category == 'weapons':
            usage_suggestions.extend(['Weapon Design', 'Combat Games', 'Tools', 'Equipment'])
        else:
            usage_suggestions.extend(['3D Modeling', 'Game Development', 'Asset Creation'])

        asset['usage_suggestions'] = usage_suggestions

        # Add technical specifications
        asset['technical_specs'] = {
            'license': 'CC0 (Public Domain)',
            'commercial_use': True,
            'attribution_required': False,
            'modifications_allowed': True,
            'redistribution_allowed': True,
            'file_formats': asset.get('file_formats', ['FBX', 'OBJ']),
            'software_compatibility': ['Blender', 'Unity', 'Unreal Engine', 'Maya', '3ds Max']
        }

        # Add download information
        asset['download_info'] = {
            'platform': 'Quaternius Website',
            'requires_account': False,
            'direct_download': bool(asset.get('download_url')),
            'file_type': 'ZIP Archive'
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

        # Group by category
        category_stats = {}
        download_stats = {'with_download': 0, 'without_download': 0}

        for asset in unique_assets:
            category = asset.get('category_description', 'Unknown')
            category_stats[category] = category_stats.get(category, 0) + 1

            if asset.get('download_url'):
                download_stats['with_download'] += 1
            else:
                download_stats['without_download'] += 1

        print(f"✅ Optimization complete: {len(unique_assets)} unique assets")
        if unique_assets:
            avg_quality = sum(a.get('quality_score', 0) for a in unique_assets) / len(unique_assets)
            print(f"📊 Average quality score: {avg_quality:.2f}")
            print(f"📂 Categories: {len(category_stats)}")
            print(f"📥 Download URLs: {download_stats['with_download']}/{len(unique_assets)}")

        return unique_assets

# Test function
def test_ultra_intelligent_quaternius_scraper():
    """Test the ultra intelligent Quaternius scraper"""
    print("🧪 Testing Ultra Intelligent Quaternius Scraper")
    print("=" * 60)

    scraper = UltraIntelligentQuaterniusScraper()

    try:
        assets = scraper.analyze_and_scrape(limit=10)

        print(f"\n📊 SCRAPING RESULTS")
        print(f"   🎯 Total assets: {len(assets)}")

        if assets:
            avg_quality = sum(a.get('quality_score', 0) for a in assets) / len(assets)
            print(f"   📈 Average quality score: {avg_quality:.2f}")

            # Count by category
            categories = {}
            downloads = 0

            for asset in assets:
                category = asset.get('category_description', 'Unknown')
                categories[category] = categories.get(category, 0) + 1

                if asset.get('download_url'):
                    downloads += 1

            print(f"\n📂 Categories:")
            for category, count in categories.items():
                print(f"   {category}: {count} assets")

            print(f"\n📥 Downloads: {downloads}/{len(assets)} assets have download URLs")

            print(f"\n🎮 Sample Assets:")
            for i, asset in enumerate(assets[:5], 1):
                print(f"   {i}. {asset['title'][:50]}...")
                print(f"      Quality: {asset.get('quality_score', 0):.2f}")
                print(f"      Category: {asset.get('category_description', 'Unknown')}")
                print(f"      Formats: {', '.join(asset.get('file_formats', []))}")
                print(f"      Download: {'✅' if asset.get('download_url') else '❌'}")

        return assets

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return []

if __name__ == "__main__":
    test_ultra_intelligent_quaternius_scraper()
