#!/usr/bin/env python3
"""
Intelligent Quaternius Scraper
3D asset'ler için özelleştirilmiş intelligent scraping
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json
import re
from typing import List, Dict, Optional

class IntelligentQuaterniusScraper:
    """Intelligent Quaternius.com scraper - 3D assets specialist"""
    
    def __init__(self):
        self.base_url = 'https://quaternius.com'
        self.assets_url = 'https://quaternius.com'  # Ana sayfa deneyelim
        self.session = self._create_session()
        
        # Quaternius-specific patterns
        self.asset_patterns = [
            '/packs/',
            'ultimate',
            'lowpoly',
            'stylized',
            'nature',
            'characters',
            'vehicles',
            'weapons',
            'buildings'
        ]
        
        self.exclude_patterns = [
            '/blog/',
            '/about/',
            '/contact/',
            '/tutorials/',
            '#',
            'mailto:'
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
            'Referer': 'https://quaternius.com'
        })
        return session
    
    def scrape_assets(self, limit=30):
        """Ana scraping metodu"""
        print("🎯 Intelligent Quaternius Scraping Started...")
        print("=" * 50)
        
        assets = []
        
        try:
            # Packs sayfasını al
            print("📡 Fetching packs page...")
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
                    
                    # Rate limiting - Quaternius is a smaller site, be extra respectful
                    time.sleep(1.0)
            
        except Exception as e:
            print(f"❌ Scraping error: {e}")
        
        print(f"\n📊 Scraping completed: {len(assets)} assets found")
        return assets
    
    def _find_asset_links(self, soup):
        """Asset linklerini bul - Quaternius specific"""
        asset_links = []
        
        # Tüm linkleri al
        all_links = soup.find_all('a', href=True)
        print(f"   Total links found: {len(all_links)}")
        
        for link in all_links:
            href = link.get('href', '')
            
            # Quaternius pack pattern matching
            if any(pattern in href.lower() for pattern in self.asset_patterns):
                full_url = urljoin(self.base_url, href)
                
                # Exclude non-asset pages
                if not any(exclude in href for exclude in self.exclude_patterns):
                    if full_url not in asset_links and self.base_url in full_url:
                        asset_links.append(full_url)
                        print(f"   Found asset: {href}")
        
        # Fallback: Look for pack cards/containers
        if len(asset_links) < 5:
            print("   🔄 Using fallback: pack card extraction")
            
            # Quaternius uses specific structures for pack cards
            pack_cards = soup.find_all(['div', 'article', 'section'], class_=lambda x: x and any(
                keyword in str(x).lower() for keyword in ['pack', 'card', 'item', 'grid', 'asset']
            ))
            
            for card in pack_cards:
                links = card.find_all('a', href=True)
                for link in links:
                    href = link.get('href', '')
                    if href and not href.startswith('#'):
                        full_url = urljoin(self.base_url, href)
                        if (full_url not in asset_links and 
                            self.base_url in full_url and
                            not any(exclude in href for exclude in self.exclude_patterns)):
                            asset_links.append(full_url)
                            print(f"   Card asset: {href}")
        
        return asset_links
    
    def _extract_asset_details(self, asset_url):
        """Asset detaylarını çıkar - Quaternius specific"""
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
            
            # Download URL çıkar (Quaternius has direct download links)
            download_url = self._extract_download_url(soup, asset_url)
            
            # Category ve type belirle
            category = self._determine_category(title, asset_url)
            asset_type = self._determine_type(title, asset_url)
            
            # Tags çıkar
            tags = self._extract_tags(title, soup)
            
            # File info çıkar
            file_info = self._extract_file_info(soup)
            
            # 3D specific info
            model_info = self._extract_3d_info(soup)
            
            return {
                'title': title,
                'description': description,
                'preview_image': preview_image,
                'download_url': download_url,
                'source_url': asset_url,
                'site': 'quaternius',
                'category': category,
                'asset_type': asset_type,
                'tags': tags,
                'license': 'CC0',  # Quaternius uses CC0 license
                'file_size': file_info.get('size', 'unknown'),
                'format': file_info.get('format', '3D Model'),
                'author': 'Quaternius',
                'poly_count': model_info.get('poly_count', 'unknown'),
                'textures': model_info.get('textures', 'unknown'),
                'rigged': model_info.get('rigged', False)
            }
            
        except Exception as e:
            print(f"     Error extracting {asset_url}: {e}")
            return None
    
    def _extract_title(self, soup):
        """Title çıkar - Quaternius specific"""
        title_selectors = [
            'h1',
            'h2',
            '.title',
            '.pack-title',
            '.asset-title',
            'title'
        ]
        
        for selector in title_selectors:
            elem = soup.select_one(selector)
            if elem:
                title = elem.get_text(strip=True)
                if title and len(title) > 3 and 'quaternius' not in title.lower():
                    return title
        
        return None
    
    def _extract_description(self, soup):
        """Description çıkar"""
        desc_selectors = [
            '.description',
            '.pack-description',
            '.content p',
            '.info p',
            'p'
        ]
        
        for selector in desc_selectors:
            elem = soup.select_one(selector)
            if elem:
                desc = elem.get_text(strip=True)
                if desc and len(desc) > 20:
                    return desc[:500]  # Longer description for 3D assets
        
        return ''
    
    def _extract_preview_image(self, soup, base_url):
        """Preview image çıkar"""
        img_selectors = [
            '.preview img',
            '.pack-preview img',
            '.screenshot img',
            '.featured-image img',
            '.gallery img',
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
        """Download URL çıkar - Quaternius specific"""
        download_selectors = [
            'a[href*="download"]',
            'a[href*=".zip"]',
            'a[href*=".rar"]',
            '.download-button',
            '.btn-download',
            'a[href*="quaternius.com"]'
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
        """Category belirle - Quaternius specific"""
        title_lower = title.lower()
        url_lower = url.lower()
        
        # Quaternius'un ana kategorileri
        if any(word in title_lower or word in url_lower for word in ['character', 'people', 'human']):
            return 'characters'
        elif any(word in title_lower or word in url_lower for word in ['nature', 'tree', 'plant', 'rock']):
            return 'nature'
        elif any(word in title_lower or word in url_lower for word in ['vehicle', 'car', 'truck', 'ship']):
            return 'vehicles'
        elif any(word in title_lower or word in url_lower for word in ['weapon', 'sword', 'gun', 'bow']):
            return 'weapons'
        elif any(word in title_lower or word in url_lower for word in ['building', 'house', 'structure']):
            return 'buildings'
        elif any(word in title_lower or word in url_lower for word in ['furniture', 'prop', 'object']):
            return 'props'
        elif any(word in title_lower or word in url_lower for word in ['ultimate', 'collection', 'pack']):
            return 'collections'
        else:
            return '3d-assets'
    
    def _determine_type(self, title, url):
        """Asset type belirle"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['lowpoly', 'low-poly', 'low poly']):
            return 'lowpoly_3d'
        elif any(word in title_lower for word in ['stylized', 'cartoon']):
            return 'stylized_3d'
        elif any(word in title_lower for word in ['realistic', 'photorealistic']):
            return 'realistic_3d'
        else:
            return '3d_model'
    
    def _extract_tags(self, title, soup):
        """Tags çıkar"""
        tags = []
        title_lower = title.lower()
        
        # Title'dan tag'ler
        tag_keywords = [
            '3d', 'lowpoly', 'stylized', 'free', 'cc0',
            'character', 'nature', 'vehicle', 'weapon', 'building',
            'ultimate', 'pack', 'collection'
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
        info = {'size': 'unknown', 'format': '3D Model'}
        
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
        if any(fmt in text_content.lower() for fmt in ['.fbx', 'fbx']):
            info['format'] = 'FBX'
        elif any(fmt in text_content.lower() for fmt in ['.obj', 'obj']):
            info['format'] = 'OBJ'
        elif any(fmt in text_content.lower() for fmt in ['.blend', 'blender']):
            info['format'] = 'Blender'
        elif any(fmt in text_content.lower() for fmt in ['.gltf', 'gltf']):
            info['format'] = 'GLTF'
        
        return info
    
    def _extract_3d_info(self, soup):
        """3D specific bilgileri çıkar"""
        info = {'poly_count': 'unknown', 'textures': 'unknown', 'rigged': False}
        
        text_content = soup.get_text().lower()
        
        # Poly count
        poly_patterns = [
            r'(\d+(?:,\d+)?)\s*(?:poly|polygons|tris|triangles)',
            r'poly(?:gon)?s?:\s*(\d+(?:,\d+)?)',
            r'(\d+(?:,\d+)?)\s*vertices'
        ]
        
        for pattern in poly_patterns:
            match = re.search(pattern, text_content, re.IGNORECASE)
            if match:
                info['poly_count'] = match.group(1)
                break
        
        # Textures
        if any(word in text_content for word in ['texture', 'material', 'uv']):
            if any(word in text_content for word in ['1024', '2048', '4096']):
                info['textures'] = 'Included'
            else:
                info['textures'] = 'Yes'
        
        # Rigged
        if any(word in text_content for word in ['rigged', 'armature', 'skeleton', 'bones']):
            info['rigged'] = True
        
        return info
    
    def save_results(self, assets, filename='quaternius_assets.json'):
        """Sonuçları kaydet"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(assets, f, indent=2, ensure_ascii=False)
        print(f"💾 Results saved to {filename}")


# Test the Quaternius scraper
if __name__ == "__main__":
    scraper = IntelligentQuaterniusScraper()
    assets = scraper.scrape_assets(limit=8)
    
    print(f"\n🎯 QUATERNIUS SCRAPING RESULTS")
    print(f"=" * 50)
    print(f"Total assets found: {len(assets)}")
    
    for i, asset in enumerate(assets, 1):
        print(f"\n{i}. {asset['title']}")
        print(f"   Category: {asset['category']}")
        print(f"   Type: {asset['asset_type']}")
        print(f"   License: {asset['license']}")
        print(f"   Poly Count: {asset.get('poly_count', 'unknown')}")
        print(f"   URL: {asset['source_url']}")
        if asset['download_url']:
            print(f"   Download: {asset['download_url'][:60]}...")
        if asset['tags']:
            print(f"   Tags: {', '.join(asset['tags'][:5])}")
    
    if assets:
        scraper.save_results(assets)
        print(f"\n✅ Quaternius scraping completed successfully!")
    else:
        print(f"\n❌ No assets found. Check site structure or patterns.")
