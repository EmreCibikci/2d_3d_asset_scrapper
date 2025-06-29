#!/usr/bin/env python3
"""
Batch operations for asset management
"""

import shutil
from pathlib import Path
from typing import List, Dict
import config
from asset_manager import AssetManager

class BatchOperations:
    """Handle batch operations on assets"""
    
    def __init__(self):
        self.asset_manager = AssetManager()
        self.downloads_dir = Path(config.DOWNLOAD_DIR)
    
    def batch_download_by_criteria(self, criteria: Dict) -> Dict:
        """Download multiple assets based on criteria"""
        print(f"🔍 Finding assets matching criteria: {criteria}")
        
        # Get matching assets
        assets = self.asset_manager.db.get_assets(criteria)
        
        if not assets:
            print("❌ No assets found matching criteria")
            return {'total': 0, 'successful': 0, 'failed': 0}
        
        print(f"📦 Found {len(assets)} matching assets")
        
        # Filter assets that have download URLs
        downloadable_assets = [asset for asset in assets if asset.get('download_url')]
        
        if not downloadable_assets:
            print("❌ No assets have download URLs")
            return {'total': 0, 'successful': 0, 'failed': 0}
        
        print(f"⬇️  Downloading {len(downloadable_assets)} assets...")
        
        # Download assets
        results = self.asset_manager.download_assets(criteria)
        
        print(f"✅ Batch download complete!")
        print(f"   Total: {results['total']}")
        print(f"   Successful: {results['successful']}")
        print(f"   Failed: {results['failed']}")
        
        return results
    
    def batch_organize_files(self) -> Dict:
        """Organize all downloaded files by type and category"""
        if not self.downloads_dir.exists():
            print("❌ Downloads directory not found")
            return {'moved': 0, 'errors': 0}
        
        print("📁 Organizing downloaded files...")
        
        moved_count = 0
        error_count = 0
        
        # Create organized structure
        organized_dir = self.downloads_dir / "organized"
        organized_dir.mkdir(exist_ok=True)
        
        # File type mappings
        file_categories = {
            'images': {
                'extensions': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tga', '.svg'],
                'subcategories': ['sprites', 'textures', 'ui', 'backgrounds']
            },
            'models': {
                'extensions': ['.fbx', '.obj', '.dae', '.blend', '.3ds', '.max', '.ma', '.mb'],
                'subcategories': ['characters', 'environments', 'props', 'vehicles']
            },
            'audio': {
                'extensions': ['.mp3', '.wav', '.ogg', '.m4a', '.flac'],
                'subcategories': ['music', 'sfx', 'voice']
            },
            'archives': {
                'extensions': ['.zip', '.rar', '.7z', '.tar.gz'],
                'subcategories': ['asset_packs', 'tools', 'source']
            }
        }
        
        # Process all files
        for file_path in self.downloads_dir.rglob('*'):
            if (file_path.is_file() and 
                not file_path.name.startswith('thumb_') and
                'organized' not in str(file_path)):
                
                try:
                    # Determine category
                    file_ext = file_path.suffix.lower()
                    category = None
                    
                    for cat_name, cat_info in file_categories.items():
                        if file_ext in cat_info['extensions']:
                            category = cat_name
                            break
                    
                    if not category:
                        category = 'other'
                    
                    # Create category directory
                    category_dir = organized_dir / category
                    category_dir.mkdir(exist_ok=True)
                    
                    # Determine subcategory based on file name/path
                    subcategory = self._determine_subcategory(file_path, category, file_categories)
                    
                    if subcategory:
                        target_dir = category_dir / subcategory
                    else:
                        target_dir = category_dir
                    
                    target_dir.mkdir(exist_ok=True)
                    
                    # Move file
                    target_path = target_dir / file_path.name
                    if not target_path.exists():
                        shutil.copy2(file_path, target_path)
                        moved_count += 1
                        print(f"📁 Moved: {file_path.name} -> {category}/{subcategory or ''}")
                
                except Exception as e:
                    print(f"❌ Error moving {file_path.name}: {e}")
                    error_count += 1
        
        print(f"\n📊 Organization complete!")
        print(f"   Files moved: {moved_count}")
        print(f"   Errors: {error_count}")
        
        return {'moved': moved_count, 'errors': error_count}
    
    def _determine_subcategory(self, file_path: Path, category: str, file_categories: Dict) -> str:
        """Determine subcategory based on file name and path"""
        file_name_lower = file_path.name.lower()
        path_lower = str(file_path.parent).lower()
        
        # Keywords for subcategorization
        keywords = {
            'images': {
                'sprites': ['sprite', 'character', 'player', 'enemy', 'npc'],
                'textures': ['texture', 'material', 'surface', 'pattern'],
                'ui': ['ui', 'button', 'icon', 'menu', 'interface', 'hud'],
                'backgrounds': ['background', 'bg', 'landscape', 'sky', 'environment']
            },
            'models': {
                'characters': ['character', 'player', 'enemy', 'npc', 'human', 'creature'],
                'environments': ['building', 'house', 'tree', 'rock', 'terrain', 'landscape'],
                'props': ['prop', 'furniture', 'object', 'item', 'tool'],
                'vehicles': ['car', 'vehicle', 'ship', 'plane', 'bike', 'truck']
            },
            'audio': {
                'music': ['music', 'song', 'track', 'theme', 'bgm'],
                'sfx': ['sfx', 'sound', 'effect', 'noise', 'impact'],
                'voice': ['voice', 'speech', 'talk', 'dialogue']
            }
        }
        
        if category in keywords:
            for subcategory, subcat_keywords in keywords[category].items():
                for keyword in subcat_keywords:
                    if keyword in file_name_lower or keyword in path_lower:
                        return subcategory
        
        return None
    
    def batch_cleanup(self) -> Dict:
        """Clean up duplicate and invalid files"""
        if not self.downloads_dir.exists():
            return {'removed': 0, 'errors': 0}
        
        print("🧹 Cleaning up downloads...")
        
        removed_count = 0
        error_count = 0
        
        # Find and remove duplicate files
        file_hashes = {}
        duplicates = []
        
        for file_path in self.downloads_dir.rglob('*'):
            if file_path.is_file() and not file_path.name.startswith('thumb_'):
                try:
                    # Simple duplicate detection by size and name
                    file_key = (file_path.name, file_path.stat().st_size)
                    
                    if file_key in file_hashes:
                        duplicates.append(file_path)
                        print(f"🔍 Found duplicate: {file_path.name}")
                    else:
                        file_hashes[file_key] = file_path
                
                except Exception as e:
                    print(f"❌ Error checking {file_path.name}: {e}")
                    error_count += 1
        
        # Remove duplicates
        for duplicate_path in duplicates:
            try:
                duplicate_path.unlink()
                removed_count += 1
                print(f"🗑️  Removed duplicate: {duplicate_path.name}")
            except Exception as e:
                print(f"❌ Error removing {duplicate_path.name}: {e}")
                error_count += 1
        
        # Remove empty directories
        for dir_path in self.downloads_dir.rglob('*'):
            if dir_path.is_dir():
                try:
                    if not any(dir_path.iterdir()):
                        dir_path.rmdir()
                        print(f"📁 Removed empty directory: {dir_path.name}")
                except Exception:
                    pass  # Directory not empty or other error
        
        print(f"\n📊 Cleanup complete!")
        print(f"   Files removed: {removed_count}")
        print(f"   Errors: {error_count}")
        
        return {'removed': removed_count, 'errors': error_count}
    
    def batch_generate_metadata(self) -> Dict:
        """Generate metadata files for all assets"""
        if not self.downloads_dir.exists():
            return {'generated': 0, 'errors': 0}
        
        print("📝 Generating metadata files...")
        
        generated_count = 0
        error_count = 0
        
        for file_path in self.downloads_dir.rglob('*'):
            if (file_path.is_file() and 
                not file_path.name.startswith('thumb_') and
                not file_path.name.endswith('.meta')):
                
                try:
                    # Create metadata file
                    meta_path = file_path.with_suffix(file_path.suffix + '.meta')
                    
                    if not meta_path.exists():
                        metadata = self._generate_file_metadata(file_path)
                        
                        with open(meta_path, 'w', encoding='utf-8') as f:
                            f.write(metadata)
                        
                        generated_count += 1
                        print(f"📝 Generated metadata: {file_path.name}.meta")
                
                except Exception as e:
                    print(f"❌ Error generating metadata for {file_path.name}: {e}")
                    error_count += 1
        
        print(f"\n📊 Metadata generation complete!")
        print(f"   Files generated: {generated_count}")
        print(f"   Errors: {error_count}")
        
        return {'generated': generated_count, 'errors': error_count}
    
    def _generate_file_metadata(self, file_path: Path) -> str:
        """Generate metadata content for a file"""
        try:
            stat = file_path.stat()
            size_mb = stat.st_size / (1024 * 1024)
            
            metadata = f"""# Asset Metadata
File: {file_path.name}
Size: {size_mb:.2f} MB
Type: {file_path.suffix.upper()[1:] if file_path.suffix else 'Unknown'}
Created: {stat.st_ctime}
Modified: {stat.st_mtime}
Path: {file_path}

# Tags
# Add your custom tags here

# Notes
# Add your notes here
"""
            return metadata
            
        except Exception as e:
            return f"# Error generating metadata: {e}"

def main():
    """Main function"""
    batch_ops = BatchOperations()
    
    print("Batch Operations Manager")
    print("=" * 30)
    print("1. Download assets by type")
    print("2. Download assets by site")
    print("3. Download assets by category")
    print("4. Organize all files")
    print("5. Cleanup duplicates")
    print("6. Generate metadata")
    print("7. Full maintenance (organize + cleanup + metadata)")
    
    choice = input("\nSelect option (1-7): ").strip()
    
    if choice == "1":
        asset_type = input("Enter asset type (2d/3d/audio): ").strip()
        batch_ops.batch_download_by_criteria({'asset_type': asset_type})
    
    elif choice == "2":
        site = input("Enter site name (kenney/opengameart/craftpix): ").strip()
        batch_ops.batch_download_by_criteria({'source_site': site})
    
    elif choice == "3":
        category = input("Enter category: ").strip()
        batch_ops.batch_download_by_criteria({'category': category})
    
    elif choice == "4":
        batch_ops.batch_organize_files()
    
    elif choice == "5":
        batch_ops.batch_cleanup()
    
    elif choice == "6":
        batch_ops.batch_generate_metadata()
    
    elif choice == "7":
        print("🚀 Running full maintenance...")
        batch_ops.batch_organize_files()
        batch_ops.batch_cleanup()
        batch_ops.batch_generate_metadata()
        print("✅ Full maintenance complete!")
    
    else:
        print("Invalid choice!")

if __name__ == '__main__':
    main()
