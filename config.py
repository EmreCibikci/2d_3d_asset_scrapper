import os
import random
from pathlib import Path

# Base configuration
BASE_DIR = Path(__file__).parent
DOWNLOAD_DIR = BASE_DIR / "downloads"
DATABASE_PATH = BASE_DIR / "assets.db"

# Create directories if they don't exist
DOWNLOAD_DIR.mkdir(exist_ok=True)

# Download settings - Güvenli ve etik scraping için optimize edildi
MAX_CONCURRENT_DOWNLOADS = 3  # Daha düşük eş zamanlı indirme
CHUNK_SIZE = 8192
REQUEST_TIMEOUT = 30
RETRY_ATTEMPTS = 2  # Daha az deneme
DELAY_BETWEEN_REQUESTS = random.uniform(3, 7)  # 3-7 saniye arası rastgele gecikme

# Gelişmiş Rate limiting - Site bazında özelleştirilebilir
RATE_LIMITS = {
    'default': {
        'requests_per_minute': 6,
        'requests_per_hour': 40,
        'min_delay': 3,
        'max_delay': 8
    },
    'kenney.nl': {
        'requests_per_minute': 30,  # Kenney çok toleranslı
        'requests_per_hour': 200,
        'min_delay': 1,
        'max_delay': 3
    },
    'opengameart.org': {
        'requests_per_minute': 8,
        'requests_per_hour': 50,
        'min_delay': 3,
        'max_delay': 7
    },
    'itch.io': {
        'requests_per_minute': 5,  # Itch.io daha katı
        'requests_per_hour': 30,
        'min_delay': 4,
        'max_delay': 10
    },
    'game-icons.net': {
        'requests_per_minute': 8,
        'requests_per_hour': 45,
        'min_delay': 2,
        'max_delay': 6
    }
}

# Backward compatibility
MAX_REQUESTS_PER_MINUTE = RATE_LIMITS['default']['requests_per_minute']
REQUESTS_PER_SITE_PER_HOUR = RATE_LIMITS['default']['requests_per_hour']

# Gelişmiş User Agent rotation - Gerçek tarayıcı imzaları
USER_AGENTS = [
    # Chrome - Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # Chrome - macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # Firefox - Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    # Firefox - macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0",
    # Safari - macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    # Edge - Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    # Chrome - Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
]

# User-Agent rotation ayarları
USER_AGENT_ROTATION_CHANCE = 0.15  # %15 ihtimalle değiştir (daha sık)
USER_AGENT_CHANGE_PER_DOMAIN = True  # Domain başına farklı UA

# Varsayılan User Agent
USER_AGENT = random.choice(USER_AGENTS)

# Proxy ayarları - GÜVENLİK NEDENİYLE DEVRE DIŞI
USE_PROXY = False  # Proxy kullanımı kapatıldı
PROXY_ENABLED = False

# Supported file extensions
SUPPORTED_2D_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp']
SUPPORTED_3D_EXTENSIONS = ['.obj', '.fbx', '.dae', '.blend', '.3ds', '.max', '.ma', '.mb']
SUPPORTED_AUDIO_EXTENSIONS = ['.mp3', '.wav', '.ogg', '.m4a']

# Site configurations
SITES_CONFIG = {
    'craftpix': {
        'base_url': 'https://craftpix.net',
        'freebies_url': 'https://craftpix.net/freebies/',
        'enabled': False  # Requires registration
    },
    'kenney': {
        'base_url': 'https://kenney.nl',
        'assets_url': 'https://kenney.nl/assets',
        'enabled': True
    },
    'opengameart': {
        'base_url': 'https://opengameart.org',
        'enabled': True
    },
    'itch_io': {
        'base_url': 'https://itch.io',
        'game_assets_url': 'https://itch.io/game-assets',
        'enabled': True
    },
    'freepik': {
        'base_url': 'https://www.freepik.com',
        'enabled': False  # Bot protection, requires special handling
    },
    'game_icons': {
        'base_url': 'https://game-icons.net',
        'enabled': True
    },
    'pixabay': {
        'base_url': 'https://pixabay.com',
        'enabled': False  # Bot protection, requires special handling
    },
    'spriters_resource': {
        'base_url': 'https://www.spriters-resource.com',
        'enabled': False  # Complex structure, future implementation
    }
}

# Database settings
DB_TIMEOUT = 30
