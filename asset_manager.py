import asyncio
from typing import Dict, List, Optional
from database import DatabaseManager
from downloader import AssetDownloader
from scrapers.craftpix_scraper import CraftPixScraper
from scrapers.kenney_scraper import KenneyScraper
from scrapers.opengameart_scraper import OpenGameArtScraper
from scrapers.itch_scraper import ItchScraper
from scrapers.freepik_scraper import FreepikScraper
from scrapers.gameicons_scraper import GameIconsScraper
from scrapers.pixabay_scraper import PixabayScraper
import config

class AssetManager:
    """Main class for managing asset scraping and downloading"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.scrapers = {
            'craftpix': CraftPixScraper(),
            'kenney': KenneyScraper(),
            'opengameart': OpenGameArtScraper(),
            'itch_io': ItchScraper(),
            'freepik': FreepikScraper(),
            'game_icons': GameIconsScraper(),
            'pixabay': PixabayScraper()
        }
    
    def scrape_site(self, site_name: str, limit: int = None) -> List[Dict]:
        """Scrape assets from a specific site"""
        if site_name not in self.scrapers:
            print(f"Unknown site: {site_name}")
            return []
        
        if not config.SITES_CONFIG.get(site_name, {}).get('enabled', False):
            print(f"Site {site_name} is disabled in config")
            return []
        
        print(f"Starting to scrape {site_name}...")
        self.db.update_site_status(site_name, 'scraping')
        
        try:
            scraper = self.scrapers[site_name]
            assets = scraper.scrape_assets(limit)
            
            # Save assets to database
            saved_count = 0
            for asset_data in assets:
                try:
                    # Get download URL if not already present
                    if not asset_data.get('download_url'):
                        download_url = scraper.get_download_url(asset_data['url'])
                        asset_data['download_url'] = download_url
                    
                    asset_id = self.db.add_asset(asset_data)
                    asset_data['id'] = asset_id
                    saved_count += 1
                    
                except Exception as e:
                    print(f"Error saving asset {asset_data.get('title', 'Unknown')}: {e}")
            
            self.db.update_site_status(site_name, 'completed', saved_count)
            print(f"Scraped {saved_count} assets from {site_name}")
            return assets
            
        except Exception as e:
            error_msg = f"Error scraping {site_name}: {e}"
            print(error_msg)
            self.db.update_site_status(site_name, 'error', error_message=error_msg)
            return []
    
    def scrape_all_sites(self, limit_per_site: int = None) -> Dict[str, List[Dict]]:
        """Scrape assets from all enabled sites"""
        all_assets = {}
        
        for site_name in self.scrapers.keys():
            if config.SITES_CONFIG.get(site_name, {}).get('enabled', False):
                assets = self.scrape_site(site_name, limit_per_site)
                all_assets[site_name] = assets
            else:
                print(f"Skipping disabled site: {site_name}")
        
        return all_assets
    
    def download_assets(self, filters: Dict = None, limit: int = None) -> Dict:
        """Download assets based on filters"""
        # Get assets from database
        assets = self.db.get_assets(filters)
        
        if limit:
            assets = assets[:limit]
        
        if not assets:
            print("No assets found matching the criteria")
            return {'total': 0, 'successful': 0, 'failed': 0}
        
        print(f"Found {len(assets)} assets to download")
        
        # Filter assets that have download URLs
        downloadable_assets = [asset for asset in assets if asset.get('download_url')]
        
        if not downloadable_assets:
            print("No assets have download URLs")
            return {'total': 0, 'successful': 0, 'failed': 0}
        
        print(f"Downloading {len(downloadable_assets)} assets...")
        
        # Use async downloader for better performance
        return asyncio.run(self._download_assets_async(downloadable_assets))
    
    async def _download_assets_async(self, assets: List[Dict]) -> Dict:
        """Async method to download assets"""
        async with AssetDownloader(self.db) as downloader:
            return await downloader.download_multiple_assets(assets)
    
    def download_single_asset(self, asset_id: int) -> bool:
        """Download a single asset by ID"""
        assets = self.db.get_assets({'id': asset_id})
        if not assets:
            print(f"Asset with ID {asset_id} not found")
            return False
        
        asset = assets[0]
        if not asset.get('download_url'):
            print(f"Asset {asset['title']} has no download URL")
            return False
        
        downloader = AssetDownloader(self.db)
        return downloader.download_asset_sync(asset)
    
    def search_assets(self, query: str, filters: Dict = None) -> List[Dict]:
        """Search assets by title or description"""
        all_assets = self.db.get_assets(filters)
        
        query_lower = query.lower()
        matching_assets = []
        
        for asset in all_assets:
            title = asset.get('title', '').lower()
            description = asset.get('description', '').lower()
            tags = asset.get('tags', '[]')
            
            if (query_lower in title or 
                query_lower in description or 
                query_lower in tags):
                matching_assets.append(asset)
        
        return matching_assets
    
    def get_assets_by_category(self, category: str) -> List[Dict]:
        """Get assets by category"""
        return self.db.get_assets({'category': category})
    
    def get_assets_by_type(self, asset_type: str) -> List[Dict]:
        """Get assets by type (2d, 3d, audio)"""
        return self.db.get_assets({'asset_type': asset_type})
    
    def get_assets_by_site(self, site_name: str) -> List[Dict]:
        """Get assets by source site"""
        return self.db.get_assets({'source_site': site_name})
    
    def get_free_assets(self) -> List[Dict]:
        """Get only free assets"""
        return self.db.get_assets({'is_free': True})
    
    def get_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        all_assets = self.db.get_assets()
        download_stats = self.db.get_download_stats()
        
        # Asset statistics
        asset_stats = {
            'total_assets': len(all_assets),
            'by_type': {},
            'by_category': {},
            'by_site': {},
            'free_assets': len([a for a in all_assets if a.get('is_free', True)])
        }
        
        for asset in all_assets:
            # By type
            asset_type = asset.get('asset_type', 'unknown')
            asset_stats['by_type'][asset_type] = asset_stats['by_type'].get(asset_type, 0) + 1
            
            # By category
            category = asset.get('category', 'unknown')
            asset_stats['by_category'][category] = asset_stats['by_category'].get(category, 0) + 1
            
            # By site
            site = asset.get('source_site', 'unknown')
            asset_stats['by_site'][site] = asset_stats['by_site'].get(site, 0) + 1
        
        return {
            'assets': asset_stats,
            'downloads': download_stats
        }
    
    def print_statistics(self):
        """Print formatted statistics"""
        stats = self.get_statistics()
        
        print("\n=== ASSET STATISTICS ===")
        print(f"Total Assets: {stats['assets']['total_assets']}")
        print(f"Free Assets: {stats['assets']['free_assets']}")
        
        print("\nBy Type:")
        for asset_type, count in stats['assets']['by_type'].items():
            print(f"  {asset_type}: {count}")
        
        print("\nBy Category:")
        for category, count in stats['assets']['by_category'].items():
            print(f"  {category}: {count}")
        
        print("\nBy Site:")
        for site, count in stats['assets']['by_site'].items():
            print(f"  {site}: {count}")
        
        print("\n=== DOWNLOAD STATISTICS ===")
        print(f"Total Downloads: {stats['downloads']['total_downloads']}")
        print(f"Completed: {stats['downloads']['completed']}")
        print(f"Failed: {stats['downloads']['failed']}")
        print(f"In Progress: {stats['downloads']['in_progress']}")
