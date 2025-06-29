import os
import requests
import asyncio
import aiohttp
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse
from tqdm import tqdm
import config
from database import DatabaseManager

class AssetDownloader:
    """Handles downloading of assets with progress tracking and resume capability"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.download_dir = config.DOWNLOAD_DIR
        self.session = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=config.REQUEST_TIMEOUT),
            headers={'User-Agent': config.USER_AGENT}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    def download_asset_sync(self, asset_data: Dict) -> bool:
        """Synchronous download method with HTML detection"""
        try:
            download_url = asset_data.get('download_url')
            if not download_url:
                print(f"No download URL for asset: {asset_data['title']}")
                return False

            # Create local file path
            local_path = self._create_local_path(asset_data)

            # Add download record to database
            download_id = self.db.add_download(asset_data['id'], str(local_path))

            # Check if file already exists and is valid
            if local_path.exists():
                if self._is_valid_file(local_path):
                    print(f"Valid file already exists: {local_path}")
                    self.db.complete_download(download_id, True)
                    return True
                else:
                    print(f"Invalid file exists, re-downloading: {local_path}")
                    local_path.unlink()  # Delete invalid file

            # Create directory if it doesn't exist
            local_path.parent.mkdir(parents=True, exist_ok=True)

            # Download the file with better headers
            headers = {
                'User-Agent': config.USER_AGENT,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }

            response = requests.get(
                download_url,
                stream=True,
                headers=headers,
                timeout=config.REQUEST_TIMEOUT,
                allow_redirects=True
            )
            response.raise_for_status()

            # Check if response is HTML (indicates login page or error)
            content_type = response.headers.get('content-type', '').lower()
            if 'text/html' in content_type:
                print(f"Warning: Received HTML instead of file for {asset_data['title']}")
                print(f"URL: {download_url}")
                print(f"Content-Type: {content_type}")
                # Still save it for debugging, but mark as failed

            total_size = int(response.headers.get('content-length', 0))

            with open(local_path, 'wb') as file:
                downloaded = 0
                with tqdm(total=total_size, unit='B', unit_scale=True, desc=asset_data['title'][:50]) as pbar:
                    for chunk in response.iter_content(chunk_size=config.CHUNK_SIZE):
                        if chunk:
                            file.write(chunk)
                            downloaded += len(chunk)
                            pbar.update(len(chunk))

                            # Update progress in database
                            progress = (downloaded / total_size * 100) if total_size > 0 else 0
                            self.db.update_download_progress(download_id, progress, downloaded)

            # Validate downloaded file
            if self._is_valid_file(local_path):
                print(f"Downloaded: {asset_data['title']} -> {local_path}")
                self.db.complete_download(download_id, True)
                return True
            else:
                error_msg = f"Downloaded file is invalid (likely HTML page)"
                print(f"Error: {error_msg}")
                self.db.complete_download(download_id, False, error_msg)
                return False

        except Exception as e:
            print(f"Error downloading {asset_data['title']}: {e}")
            if 'download_id' in locals():
                self.db.complete_download(download_id, False, str(e))
            return False
    
    async def download_asset_async(self, asset_data: Dict) -> bool:
        """Asynchronous download method"""
        try:
            download_url = asset_data.get('download_url')
            if not download_url:
                print(f"No download URL for asset: {asset_data['title']}")
                return False
            
            local_path = self._create_local_path(asset_data)
            download_id = self.db.add_download(asset_data['id'], str(local_path))
            
            if local_path.exists():
                print(f"File already exists: {local_path}")
                self.db.complete_download(download_id, True)
                return True
            
            local_path.parent.mkdir(parents=True, exist_ok=True)
            
            async with self.session.get(download_url) as response:
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                
                with open(local_path, 'wb') as file:
                    downloaded = 0
                    async for chunk in response.content.iter_chunked(config.CHUNK_SIZE):
                        file.write(chunk)
                        downloaded += len(chunk)
                        
                        progress = (downloaded / total_size * 100) if total_size > 0 else 0
                        self.db.update_download_progress(download_id, progress, downloaded)
            
            print(f"Downloaded: {asset_data['title']} -> {local_path}")
            self.db.complete_download(download_id, True)
            return True
            
        except Exception as e:
            print(f"Error downloading {asset_data['title']}: {e}")
            self.db.complete_download(download_id, False, str(e))
            return False
    
    async def download_multiple_assets(self, assets: List[Dict]) -> Dict:
        """Download multiple assets concurrently"""
        semaphore = asyncio.Semaphore(config.MAX_CONCURRENT_DOWNLOADS)
        
        async def download_with_semaphore(asset):
            async with semaphore:
                return await self.download_asset_async(asset)
        
        tasks = [download_with_semaphore(asset) for asset in assets]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        successful = sum(1 for result in results if result is True)
        failed = len(results) - successful
        
        return {
            'total': len(assets),
            'successful': successful,
            'failed': failed
        }
    
    def _create_local_path(self, asset_data: Dict) -> Path:
        """Create local file path for asset"""
        # Create directory structure: downloads/site_name/category/
        site_dir = self.download_dir / asset_data['source_site']
        category_dir = site_dir / asset_data.get('category', 'other')
        
        # Clean filename
        filename = self._clean_filename(asset_data['title'])
        
        # Try to determine file extension from download URL
        download_url = asset_data.get('download_url', '')
        parsed_url = urlparse(download_url)
        url_path = parsed_url.path
        
        if '.' in url_path:
            extension = Path(url_path).suffix
        else:
            # Default to .zip for archives
            extension = '.zip'
        
        if not filename.endswith(extension):
            filename += extension
        
        return category_dir / filename
    
    def _clean_filename(self, filename: str) -> str:
        """Clean filename for filesystem compatibility"""
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Limit length
        if len(filename) > 100:
            filename = filename[:100]
        
        return filename.strip()
    
    def _is_valid_file(self, file_path: Path) -> bool:
        """Check if downloaded file is valid (not HTML)"""
        try:
            if not file_path.exists() or file_path.stat().st_size == 0:
                return False

            # Read first few bytes to check file type
            with open(file_path, 'rb') as f:
                first_bytes = f.read(100)

            # Check if it's HTML
            if b'<html' in first_bytes.lower() or b'<!doctype' in first_bytes.lower():
                return False

            # Check file extension vs content
            file_ext = file_path.suffix.lower()

            if file_ext == '.zip':
                return first_bytes.startswith(b'PK')
            elif file_ext in ['.jpg', '.jpeg']:
                return first_bytes.startswith(b'\xff\xd8\xff')
            elif file_ext == '.png':
                return first_bytes.startswith(b'\x89PNG')
            elif file_ext in ['.gif']:
                return first_bytes.startswith(b'GIF')
            elif file_ext in ['.fbx', '.obj', '.dae']:
                return True  # 3D files are harder to validate
            elif file_ext == '.txt':
                return True
            else:
                # For unknown extensions, just check it's not HTML
                return True

        except Exception:
            return False

    def get_download_stats(self) -> Dict:
        """Get download statistics"""
        return self.db.get_download_stats()
