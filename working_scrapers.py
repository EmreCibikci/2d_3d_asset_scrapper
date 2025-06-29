#!/usr/bin/env python3
"""
Working Scrapers - Çalışan scraper'lar için unified sistem
Tüm siteleri deep scraping için optimize eder
"""

import re
import time
import json
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from safe_scraping import SafeScrapingManager

class WorkingBaseScraper:
    """Çalışan base scraper - Abstract değil"""
    
    def __init__(self, site_name: str, base_url: str):
        self.site_name = site_name
        self.base_url = base_url
        self.safe_scraper = SafeScrapingManager()
        
    def scrape(self, limit: int = 50) -> List[Dict]:
        """Ana scraping metodu"""
        return self.scrape_assets(limit)
    
    def scrape_assets(self, limit: int = 50) -> List[Dict]:
        """Override edilecek metod"""
        return []
    
    def get_soup(self, url: str) -> Optional[BeautifulSoup]:
        """URL'den soup al"""
        response = self.safe_scraper.safe_get(url)
        if response:
            return BeautifulSoup(response.content, 'html.parser')
        return None
    
    def determine_category(self, title: str, description: str = "", tags: List[str] = None) -> str:
        """Kategori belirle"""
        text = f"{title} {description}".lower()
        
        if any(word in text for word in ['ui', 'interface', 'button', 'menu', 'hud']):
            return 'ui'
        elif any(word in text for word in ['character', 'player', 'hero', 'sprite']):
            return 'character'
        elif any(word in text for word in ['tile', 'tileset', 'platform']):
            return 'tileset'
        elif any(word in text for word in ['background', 'environment', 'landscape']):
            return 'environment'
        elif any(word in text for word in ['weapon', 'sword', 'gun', 'armor']):
            return 'weapon'
        elif any(word in text for word in ['vehicle', 'car', 'ship', 'plane']):
            return 'vehicle'
        else:
            return 'other'

class WorkingKenneyScraper(WorkingBaseScraper):
    """Çalışan Kenney scraper"""
    
    def __init__(self):
        super().__init__('kenney', 'https://kenney.nl')
        self.assets_url = 'https://kenney.nl/assets'
    
    def scrape_assets(self, limit: int = 50) -> List[Dict]:
        """Kenney asset'lerini deep scraping ile scrape et"""
        assets = []

        print(f"🎯 Kenney.nl deep scraping (limit: {limit})...")

        # 1. Ana sayfa ile başla
        main_assets = self._scrape_main_page()
        assets.extend(main_assets[:limit])

        if len(assets) >= limit:
            return assets[:limit]

        # 2. Kategori sayfaları - Deep scraping
        categories = ['2d', '3d', 'audio', 'ui', 'fonts', 'pixel', 'vector']
        for category in categories:
            if len(assets) >= limit:
                break

            category_assets = self._scrape_category_deep(category, limit - len(assets))
            new_assets = [a for a in category_assets if a['url'] not in [existing['url'] for existing in assets]]
            assets.extend(new_assets)

        # 3. Pagination scraping
        if len(assets) < limit:
            paginated_assets = self._scrape_with_pagination(limit - len(assets))
            new_paginated = [a for a in paginated_assets if a['url'] not in [existing['url'] for existing in assets]]
            assets.extend(new_paginated)

        return assets[:limit]
    
    def _scrape_main_page(self) -> List[Dict]:
        """Ana sayfayı scrape et"""
        assets = []
        
        soup = self.get_soup(self.assets_url)
        if not soup:
            return assets
        
        # Asset linklerini bul
        asset_links = soup.find_all('a', href=re.compile(r'/assets/[^/]+/?$'))
        
        for link in asset_links[:30]:  # İlk 30 link
            asset_url = urljoin(self.base_url, link['href'])
            title = link.get_text(strip=True) or asset_url.split('/')[-1].replace('-', ' ').title()
            
            asset_data = {
                'title': title,
                'url': asset_url,
                'source_site': self.site_name,
                'category': self.determine_category(title),
                'asset_type': '2d',
                'is_free': True,
                'license_info': 'CC0 1.0 Universal',
                'scraped_at': time.time()
            }
            
            assets.append(asset_data)
        
        return assets
    
    def _scrape_category(self, category: str) -> List[Dict]:
        """Kategori sayfasını scrape et"""
        assets = []
        
        category_url = f"{self.assets_url}?q={category}"
        soup = self.get_soup(category_url)
        
        if not soup:
            return assets
        
        asset_links = soup.find_all('a', href=re.compile(r'/assets/[^/]+/?$'))
        
        for link in asset_links[:20]:  # Kategori başına 20 asset
            asset_url = urljoin(self.base_url, link['href'])
            title = link.get_text(strip=True) or asset_url.split('/')[-1].replace('-', ' ').title()
            
            asset_data = {
                'title': title,
                'url': asset_url,
                'source_site': self.site_name,
                'category': self.determine_category(title),
                'asset_type': '3d' if category == '3D' else '2d',
                'is_free': True,
                'license_info': 'CC0 1.0 Universal',
                'scraped_at': time.time()
            }
            
            assets.append(asset_data)
        
        return assets

    def _scrape_category_deep(self, category: str, limit: int) -> List[Dict]:
        """Kategoriyi derin scraping ile tara"""
        assets = []

        # Kenney kategori URL'leri
        category_url = f"{self.assets_url}?q={category}"

        # Sayfalama ile tara
        for page in range(1, 6):  # İlk 5 sayfa
            if len(assets) >= limit:
                break

            page_url = f"{category_url}&page={page}"
            soup = self.get_soup(page_url)

            if not soup:
                break

            # Asset linklerini bul
            asset_links = soup.find_all('a', href=re.compile(r'/assets/[^/]+/?$'))

            if not asset_links:
                break

            for link in asset_links:
                if len(assets) >= limit:
                    break

                asset_url = urljoin(self.base_url, link['href'])

                if asset_url not in getattr(self, 'visited_urls', set()):
                    if not hasattr(self, 'visited_urls'):
                        self.visited_urls = set()
                    self.visited_urls.add(asset_url)

                    title = link.get_text(strip=True) or asset_url.split('/')[-1].replace('-', ' ').title()

                    asset_data = {
                        'title': title,
                        'url': asset_url,
                        'source_site': self.site_name,
                        'category': self.determine_category(title),
                        'asset_type': '2d',
                        'is_free': True,
                        'license_info': 'CC0 1.0 Universal',
                        'scraped_at': time.time()
                    }

                    assets.append(asset_data)

        return assets

    def _scrape_with_pagination(self, limit: int) -> List[Dict]:
        """Sayfalama ile scraping yap"""
        assets = []

        for page in range(1, 11):  # İlk 10 sayfa
            if len(assets) >= limit:
                break

            page_url = f"{self.assets_url}?page={page}"
            soup = self.get_soup(page_url)

            if not soup:
                break

            # Asset linklerini bul
            asset_links = soup.find_all('a', href=re.compile(r'/assets/[^/]+/?$'))

            if not asset_links:
                break

            for link in asset_links:
                if len(assets) >= limit:
                    break

                asset_url = urljoin(self.base_url, link['href'])

                if asset_url not in getattr(self, 'visited_urls', set()):
                    if not hasattr(self, 'visited_urls'):
                        self.visited_urls = set()
                    self.visited_urls.add(asset_url)

                    title = link.get_text(strip=True) or asset_url.split('/')[-1].replace('-', ' ').title()

                    asset_data = {
                        'title': title,
                        'url': asset_url,
                        'source_site': self.site_name,
                        'category': self.determine_category(title),
                        'asset_type': '2d',
                        'is_free': True,
                        'license_info': 'CC0 1.0 Universal',
                        'scraped_at': time.time()
                    }

                    assets.append(asset_data)

        return assets

class WorkingOpenGameArtScraper(WorkingBaseScraper):
    """Çalışan OpenGameArt scraper"""
    
    def __init__(self):
        super().__init__('opengameart', 'https://opengameart.org')
    
    def scrape_assets(self, limit: int = 50) -> List[Dict]:
        """OpenGameArt asset'lerini scrape et"""
        assets = []
        
        print(f"🎯 OpenGameArt.org scraping (limit: {limit})...")
        
        # Farklı kategoriler
        search_urls = [
            "https://opengameart.org/art-search-advanced?field_art_type_tid[]=9",  # 2D
            "https://opengameart.org/art-search-advanced?field_art_type_tid[]=10", # 3D
            "https://opengameart.org/art-search-advanced?field_art_type_tid[]=12"  # Texture
        ]
        
        for search_url in search_urls:
            if len(assets) >= limit:
                break
            
            # Her arama için 2 sayfa
            for page in range(0, 2):
                if len(assets) >= limit:
                    break
                
                page_url = f"{search_url}&page={page}"
                page_assets = self._scrape_search_page(page_url)
                assets.extend(page_assets[:limit - len(assets)])
        
        return assets[:limit]
    
    def _scrape_search_page(self, url: str) -> List[Dict]:
        """Arama sayfasını scrape et"""
        assets = []
        
        soup = self.get_soup(url)
        if not soup:
            return assets
        
        # Asset entries
        entries = soup.find_all('div', class_=['art-preview', 'views-row'])
        
        for entry in entries[:10]:  # Sayfa başına 10 asset
            try:
                # Title
                title_elem = entry.find('h2') or entry.find('a')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                
                # URL
                link_elem = entry.find('a', href=True)
                if not link_elem:
                    continue
                
                asset_url = urljoin(self.base_url, link_elem['href'])
                
                asset_data = {
                    'title': title,
                    'url': asset_url,
                    'source_site': self.site_name,
                    'category': self.determine_category(title),
                    'asset_type': '2d',
                    'is_free': True,
                    'license_info': 'Various Open Licenses',
                    'scraped_at': time.time()
                }
                
                assets.append(asset_data)
                
            except Exception as e:
                continue
        
        return assets

class WorkingItchScraper(WorkingBaseScraper):
    """Çalışan Itch.io scraper"""
    
    def __init__(self):
        super().__init__('itch', 'https://itch.io')
    
    def scrape_assets(self, limit: int = 50) -> List[Dict]:
        """Itch.io asset'lerini scrape et"""
        assets = []
        
        print(f"🎯 Itch.io scraping (limit: {limit})...")
        
        # Farklı kategoriler
        categories = [
            "game-assets/free",
            "game-assets/free?tag=2d",
            "game-assets/free?tag=sprites"
        ]
        
        for category in categories:
            if len(assets) >= limit:
                break
            
            # Her kategori için 2 sayfa
            for page in range(1, 3):
                if len(assets) >= limit:
                    break
                
                page_url = f"https://itch.io/{category}?page={page}"
                page_assets = self._scrape_category_page(page_url)
                assets.extend(page_assets[:limit - len(assets)])
        
        return assets[:limit]
    
    def _scrape_category_page(self, url: str) -> List[Dict]:
        """Kategori sayfasını scrape et"""
        assets = []
        
        soup = self.get_soup(url)
        if not soup:
            return assets
        
        # Game/asset entries
        entries = soup.find_all('div', class_=['game_cell', 'game_link'])
        
        for entry in entries[:8]:  # Sayfa başına 8 asset
            try:
                # Title
                title_elem = entry.find('a', class_='title') or entry.find('a')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                
                # URL
                asset_url = urljoin(self.base_url, title_elem['href'])
                
                asset_data = {
                    'title': title,
                    'url': asset_url,
                    'source_site': self.site_name,
                    'category': self.determine_category(title),
                    'asset_type': '2d',
                    'is_free': True,
                    'license_info': 'Various',
                    'scraped_at': time.time()
                }
                
                assets.append(asset_data)
                
            except Exception as e:
                continue
        
        return assets

# Diğer scraper'lar için placeholder'lar
class WorkingCraftPixScraper(WorkingBaseScraper):
    def __init__(self):
        super().__init__('craftpix', 'https://craftpix.net')
        self.freebies_url = 'https://craftpix.net/freebies'

    def scrape_assets(self, limit: int = 50) -> List[Dict]:
        print(f"🎯 CraftPix.net deep scraping (limit: {limit})...")
        assets = []

        # Ücretsiz kategoriler
        categories = ['freebies', 'free-game-assets', 'free-2d-game-assets']

        for category in categories:
            if len(assets) >= limit:
                break

            # Her kategori için sayfalama
            for page in range(1, 4):
                if len(assets) >= limit:
                    break

                page_url = f"https://craftpix.net/category/{category}/page/{page}/"
                page_assets = self._scrape_craftpix_page(page_url)
                assets.extend(page_assets[:limit - len(assets)])

        return assets[:limit]

    def _scrape_craftpix_page(self, url: str) -> List[Dict]:
        """CraftPix sayfasını scrape et"""
        assets = []

        soup = self.get_soup(url)
        if not soup:
            return assets

        # Asset cards
        cards = soup.find_all('div', class_=['product-item', 'item-product'])

        for card in cards[:8]:
            try:
                # Title
                title_elem = card.find('h3') or card.find('a')
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)

                # URL
                link_elem = card.find('a', href=True)
                if not link_elem:
                    continue

                asset_url = urljoin(self.base_url, link_elem['href'])

                asset_data = {
                    'title': title,
                    'url': asset_url,
                    'source_site': self.site_name,
                    'category': self.determine_category(title),
                    'asset_type': '2d',
                    'is_free': True,
                    'license_info': 'Free for commercial use',
                    'scraped_at': time.time()
                }

                assets.append(asset_data)

            except Exception as e:
                continue

        return assets

class WorkingGameIconsScraper(WorkingBaseScraper):
    def __init__(self):
        super().__init__('gameicons', 'https://game-icons.net')

    def scrape_assets(self, limit: int = 50) -> List[Dict]:
        print(f"🎯 Game-Icons.net deep scraping (limit: {limit})...")
        assets = []

        # Farklı kategoriler
        categories = ['game', 'weapon', 'armor', 'magic', 'creature', 'item']

        for category in categories:
            if len(assets) >= limit:
                break

            category_url = f"https://game-icons.net/tags/{category}.html"
            category_assets = self._scrape_gameicons_category(category_url, category)
            assets.extend(category_assets[:limit - len(assets)])

        return assets[:limit]

    def _scrape_gameicons_category(self, url: str, category: str) -> List[Dict]:
        """Game Icons kategori sayfasını scrape et"""
        assets = []

        soup = self.get_soup(url)
        if not soup:
            return assets

        # Icon elements
        icons = soup.find_all('div', class_='icon')

        for icon in icons[:15]:  # Kategori başına 15 icon
            try:
                # Icon link
                link_elem = icon.find('a', href=True)
                if not link_elem:
                    continue

                icon_url = urljoin(self.base_url, link_elem['href'])

                # Title from URL or alt text
                title = link_elem.get('title') or icon_url.split('/')[-1].replace('.html', '').replace('-', ' ').title()

                asset_data = {
                    'title': f"{title} Icon",
                    'url': icon_url,
                    'source_site': self.site_name,
                    'category': 'ui',
                    'asset_type': '2d',
                    'is_free': True,
                    'license_info': 'CC BY 3.0',
                    'scraped_at': time.time()
                }

                assets.append(asset_data)

            except Exception as e:
                continue

        return assets

class WorkingPixabayScraper(WorkingBaseScraper):
    def __init__(self):
        super().__init__('pixabay', 'https://pixabay.com')

    def scrape_assets(self, limit: int = 50) -> List[Dict]:
        print(f"🎯 Pixabay.com deep scraping (limit: {limit})...")
        assets = []

        # Game-related search terms
        search_terms = ['game sprites', 'game ui', 'pixel art', 'game backgrounds']

        for term in search_terms:
            if len(assets) >= limit:
                break

            # Her terim için 2 sayfa
            for page in range(1, 3):
                if len(assets) >= limit:
                    break

                search_url = f"https://pixabay.com/images/search/{term.replace(' ', '+')}/?pagi={page}"
                page_assets = self._scrape_pixabay_search(search_url)
                assets.extend(page_assets[:limit - len(assets)])

        return assets[:limit]

    def _scrape_pixabay_search(self, url: str) -> List[Dict]:
        """Pixabay arama sayfasını scrape et"""
        assets = []

        soup = self.get_soup(url)
        if not soup:
            return assets

        # Image containers
        containers = soup.find_all('div', class_=['item', 'image-container'])

        for container in containers[:8]:
            try:
                # Image link
                link_elem = container.find('a', href=True)
                if not link_elem:
                    continue

                image_url = urljoin(self.base_url, link_elem['href'])

                # Title from alt or URL
                img_elem = container.find('img')
                title = img_elem.get('alt') if img_elem else image_url.split('/')[-1]

                asset_data = {
                    'title': title,
                    'url': image_url,
                    'source_site': self.site_name,
                    'category': self.determine_category(title),
                    'asset_type': '2d',
                    'is_free': True,
                    'license_info': 'Pixabay License',
                    'scraped_at': time.time()
                }

                assets.append(asset_data)

            except Exception as e:
                continue

        return assets

# Scraper registry
WORKING_SCRAPERS = {
    'kenney': WorkingKenneyScraper,
    'opengameart': WorkingOpenGameArtScraper,
    'itch': WorkingItchScraper,
    'craftpix': WorkingCraftPixScraper,
    'gameicons': WorkingGameIconsScraper,
    'pixabay': WorkingPixabayScraper
}

def test_working_scrapers():
    """Çalışan scraper'ları test et"""
    print("🧪 Working Scrapers Test")
    print("=" * 40)
    
    for name, scraper_class in WORKING_SCRAPERS.items():
        print(f"\n🎯 Testing {name}...")
        
        try:
            scraper = scraper_class()
            assets = scraper.scrape(limit=5)
            
            if assets:
                print(f"  ✅ {name}: {len(assets)} asset")
                for i, asset in enumerate(assets[:3], 1):
                    print(f"    {i}. {asset['title']} ({asset['category']})")
            else:
                print(f"  ⚠️ {name}: Boş sonuç")
                
        except Exception as e:
            print(f"  ❌ {name}: Hata - {e}")

if __name__ == "__main__":
    test_working_scrapers()
