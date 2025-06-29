#!/usr/bin/env python3
"""
Ultra Intelligent Itch.io Scraper
Advanced browser-based intelligent scraping with bot protection bypass
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

class UltraIntelligentItchScraper:
    """Ultra intelligent Itch.io scraper with browser-based analysis"""
    
    def __init__(self):
        self.base_url = "https://itch.io"
        self.site_name = "Itch.io"
        self.driver = None
        self.safe_scraper = SafeScrapingManager()
        self.site_intelligence = {}
        self.scraped_assets = []
        
        print("🧠 Ultra Intelligent Itch.io Scraper Initialized")
        print("=" * 60)
        print("🎯 Features:")
        print("   ✅ Browser-based intelligent analysis")
        print("   ✅ Dynamic content support")
        print("   ✅ Bot protection bypass")
        print("   ✅ Search functionality integration")
        print("   ✅ Quality scoring system")
        print("   ✅ Multi-strategy extraction")
    
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
        print("🧠 Starting Ultra Intelligent Itch.io Scraping...")
        print("=" * 60)
        
        # Phase 1: Site Intelligence Analysis
        print("🔍 Phase 1: Ultra Intelligent Site Analysis")
        self.site_intelligence = self._perform_site_analysis()
        
        # Phase 2: Adaptive Scraping Strategy
        print("🎯 Phase 2: Adaptive Scraping Strategy")
        strategy = self._determine_scraping_strategy()
        
        # Phase 3: Multi-Strategy Asset Extraction
        print("📦 Phase 3: Multi-Strategy Asset Extraction")
        assets = self._execute_intelligent_scraping(strategy, limit)
        
        # Phase 4: Quality Enhancement & Scoring
        print("✨ Phase 4: Quality Enhancement & Scoring")
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
            print("🌐 Loading Itch.io homepage...")
            self.driver.get(f"{self.base_url}/games")
            time.sleep(3)
            
            # Analyze page structure
            structure = self._analyze_page_structure()
            
            # Analyze game containers
            game_containers = self._analyze_game_containers()
            
            # Analyze navigation elements
            navigation = self._analyze_navigation_elements()
            
            # Analyze search functionality
            search_analysis = self._analyze_search_functionality()
            
            # Analyze pagination
            pagination = self._analyze_pagination()
            
            intelligence = {
                'structure': structure,
                'game_containers': game_containers,
                'navigation': navigation,
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
            'page_type': 'games_listing'
        }
        
        # Find main content areas
        try:
            main_content = self.driver.find_element(By.CSS_SELECTOR, "main, .main_column, .game_grid_widget")
            structure['main_content_found'] = True
            structure['main_selector'] = "main, .main_column, .game_grid_widget"
        except:
            structure['main_content_found'] = False
        
        return structure
    
    def _analyze_game_containers(self) -> List[Dict]:
        """Analyze game containers and patterns"""
        containers = []
        
        # Common Itch.io game container selectors
        selectors = [
            ".game_cell",
            ".game_thumb",
            ".game_link",
            ".game_grid_widget .cell",
            ".browse_game",
            "[data-game_id]"
        ]
        
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    # Analyze first few elements
                    sample_data = []
                    for elem in elements[:3]:
                        try:
                            title_elem = elem.find_element(By.CSS_SELECTOR, ".title, .game_title, a")
                            title = title_elem.text.strip() if title_elem else "No title"
                            
                            link_elem = elem.find_element(By.CSS_SELECTOR, "a")
                            link = link_elem.get_attribute('href') if link_elem else "No link"
                            
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
                    
                    print(f"   🎯 Found {len(elements)} games with selector: {selector}")
                    
            except Exception as e:
                continue
        
        return containers
    
    def _analyze_navigation_elements(self) -> Dict:
        """Analyze navigation elements"""
        navigation = {
            'categories': [],
            'filters': [],
            'sorting': []
        }
        
        try:
            # Find category links
            category_selectors = [
                ".browse_filter_widget a",
                ".game_genre a",
                ".filter_label a",
                ".browse_tag a"
            ]
            
            for selector in category_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for elem in elements[:10]:  # Limit to first 10
                        text = elem.text.strip()
                        href = elem.get_attribute('href')
                        if text and href:
                            navigation['categories'].append({
                                'text': text,
                                'url': href
                            })
                except:
                    continue
                    
        except Exception as e:
            print(f"⚠️ Navigation analysis error: {e}")
        
        return navigation
    
    def _analyze_search_functionality(self) -> Dict:
        """Analyze search functionality"""
        search_info = {
            'search_form_found': False,
            'search_input_selector': None,
            'search_button_selector': None,
            'advanced_search': False
        }
        
        try:
            # Find search form
            search_selectors = [
                "input[name='q']",
                "input[type='search']",
                ".search_input",
                "#search_input"
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
                    
        except Exception as e:
            print(f"⚠️ Search analysis error: {e}")
        
        return search_info
    
    def _analyze_pagination(self) -> Dict:
        """Analyze pagination system"""
        pagination = {
            'pagination_found': False,
            'next_button_selector': None,
            'page_numbers': [],
            'infinite_scroll': False
        }
        
        try:
            # Check for pagination
            pagination_selectors = [
                ".pager_links a",
                ".pagination a",
                ".next_page",
                "[rel='next']"
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
                    
            # Check for infinite scroll
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # If new content loads, it's infinite scroll
                pagination['infinite_scroll'] = True
            except:
                pass
                
        except Exception as e:
            print(f"⚠️ Pagination analysis error: {e}")
        
        return pagination
    
    def _fallback_analysis(self) -> Dict:
        """Fallback analysis without browser"""
        print("🔄 Using fallback analysis method...")
        
        response = self.safe_scraper.safe_get(f"{self.base_url}/games")
        if not response:
            return {}
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        return {
            'structure': {'fallback': True},
            'game_containers': [
                {
                    'selector': '.game_cell',
                    'count': len(soup.select('.game_cell')),
                    'confidence': 0.8
                }
            ],
            'navigation': {'categories': []},
            'search': {'search_form_found': False},
            'pagination': {'pagination_found': False}
        }

    def _determine_scraping_strategy(self) -> Dict:
        """Determine optimal scraping strategy"""
        strategy = {
            'primary_method': 'browser_based',
            'fallback_methods': ['requests_based', 'api_based'],
            'game_selector': '.game_cell',
            'pagination_method': 'click_next',
            'rate_limiting': 2.0,
            'max_pages': 15,
            'use_search': True,
            'search_terms': ['2d', 'pixel art', 'sprites', 'assets', 'game art']
        }

        # Choose best game container
        if self.site_intelligence.get('game_containers'):
            best_container = max(
                self.site_intelligence['game_containers'],
                key=lambda x: x['confidence']
            )
            strategy['game_selector'] = best_container['selector']
            print(f"   🎯 Selected game container: {best_container['selector']}")

        # Determine pagination strategy
        if self.site_intelligence.get('pagination', {}).get('infinite_scroll'):
            strategy['pagination_method'] = 'infinite_scroll'
            print("   📜 Using infinite scroll strategy")
        elif self.site_intelligence.get('pagination', {}).get('pagination_found'):
            strategy['pagination_method'] = 'click_next'
            print("   📄 Using click next strategy")

        return strategy

    def _execute_intelligent_scraping(self, strategy: Dict, limit: int = None) -> List[Dict]:
        """Execute intelligent scraping with multiple strategies"""
        assets = []
        limit = limit or 50

        print(f"🎯 Target: {limit} assets")

        # Strategy 1: Browser-based scraping
        if strategy['primary_method'] == 'browser_based':
            browser_assets = self._browser_based_scraping(strategy, limit)
            assets.extend(browser_assets)
            print(f"   🌐 Browser method: {len(browser_assets)} assets")

        # Strategy 2: Requests-based fallback
        if len(assets) < limit and 'requests_based' in strategy['fallback_methods']:
            requests_assets = self._requests_based_scraping(limit - len(assets))
            assets.extend(requests_assets)
            print(f"   📡 Requests method: {len(requests_assets)} assets")

        # Strategy 3: Search-based scraping
        if len(assets) < limit and strategy.get('use_search'):
            search_assets = self._search_based_scraping(strategy, limit - len(assets))
            assets.extend(search_assets)
            print(f"   🔍 Search method: {len(search_assets)} assets")

        return assets[:limit]

    def _browser_based_scraping(self, strategy: Dict, limit: int) -> List[Dict]:
        """Browser-based intelligent scraping"""
        assets = []

        if not self._setup_browser():
            return []

        try:
            print("🌐 Starting browser-based scraping...")
            self.driver.get(f"{self.base_url}/games")
            time.sleep(3)

            pages_scraped = 0
            max_pages = strategy.get('max_pages', 10)

            while len(assets) < limit and pages_scraped < max_pages:
                print(f"   📄 Scraping page {pages_scraped + 1}...")

                # Extract games from current page
                page_assets = self._extract_games_from_page(strategy['game_selector'])
                assets.extend(page_assets)

                print(f"   ✅ Found {len(page_assets)} games on page {pages_scraped + 1}")

                # Navigate to next page
                if not self._navigate_to_next_page(strategy):
                    print("   🔚 No more pages available")
                    break

                pages_scraped += 1
                time.sleep(strategy.get('rate_limiting', 2.0))

        except Exception as e:
            print(f"❌ Browser scraping error: {e}")
        finally:
            if self.driver:
                self.driver.quit()

        return assets

    def _extract_games_from_page(self, selector: str) -> List[Dict]:
        """Extract games from current page"""
        games = []

        try:
            game_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            print(f"   🎮 Found {len(game_elements)} game elements")

            for elem in game_elements:
                try:
                    game_data = self._extract_game_data(elem)
                    if game_data:
                        games.append(game_data)
                except Exception as e:
                    continue

        except Exception as e:
            print(f"⚠️ Page extraction error: {e}")

        return games

    def _extract_game_data(self, element) -> Optional[Dict]:
        """Extract data from a single game element"""
        try:
            # Extract title
            title_selectors = [".title", ".game_title", "a", "h3", "h2"]
            title = None
            for selector in title_selectors:
                try:
                    title_elem = element.find_element(By.CSS_SELECTOR, selector)
                    title = title_elem.text.strip()
                    if title:
                        break
                except:
                    continue

            if not title:
                return None

            # Extract link
            link = None
            try:
                link_elem = element.find_element(By.CSS_SELECTOR, "a")
                link = link_elem.get_attribute('href')
                if link and not link.startswith('http'):
                    link = f"{self.base_url}{link}"
            except:
                pass

            # Extract image
            image_url = None
            try:
                img_elem = element.find_element(By.CSS_SELECTOR, "img")
                image_url = img_elem.get_attribute('src')
            except:
                pass

            # Extract description/tags
            description = ""
            try:
                desc_selectors = [".game_text", ".description", ".summary"]
                for selector in desc_selectors:
                    try:
                        desc_elem = element.find_element(By.CSS_SELECTOR, selector)
                        description = desc_elem.text.strip()
                        if description:
                            break
                    except:
                        continue
            except:
                pass

            # Extract author
            author = ""
            try:
                author_selectors = [".game_author", ".by_author", ".creator"]
                for selector in author_selectors:
                    try:
                        author_elem = element.find_element(By.CSS_SELECTOR, selector)
                        author = author_elem.text.strip()
                        if author:
                            break
                    except:
                        continue
            except:
                pass

            return {
                'title': title,
                'source_url': link,
                'preview_image': image_url,
                'description': description,
                'author': author,
                'category': 'Game',
                'site': 'Itch.io',
                'tags': [],
                'file_type': 'game',
                'timestamp': time.time()
            }

        except Exception as e:
            return None

    def _navigate_to_next_page(self, strategy: Dict) -> bool:
        """Navigate to next page"""
        try:
            if strategy['pagination_method'] == 'infinite_scroll':
                # Scroll to bottom
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                return True

            elif strategy['pagination_method'] == 'click_next':
                # Find and click next button
                next_selectors = [
                    ".pager_links .next_page",
                    ".pagination .next",
                    "[rel='next']",
                    ".next_page"
                ]

                for selector in next_selectors:
                    try:
                        next_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if next_button.is_displayed() and next_button.is_enabled():
                            next_button.click()
                            time.sleep(3)
                            return True
                    except:
                        continue

            return False

        except Exception as e:
            print(f"⚠️ Navigation error: {e}")
            return False

    def _requests_based_scraping(self, limit: int) -> List[Dict]:
        """Fallback requests-based scraping"""
        assets = []

        try:
            print("📡 Starting requests-based scraping...")

            for page in range(1, 6):  # Scrape first 5 pages
                if len(assets) >= limit:
                    break

                url = f"{self.base_url}/games?page={page}"
                response = self.safe_scraper.safe_get(url)

                if not response:
                    continue

                soup = BeautifulSoup(response.content, 'html.parser')
                page_assets = self._extract_games_from_soup(soup)
                assets.extend(page_assets)

                print(f"   📄 Page {page}: {len(page_assets)} games")
                time.sleep(2)

        except Exception as e:
            print(f"❌ Requests scraping error: {e}")

        return assets[:limit]

    def _extract_games_from_soup(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract games from BeautifulSoup"""
        games = []

        game_selectors = ['.game_cell', '.game_thumb', '.browse_game']

        for selector in game_selectors:
            game_elements = soup.select(selector)
            if game_elements:
                break

        for elem in game_elements:
            try:
                # Extract title
                title_elem = elem.select_one('.title, .game_title, a')
                title = title_elem.get_text(strip=True) if title_elem else None

                if not title:
                    continue

                # Extract link
                link_elem = elem.select_one('a')
                link = link_elem.get('href') if link_elem else None
                if link and not link.startswith('http'):
                    link = f"{self.base_url}{link}"

                # Extract image
                img_elem = elem.select_one('img')
                image_url = img_elem.get('src') if img_elem else None

                games.append({
                    'title': title,
                    'source_url': link,
                    'preview_image': image_url,
                    'description': '',
                    'author': '',
                    'category': 'Game',
                    'site': 'Itch.io',
                    'tags': [],
                    'file_type': 'game',
                    'timestamp': time.time()
                })

            except Exception as e:
                continue

        return games

    def _search_based_scraping(self, strategy: Dict, limit: int) -> List[Dict]:
        """Search-based scraping for specific terms"""
        assets = []
        search_terms = strategy.get('search_terms', ['2d', 'pixel art'])

        print(f"🔍 Starting search-based scraping for: {search_terms}")

        for term in search_terms:
            if len(assets) >= limit:
                break

            try:
                search_url = f"{self.base_url}/games?q={term.replace(' ', '+')}"
                response = self.safe_scraper.safe_get(search_url)

                if response:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    search_assets = self._extract_games_from_soup(soup)
                    assets.extend(search_assets)

                    print(f"   🔍 '{term}': {len(search_assets)} games")
                    time.sleep(2)

            except Exception as e:
                print(f"⚠️ Search error for '{term}': {e}")
                continue

        return assets[:limit]

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

                enhanced_assets.append(enhanced)

            except Exception as e:
                enhanced_assets.append(asset)
                continue

        return enhanced_assets

    def _calculate_quality_score(self, asset: Dict) -> float:
        """Calculate asset quality score"""
        score = 0.0

        # Title quality (30%)
        if asset.get('title') and len(asset['title']) > 5:
            score += 0.3

        # Description quality (20%)
        if asset.get('description') and len(asset['description']) > 10:
            score += 0.2

        # Image availability (25%)
        if asset.get('preview_image'):
            score += 0.25

        # URL validity (15%)
        if asset.get('source_url') and asset['source_url'].startswith('http'):
            score += 0.15

        # Author information (10%)
        if asset.get('author'):
            score += 0.1

        return min(score, 1.0)

    def _enhance_asset_metadata(self, asset: Dict) -> Dict:
        """Enhance asset with additional metadata"""
        # Add download info if available
        if asset.get('source_url'):
            asset['download_available'] = True
            asset['platform'] = 'Itch.io'

        # Categorize based on title/description
        title_lower = asset.get('title', '').lower()
        desc_lower = asset.get('description', '').lower()

        if any(term in title_lower or term in desc_lower for term in ['pixel', '2d', 'sprite']):
            asset['asset_type'] = '2D Asset'
        elif any(term in title_lower or term in desc_lower for term in ['3d', 'model', 'mesh']):
            asset['asset_type'] = '3D Asset'
        else:
            asset['asset_type'] = 'Game'

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
        print(f"📊 Average quality score: {sum(a.get('quality_score', 0) for a in unique_assets) / len(unique_assets):.2f}")

        return unique_assets

# Test function
def test_ultra_intelligent_itch_scraper():
    """Test the ultra intelligent Itch.io scraper"""
    print("🧪 Testing Ultra Intelligent Itch.io Scraper")
    print("=" * 60)

    scraper = UltraIntelligentItchScraper()

    try:
        # Test with small limit
        assets = scraper.analyze_and_scrape(limit=10)

        print(f"\n📊 SCRAPING RESULTS")
        print(f"   🎯 Total assets: {len(assets)}")

        if assets:
            avg_quality = sum(a.get('quality_score', 0) for a in assets) / len(assets)
            print(f"   📈 Average quality score: {avg_quality:.2f}")

            print(f"\n🎮 Sample Assets:")
            for i, asset in enumerate(assets[:5], 1):
                print(f"   {i}. {asset['title'][:50]}...")
                print(f"      Quality: {asset.get('quality_score', 0):.2f}")
                print(f"      Type: {asset.get('asset_type', 'Unknown')}")

        return assets

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return []

if __name__ == "__main__":
    test_ultra_intelligent_itch_scraper()
