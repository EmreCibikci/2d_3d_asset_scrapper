"""
Güvenli ve Etik Web Scraping Yardımcı Fonksiyonları
Proxy olmadan güvenli scraping için gerekli araçlar
"""

import time
import random
import requests
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse
import logging
from typing import Optional, Dict, List
import config

class SafeScrapingManager:
    """Güvenli scraping için yönetici sınıf"""
    
    def __init__(self):
        self.request_times = {}  # Site bazında istek zamanları
        self.robots_cache = {}  # Robots.txt cache
        self.domain_user_agents = {}  # Domain başına User-Agent
        self.session = requests.Session()
        self.setup_session()
    
    def setup_session(self):
        """Güvenli session ayarları"""
        # Rastgele User-Agent seç
        self.session.headers.update({
            'User-Agent': random.choice(config.USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def check_robots_txt(self, url: str, user_agent: str = '*') -> bool:
        """Gelişmiş Robots.txt kontrolü - Cache ile"""
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            robots_url = f"{parsed_url.scheme}://{domain}/robots.txt"

            # Cache kontrolü
            if domain not in self.robots_cache:
                print(f"🤖 Robots.txt kontrol ediliyor: {domain}")
                rp = RobotFileParser()
                rp.set_url(robots_url)
                rp.read()
                self.robots_cache[domain] = rp
                print(f"✅ Robots.txt cache'lendi: {domain}")
            else:
                rp = self.robots_cache[domain]

            # İzin kontrolü
            allowed = rp.can_fetch(user_agent, url)
            if not allowed:
                print(f"🚫 Robots.txt tarafından yasaklandı: {url}")
            else:
                print(f"✅ Robots.txt izin veriyor: {url}")

            return allowed

        except Exception as e:
            logging.warning(f"Robots.txt kontrolü başarısız ({domain}): {e}")
            print(f"⚠️  Robots.txt hatası, izin veriliyor: {domain}")
            return True  # Hata durumunda izin ver
    
    def get_domain_rate_limits(self, domain: str) -> Dict:
        """Domain için rate limit ayarlarını getir"""
        return config.RATE_LIMITS.get(domain, config.RATE_LIMITS['default'])

    def rate_limit_check(self, domain: str) -> bool:
        """Gelişmiş rate limiting kontrolü - Domain bazında"""
        current_time = time.time()

        if domain not in self.request_times:
            self.request_times[domain] = []

        # Domain için özel ayarları al
        limits = self.get_domain_rate_limits(domain)

        # Son 1 dakikadaki istekleri filtrele
        minute_ago = current_time - 60
        recent_requests = [
            req_time for req_time in self.request_times[domain]
            if req_time > minute_ago
        ]

        # Son 1 saatteki istekleri filtrele
        hour_ago = current_time - 3600
        hourly_requests = [
            req_time for req_time in self.request_times[domain]
            if req_time > hour_ago
        ]

        # Dakikalık limit kontrolü
        if len(recent_requests) >= limits['requests_per_minute']:
            print(f"⏱️  Rate limit (dakika): {domain} - {len(recent_requests)}/{limits['requests_per_minute']}")
            return False

        # Saatlik limit kontrolü
        if len(hourly_requests) >= limits['requests_per_hour']:
            print(f"⏱️  Rate limit (saat): {domain} - {len(hourly_requests)}/{limits['requests_per_hour']}")
            return False

        return True
    
    def get_domain_user_agent(self, domain: str) -> str:
        """Domain için tutarlı User-Agent getir veya yeni ata"""
        if config.USER_AGENT_CHANGE_PER_DOMAIN:
            if domain not in self.domain_user_agents:
                self.domain_user_agents[domain] = random.choice(config.USER_AGENTS)
                print(f"🔄 Yeni User-Agent atandı: {domain}")
            return self.domain_user_agents[domain]
        else:
            return random.choice(config.USER_AGENTS)

    def smart_delay(self, domain: str):
        """Gelişmiş akıllı gecikme sistemi - Domain bazında"""
        if domain not in self.request_times:
            self.request_times[domain] = []

        current_time = time.time()
        limits = self.get_domain_rate_limits(domain)

        # Son istek zamanını kontrol et
        if self.request_times[domain]:
            last_request = max(self.request_times[domain])
            time_since_last = current_time - last_request

            # Domain için özel gecikme süresi
            min_delay = random.uniform(limits['min_delay'], limits['max_delay'])
            if time_since_last < min_delay:
                sleep_time = min_delay - time_since_last
                print(f"⏱️  Akıllı gecikme ({domain}): {sleep_time:.2f} saniye bekleniyor...")
                time.sleep(sleep_time)

        # İstek zamanını kaydet
        self.request_times[domain].append(time.time())
    
    def safe_get(self, url: str, **kwargs) -> Optional[requests.Response]:
        """Güvenli GET isteği"""
        try:
            # Domain çıkar
            domain = urlparse(url).netloc
            
            # Robots.txt kontrolü
            if not self.check_robots_txt(url):
                logging.warning(f"Robots.txt tarafından yasaklandı: {url}")
                return None
            
            # Rate limiting kontrolü
            if not self.rate_limit_check(domain):
                logging.warning(f"Rate limit aşıldı: {domain}")
                return None
            
            # Akıllı gecikme
            self.smart_delay(domain)
            
            # Gelişmiş User-Agent rotation
            if random.random() < config.USER_AGENT_ROTATION_CHANCE:
                new_ua = self.get_domain_user_agent(domain)
                self.session.headers['User-Agent'] = new_ua
                print(f"🔄 User-Agent değiştirildi: {domain}")
            else:
                # Domain için mevcut UA'yı kullan
                self.session.headers['User-Agent'] = self.get_domain_user_agent(domain)
            
            # İsteği gönder
            response = self.session.get(
                url, 
                timeout=config.REQUEST_TIMEOUT,
                **kwargs
            )
            
            # Başarı durumunu logla
            logging.info(f"✅ Başarılı istek: {url} (Status: {response.status_code})")
            return response
            
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ İstek hatası: {url} - {e}")
            return None
        except Exception as e:
            logging.error(f"❌ Beklenmeyen hata: {url} - {e}")
            return None
    
    def get_safe_headers(self) -> Dict[str, str]:
        """Güvenli header'lar döndür"""
        return {
            'User-Agent': random.choice(config.USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
        }

# Global instance
safe_scraper = SafeScrapingManager()

def get_safe_session() -> SafeScrapingManager:
    """Güvenli scraping session'ı döndür"""
    return safe_scraper

def is_scraping_allowed(url: str) -> bool:
    """URL'nin scraping için güvenli olup olmadığını kontrol et"""
    return safe_scraper.check_robots_txt(url)

def safe_request(url: str, **kwargs) -> Optional[requests.Response]:
    """Güvenli HTTP isteği wrapper'ı"""
    return safe_scraper.safe_get(url, **kwargs)
