#!/usr/bin/env python3
"""
Ultra Intelligent CraftPix Scraper
Browser intelligence'a dayalı gerçek intelligent scraper
"""

import time
import json
import re
from typing import Dict, List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup

class UltraIntelligentCraftPixScraper:
    """Browser intelligence kullanarak ultra intelligent scraping"""
    
    def __init__(self, headless: bool = True):
        self.base_url = 'https://craftpix.net'
        self.freebies_url = 'https://craftpix.net/freebies/'
        self.driver = None
        self.headless = headless
        
        # Browser intelligence'dan öğrenilen patterns
        self.intelligence = {
            'asset_containers': ['article', '[class*="product"]', '[class*="grid"]'],
            'total_assets_per_page': 16,
            'lazy_loaded_images': True,
            'search_form_available': True,
            'pagination_method': 'scroll_or_click'
        }
        
    def _setup_browser(self):
        """Advanced browser setup with anti-detection"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        # Anti-detection measures
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Real browser simulation
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_argument('--window-size=1920,1080')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return True
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return False
    
    def analyze_and_scrape(self, limit: int = None) -> List[Dict]:
        """Main ultra intelligent scraping method - unified interface"""
        return self.intelligent_scrape(limit)

    def intelligent_scrape(self, limit: int = None) -> List[Dict]:
        """Intelligence-based scraping"""
        print("🧠 ULTRA INTELLIGENT CRAFTPIX SCRAPING")
        print("=" * 70)
        
        if not self._setup_browser():
            print("❌ Browser setup failed, cannot proceed")
            return []
        
        assets = []
        
        try:
            # Phase 1: Navigate and wait for page load
            print("🌐 Phase 1: Intelligent Navigation")
            self.driver.get(self.freebies_url)
            self._wait_for_page_load()
            
            # Phase 2: Handle lazy loading
            print("📦 Phase 2: Lazy Content Loading")
            self._handle_lazy_loading()
            
            # Phase 3: Extract assets using intelligence
            print("🎯 Phase 3: Intelligent Asset Extraction")
            assets = self._extract_assets_intelligently(limit)
            
            # Phase 4: Enhanced asset details
            print("✨ Phase 4: Enhanced Asset Details")
            enhanced_assets = self._enhance_asset_details(assets)
            
            return enhanced_assets
            
        except Exception as e:
            print(f"❌ Scraping error: {e}")
            return assets
        
        finally:
            if self.driver:
                self.driver.quit()
    
    def _wait_for_page_load(self):
        """Sayfa yüklenmesini bekle"""
        try:
            # Wait for main content
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "article"))
            )
            print("   ✅ Page loaded successfully")
            time.sleep(2)  # Additional wait for dynamic content
            
        except TimeoutException:
            print("   ⚠️ Page load timeout, continuing anyway")
    
    def _handle_lazy_loading(self):
        """Lazy loading'i handle et"""
        try:
            # Scroll to trigger lazy loading
            print("   🔄 Triggering lazy loading...")
            
            # Get initial image count
            initial_images = len(self.driver.find_elements(By.TAG_NAME, "img"))
            
            # Scroll down to trigger lazy loading
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            
            # Check if more images loaded
            final_images = len(self.driver.find_elements(By.TAG_NAME, "img"))
            
            if final_images > initial_images:
                print(f"   ✅ Lazy loading triggered: {final_images - initial_images} new images")
            else:
                print("   ℹ️ No additional lazy content detected")
                
        except Exception as e:
            print(f"   ⚠️ Lazy loading error: {e}")
    
    def _extract_assets_intelligently(self, limit: int = None) -> List[Dict]:
        """Intelligence kullanarak asset'ları çıkar"""
        assets = []
        
        # Intelligence'dan öğrenilen en iyi selector'ları kullan
        primary_selector = "article"  # Browser intelligence'dan
        
        try:
            # Find asset elements
            asset_elements = self.driver.find_elements(By.TAG_NAME, "article")
            print(f"   📦 Found {len(asset_elements)} asset elements")
            
            # Limit check
            if limit:
                asset_elements = asset_elements[:limit]
                print(f"   🎯 Processing {len(asset_elements)} assets (limited)")
            
            # Extract each asset
            for i, element in enumerate(asset_elements, 1):
                try:
                    print(f"   🔍 Processing asset {i}/{len(asset_elements)}")
                    
                    asset_data = self._extract_single_asset(element)
                    if asset_data:
                        assets.append(asset_data)
                        print(f"     ✅ {asset_data['title'][:50]}...")
                    else:
                        print(f"     ❌ Failed to extract asset {i}")
                        
                except Exception as e:
                    print(f"     ⚠️ Error processing asset {i}: {e}")
                    continue
            
            print(f"   📊 Successfully extracted {len(assets)} assets")
            
        except Exception as e:
            print(f"   ❌ Asset extraction error: {e}")
        
        return assets
    
    def _extract_single_asset(self, element) -> Optional[Dict]:
        """Tek bir asset'ı detaylı şekilde çıkar"""
        try:
            # Title extraction with multiple strategies
            title = self._extract_title_intelligent(element)
            if not title:
                return None
            
            # URL extraction
            asset_url = self._extract_url_intelligent(element)
            if not asset_url:
                return None
            
            # Image extraction
            preview_image = self._extract_image_intelligent(element)
            
            # Category and metadata
            category = self._extract_category_intelligent(element)
            description = self._extract_description_intelligent(element)
            
            # Price/Free status
            is_free = self._check_free_status(element)
            
            # Tags extraction
            tags = self._extract_tags_intelligent(title, description, category)
            
            return {
                'title': title,
                'description': description,
                'source_url': asset_url,
                'preview_image': preview_image,
                'category': category,
                'site': 'craftpix',
                'asset_type': self._determine_asset_type(title, category),
                'tags': tags,
                'is_free': is_free,
                'license': 'Check individual asset',
                'extraction_method': 'ultra_intelligent_browser'
            }
            
        except Exception as e:
            print(f"       Error in single asset extraction: {e}")
            return None
    
    def _extract_title_intelligent(self, element):
        """Intelligent title extraction"""
        title_strategies = [
            lambda e: e.find_element(By.CSS_SELECTOR, "h3").text,
            lambda e: e.find_element(By.CSS_SELECTOR, "h2").text,
            lambda e: e.find_element(By.CSS_SELECTOR, "h4").text,
            lambda e: e.find_element(By.CSS_SELECTOR, ".title").text,
            lambda e: e.find_element(By.CSS_SELECTOR, "a").get_attribute("title"),
            lambda e: e.find_element(By.CSS_SELECTOR, "a").text
        ]
        
        for strategy in title_strategies:
            try:
                title = strategy(element)
                if title and len(title.strip()) > 3:
                    return title.strip()
            except:
                continue
        
        return None
    
    def _extract_url_intelligent(self, element):
        """Intelligent URL extraction"""
        try:
            # Find the main link
            link_element = element.find_element(By.CSS_SELECTOR, "a")
            href = link_element.get_attribute("href")
            
            if href and href.startswith('http'):
                return href
            elif href:
                return f"{self.base_url}{href}" if href.startswith('/') else f"{self.base_url}/{href}"
                
        except:
            pass
        
        return None
    
    def _extract_image_intelligent(self, element):
        """Intelligent image extraction"""
        try:
            # Multiple image extraction strategies
            img_strategies = [
                lambda e: e.find_element(By.CSS_SELECTOR, "img").get_attribute("src"),
                lambda e: e.find_element(By.CSS_SELECTOR, "img").get_attribute("data-src"),
                lambda e: e.find_element(By.CSS_SELECTOR, ".image img").get_attribute("src"),
                lambda e: e.find_element(By.CSS_SELECTOR, ".thumbnail img").get_attribute("src")
            ]
            
            for strategy in img_strategies:
                try:
                    img_src = strategy(element)
                    if img_src and img_src.startswith('http'):
                        return img_src
                except:
                    continue
                    
        except:
            pass
        
        return None
    
    def _extract_category_intelligent(self, element):
        """Intelligent category extraction"""
        try:
            # Look for category indicators
            category_text = element.text.lower()
            
            if 'icon' in category_text:
                return 'icons'
            elif 'character' in category_text:
                return 'characters'
            elif 'background' in category_text:
                return 'backgrounds'
            elif 'ui' in category_text or 'interface' in category_text:
                return 'ui'
            elif 'tile' in category_text:
                return 'tiles'
            elif 'sprite' in category_text:
                return 'sprites'
            else:
                return 'game-assets'
                
        except:
            return 'misc'
    
    def _extract_description_intelligent(self, element):
        """Intelligent description extraction"""
        try:
            # Try to find description text
            desc_strategies = [
                lambda e: e.find_element(By.CSS_SELECTOR, ".description").text,
                lambda e: e.find_element(By.CSS_SELECTOR, ".excerpt").text,
                lambda e: e.find_element(By.CSS_SELECTOR, "p").text
            ]
            
            for strategy in desc_strategies:
                try:
                    desc = strategy(element)
                    if desc and len(desc) > 10:
                        return desc[:300]
                except:
                    continue
                    
        except:
            pass
        
        return ""
    
    def _check_free_status(self, element):
        """Check if asset is free"""
        try:
            element_text = element.text.lower()
            return 'free' in element_text or '$0' in element_text
        except:
            return True  # Assume free for freebies page
    
    def _extract_tags_intelligent(self, title: str, description: str, category: str) -> List[str]:
        """Intelligent tag extraction"""
        tags = []
        text = f"{title} {description} {category}".lower()
        
        tag_keywords = [
            'free', 'game', 'asset', 'sprite', 'icon', 'ui', 'character',
            'background', 'tile', '2d', 'pixel', 'cartoon', 'fantasy',
            'modern', 'medieval', 'sci-fi', 'rpg', 'platformer'
        ]
        
        for keyword in tag_keywords:
            if keyword in text:
                tags.append(keyword)
        
        return list(set(tags))[:8]
    
    def _determine_asset_type(self, title: str, category: str) -> str:
        """Determine asset type"""
        text = f"{title} {category}".lower()
        
        if any(word in text for word in ['3d', 'model', 'mesh']):
            return '3d'
        elif any(word in text for word in ['sound', 'audio', 'music']):
            return 'audio'
        else:
            return '2d'
    
    def _enhance_asset_details(self, assets: List[Dict]) -> List[Dict]:
        """Asset detaylarını geliştir"""
        print(f"   🔧 Enhancing {len(assets)} assets...")
        
        enhanced_assets = []
        
        for asset in assets:
            try:
                # Add quality score
                quality_score = self._calculate_quality_score(asset)
                asset['quality_score'] = quality_score
                
                # Add extraction timestamp
                asset['extracted_at'] = time.time()
                
                # Add source method
                asset['extraction_method'] = 'ultra_intelligent_browser'
                
                enhanced_assets.append(asset)
                
            except Exception as e:
                print(f"     ⚠️ Enhancement error: {e}")
                enhanced_assets.append(asset)  # Add without enhancement
        
        print(f"   ✅ Enhanced {len(enhanced_assets)} assets")
        return enhanced_assets
    
    def _calculate_quality_score(self, asset: Dict) -> float:
        """Asset kalite skoru hesapla"""
        score = 0.0
        
        # Title quality
        if asset.get('title') and len(asset['title']) > 10:
            score += 0.3
        
        # Description quality
        if asset.get('description') and len(asset['description']) > 20:
            score += 0.2
        
        # Image availability
        if asset.get('preview_image'):
            score += 0.2
        
        # Tags quality
        if asset.get('tags') and len(asset['tags']) > 2:
            score += 0.2
        
        # URL validity
        if asset.get('source_url') and asset['source_url'].startswith('http'):
            score += 0.1
        
        return min(score, 1.0)
    
    def save_results(self, assets: List[Dict], filename: str = None):
        """Sonuçları kaydet"""
        if not filename:
            filename = f"ultra_intelligent_craftpix_{int(time.time())}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(assets, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to: {filename}")
        return filename


# Test the ultra intelligent scraper
if __name__ == "__main__":
    print("🧠 ULTRA INTELLIGENT CRAFTPIX SCRAPER TEST")
    print("=" * 70)
    
    scraper = UltraIntelligentCraftPixScraper(headless=True)
    assets = scraper.intelligent_scrape(limit=5)
    
    print(f"\n🎯 ULTRA INTELLIGENT SCRAPING RESULTS")
    print("=" * 60)
    print(f"Total assets found: {len(assets)}")
    
    for i, asset in enumerate(assets, 1):
        print(f"\n{i}. {asset['title']}")
        print(f"   Category: {asset['category']}")
        print(f"   Type: {asset['asset_type']}")
        print(f"   Quality Score: {asset['quality_score']:.2f}")
        print(f"   Tags: {', '.join(asset['tags'][:5])}")
        print(f"   URL: {asset['source_url']}")
        if asset['preview_image']:
            print(f"   Image: {asset['preview_image'][:60]}...")
    
    if assets:
        scraper.save_results(assets)
        print(f"\n✅ Ultra intelligent scraping completed successfully!")
        print(f"🧠 Used browser intelligence for optimal extraction")
    else:
        print(f"\n❌ No assets found. Check site structure or patterns.")
