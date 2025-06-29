#!/usr/bin/env python3
"""
Ultra Intelligent OpenGameArt Scraper
Advanced browser-based intelligent scraping with comprehensive asset extraction
"""

import time
import json
import random
from typing import Dict, List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import requests
from safe_scraping import SafeScrapingManager

class UltraIntelligentOpenGameArtScraper:
    """Ultra intelligent OpenGameArt scraper with browser-based analysis"""
    
    def __init__(self):
        self.base_url = "https://opengameart.org"
        self.site_name = "OpenGameArt"
        self.driver = None
        self.safe_scraper = SafeScrapingManager()
        self.site_intelligence = {}
        self.scraped_assets = []
        
        print("🧠 Ultra Intelligent OpenGameArt Scraper Initialized")
        print("=" * 60)
        print("🎯 Features:")
        print("   ✅ Browser-based intelligent analysis")
        print("   ✅ Multi-category asset extraction")
        print("   ✅ License information parsing")
        print("   ✅ Download link extraction")
        print("   ✅ Quality scoring system")
        print("   ✅ Advanced filtering capabilities")
    
    def _setup_browser(self) -> bool:
        """Setup Chrome browser with anti-detection"""
        print("🌐 Setting up intelligent browser...")
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("✅ Browser setup successful")
            return True
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return False
    
    def analyze_and_scrape(self, limit: int = None) -> List[Dict]:
        """Main ultra intelligent scraping method"""
        print("🧠 Starting Ultra Intelligent OpenGameArt Scraping...")
        print("=" * 60)
        
        # Phase 1: Site Intelligence Analysis
        print("🔍 Phase 1: Ultra Intelligent Site Analysis")
        self.site_intelligence = self._perform_site_analysis()
        
        # Phase 2: Category-Based Strategy
        print("🎯 Phase 2: Category-Based Scraping Strategy")
        strategy = self._determine_scraping_strategy()
        
        # Phase 3: Multi-Category Asset Extraction
        print("📦 Phase 3: Multi-Category Asset Extraction")
        assets = self._execute_intelligent_scraping(strategy, limit)
        
        # Phase 4: License & Quality Enhancement
        print("✨ Phase 4: License & Quality Enhancement")
        enhanced_assets = self._enhance_and_score_assets(assets)
        
        # Phase 5: Results Optimization
        print("🎯 Phase 5: Results Optimization")
        optimized_assets = self._optimize_results(enhanced_assets)
        
        return optimized_assets
    
    def _perform_site_analysis(self) -> Dict:
        """Perform ultra intelligent site analysis"""
        if not self._setup_browser():
            return self._fallback_analysis()
        
        try:
            print("🌐 Loading OpenGameArt homepage...")
            self.driver.get(f"{self.base_url}/art-search")
            time.sleep(3)
            
            # Analyze page structure
            structure = self._analyze_page_structure()
            
            # Analyze asset containers
            asset_containers = self._analyze_asset_containers()
            
            # Analyze categories
            categories = self._analyze_categories()
            
            # Analyze search functionality
            search_analysis = self._analyze_search_functionality()
            
            # Analyze pagination
            pagination = self._analyze_pagination()
            
            intelligence = {
                'structure': structure,
                'asset_containers': asset_containers,
                'categories': categories,
                'search': search_analysis,
                'pagination': pagination,
                'timestamp': time.time()
            }
            
            print("✅ Site analysis completed")
            return intelligence
            
        except Exception as e:
            print(f"❌ Browser analysis failed: {e}")
            return self._fallback_analysis()
        finally:
            if self.driver:
                self.driver.quit()
    
    def _analyze_page_structure(self) -> Dict:
        """Analyze page structure"""
        structure = {
            'title': self.driver.title,
            'url': self.driver.current_url,
            'page_type': 'art_search'
        }
        
        # Find main content areas
        try:
            main_content = self.driver.find_element(By.CSS_SELECTOR, "main, .main-content, .art-preview")
            structure['main_content_found'] = True
            structure['main_selector'] = "main, .main-content, .art-preview"
        except:
            structure['main_content_found'] = False
        
        return structure
    
    def _analyze_asset_containers(self) -> List[Dict]:
        """Analyze asset containers and patterns"""
        containers = []
        
        # Common OpenGameArt asset container selectors
        selectors = [
            ".art-preview",
            ".art-preview-container",
            ".views-row",
            ".node-art",
            ".art-item",
            "[class*='art-preview']"
        ]
        
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    # Analyze first few elements
                    sample_data = []
                    for elem in elements[:3]:
                        try:
                            title_elem = elem.find_element(By.CSS_SELECTOR, ".art-preview-title a, h3 a, .title a")
                            title = title_elem.text.strip() if title_elem else "No title"
                            
                            link = title_elem.get_attribute('href') if title_elem else "No link"
                            
                            sample_data.append({
                                'title': title,
                                'link': link
                            })
                        except:
                            continue
                    
                    containers.append({
                        'selector': selector,
                        'count': len(elements),
                        'confidence': len(sample_data) / max(len(elements[:3]), 1),
                        'sample_data': sample_data
                    })
                    
                    print(f"   🎯 Found {len(elements)} assets with selector: {selector}")
                    
            except Exception as e:
                continue
        
        return containers
    
    def _analyze_categories(self) -> List[Dict]:
        """Analyze available categories"""
        categories = []
        
        try:
            # Find category filters
            category_selectors = [
                ".form-item-category select option",
                ".category-filter option",
                ".art-category a",
                ".taxonomy-term a"
            ]
            
            for selector in category_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for elem in elements:
                        text = elem.text.strip()
                        value = elem.get_attribute('value') if elem.tag_name == 'option' else elem.get_attribute('href')
                        
                        if text and text != "- Any -":
                            categories.append({
                                'name': text,
                                'value': value,
                                'selector': selector
                            })
                            
                    if categories:
                        break  # Found categories, no need to check other selectors
                        
                except:
                    continue
                    
        except Exception as e:
            print(f"⚠️ Category analysis error: {e}")
        
        print(f"   📂 Found {len(categories)} categories")
        return categories
    
    def _analyze_search_functionality(self) -> Dict:
        """Analyze search functionality"""
        search_info = {
            'search_form_found': False,
            'search_input_selector': None,
            'advanced_filters': []
        }
        
        try:
            # Find search form
            search_selectors = [
                "input[name='title']",
                "input[name='search']",
                "#edit-title",
                ".form-text"
            ]
            
            for selector in search_selectors:
                try:
                    search_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if search_input.is_displayed():
                        search_info['search_form_found'] = True
                        search_info['search_input_selector'] = selector
                        print(f"   🔍 Search input found: {selector}")
                        break
                except:
                    continue
            
            # Find advanced filters
            filter_selectors = [
                "select[name='category']",
                "select[name='licenses']",
                "select[name='field_art_type_value']"
            ]
            
            for selector in filter_selectors:
                try:
                    filter_elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if filter_elem.is_displayed():
                        search_info['advanced_filters'].append(selector)
                except:
                    continue
                    
        except Exception as e:
            print(f"⚠️ Search analysis error: {e}")
        
        return search_info
    
    def _analyze_pagination(self) -> Dict:
        """Analyze pagination system"""
        pagination = {
            'pagination_found': False,
            'next_button_selector': None,
            'page_numbers': []
        }
        
        try:
            # Check for pagination
            pagination_selectors = [
                ".pager-next a",
                ".pagination .next",
                ".pager .pager-next",
                "[title='Go to next page']"
            ]
            
            for selector in pagination_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        pagination['pagination_found'] = True
                        pagination['next_button_selector'] = selector
                        print(f"   📄 Pagination found: {selector}")
                        break
                except:
                    continue
                    
        except Exception as e:
            print(f"⚠️ Pagination analysis error: {e}")
        
        return pagination
    
    def _fallback_analysis(self) -> Dict:
        """Fallback analysis without browser"""
        print("🔄 Using fallback analysis method...")
        
        response = self.safe_scraper.safe_get(f"{self.base_url}/art-search")
        if not response:
            return {}
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        return {
            'structure': {'fallback': True},
            'asset_containers': [
                {
                    'selector': '.art-preview',
                    'count': len(soup.select('.art-preview')),
                    'confidence': 0.8
                }
            ],
            'categories': [],
            'search': {'search_form_found': False},
            'pagination': {'pagination_found': False}
        }

    def _determine_scraping_strategy(self) -> Dict:
        """Determine optimal scraping strategy"""
        strategy = {
            'primary_method': 'category_based',
            'fallback_methods': ['search_based', 'requests_based'],
            'asset_selector': '.art-preview',
            'pagination_method': 'click_next',
            'rate_limiting': 2.0,
            'max_pages': 20,
            'categories_to_scrape': [
                '2D Art', 'Sprites', 'Textures', 'UI Elements',
                'Icons', 'Backgrounds', 'Concept Art'
            ]
        }

        # Choose best asset container
        if self.site_intelligence.get('asset_containers'):
            best_container = max(
                self.site_intelligence['asset_containers'],
                key=lambda x: x['confidence']
            )
            strategy['asset_selector'] = best_container['selector']
            print(f"   🎯 Selected asset container: {best_container['selector']}")

        # Use available categories
        if self.site_intelligence.get('categories'):
            available_categories = [cat['name'] for cat in self.site_intelligence['categories']]
            strategy['available_categories'] = available_categories
            print(f"   📂 Available categories: {len(available_categories)}")

        return strategy

    def _execute_intelligent_scraping(self, strategy: Dict, limit: int = None) -> List[Dict]:
        """Execute intelligent scraping with multiple strategies"""
        assets = []
        limit = limit or 100

        print(f"🎯 Target: {limit} assets")

        # Strategy 1: Category-based scraping
        if strategy['primary_method'] == 'category_based':
            category_assets = self._category_based_scraping(strategy, limit)
            assets.extend(category_assets)
            print(f"   📂 Category method: {len(category_assets)} assets")

        # Strategy 2: Search-based scraping
        if len(assets) < limit and 'search_based' in strategy['fallback_methods']:
            search_assets = self._search_based_scraping(strategy, limit - len(assets))
            assets.extend(search_assets)
            print(f"   🔍 Search method: {len(search_assets)} assets")

        # Strategy 3: General browsing
        if len(assets) < limit and 'requests_based' in strategy['fallback_methods']:
            browse_assets = self._general_browsing_scraping(limit - len(assets))
            assets.extend(browse_assets)
            print(f"   🌐 Browse method: {len(browse_assets)} assets")

        return assets[:limit]

    def _category_based_scraping(self, strategy: Dict, limit: int) -> List[Dict]:
        """Category-based intelligent scraping"""
        assets = []
        categories = strategy.get('categories_to_scrape', ['2D Art', 'Sprites'])

        print(f"📂 Scraping categories: {categories}")

        for category in categories:
            if len(assets) >= limit:
                break

            try:
                category_assets = self._scrape_category(category, strategy)
                assets.extend(category_assets)
                print(f"   📂 {category}: {len(category_assets)} assets")
                time.sleep(strategy.get('rate_limiting', 2.0))

            except Exception as e:
                print(f"⚠️ Error scraping category {category}: {e}")
                continue

        return assets

    def _scrape_category(self, category: str, strategy: Dict) -> List[Dict]:
        """Scrape assets from a specific category"""
        assets = []

        try:
            # Build category URL
            category_url = f"{self.base_url}/art-search?category={category.replace(' ', '+')}"
            response = self.safe_scraper.safe_get(category_url)

            if not response:
                return []

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract assets from page
            asset_elements = soup.select(strategy['asset_selector'])

            for elem in asset_elements:
                try:
                    asset_data = self._extract_asset_data_from_soup(elem)
                    if asset_data:
                        asset_data['category'] = category
                        assets.append(asset_data)
                except Exception as e:
                    continue

            # Handle pagination for this category
            page = 1
            max_pages = min(strategy.get('max_pages', 5), 5)  # Limit per category

            while len(assets) < 50 and page < max_pages:  # Max 50 per category
                page += 1
                page_url = f"{category_url}&page={page}"

                response = self.safe_scraper.safe_get(page_url)
                if not response:
                    break

                soup = BeautifulSoup(response.content, 'html.parser')
                page_elements = soup.select(strategy['asset_selector'])

                if not page_elements:
                    break

                for elem in page_elements:
                    try:
                        asset_data = self._extract_asset_data_from_soup(elem)
                        if asset_data:
                            asset_data['category'] = category
                            assets.append(asset_data)
                    except:
                        continue

                time.sleep(1)

        except Exception as e:
            print(f"❌ Category scraping error: {e}")

        return assets

    def _extract_asset_data_from_soup(self, element) -> Optional[Dict]:
        """Extract asset data from BeautifulSoup element"""
        try:
            # Extract title and link
            title_elem = element.select_one('.art-preview-title a, h3 a, .title a')
            if not title_elem:
                return None

            title = title_elem.get_text(strip=True)
            link = title_elem.get('href')

            if link and not link.startswith('http'):
                link = f"{self.base_url}{link}"

            # Extract preview image
            img_elem = element.select_one('img')
            preview_image = img_elem.get('src') if img_elem else None
            if preview_image and not preview_image.startswith('http'):
                preview_image = f"{self.base_url}{preview_image}"

            # Extract author
            author_elem = element.select_one('.art-preview-author, .username, .author')
            author = author_elem.get_text(strip=True) if author_elem else ""

            # Extract description/summary
            desc_elem = element.select_one('.art-preview-description, .description, .summary')
            description = desc_elem.get_text(strip=True) if desc_elem else ""

            # Extract license info
            license_elem = element.select_one('.license, .art-license')
            license_info = license_elem.get_text(strip=True) if license_elem else ""

            # Extract tags
            tag_elements = element.select('.art-tags a, .tags a')
            tags = [tag.get_text(strip=True) for tag in tag_elements]

            return {
                'title': title,
                'source_url': link,
                'preview_image': preview_image,
                'description': description,
                'author': author,
                'license': license_info,
                'tags': tags,
                'site': 'OpenGameArt',
                'file_type': 'asset',
                'timestamp': time.time()
            }

        except Exception as e:
            return None

    def _search_based_scraping(self, strategy: Dict, limit: int) -> List[Dict]:
        """Search-based scraping for specific terms"""
        assets = []
        search_terms = ['2d', 'sprite', 'texture', 'icon', 'ui', 'background']

        print(f"🔍 Starting search-based scraping...")

        for term in search_terms:
            if len(assets) >= limit:
                break

            try:
                search_url = f"{self.base_url}/art-search?title={term}"
                response = self.safe_scraper.safe_get(search_url)

                if response:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    search_assets = self._extract_assets_from_soup(soup, strategy)
                    assets.extend(search_assets)

                    print(f"   🔍 '{term}': {len(search_assets)} assets")
                    time.sleep(2)

            except Exception as e:
                print(f"⚠️ Search error for '{term}': {e}")
                continue

        return assets[:limit]

    def _general_browsing_scraping(self, limit: int) -> List[Dict]:
        """General browsing scraping"""
        assets = []

        try:
            print("🌐 Starting general browsing scraping...")

            for page in range(0, 10):  # Browse first 10 pages
                if len(assets) >= limit:
                    break

                url = f"{self.base_url}/art-search?page={page}"
                response = self.safe_scraper.safe_get(url)

                if not response:
                    continue

                soup = BeautifulSoup(response.content, 'html.parser')
                page_assets = self._extract_assets_from_soup(soup, {'asset_selector': '.art-preview'})
                assets.extend(page_assets)

                print(f"   📄 Page {page}: {len(page_assets)} assets")
                time.sleep(2)

        except Exception as e:
            print(f"❌ General browsing error: {e}")

        return assets[:limit]

    def _extract_assets_from_soup(self, soup: BeautifulSoup, strategy: Dict) -> List[Dict]:
        """Extract assets from BeautifulSoup"""
        assets = []

        asset_elements = soup.select(strategy.get('asset_selector', '.art-preview'))

        for elem in asset_elements:
            try:
                asset_data = self._extract_asset_data_from_soup(elem)
                if asset_data:
                    assets.append(asset_data)
            except Exception as e:
                continue

        return assets

    def _enhance_and_score_assets(self, assets: List[Dict]) -> List[Dict]:
        """Enhance assets with additional data and quality scoring"""
        enhanced_assets = []

        print(f"✨ Enhancing {len(assets)} assets...")

        for asset in assets:
            try:
                enhanced = asset.copy()

                # Calculate quality score
                enhanced['quality_score'] = self._calculate_quality_score(asset)

                # Enhance with additional metadata
                enhanced = self._enhance_asset_metadata(enhanced)

                # Extract download information
                enhanced = self._extract_download_info(enhanced)

                enhanced_assets.append(enhanced)

            except Exception as e:
                enhanced_assets.append(asset)
                continue

        return enhanced_assets

    def _calculate_quality_score(self, asset: Dict) -> float:
        """Calculate asset quality score"""
        score = 0.0

        # Title quality (25%)
        if asset.get('title') and len(asset['title']) > 5:
            score += 0.25

        # Description quality (20%)
        if asset.get('description') and len(asset['description']) > 20:
            score += 0.2

        # Preview image (20%)
        if asset.get('preview_image'):
            score += 0.2

        # License information (15%)
        if asset.get('license'):
            score += 0.15

        # Author information (10%)
        if asset.get('author'):
            score += 0.1

        # Tags (10%)
        if asset.get('tags') and len(asset['tags']) > 0:
            score += 0.1

        return min(score, 1.0)

    def _enhance_asset_metadata(self, asset: Dict) -> Dict:
        """Enhance asset with additional metadata"""
        # Categorize based on title/description/tags
        title_lower = asset.get('title', '').lower()
        desc_lower = asset.get('description', '').lower()
        tags_lower = ' '.join(asset.get('tags', [])).lower()

        combined_text = f"{title_lower} {desc_lower} {tags_lower}"

        # Determine asset type
        if any(term in combined_text for term in ['sprite', 'character', 'animation']):
            asset['asset_type'] = 'Sprite/Character'
        elif any(term in combined_text for term in ['texture', 'material', 'surface']):
            asset['asset_type'] = 'Texture'
        elif any(term in combined_text for term in ['icon', 'ui', 'button', 'interface']):
            asset['asset_type'] = 'UI Element'
        elif any(term in combined_text for term in ['background', 'environment', 'landscape']):
            asset['asset_type'] = 'Background'
        elif any(term in combined_text for term in ['sound', 'music', 'audio']):
            asset['asset_type'] = 'Audio'
        else:
            asset['asset_type'] = '2D Asset'

        # Add platform info
        asset['platform'] = 'OpenGameArt'
        asset['open_source'] = True

        return asset

    def _extract_download_info(self, asset: Dict) -> Dict:
        """Extract download information from asset page"""
        if not asset.get('source_url'):
            return asset

        try:
            # Visit asset page to get download links
            response = self.safe_scraper.safe_get(asset['source_url'])
            if response:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find download links
                download_links = []
                download_selectors = [
                    '.file a[href*="download"]',
                    '.attachment a',
                    '.field-name-field-art-files a'
                ]

                for selector in download_selectors:
                    links = soup.select(selector)
                    for link in links:
                        href = link.get('href')
                        if href:
                            if not href.startswith('http'):
                                href = f"{self.base_url}{href}"
                            download_links.append({
                                'url': href,
                                'text': link.get_text(strip=True)
                            })

                if download_links:
                    asset['download_links'] = download_links
                    asset['download_available'] = True

                # Extract file size info
                size_elem = soup.select_one('.file-size, .filesize')
                if size_elem:
                    asset['file_size'] = size_elem.get_text(strip=True)

        except Exception as e:
            pass  # Don't fail if we can't get download info

        return asset

    def _optimize_results(self, assets: List[Dict]) -> List[Dict]:
        """Optimize and filter results"""
        print(f"🎯 Optimizing {len(assets)} assets...")

        # Remove duplicates based on title and URL
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

        print(f"✅ Optimization complete: {len(unique_assets)} unique assets")
        if unique_assets:
            avg_quality = sum(a.get('quality_score', 0) for a in unique_assets) / len(unique_assets)
            print(f"📊 Average quality score: {avg_quality:.2f}")

        return unique_assets

# Test function
def test_ultra_intelligent_opengameart_scraper():
    """Test the ultra intelligent OpenGameArt scraper"""
    print("🧪 Testing Ultra Intelligent OpenGameArt Scraper")
    print("=" * 60)

    scraper = UltraIntelligentOpenGameArtScraper()

    try:
        # Test with small limit
        assets = scraper.analyze_and_scrape(limit=15)

        print(f"\n📊 SCRAPING RESULTS")
        print(f"   🎯 Total assets: {len(assets)}")

        if assets:
            avg_quality = sum(a.get('quality_score', 0) for a in assets) / len(assets)
            print(f"   📈 Average quality score: {avg_quality:.2f}")

            # Count by asset type
            asset_types = {}
            for asset in assets:
                asset_type = asset.get('asset_type', 'Unknown')
                asset_types[asset_type] = asset_types.get(asset_type, 0) + 1

            print(f"\n📂 Asset Types:")
            for asset_type, count in asset_types.items():
                print(f"   {asset_type}: {count}")

            print(f"\n🎨 Sample Assets:")
            for i, asset in enumerate(assets[:5], 1):
                print(f"   {i}. {asset['title'][:50]}...")
                print(f"      Quality: {asset.get('quality_score', 0):.2f}")
                print(f"      Type: {asset.get('asset_type', 'Unknown')}")
                print(f"      License: {asset.get('license', 'Unknown')}")

        return assets

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return []

if __name__ == "__main__":
    test_ultra_intelligent_opengameart_scraper()
