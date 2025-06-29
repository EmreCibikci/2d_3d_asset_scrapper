#!/usr/bin/env python3
"""
2D/3D Asset Downloader
Ücretsiz 2D ve 3D asset'leri çeşitli sitelerden indiren Python uygulaması
"""

import argparse
import sys
from asset_manager import AssetManager
import config

def main():
    parser = argparse.ArgumentParser(description='2D/3D Asset Downloader')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Scrape command
    scrape_parser = subparsers.add_parser('scrape', help='Scrape assets from websites')
    scrape_parser.add_argument('--site', choices=['craftpix', 'kenney', 'opengameart', 'all'], 
                              default='all', help='Site to scrape')
    scrape_parser.add_argument('--limit', type=int, help='Limit number of assets per site')
    
    # Download command
    download_parser = subparsers.add_parser('download', help='Download assets')
    download_parser.add_argument('--type', choices=['2d', '3d', 'audio'], help='Asset type filter')
    download_parser.add_argument('--category', help='Asset category filter')
    download_parser.add_argument('--site', help='Source site filter')
    download_parser.add_argument('--limit', type=int, help='Limit number of downloads')
    download_parser.add_argument('--id', type=int, help='Download specific asset by ID')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search assets')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--type', choices=['2d', '3d', 'audio'], help='Asset type filter')
    search_parser.add_argument('--category', help='Asset category filter')
    search_parser.add_argument('--site', help='Source site filter')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List assets')
    list_parser.add_argument('--type', choices=['2d', '3d', 'audio'], help='Asset type filter')
    list_parser.add_argument('--category', help='Asset category filter')
    list_parser.add_argument('--site', help='Source site filter')
    list_parser.add_argument('--limit', type=int, default=20, help='Limit number of results')
    
    # Stats command
    subparsers.add_parser('stats', help='Show statistics')
    
    # Interactive command
    subparsers.add_parser('interactive', help='Start interactive mode')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    asset_manager = AssetManager()
    
    try:
        if args.command == 'scrape':
            handle_scrape_command(asset_manager, args)
        elif args.command == 'download':
            handle_download_command(asset_manager, args)
        elif args.command == 'search':
            handle_search_command(asset_manager, args)
        elif args.command == 'list':
            handle_list_command(asset_manager, args)
        elif args.command == 'stats':
            asset_manager.print_statistics()
        elif args.command == 'interactive':
            interactive_mode(asset_manager)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Error: {e}")

def handle_scrape_command(asset_manager, args):
    """Handle scrape command"""
    if args.site == 'all':
        print("Scraping all enabled sites...")
        results = asset_manager.scrape_all_sites(args.limit)
        
        total_assets = sum(len(assets) for assets in results.values())
        print(f"\nScraping completed! Total assets found: {total_assets}")
        
        for site, assets in results.items():
            print(f"  {site}: {len(assets)} assets")
    else:
        print(f"Scraping {args.site}...")
        assets = asset_manager.scrape_site(args.site, args.limit)
        print(f"Found {len(assets)} assets from {args.site}")

def handle_download_command(asset_manager, args):
    """Handle download command"""
    if args.id:
        # Download specific asset
        success = asset_manager.download_single_asset(args.id)
        if success:
            print(f"Asset {args.id} downloaded successfully")
        else:
            print(f"Failed to download asset {args.id}")
        return
    
    # Build filters
    filters = {}
    if args.type:
        filters['asset_type'] = args.type
    if args.category:
        filters['category'] = args.category
    if args.site:
        filters['source_site'] = args.site
    
    # Download assets
    results = asset_manager.download_assets(filters, args.limit)
    print(f"\nDownload completed!")
    print(f"Total: {results['total']}")
    print(f"Successful: {results['successful']}")
    print(f"Failed: {results['failed']}")

def handle_search_command(asset_manager, args):
    """Handle search command"""
    filters = {}
    if args.type:
        filters['asset_type'] = args.type
    if args.category:
        filters['category'] = args.category
    if args.site:
        filters['source_site'] = args.site
    
    assets = asset_manager.search_assets(args.query, filters)
    
    print(f"Found {len(assets)} assets matching '{args.query}':")
    for asset in assets[:20]:  # Show first 20 results
        print(f"  [{asset['id']}] {asset['title']} ({asset['source_site']}) - {asset['asset_type']}/{asset['category']}")

def handle_list_command(asset_manager, args):
    """Handle list command"""
    filters = {}
    if args.type:
        filters['asset_type'] = args.type
    if args.category:
        filters['category'] = args.category
    if args.site:
        filters['source_site'] = args.site
    
    assets = asset_manager.db.get_assets(filters)
    
    print(f"Found {len(assets)} assets:")
    for asset in assets[:args.limit]:
        print(f"  [{asset['id']}] {asset['title']} ({asset['source_site']}) - {asset['asset_type']}/{asset['category']}")

def interactive_mode(asset_manager):
    """Interactive mode for easier usage"""
    print("=== 2D/3D Asset Downloader - Interactive Mode ===")
    print("Commands: scrape, download, search, list, stats, help, quit")
    
    while True:
        try:
            command = input("\n> ").strip().lower()
            
            if command == 'quit' or command == 'exit':
                break
            elif command == 'help':
                print_interactive_help()
            elif command == 'stats':
                asset_manager.print_statistics()
            elif command.startswith('scrape'):
                handle_interactive_scrape(asset_manager, command)
            elif command.startswith('download'):
                handle_interactive_download(asset_manager, command)
            elif command.startswith('search'):
                handle_interactive_search(asset_manager, command)
            elif command.startswith('list'):
                handle_interactive_list(asset_manager, command)
            else:
                print("Unknown command. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\nUse 'quit' to exit")
        except Exception as e:
            print(f"Error: {e}")

def print_interactive_help():
    """Print help for interactive mode"""
    print("""
Available commands:
  scrape [site]           - Scrape assets (site: craftpix, kenney, opengameart, all)
  download [type]         - Download assets (type: 2d, 3d, audio)
  search <query>          - Search assets by name
  list [type]             - List assets
  stats                   - Show statistics
  help                    - Show this help
  quit                    - Exit program
    """)

def handle_interactive_scrape(asset_manager, command):
    """Handle interactive scrape command"""
    parts = command.split()
    site = parts[1] if len(parts) > 1 else 'all'
    
    if site == 'all':
        results = asset_manager.scrape_all_sites(50)  # Limit to 50 per site in interactive mode
        total = sum(len(assets) for assets in results.values())
        print(f"Scraped {total} assets from all sites")
    else:
        assets = asset_manager.scrape_site(site, 50)
        print(f"Scraped {len(assets)} assets from {site}")

def handle_interactive_download(asset_manager, command):
    """Handle interactive download command"""
    parts = command.split()
    asset_type = parts[1] if len(parts) > 1 else None
    
    filters = {}
    if asset_type:
        filters['asset_type'] = asset_type
    
    results = asset_manager.download_assets(filters, 10)  # Limit to 10 in interactive mode
    print(f"Downloaded {results['successful']}/{results['total']} assets")

def handle_interactive_search(asset_manager, command):
    """Handle interactive search command"""
    parts = command.split(maxsplit=1)
    if len(parts) < 2:
        print("Usage: search <query>")
        return
    
    query = parts[1]
    assets = asset_manager.search_assets(query)
    
    print(f"Found {len(assets)} assets:")
    for asset in assets[:10]:
        print(f"  [{asset['id']}] {asset['title']} - {asset['asset_type']}/{asset['category']}")

def handle_interactive_list(asset_manager, command):
    """Handle interactive list command"""
    parts = command.split()
    asset_type = parts[1] if len(parts) > 1 else None
    
    filters = {}
    if asset_type:
        filters['asset_type'] = asset_type
    
    assets = asset_manager.db.get_assets(filters)
    
    print(f"Found {len(assets)} assets:")
    for asset in assets[:10]:
        print(f"  [{asset['id']}] {asset['title']} - {asset['asset_type']}/{asset['category']}")

if __name__ == '__main__':
    main()
