"""
Enhanced secure scraper for PixelJoint.com pixel art community with advanced bot protection
"""

import re
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from .enhanced_base_scraper import EnhancedBaseScraper
import config

class PixelJointScraper(EnhancedBaseScraper):
    """Enhanced secure scraper for PixelJoint.com pixel art community"""
    
    def __init__(self):
        super().__init__('pixeljoint', enable_advanced_security=True)
        self.base_url = 'http://pixeljoint.com'
        self.gallery_url = 'http://pixeljoint.com/pixels/new_icons.asp'
        
    def scrape_assets(self, limit: int = None) -> List[Dict]:
        """Scrape pixel art from PixelJoint"""
        assets = []
        
        try:
            print(f"🔍 Starting PixelJoint scraping (limit: {limit or 'unlimited'})")
            
            # Start with gallery page
            soup = self.get_soup(self.gallery_url)
            if not soup:
                print("❌ Failed to load PixelJoint gallery page")
                return assets
            
            # Find pixel art links
            pixel_links = self._find_pixel_links(soup)
            
            print(f"🎨 Found {len(pixel_links)} pixel art links")
            
            for i, pixel_link in enumerate(pixel_links):
                if limit and len(assets) >= limit:
                    break
                
                try:
                    asset_data = self._extract_pixel_data(pixel_link)
                    if asset_data:
                        assets.append(asset_data)
                        print(f"✅ Extracted: {asset_data['title'][:50]}...")
                    
                except Exception as e:
                    print(f"⚠️ Error extracting pixel art {i+1}: {e}")
                    continue
            
            # Try additional gallery pages
            if not limit or len(assets) < limit:
                additional_assets = self._scrape_additional_pages(limit - len(assets) if limit else None)
                assets.extend(additional_assets)
            
            # Log security statistics
            stats = self.get_stats()
            if stats['bot_detections'] > 0:
                print(f"⚠️ Bot protection encountered {stats['bot_detections']} times")
            print(f"📊 Success rate: {stats['success_rate']:.1%} ({stats['successful_requests']}/{stats['requests_made']} requests)")
            
        except Exception as e:
            print(f"💥 PixelJoint scraping failed: {e}")
        
        return assets
    
    def _find_pixel_links(self, soup) -> List[str]:
        """Find pixel art page links"""
        pixel_links = []
        
        # Look for pixel art links in gallery
        link_selectors = [
            'a[href*="pixel"]',
            'a[href*="icon"]',
            'a[href*="view"]',
            '.pixel-link',
            '.icon-link'
        ]
        
        for selector in link_selectors:
            links = soup.select(selector)
            for link in links:
                href = link.get('href')
                if href:
                    full_url = urljoin(self.base_url, href)
                    if full_url not in pixel_links:
                        pixel_links.append(full_url)
        
        # Look for image links that might lead to pixel art
        all_links = soup.find_all('a', href=True)
        for link in all_links:
            href = link.get('href')
            if href:
                # Check for pixel art related URLs
                if any(keyword in href.lower() for keyword in ['pixel', 'icon', 'view', 'art']):
                    full_url = urljoin(self.base_url, href)
                    if full_url not in pixel_links and self.base_url in full_url:
                        pixel_links.append(full_url)
        
        return pixel_links[:40]  # Limit to avoid overwhelming
    
    def _extract_pixel_data(self, pixel_url: str) -> Optional[Dict]:
        """Extract pixel art data from individual page"""
        soup = self.get_soup(pixel_url)
        if not soup:
            return None
        
        # Extract title
        title = self._extract_title(soup)
        if not title:
            return None
        
        # Extract other data
        description = self._extract_description(soup)
        image_url = self._extract_image_url(soup, pixel_url)
        artist = self._extract_artist(soup)
        tags = self._extract_tags(soup)
        
        # Skip if no image found
        if not image_url:
            return None
        
        # Determine category
        category = self.determine_category(title, description or '', tags)
        
        return {
            'title': title,
            'description': description or '',
            'download_url': image_url,  # Direct image URL
            'preview_image': image_url,
            'source_url': pixel_url,
            'site': 'pixeljoint',
            'license': 'various',  # PixelJoint has various licenses
            'tags': tags + ['pixel-art', '2d'],
            'asset_type': '2d',
            'category': category,
            'artist': artist,
            'file_size': 'unknown',
            'format': self._guess_format_from_url(image_url)
        }
    
    def _extract_title(self, soup) -> Optional[str]:
        """Extract pixel art title"""
        title_selectors = [
            'h1',
            'h2',
            '.title',
            '.pixel-title',
            '.art-title',
            '[class*="title"]'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                title = element.get_text(strip=True)
                if title and len(title) > 2:
                    return title
        
        # Look for title in page structure
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text(strip=True)
            # Clean up common suffixes
            title = re.sub(r'\s*[-|]\s*PixelJoint.*$', '', title, flags=re.IGNORECASE)
            title = re.sub(r'\s*[-|]\s*Pixel Art.*$', '', title, flags=re.IGNORECASE)
            if title and len(title) > 2:
                return title
        
        # Fallback: extract from URL or image alt text
        images = soup.find_all('img', alt=True)
        for img in images:
            alt = img.get('alt', '').strip()
            if alt and len(alt) > 2 and 'pixel' not in alt.lower():
                return alt
        
        return None
    
    def _extract_description(self, soup) -> Optional[str]:
        """Extract pixel art description"""
        desc_selectors = [
            '.description',
            '.content',
            '.pixel-description',
            '.art-description',
            'p'
        ]
        
        for selector in desc_selectors:
            element = soup.select_one(selector)
            if element:
                desc = element.get_text(strip=True)
                if desc and len(desc) > 5:
                    return desc[:300]  # Limit description length
        
        return None
    
    def _extract_image_url(self, soup, pixel_url: str) -> Optional[str]:
        """Extract the main pixel art image URL"""
        # Look for the main pixel art image
        img_selectors = [
            'img[src*="pixel"]',
            'img[src*="icon"]',
            'img[src*="art"]',
            '.pixel-image img',
            '.main-image img',
            '.art-image img'
        ]
        
        for selector in img_selectors:
            element = soup.select_one(selector)
            if element:
                src = element.get('src')
                if src:
                    # Check if it's a valid image
                    if any(ext in src.lower() for ext in ['.png', '.gif', '.jpg', '.jpeg']):
                        return urljoin(pixel_url, src)
        
        # Look for any image that might be the pixel art
        all_images = soup.find_all('img', src=True)
        for img in all_images:
            src = img.get('src')
            if src:
                # Skip common UI elements
                if any(skip in src.lower() for skip in ['logo', 'banner', 'button', 'icon', 'avatar']):
                    continue
                
                # Check for image extensions
                if any(ext in src.lower() for ext in ['.png', '.gif', '.jpg', '.jpeg']):
                    return urljoin(pixel_url, src)
        
        return None
    
    def _extract_artist(self, soup) -> Optional[str]:
        """Extract artist name"""
        artist_selectors = [
            '.artist',
            '.author',
            '.creator',
            '.by',
            '[class*="artist"]',
            '[class*="author"]'
        ]
        
        for selector in artist_selectors:
            element = soup.select_one(selector)
            if element:
                artist = element.get_text(strip=True)
                if artist and len(artist) > 1:
                    return artist
        
        # Look for "by [artist]" patterns in text
        text_content = soup.get_text()
        artist_match = re.search(r'by\s+([A-Za-z0-9_-]+)', text_content, re.IGNORECASE)
        if artist_match:
            return artist_match.group(1)
        
        return None
    
    def _extract_tags(self, soup) -> List[str]:
        """Extract tags/keywords"""
        tags = []
        
        tag_selectors = [
            '.tags a',
            '.categories a',
            '.keywords',
            '[class*="tag"]'
        ]
        
        for selector in tag_selectors:
            elements = soup.select(selector)
            for element in elements:
                tag = element.get_text(strip=True)
                if tag and tag not in tags:
                    tags.append(tag)
        
        # Extract from meta keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            keywords = meta_keywords.get('content', '')
            for keyword in keywords.split(','):
                keyword = keyword.strip()
                if keyword and keyword not in tags:
                    tags.append(keyword)
        
        # Add common pixel art tags based on content
        content_text = soup.get_text().lower()
        pixel_keywords = ['sprite', 'character', 'tile', 'animation', 'game', 'retro', '8bit', '16bit']
        for keyword in pixel_keywords:
            if keyword in content_text and keyword not in tags:
                tags.append(keyword)
        
        return tags[:8]  # Limit to 8 tags
    
    def _guess_format_from_url(self, url: str) -> str:
        """Guess file format from URL"""
        if not url:
            return 'unknown'
        
        url_lower = url.lower()
        
        if '.png' in url_lower:
            return 'png'
        elif '.gif' in url_lower:
            return 'gif'
        elif '.jpg' in url_lower or '.jpeg' in url_lower:
            return 'jpeg'
        else:
            return 'png'  # Default for pixel art
    
    def _scrape_additional_pages(self, remaining_limit: Optional[int]) -> List[Dict]:
        """Scrape additional gallery pages"""
        additional_assets = []
        
        # Try different gallery pages
        gallery_pages = [
            'http://pixeljoint.com/pixels/new_icons.asp?pg=2',
            'http://pixeljoint.com/pixels/new_icons.asp?pg=3',
            'http://pixeljoint.com/gallery/gallery.asp'
        ]
        
        for page_url in gallery_pages:
            if remaining_limit and len(additional_assets) >= remaining_limit:
                break
            
            try:
                soup = self.get_soup(page_url)
                if soup:
                    pixel_links = self._find_pixel_links(soup)
                    
                    for pixel_link in pixel_links:
                        if remaining_limit and len(additional_assets) >= remaining_limit:
                            break
                        
                        try:
                            asset_data = self._extract_pixel_data(pixel_link)
                            if asset_data:
                                additional_assets.append(asset_data)
                        except Exception as e:
                            continue
                            
            except Exception as e:
                print(f"⚠️ Error scraping additional page {page_url}: {e}")
                continue
        
        return additional_assets
    
    def get_download_url(self, asset_url: str) -> Optional[str]:
        """Get direct download URL for a pixel art"""
        soup = self.get_soup(asset_url)
        if soup:
            return self._extract_image_url(soup, asset_url)
        return None
