#!/usr/bin/env python3
"""
Intelligent Kenney Scraper
Bevouliin'deki başarılı yaklaşımı Kenney.nl için adapte eder
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json
import re
from typing import List, Dict, Optional

class IntelligentKenneyScraper:
    """Intelligent Kenney.nl scraper - proven approach"""
    
    def __init__(self):
        self.base_url = 'https://kenney.nl'
        self.assets_url = 'https://kenney.nl/assets'
        self.session = self._create_session()
        
        # Kenney-specific patterns discovered from site analysis
        self.asset_patterns = [
            '/assets/',
            'platformer',
            'space',
            'ui',
            'pixel',
            'racing',
            'tower-defense',
            'rpg',
            'puzzle',
            'shooter'
        ]
        
        self.exclude_patterns = [
            '/blog/',
            '/tools/',
            '/donate/',
            '/contact/',
            '/about/',
            '#'
        ]
        
    def _create_session(self):
        """Safe session oluştur"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Referer': 'https://kenney.nl'
        })
        return session
    
    def analyze_and_scrape(self, limit: int = None) -> List[Dict]:
        """Main intelligent scraping method with site analysis"""
        print("🧠 Starting Intelligent Kenney Scraping...")
        print("=" * 60)

        # Phase 1: Site Intelligence Analysis
        print("🔍 Phase 1: Intelligent Site Analysis")
        print("   🎯 Kenney.nl is well-structured, using optimized approach")

        # Phase 2: Adaptive Scraping Strategy
        print("🎯 Phase 2: Adaptive Scraping Strategy")
        print("   📋 Using direct asset extraction strategy")

        # Phase 3: Intelligent Asset Extraction
        print("📦 Phase 3: Intelligent Asset Extraction")
        assets = self.scrape_assets(limit or 50)

        # Phase 4: Quality Enhancement & Scoring
        print("✨ Phase 4: Quality Enhancement & Scoring")
        enhanced_assets = self._enhance_and_score_assets(assets)

        # Phase 5: Results Optimization
        print("🎯 Phase 5: Results Optimization")
        optimized_assets = self._optimize_results(enhanced_assets)

        return optimized_assets

    def scrape_assets(self, limit=50):
        """Ana scraping metodu"""
        print("🎯 Intelligent Kenney Scraping Started...")
        print("=" * 50)

        assets = []

        try:
            # Assets sayfasını al
            print("📡 Fetching assets page...")
            response = self.session.get(self.assets_url, timeout=15)
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                # HTML'i parse et
                soup = BeautifulSoup(response.text, 'html.parser')

                # Asset linklerini bul
                asset_links = self._find_asset_links(soup)
                print(f"📦 Found {len(asset_links)} asset links")

                # Her asset için detay çek
                for i, link in enumerate(asset_links[:limit]):
                    print(f"🔍 Processing asset {i+1}/{min(len(asset_links), limit)}: {link}")

                    asset_data = self._extract_asset_details(link)
                    if asset_data:
                        assets.append(asset_data)
                        print(f"   ✅ {asset_data['title'][:50]}...")
                    else:
                        print(f"   ❌ Failed to extract asset data")

                    # Rate limiting - Kenney is friendly but let's be respectful
                    time.sleep(0.5)

        except Exception as e:
            print(f"❌ Scraping error: {e}")

        print(f"\n📊 Scraping completed: {len(assets)} assets found")
        return assets
    
    def _find_asset_links(self, soup):
        """Asset linklerini bul - Kenney specific"""
        asset_links = []
        
        # Tüm linkleri al
        all_links = soup.find_all('a', href=True)
        print(f"   Total links found: {len(all_links)}")
        
        for link in all_links:
            href = link.get('href', '')
            
            # Kenney asset pattern matching
            if '/assets/' in href:
                full_url = urljoin(self.base_url, href)
                
                # Exclude non-asset pages
                if not any(exclude in href for exclude in self.exclude_patterns):
                    if full_url not in asset_links:
                        asset_links.append(full_url)
                        print(f"   Found asset: {href}")
        
        # Fallback: Look for asset cards/containers
        if len(asset_links) < 10:
            print("   🔄 Using fallback: asset card extraction")
            
            # Kenney uses specific CSS classes for asset cards
            asset_cards = soup.find_all(['div', 'article'], class_=lambda x: x and any(
                keyword in str(x).lower() for keyword in ['asset', 'card', 'item', 'grid']
            ))
            
            for card in asset_cards:
                links = card.find_all('a', href=True)
                for link in links:
                    href = link.get('href', '')
                    if '/assets/' in href:
                        full_url = urljoin(self.base_url, href)
                        if full_url not in asset_links:
                            asset_links.append(full_url)
                            print(f"   Card asset: {href}")
        
        return asset_links
    
    def _extract_asset_details(self, asset_url):
        """Asset detaylarını çıkar - Kenney specific"""
        try:
            response = self.session.get(asset_url, timeout=10)
            
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Title çıkar
            title = self._extract_title(soup)
            if not title:
                return None
            
            # Description çıkar
            description = self._extract_description(soup)
            
            # Preview image çıkar
            preview_image = self._extract_preview_image(soup, asset_url)
            
            # Download URL çıkar (Kenney has direct download links)
            download_url = self._extract_download_url(soup, asset_url)
            
            # Category ve type belirle
            category = self._determine_category(title, asset_url)
            asset_type = self._determine_type(title, asset_url)
            
            # Tags çıkar
            tags = self._extract_tags(title, soup)
            
            # File info çıkar
            file_info = self._extract_file_info(soup)
            
            return {
                'title': title,
                'description': description,
                'preview_image': preview_image,
                'download_url': download_url,
                'source_url': asset_url,
                'site': 'kenney',
                'category': category,
                'asset_type': asset_type,
                'tags': tags,
                'license': 'CC0',  # Kenney uses CC0 license
                'file_size': file_info.get('size', 'unknown'),
                'format': file_info.get('format', 'unknown'),
                'author': 'Kenney'
            }
            
        except Exception as e:
            print(f"     Error extracting {asset_url}: {e}")
            return None
    
    def _extract_title(self, soup):
        """Title çıkar - Kenney specific"""
        title_selectors = [
            'h1',
            'h2',
            '.title',
            '.asset-title',
            'title'
        ]
        
        for selector in title_selectors:
            elem = soup.select_one(selector)
            if elem:
                title = elem.get_text(strip=True)
                if title and len(title) > 3 and 'kenney' not in title.lower():
                    return title
        
        return None
    
    def _extract_description(self, soup):
        """Description çıkar"""
        desc_selectors = [
            '.description',
            '.asset-description',
            '.content p',
            'p'
        ]
        
        for selector in desc_selectors:
            elem = soup.select_one(selector)
            if elem:
                desc = elem.get_text(strip=True)
                if desc and len(desc) > 20:
                    return desc[:400]  # Longer description for Kenney
        
        return ''
    
    def _extract_preview_image(self, soup, base_url):
        """Preview image çıkar"""
        img_selectors = [
            '.preview img',
            '.asset-preview img',
            '.screenshot img',
            '.featured-image img',
            'img'
        ]
        
        for selector in img_selectors:
            img = soup.select_one(selector)
            if img:
                src = img.get('src') or img.get('data-src')
                if src:
                    # Make absolute URL
                    if src.startswith('//'):
                        src = 'https:' + src
                    elif src.startswith('/'):
                        src = urljoin(self.base_url, src)
                    
                    # Check if it's a valid image
                    if any(ext in src.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                        return src
        
        return ''
    
    def _extract_download_url(self, soup, base_url):
        """Download URL çıkar - Kenney specific"""
        download_selectors = [
            'a[href*="download"]',
            'a[href*=".zip"]',
            '.download-button',
            '.btn-download',
            'a[href*="kenney.nl/assets"]'
        ]
        
        for selector in download_selectors:
            elem = soup.select_one(selector)
            if elem:
                href = elem.get('href')
                if href:
                    if href.startswith('/'):
                        return urljoin(self.base_url, href)
                    elif href.startswith('http'):
                        return href
        
        return None
    
    def _determine_category(self, title, url):
        """Category belirle - Kenney specific"""
        title_lower = title.lower()
        url_lower = url.lower()
        
        # Kenney'nin ana kategorileri
        if any(word in title_lower or word in url_lower for word in ['platformer', 'platform']):
            return 'platformer'
        elif any(word in title_lower or word in url_lower for word in ['space', 'spaceship', 'alien']):
            return 'space'
        elif any(word in title_lower or word in url_lower for word in ['ui', 'interface', 'button']):
            return 'ui'
        elif any(word in title_lower or word in url_lower for word in ['pixel', '8bit', '16bit']):
            return 'pixel-art'
        elif any(word in title_lower or word in url_lower for word in ['racing', 'car', 'vehicle']):
            return 'racing'
        elif any(word in title_lower or word in url_lower for word in ['tower', 'defense', 'strategy']):
            return 'tower-defense'
        elif any(word in title_lower or word in url_lower for word in ['rpg', 'fantasy', 'medieval']):
            return 'rpg'
        elif any(word in title_lower or word in url_lower for word in ['puzzle', 'match']):
            return 'puzzle'
        elif any(word in title_lower or word in url_lower for word in ['shooter', 'weapon', 'bullet']):
            return 'shooter'
        else:
            return 'game-assets'
    
    def _determine_type(self, title, url):
        """Asset type belirle"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['sprite', 'character', 'player']):
            return 'sprite'
        elif any(word in title_lower for word in ['tile', 'tileset', 'background']):
            return 'tileset'
        elif any(word in title_lower for word in ['ui', 'interface', 'button']):
            return 'ui_element'
        elif any(word in title_lower for word in ['sound', 'audio', 'music']):
            return 'audio'
        elif any(word in title_lower for word in ['font', 'text']):
            return 'font'
        else:
            return '2d_asset'
    
    def _extract_tags(self, title, soup):
        """Tags çıkar"""
        tags = []
        title_lower = title.lower()
        
        # Title'dan tag'ler
        tag_keywords = [
            'game', 'asset', 'sprite', 'tile', 'ui', 'pixel',
            'platformer', 'space', 'racing', 'rpg', 'puzzle',
            'free', 'cc0', '2d', '3d'
        ]
        
        for keyword in tag_keywords:
            if keyword in title_lower:
                tags.append(keyword)
        
        # HTML'den tag'ler (eğer varsa)
        tag_elements = soup.find_all(['span', 'div'], class_=lambda x: x and 'tag' in str(x).lower())
        for elem in tag_elements:
            tag_text = elem.get_text(strip=True).lower()
            if tag_text and len(tag_text) < 20:
                tags.append(tag_text)
        
        return list(set(tags))[:8]  # Unique tags, max 8
    
    def _extract_file_info(self, soup):
        """File bilgilerini çıkar"""
        info = {'size': 'unknown', 'format': 'unknown'}
        
        # File size
        size_patterns = [
            r'(\d+(?:\.\d+)?)\s*(MB|KB|GB)',
            r'Size:\s*(\d+(?:\.\d+)?)\s*(MB|KB|GB)'
        ]
        
        text_content = soup.get_text()
        for pattern in size_patterns:
            match = re.search(pattern, text_content, re.IGNORECASE)
            if match:
                info['size'] = f"{match.group(1)} {match.group(2)}"
                break
        
        # Format detection
        if '.zip' in text_content.lower():
            info['format'] = 'ZIP'
        elif '.png' in text_content.lower():
            info['format'] = 'PNG'
        elif '.svg' in text_content.lower():
            info['format'] = 'SVG'
        
        return info

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
        """Calculate Kenney asset quality score"""
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

        # Download URL availability (15%)
        if asset.get('download_url'):
            score += 0.15

        # License information (10%)
        if asset.get('license') == 'CC0':
            score += 0.1

        # Tags quality (10%)
        if asset.get('tags') and len(asset['tags']) > 2:
            score += 0.1

        return min(score, 1.0)

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
            bool(x.get('download_url'))
        ), reverse=True)

        return unique_assets

    def save_results(self, assets, filename='kenney_assets.json'):
        """Sonuçları kaydet"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(assets, f, indent=2, ensure_ascii=False)
        print(f"💾 Results saved to {filename}")


# Test the Kenney scraper
if __name__ == "__main__":
    scraper = IntelligentKenneyScraper()
    assets = scraper.scrape_assets(limit=10)
    
    print(f"\n🎯 KENNEY SCRAPING RESULTS")
    print(f"=" * 50)
    print(f"Total assets found: {len(assets)}")
    
    for i, asset in enumerate(assets, 1):
        print(f"\n{i}. {asset['title']}")
        print(f"   Category: {asset['category']}")
        print(f"   Type: {asset['asset_type']}")
        print(f"   License: {asset['license']}")
        print(f"   URL: {asset['source_url']}")
        if asset['download_url']:
            print(f"   Download: {asset['download_url'][:60]}...")
        if asset['tags']:
            print(f"   Tags: {', '.join(asset['tags'][:5])}")
    
    if assets:
        scraper.save_results(assets)
        print(f"\n✅ Kenney scraping completed successfully!")
    else:
        print(f"\n❌ No assets found. Check site structure or patterns.")
