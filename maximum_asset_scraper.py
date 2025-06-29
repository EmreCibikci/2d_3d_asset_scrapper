#!/usr/bin/env python3
"""
Maximum Asset Scraper
Her siteden alabileceğimiz maksimum asset'i al
Hedef yok, sadece maksimum toplama
"""

import time
import json
from datetime import datetime
from typing import Dict, List

class MaximumAssetScraper:
    """Her siteden maksimum asset toplayan scraper"""
    
    def __init__(self):
        # Maksimum asset configuration - limit yok!
        self.scrapers = {
            'kenney': {
                'class': 'WorkingKenneyScraper',
                'module': 'working_scrapers',
                'limit': None,  # Maksimum
                'priority': 1,
                'status': 'ready',
                'type': 'working'
            },
            'opengameart': {
                'class': 'WorkingOpenGameArtScraper',
                'module': 'working_scrapers',
                'limit': None,  # Maksimum
                'priority': 2,
                'status': 'ready',
                'type': 'working'
            },
            'craftpix': {
                'class': 'UltraIntelligentCraftPixScraper',
                'module': 'ultra_intelligent_craftpix_scraper',
                'limit': None,  # Maksimum
                'priority': 3,
                'status': 'ready',
                'type': 'ultra_intelligent'
            },
            'gameicons': {
                'class': 'WorkingGameIconsScraper',
                'module': 'working_scrapers',
                'limit': None,  # Maksimum
                'priority': 4,
                'status': 'ready',
                'type': 'working'
            }
        }
        
        self.results = {}
        self.start_time = None
        
    def initialize_scrapers(self):
        """Initialize maximum scrapers"""
        print("🚀 MAXIMUM ASSET SCRAPER INITIALIZATION")
        print("=" * 60)
        print("Hedef: Her siteden maksimum asset")
        print("Limit: YOK - Ne kadar varsa o kadar!")
        print()
        
        initialized = {}
        
        for name, config in self.scrapers.items():
            try:
                print(f"🔧 Initializing {name}...")
                
                # Dynamic import
                module = __import__(config['module'])
                scraper_class = getattr(module, config['class'])
                scraper_instance = scraper_class()
                
                initialized[name] = {
                    'scraper': scraper_instance,
                    'config': config,
                    'status': 'ready'
                }
                
                print(f"  ✅ {name}: {config['type']} scraper ready (MAKSIMUM)")
                
            except Exception as e:
                print(f"  ❌ {name}: Failed to initialize - {e}")
                initialized[name] = {
                    'scraper': None,
                    'config': config,
                    'status': 'failed',
                    'error': str(e)
                }
        
        return initialized
    
    def scrape_maximum_assets(self, name: str, scraper_data: Dict) -> Dict:
        """Maksimum asset scraping"""
        print(f"\n🎯 Starting {name} MAXIMUM scraping...")
        print(f"   Target: MAKSIMUM ASSET (limit yok)")
        
        start_time = time.time()
        
        try:
            scraper = scraper_data['scraper']
            
            # Maksimum asset için büyük limit
            max_limit = 50000  # Çok büyük limit
            
            # Use appropriate scraping method
            if scraper_data['config']['type'] == 'ultra_intelligent':
                print(f"   🧠 Ultra intelligent mode: Maksimum asset arayışı")
                assets = scraper.analyze_and_scrape(limit=max_limit)
            else:
                print(f"   🔄 Working scraper mode: Deep maksimum scraping")
                assets = scraper.scrape(limit=max_limit)
            
            end_time = time.time()
            duration = end_time - start_time
            
            result = {
                'site': name,
                'status': 'success',
                'assets_found': len(assets),
                'duration_seconds': duration,
                'duration_minutes': duration / 60,
                'assets_per_minute': len(assets) / (duration / 60) if duration > 0 else 0,
                'assets': assets,
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"  ✅ {name}: {len(assets):,} assets in {duration/60:.1f} minutes")
            print(f"     Rate: {result['assets_per_minute']:.1f} assets/minute")
            
            return result
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            
            result = {
                'site': name,
                'status': 'error',
                'assets_found': 0,
                'duration_seconds': duration,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"  ❌ {name}: Error - {e}")
            return result
    
    def run_maximum_scraping(self):
        """Run maximum asset scraping"""
        print("\n🚀 STARTING MAXIMUM ASSET SCRAPING")
        print("=" * 80)
        print("Her siteden alabileceğimiz maksimum asset'i topluyoruz!")
        
        self.start_time = time.time()
        
        # Initialize scrapers
        initialized_scrapers = self.initialize_scrapers()
        
        # Filter ready scrapers
        ready_scrapers = {
            name: data for name, data in initialized_scrapers.items()
            if data['status'] == 'ready'
        }
        
        print(f"\n✅ Ready scrapers: {len(ready_scrapers)}")
        print(f"🎯 Hedef: MAKSIMUM ASSET (limit yok)")
        print()
        
        # Sequential maximum scraping
        for i, (name, scraper_data) in enumerate(ready_scrapers.items(), 1):
            print(f"\n📊 Scraper {i}/{len(ready_scrapers)}: {name.upper()}")
            
            result = self.scrape_maximum_assets(name, scraper_data)
            self.results[name] = result
            
            # Save intermediate results
            self._save_intermediate_results()
            
            # Show running total
            total_so_far = sum(r.get('assets_found', 0) for r in self.results.values())
            print(f"\n📈 Running Total: {total_so_far:,} assets")
            
            # Brief pause between scrapers
            if i < len(ready_scrapers):  # Not last scraper
                print("   ⏱️ Brief pause before next scraper...")
                time.sleep(30)
        
        # Generate final report
        self._generate_final_report()
    
    def _save_intermediate_results(self):
        """Save intermediate results"""
        filename = f"maximum_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
    
    def _generate_final_report(self):
        """Generate comprehensive final report"""
        end_time = time.time()
        total_duration = end_time - self.start_time
        
        print("\n📊 MAXIMUM ASSET SCRAPING COMPLETED")
        print("=" * 80)
        
        total_assets = sum(result.get('assets_found', 0) for result in self.results.values())
        successful_scrapers = sum(1 for result in self.results.values() if result.get('status') == 'success')
        
        print(f"🎯 Total Assets Collected: {total_assets:,}")
        print(f"✅ Successful Scrapers: {successful_scrapers}/{len(self.results)}")
        print(f"⏱️ Total Duration: {total_duration/60:.1f} minutes")
        print(f"📈 Average Rate: {total_assets/(total_duration/60):.1f} assets/minute")
        print()
        
        # Individual scraper results
        print("📋 INDIVIDUAL SCRAPER RESULTS:")
        print("-" * 80)
        
        # Sort by assets found (descending)
        sorted_results = sorted(
            self.results.items(), 
            key=lambda x: x[1].get('assets_found', 0), 
            reverse=True
        )
        
        for name, result in sorted_results:
            status_icon = "✅" if result.get('status') == 'success' else "❌"
            assets = result.get('assets_found', 0)
            duration = result.get('duration_minutes', 0)
            rate = result.get('assets_per_minute', 0)
            
            print(f"{status_icon} {name.upper()}")
            print(f"   Assets: {assets:,}")
            print(f"   Duration: {duration:.1f} minutes")
            print(f"   Rate: {rate:.1f} assets/minute")
            
            if result.get('status') == 'error':
                print(f"   Error: {result.get('error', 'Unknown')}")
            print()
        
        # Save final results
        final_filename = f"maximum_final_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        final_report = {
            'summary': {
                'total_assets': total_assets,
                'successful_scrapers': successful_scrapers,
                'total_scrapers': len(self.results),
                'total_duration_minutes': total_duration/60,
                'average_rate_per_minute': total_assets/(total_duration/60) if total_duration > 0 else 0,
                'start_time': datetime.fromtimestamp(self.start_time).isoformat(),
                'end_time': datetime.fromtimestamp(end_time).isoformat()
            },
            'individual_results': self.results
        }
        
        with open(final_filename, 'w', encoding='utf-8') as f:
            json.dump(final_report, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Final report saved: {final_filename}")
        
        # Success message
        if total_assets >= 1000:
            print("\n🎉 MAXIMUM SCRAPING SUCCESSFUL!")
            print(f"✅ {total_assets:,} assets collected!")
        elif total_assets >= 500:
            print("\n✅ MAXIMUM SCRAPING PARTIALLY SUCCESSFUL")
            print(f"🎯 {total_assets:,} assets collected")
        else:
            print("\n⚠️ MAXIMUM SCRAPING NEEDS IMPROVEMENT")
            print("🔧 Consider debugging scrapers")
        
        # Best performer
        if sorted_results:
            best_scraper, best_result = sorted_results[0]
            best_assets = best_result.get('assets_found', 0)
            print(f"\n🏆 BEST PERFORMER: {best_scraper.upper()}")
            print(f"   {best_assets:,} assets")

def main():
    """Main maximum scraping function"""
    print("🚀 MAXIMUM ASSET SCRAPER")
    print("=" * 80)
    print("Her siteden alabileceğimiz maksimum asset'i topluyoruz!")
    print("Hedef yok - ne kadar varsa o kadar!")
    print()
    
    # Create maximum scraper instance
    max_scraper = MaximumAssetScraper()
    
    print("⚠️ WARNING: Bu maksimum asset scraping başlatacak")
    print("Her siteden mümkün olan en fazla asset'i toplayacak")
    confirm = input("Continue? (y/N): ").strip().lower()
    
    if confirm == 'y':
        try:
            # Start maximum scraping
            max_scraper.run_maximum_scraping()
        except KeyboardInterrupt:
            print("\n⚠️ Maximum scraping interrupted by user")
        except Exception as e:
            print(f"\n❌ Maximum scraping failed: {e}")
    else:
        print("❌ Maximum scraping cancelled")

if __name__ == "__main__":
    main()
