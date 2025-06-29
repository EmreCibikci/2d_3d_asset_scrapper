#!/usr/bin/env python3
"""
Intelligent Bevouliin Scraper
Intelligent Site Analyzer'ı kullanarak güvenli ve etkili scraping
"""

from intelligent_site_analyzer import IntelligentSiteAnalyzer, SiteStructure
from scrapers.enhanced_base_scraper import EnhancedBaseScraper
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from typing import List, Dict, Optional

class IntelligentBevouliinScraper(EnhancedBaseScraper):
    """Intelligent Site Analysis kullanan gelişmiş Bevouliin scraper"""
    
    def __init__(self):
        super().__init__('bevouliin', enable_advanced_security=True)
        self.base_url = 'https://bevouliin.com'
        self.site_structure = None
        self.analyzer = IntelligentSiteAnalyzer(self.base_url)
        
        # Intelligent session
        self.session = self._create_intelligent_session()

    def _safe_get_soup(self, url: str, timeout: int = 10) -> Optional[BeautifulSoup]:
        """Safe request with enhanced encoding handling"""
        try:
            response = self.session.get(url, timeout=timeout)

            # Enhanced encoding detection and handling
            if response.encoding is None or response.encoding.lower() in ['iso-8859-1', 'windows-1252']:
                # Try to detect encoding from content
                try:
                    import chardet
                    detected = chardet.detect(response.content)
                    if detected['encoding'] and detected['confidence'] > 0.7:
                        response.encoding = detected['encoding']
                    else:
                        response.encoding = 'utf-8'
                except ImportError:
                    # Fallback if chardet not available
                    response.encoding = 'utf-8'

            # Multiple parsing strategies
            soup = None

            # Strategy 1: Use detected encoding
            try:
                soup = BeautifulSoup(response.content, 'html.parser', from_encoding=response.encoding)
            except:
                pass

            # Strategy 2: Force UTF-8
            if not soup:
                try:
                    response.encoding = 'utf-8'
                    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
                except:
                    pass

            # Strategy 3: Ignore encoding errors
            if not soup:
                try:
                    content = response.content.decode('utf-8', errors='ignore')
                    soup = BeautifulSoup(content, 'html.parser')
                except:
                    pass

            # Strategy 4: Raw content
            if not soup:
                try:
                    soup = BeautifulSoup(response.content, 'html.parser')
                except:
                    pass

            return soup

        except Exception as e:
            print(f"   ⚠️ Request failed for {url}: {e}")
            return None
        
    def _create_intelligent_session(self) -> requests.Session:
        """Intelligent ve güvenli session oluştur"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,tr;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        })
        return session
    
    def analyze_and_scrape(self, limit: int = None) -> List[Dict]:
        """Site analizi yapıp intelligent scraping gerçekleştir"""
        print("🧠 Starting Intelligent Bevouliin Scraping...")
        print("=" * 60)
        
        # Phase 1: Site Intelligence Analysis
        print("🔍 Phase 1: Intelligent Site Analysis")
        self.site_structure = self._perform_site_analysis()
        
        # Phase 2: Adaptive Scraping Strategy
        print("🎯 Phase 2: Adaptive Scraping Strategy")
        scraping_strategy = self._determine_scraping_strategy()
        
        # Phase 3: Intelligent Asset Extraction
        print("📦 Phase 3: Intelligent Asset Extraction")
        assets = self._execute_intelligent_scraping(scraping_strategy, limit)
        
        # Phase 4: Quality Enhancement & Scoring
        print("✨ Phase 4: Quality Enhancement & Scoring")
        enhanced_assets = self._enhance_and_score_assets(assets)

        # Phase 5: Results Optimization
        print("🎯 Phase 5: Results Optimization")
        optimized_assets = self._optimize_results(enhanced_assets)
        
        return optimized_assets
    
    def _perform_site_analysis(self) -> Optional[SiteStructure]:
        """Site analizi gerçekleştir"""
        try:
            # Basit ve güvenli analiz
            response = self.session.get(self.base_url, timeout=15)
            if response.status_code != 200:
                print(f"   ❌ Site access failed: {response.status_code}")
                return None
            
            # Use safe encoding method
            soup = self._safe_get_soup(self.base_url)
            
            # Manuel site yapısı analizi
            structure = self._manual_site_analysis(soup)
            print(f"   ✅ Site analysis completed")
            print(f"   📊 Found {len(structure.get('asset_patterns', []))} asset patterns")
            
            return structure
            
        except Exception as e:
            print(f"   ❌ Site analysis failed: {e}")
            return None
    
    def _manual_site_analysis(self, soup) -> Dict:
        """Manuel site analizi - encoding safe"""
        structure = {
            'title': '',
            'asset_patterns': [],
            'navigation_links': [],
            'content_containers': [],
            'pagination_indicators': []
        }
        
        try:
            # Title extraction
            title_elem = soup.find('title')
            if title_elem:
                structure['title'] = title_elem.get_text(strip=True)
            
            # Asset pattern discovery
            all_links = soup.find_all('a', href=True)
            asset_patterns = set()
            
            for link in all_links:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                
                # Asset URL patterns
                if any(keyword in href.lower() for keyword in [
                    'game', 'asset', 'sprite', 'character', 'background',
                    'winter-cat', 'halloween', 'pirate', 'trading-card'
                ]):
                    # Extract pattern
                    if '-game-' in href:
                        asset_patterns.add('-game-')
                    if '-asset' in href:
                        asset_patterns.add('-asset')
                    if 'winter-cat' in href:
                        asset_patterns.add('winter-cat')
                    if 'halloween' in href:
                        asset_patterns.add('halloween')
                    if 'trading-card' in href:
                        asset_patterns.add('trading-card')
            
            structure['asset_patterns'] = list(asset_patterns)
            
            # Navigation links
            nav_elements = soup.find_all(['nav', 'ul'], class_=lambda x: x and 'menu' in str(x).lower())
            for nav in nav_elements:
                links = nav.find_all('a', href=True)
                for link in links[:10]:  # Limit
                    structure['navigation_links'].append({
                        'text': link.get_text(strip=True),
                        'href': link.get('href')
                    })
            
            # Content containers
            articles = soup.find_all('article')
            for article in articles[:5]:  # Limit
                classes = article.get('class', [])
                if classes:
                    structure['content_containers'].append('.'.join(classes))
            
            # Pagination indicators
            pagination_selectors = ['.pagination', '.page-numbers', '[class*="page"]']
            for selector in pagination_selectors:
                if soup.select(selector):
                    structure['pagination_indicators'].append(selector)
            
        except Exception as e:
            print(f"   ⚠️ Manual analysis warning: {e}")
        
        return structure
    
    def _determine_scraping_strategy(self) -> Dict:
        """Scraping stratejisini belirle"""
        strategy = {
            'primary_method': 'direct_link_extraction',
            'fallback_methods': ['article_based', 'pattern_matching'],
            'asset_selectors': [],
            'pagination_method': 'none',
            'rate_limiting': 1.0  # seconds between requests
        }
        
        if self.site_structure:
            # Asset patterns varsa, bunları kullan
            if self.site_structure.get('asset_patterns'):
                strategy['asset_selectors'] = self.site_structure['asset_patterns']
                print(f"   ✅ Using {len(strategy['asset_selectors'])} asset patterns")
            
            # Pagination varsa, etkinleştir
            if self.site_structure.get('pagination_indicators'):
                strategy['pagination_method'] = 'url_based'
                print(f"   ✅ Pagination enabled")
            
            # Content containers varsa, kullan
            if self.site_structure.get('content_containers'):
                strategy['fallback_methods'].insert(0, 'container_based')
                print(f"   ✅ Container-based fallback enabled")
        
        return strategy
    
    def _execute_intelligent_scraping(self, strategy: Dict, limit: int = None) -> List[Dict]:
        """Intelligent scraping gerçekleştir"""
        assets = []
        
        try:
            # Primary method: Direct link extraction
            print("   🎯 Executing primary method: Direct link extraction")
            primary_assets = self._extract_assets_direct(strategy, limit)
            assets.extend(primary_assets)
            print(f"   ✅ Primary method found: {len(primary_assets)} assets")
            
            # Fallback methods if needed
            if len(assets) < (limit or 10):
                for method in strategy['fallback_methods']:
                    if len(assets) >= (limit or 50):
                        break
                    
                    print(f"   🔄 Executing fallback: {method}")
                    fallback_assets = self._execute_fallback_method(method, limit - len(assets) if limit else None)
                    
                    # Filter duplicates
                    new_assets = [a for a in fallback_assets if a['source_url'] not in [existing['source_url'] for existing in assets]]
                    assets.extend(new_assets)
                    print(f"   ✅ Fallback {method} found: {len(new_assets)} new assets")
            
        except Exception as e:
            print(f"   ❌ Intelligent scraping error: {e}")
        
        return assets
    
    def _extract_assets_direct(self, strategy: Dict, limit: int = None) -> List[Dict]:
        """Direct asset extraction"""
        assets = []
        
        try:
            soup = self._safe_get_soup(self.base_url, timeout=15)
            if not soup:
                return assets
            
            # Find asset links using patterns
            all_links = soup.find_all('a', href=True)
            asset_links = []
            
            for link in all_links:
                href = link.get('href', '')
                
                # Check against asset patterns
                if strategy.get('asset_selectors'):
                    if any(pattern in href for pattern in strategy['asset_selectors']):
                        full_url = urljoin(self.base_url, href)
                        if (full_url not in asset_links and 
                            self.base_url in full_url and
                            not any(exclude in href for exclude in ['/category/', '/wp-content/', '/tag/'])):
                            asset_links.append(full_url)
                
                # Fallback: look for game-related links
                elif any(keyword in href.lower() for keyword in ['game', 'asset', 'sprite']):
                    full_url = urljoin(self.base_url, href)
                    if (full_url not in asset_links and 
                        self.base_url in full_url and
                        not any(exclude in href for exclude in ['/category/', '/wp-content/', '/tag/'])):
                        asset_links.append(full_url)
            
            print(f"     📦 Found {len(asset_links)} potential asset links")
            
            # Extract asset data
            for i, asset_url in enumerate(asset_links):
                if limit and len(assets) >= limit:
                    break
                
                try:
                    asset_data = self._extract_single_asset(asset_url)
                    if asset_data:
                        assets.append(asset_data)
                        print(f"     ✅ {i+1}. {asset_data['title'][:40]}...")
                    
                    # Rate limiting
                    time.sleep(strategy.get('rate_limiting', 1.0))
                    
                except Exception as e:
                    print(f"     ⚠️ Asset extraction error: {e}")
                    continue
            
        except Exception as e:
            print(f"     ❌ Direct extraction error: {e}")
        
        return assets

    def _execute_fallback_method(self, method: str, limit: int = None) -> List[Dict]:
        """Fallback method execution"""
        assets = []

        try:
            if method == 'article_based':
                assets = self._extract_from_articles(limit)
            elif method == 'pattern_matching':
                assets = self._extract_by_patterns(limit)
            elif method == 'container_based':
                assets = self._extract_from_containers(limit)

        except Exception as e:
            print(f"     ❌ Fallback method {method} error: {e}")

        return assets

    def _extract_from_articles(self, limit: int = None) -> List[Dict]:
        """Article-based asset extraction"""
        assets = []

        try:
            response = self.session.get(self.base_url, timeout=15)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')

            articles = soup.find_all('article')
            print(f"     📄 Found {len(articles)} articles")

            for i, article in enumerate(articles):
                if limit and len(assets) >= limit:
                    break

                # Extract main link from article
                links = article.find_all('a', href=True)
                for link in links:
                    href = link.get('href', '')
                    if (self.base_url in href and
                        not any(exclude in href for exclude in ['/category/', '/wp-content/', '/tag/'])):

                        try:
                            asset_data = self._extract_single_asset(href)
                            if asset_data:
                                assets.append(asset_data)
                                print(f"     ✅ Article {i+1}: {asset_data['title'][:40]}...")
                                break  # One asset per article
                        except:
                            continue

                time.sleep(0.5)  # Rate limiting

        except Exception as e:
            print(f"     ❌ Article extraction error: {e}")

        return assets

    def _extract_by_patterns(self, limit: int = None) -> List[Dict]:
        """Pattern-based asset extraction"""
        assets = []

        try:
            response = self.session.get(self.base_url, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')

            # Use discovered asset patterns
            asset_patterns = self.site_structure.get('asset_patterns', [])
            if not asset_patterns:
                asset_patterns = ['game', 'asset', 'sprite', 'character']

            print(f"     🔍 Using patterns: {asset_patterns}")

            all_links = soup.find_all('a', href=True)
            asset_links = []

            for link in all_links:
                href = link.get('href', '')
                text = link.get_text(strip=True)

                # Check if link matches any pattern
                if any(pattern in href.lower() or pattern in text.lower() for pattern in asset_patterns):
                    full_url = urljoin(self.base_url, href)
                    if (full_url not in asset_links and
                        self.base_url in full_url and
                        not any(exclude in href for exclude in ['/category/', '/wp-content/', '/tag/', '/author/'])):
                        asset_links.append(full_url)

            print(f"     📦 Found {len(asset_links)} pattern-matched links")

            # Extract asset data
            for i, asset_url in enumerate(asset_links):
                if limit and len(assets) >= limit:
                    break

                try:
                    asset_data = self._extract_single_asset(asset_url)
                    if asset_data:
                        assets.append(asset_data)
                        print(f"     ✅ Pattern {i+1}: {asset_data['title'][:40]}...")

                    time.sleep(0.5)  # Rate limiting

                except Exception as e:
                    continue

        except Exception as e:
            print(f"     ❌ Pattern extraction error: {e}")

        return assets

    def _extract_from_containers(self, limit: int = None) -> List[Dict]:
        """Container-based asset extraction"""
        assets = []

        try:
            response = self.session.get(self.base_url, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')

            # Use discovered content containers
            containers = self.site_structure.get('content_containers', [])
            if not containers:
                containers = ['article', '.post', '.entry']

            print(f"     📦 Using containers: {containers}")

            for container_selector in containers:
                container_elements = soup.select(container_selector)

                for i, container in enumerate(container_elements):
                    if limit and len(assets) >= limit:
                        break

                    # Find main link in container
                    links = container.find_all('a', href=True)
                    for link in links:
                        href = link.get('href', '')
                        if (self.base_url in href and
                            not any(exclude in href for exclude in ['/category/', '/wp-content/', '/tag/'])):

                            try:
                                asset_data = self._extract_single_asset(href)
                                if asset_data:
                                    assets.append(asset_data)
                                    print(f"     ✅ Container {i+1}: {asset_data['title'][:40]}...")
                                    break  # One asset per container
                            except:
                                continue

                    time.sleep(0.3)  # Rate limiting

        except Exception as e:
            print(f"     ❌ Container extraction error: {e}")

        return assets

    def _extract_single_asset(self, asset_url: str) -> Optional[Dict]:
        """Single asset extraction"""
        try:
            response = self.session.get(asset_url, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')

            # Extract title
            title = ''
            title_selectors = ['h1', 'h2', '.entry-title', '.post-title', 'title']
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    break

            if not title:
                return None

            # Extract description
            description = ''
            desc_selectors = ['.entry-content', '.post-content', '.description', 'p']
            for selector in desc_selectors:
                desc_elem = soup.select_one(selector)
                if desc_elem:
                    description = desc_elem.get_text(strip=True)[:300]
                    break

            # Extract preview image
            preview_image = ''
            img_elem = soup.find('img')
            if img_elem:
                src = img_elem.get('src') or img_elem.get('data-src')
                if src:
                    preview_image = urljoin(self.base_url, src)

            # Determine category and type
            category = self._determine_category(title, asset_url)
            asset_type = self._determine_type(title, asset_url)

            return {
                'title': title,
                'description': description,
                'download_url': None,  # Would need deeper analysis
                'preview_image': preview_image,
                'source_url': asset_url,
                'site': 'bevouliin',
                'license': 'CC0',
                'tags': self._extract_tags(title),
                'asset_type': asset_type,
                'category': category,
                'file_size': 'unknown',
                'format': 'unknown'
            }

        except Exception as e:
            return None

    def _determine_category(self, title: str, url: str) -> str:
        """Determine asset category"""
        title_lower = title.lower()
        url_lower = url.lower()

        if any(word in title_lower for word in ['character', 'hero', 'player']):
            return 'characters'
        elif any(word in title_lower for word in ['background', 'scene']):
            return 'backgrounds'
        elif any(word in title_lower for word in ['card', 'trading']):
            return 'trading-cards'
        elif any(word in title_lower for word in ['enemy', 'monster']):
            return 'enemies'
        elif any(word in title_lower for word in ['obstacle', 'barrier']):
            return 'obstacles'
        else:
            return 'game-assets'

    def _determine_type(self, title: str, url: str) -> str:
        """Determine asset type"""
        title_lower = title.lower()

        if 'sprite' in title_lower:
            return 'sprite'
        elif 'background' in title_lower:
            return 'background'
        elif 'character' in title_lower:
            return 'character'
        else:
            return '2d_asset'

    def _extract_tags(self, title: str) -> List[str]:
        """Extract tags from title"""
        tags = []
        title_lower = title.lower()

        tag_keywords = [
            'game', 'asset', 'sprite', 'character', 'background',
            'pixel', 'cartoon', 'cute', 'fantasy', 'sci-fi'
        ]

        for keyword in tag_keywords:
            if keyword in title_lower:
                tags.append(keyword)

        return tags[:5]

    def _enhance_and_score_assets(self, assets: List[Dict]) -> List[Dict]:
        """Enhance assets with quality scoring"""
        enhanced_assets = []

        print(f"   ✨ Enhancing {len(assets)} assets...")

        for asset in assets:
            try:
                enhanced = asset.copy()

                # Calculate quality score
                enhanced['quality_score'] = self._calculate_quality_score(asset)

                # Add timestamp
                enhanced['timestamp'] = time.time()

                enhanced_assets.append(enhanced)

            except Exception as e:
                enhanced_assets.append(asset)
                continue

        return enhanced_assets

    def _calculate_quality_score(self, asset: Dict) -> float:
        """Calculate Bevouliin asset quality score"""
        score = 0.0

        # Title quality (25%)
        if asset.get('title') and len(asset['title']) > 5:
            score += 0.25

        # Description quality (20%)
        if asset.get('description') and len(asset['description']) > 20:
            score += 0.2

        # Preview image availability (20%)
        if asset.get('preview_image'):
            score += 0.2

        # Source URL validity (15%)
        if asset.get('source_url') and asset['source_url'].startswith('http'):
            score += 0.15

        # License information (10%)
        if asset.get('license'):
            score += 0.1

        # Tags quality (10%)
        if asset.get('tags') and len(asset['tags']) > 1:
            score += 0.1

        return min(score, 1.0)

    def _optimize_results(self, assets: List[Dict]) -> List[Dict]:
        """Optimize and clean results"""
        print(f"   🔧 Optimizing {len(assets)} assets...")

        # Remove duplicates
        seen_urls = set()
        unique_assets = []

        for asset in assets:
            url = asset['source_url']
            if url not in seen_urls:
                seen_urls.add(url)
                unique_assets.append(asset)

        # Sort by relevance (title length as proxy for completeness)
        unique_assets.sort(key=lambda x: len(x['title']), reverse=True)

        print(f"   ✅ Optimized to {len(unique_assets)} unique assets")
        return unique_assets

    # Abstract method implementations
    def scrape_assets(self, limit: int = None) -> List[Dict]:
        """Main scraping method - delegates to intelligent scraping"""
        return self.analyze_and_scrape(limit)

    def get_download_url(self, asset_url: str) -> Optional[str]:
        """Get download URL for an asset"""
        try:
            response = self.session.get(asset_url, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')

            # Look for download links
            download_selectors = [
                'a[href*="download"]',
                'a[href*=".zip"]',
                'a[href*=".rar"]',
                '.download-link',
                '.btn-download'
            ]

            for selector in download_selectors:
                download_elem = soup.select_one(selector)
                if download_elem:
                    href = download_elem.get('href')
                    if href:
                        return urljoin(self.base_url, href)

            return None

        except Exception as e:
            return None


# Test the intelligent scraper
if __name__ == "__main__":
    scraper = IntelligentBevouliinScraper()
    assets = scraper.analyze_and_scrape(limit=5)

    print(f"\n🎯 INTELLIGENT SCRAPING COMPLETE")
    print(f"=" * 60)
    print(f"Total assets found: {len(assets)}")

    for i, asset in enumerate(assets, 1):
        print(f"\n{i}. {asset['title']}")
        print(f"   Category: {asset['category']}")
        print(f"   Type: {asset['asset_type']}")
        print(f"   URL: {asset['source_url']}")
        if asset['tags']:
            print(f"   Tags: {', '.join(asset['tags'])}")

    print(f"\n✅ Intelligent scraping completed successfully!")
