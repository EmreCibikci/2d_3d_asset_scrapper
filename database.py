import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import config

class DatabaseManager:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or config.DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path, timeout=config.DB_TIMEOUT) as conn:
            cursor = conn.cursor()
            
            # Assets table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS assets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    url TEXT UNIQUE NOT NULL,
                    source_site TEXT NOT NULL,
                    asset_type TEXT NOT NULL, -- '2d', '3d', 'audio', 'other'
                    category TEXT, -- 'character', 'environment', 'ui', 'effect', etc.
                    tags TEXT, -- JSON array of tags
                    file_size INTEGER,
                    file_format TEXT,
                    preview_url TEXT,
                    download_url TEXT,
                    is_free BOOLEAN DEFAULT 1,
                    license_info TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Downloads table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS downloads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    asset_id INTEGER,
                    local_path TEXT NOT NULL,
                    download_status TEXT DEFAULT 'pending', -- 'pending', 'downloading', 'completed', 'failed'
                    download_progress REAL DEFAULT 0.0,
                    file_size INTEGER,
                    downloaded_size INTEGER DEFAULT 0,
                    error_message TEXT,
                    download_started_at TIMESTAMP,
                    download_completed_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (asset_id) REFERENCES assets (id)
                )
            ''')
            
            # Sites table for tracking scraping status
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    site_name TEXT UNIQUE NOT NULL,
                    last_scraped_at TIMESTAMP,
                    total_assets_found INTEGER DEFAULT 0,
                    scraping_status TEXT DEFAULT 'idle', -- 'idle', 'scraping', 'completed', 'error'
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_assets_site ON assets(source_site)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_assets_type ON assets(asset_type)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_assets_category ON assets(category)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_downloads_status ON downloads(download_status)')
            
            conn.commit()
    
    def add_asset(self, asset_data: Dict) -> int:
        """Add a new asset to the database"""
        with sqlite3.connect(self.db_path, timeout=config.DB_TIMEOUT) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO assets 
                (title, description, url, source_site, asset_type, category, tags, 
                 file_size, file_format, preview_url, download_url, is_free, license_info, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                asset_data.get('title'),
                asset_data.get('description'),
                asset_data.get('url'),
                asset_data.get('source_site'),
                asset_data.get('asset_type'),
                asset_data.get('category'),
                json.dumps(asset_data.get('tags', [])),
                asset_data.get('file_size'),
                asset_data.get('file_format'),
                asset_data.get('preview_url'),
                asset_data.get('download_url'),
                asset_data.get('is_free', True),
                asset_data.get('license_info'),
                datetime.now().isoformat()
            ))
            
            return cursor.lastrowid
    
    def get_assets(self, filters: Dict = None) -> List[Dict]:
        """Get assets with optional filters"""
        with sqlite3.connect(self.db_path, timeout=config.DB_TIMEOUT) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = "SELECT * FROM assets WHERE 1=1"
            params = []
            
            if filters:
                if 'source_site' in filters:
                    query += " AND source_site = ?"
                    params.append(filters['source_site'])
                
                if 'asset_type' in filters:
                    query += " AND asset_type = ?"
                    params.append(filters['asset_type'])
                
                if 'category' in filters:
                    query += " AND category = ?"
                    params.append(filters['category'])
                
                if 'is_free' in filters:
                    query += " AND is_free = ?"
                    params.append(filters['is_free'])
            
            query += " ORDER BY created_at DESC"
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def add_download(self, asset_id: int, local_path: str) -> int:
        """Add a new download record"""
        with sqlite3.connect(self.db_path, timeout=config.DB_TIMEOUT) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO downloads (asset_id, local_path, download_started_at)
                VALUES (?, ?, ?)
            ''', (asset_id, local_path, datetime.now().isoformat()))
            
            return cursor.lastrowid
    
    def update_download_progress(self, download_id: int, progress: float, downloaded_size: int = None):
        """Update download progress"""
        with sqlite3.connect(self.db_path, timeout=config.DB_TIMEOUT) as conn:
            cursor = conn.cursor()
            
            if downloaded_size is not None:
                cursor.execute('''
                    UPDATE downloads 
                    SET download_progress = ?, downloaded_size = ?, download_status = 'downloading'
                    WHERE id = ?
                ''', (progress, downloaded_size, download_id))
            else:
                cursor.execute('''
                    UPDATE downloads 
                    SET download_progress = ?, download_status = 'downloading'
                    WHERE id = ?
                ''', (progress, download_id))
    
    def complete_download(self, download_id: int, success: bool = True, error_message: str = None):
        """Mark download as completed or failed"""
        with sqlite3.connect(self.db_path, timeout=config.DB_TIMEOUT) as conn:
            cursor = conn.cursor()
            
            status = 'completed' if success else 'failed'
            cursor.execute('''
                UPDATE downloads 
                SET download_status = ?, download_completed_at = ?, error_message = ?
                WHERE id = ?
            ''', (status, datetime.now().isoformat(), error_message, download_id))
    
    def update_site_status(self, site_name: str, status: str, assets_found: int = None, error_message: str = None):
        """Update site scraping status"""
        with sqlite3.connect(self.db_path, timeout=config.DB_TIMEOUT) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO sites 
                (site_name, last_scraped_at, total_assets_found, scraping_status, error_message)
                VALUES (?, ?, ?, ?, ?)
            ''', (site_name, datetime.now().isoformat(), assets_found, status, error_message))
    
    def get_download_stats(self) -> Dict:
        """Get download statistics"""
        with sqlite3.connect(self.db_path, timeout=config.DB_TIMEOUT) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_downloads,
                    SUM(CASE WHEN download_status = 'completed' THEN 1 ELSE 0 END) as completed,
                    SUM(CASE WHEN download_status = 'failed' THEN 1 ELSE 0 END) as failed,
                    SUM(CASE WHEN download_status = 'downloading' THEN 1 ELSE 0 END) as in_progress
                FROM downloads
            ''')
            
            result = cursor.fetchone()
            return {
                'total_downloads': result[0],
                'completed': result[1],
                'failed': result[2],
                'in_progress': result[3]
            }
