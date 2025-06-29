"""
Secure Scraper with Advanced IP Protection and Anti-Detection
Integrates all security components for maximum protection
"""

import time
import random
import requests
import logging
from typing import Optional, Dict, Any
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
from pathlib import Path

from .proxy_manager import ProxyManager
from .anti_detection import AntiDetectionManager
from .captcha_solver import BotDetectionHandler, CaptchaChallenge
from .advanced_evasion import AdvancedEvasionManager
from .adaptive_security import AdaptiveSecurityManager, ThreatLevel
from .advanced_bot_bypass import AdvancedBotBypass

class SecureScraper:
    """Advanced secure scraper with comprehensive protection"""
    
    def __init__(self, site_name: str, config_file: str = "security/secure_config.json"):
        self.site_name = site_name
        self.config_file = Path(config_file)
        self.config = self.load_config()
        
        # Initialize security components
        self.proxy_manager = ProxyManager()
        self.anti_detection = AntiDetectionManager()
        self.bot_handler = BotDetectionHandler()
        self.advanced_evasion = AdvancedEvasionManager()
        self.adaptive_security = AdaptiveSecurityManager()
        self.bot_bypass = AdvancedBotBypass()
        
        # Session management
        self.session = requests.Session()
        self.session_start_time = time.time()
        self.requests_in_session = 0
        self.max_requests_per_session = self.config.get('max_requests_per_session', 100)
        self.max_session_duration = self.config.get('max_session_duration', 3600)  # 1 hour
        
        # Request tracking
        self.failed_requests = 0
        self.max_failed_requests = self.config.get('max_failed_requests', 5)
        self.success_rate_threshold = self.config.get('success_rate_threshold', 0.8)
        
        # Initialize session
        self._setup_session()
        
        logging.info(f"SecureScraper initialized for {site_name}")
    
    def load_config(self) -> Dict:
        """Load secure scraper configuration"""
        if not self.config_file.exists():
            self._create_default_config()
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading secure config: {e}")
            return self._get_default_config()
    
    def _create_default_config(self):
        """Create default secure configuration"""
        self.config_file.parent.mkdir(exist_ok=True)
        
        config = self._get_default_config()
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def _get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            "max_requests_per_session": 100,
            "max_session_duration": 3600,
            "max_failed_requests": 5,
            "success_rate_threshold": 0.8,
            "retry_attempts": 3,
            "base_delay": 2.0,
            "max_delay": 10.0,
            "enable_proxy_rotation": False,  # Disabled by default for testing
            "enable_profile_rotation": True,
            "enable_captcha_solving": True,
            "aggressive_mode": False,
            "stealth_mode": True
        }
    
    def _setup_session(self):
        """Setup session with security measures"""
        # Get current proxy (only if enabled and available)
        if self.config.get('enable_proxy_rotation', True):
            try:
                proxy = self.proxy_manager.get_working_proxy()
                if proxy:
                    self.session.proxies = proxy.to_dict()
                    logging.info(f"Using proxy: {proxy}")
                else:
                    logging.info("No working proxies available - using direct connection")
                    self.session.proxies = {}
            except Exception as e:
                logging.warning(f"Proxy setup failed: {e} - using direct connection")
                self.session.proxies = {}
        else:
            self.session.proxies = {}

        # Get browser profile and headers
        if self.config.get('enable_profile_rotation', True):
            profile = self.anti_detection.get_random_profile()
            headers = self.anti_detection.get_headers()
            self.session.headers.update(headers)
            logging.info(f"Using profile: {profile.user_agent[:50]}...")
        
        # Session settings
        self.session.timeout = 30
        self.session.max_redirects = 5
        
        # Reset session tracking
        self.session_start_time = time.time()
        self.requests_in_session = 0
    
    def make_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
        """Make secure HTTP request with all protections"""
        # Check if session needs renewal
        if self._should_renew_session():
            self._renew_session()
        
        # Calculate intelligent delay
        delay = self.anti_detection.calculate_delay(url)
        if delay > 0:
            logging.debug(f"Waiting {delay:.2f} seconds before request")
            time.sleep(delay)
        
        # Prepare request
        headers = kwargs.pop('headers', {})
        request_headers = self.anti_detection.get_headers(url)
        request_headers.update(headers)
        
        # Add referer if available
        if hasattr(self, 'last_url') and self.last_url:
            request_headers['Referer'] = self.last_url
        
        retry_attempts = self.config.get('retry_attempts', 3)
        
        for attempt in range(retry_attempts):
            start_time = time.time()
            
            try:
                # Make request
                response = self.session.request(
                    method=method,
                    url=url,
                    headers=request_headers,
                    timeout=30,
                    allow_redirects=True,
                    **kwargs
                )
                
                response_time = time.time() - start_time
                
                # Advanced bot detection and bypass
                protection_info = self.bot_bypass.detect_protection(response)
                if protection_info['has_protection']:
                    logging.warning(f"Bot protection detected: {protection_info['protection_types']} for {url}")

                    # Try advanced bypass
                    bypassed_response = self.bot_bypass.bypass_protection(url, protection_info)
                    if bypassed_response and self.bot_bypass._is_bypass_successful(bypassed_response):
                        response = bypassed_response
                        logging.info("Bot protection bypass successful")
                    else:
                        # Fallback to legacy handling
                        if self.config.get('enable_captcha_solving', True):
                            handled_response = self.bot_handler.handle_bot_challenge(response, self.session)
                            if handled_response:
                                response = handled_response
                            else:
                                self._handle_bot_detection()
                                continue
                        else:
                            self._handle_bot_detection()
                            continue
                
                # Check response status
                if response.status_code == 200:
                    # Success
                    self.failed_requests = 0
                    self.requests_in_session += 1
                    self.last_url = url
                    
                    # Record request for analysis
                    self.anti_detection.record_request(url, True, response_time)
                    
                    # Report proxy success
                    current_proxy = self._get_current_proxy()
                    if current_proxy:
                        self.proxy_manager.report_proxy_result(current_proxy, True, response_time)
                    
                    return response
                
                elif response.status_code in [403, 429, 503]:
                    # Rate limited or blocked
                    logging.warning(f"Rate limited or blocked (status {response.status_code}) for {url}")
                    self._handle_rate_limit(response)
                    continue
                
                else:
                    # Other error
                    logging.warning(f"HTTP {response.status_code} for {url}")
                    response.raise_for_status()
            
            except requests.exceptions.RequestException as e:
                response_time = time.time() - start_time
                logging.error(f"Request failed (attempt {attempt + 1}/{retry_attempts}): {e}")
                
                # Record failed request
                self.anti_detection.record_request(url, False, response_time)
                
                # Report proxy failure
                current_proxy = self._get_current_proxy()
                if current_proxy:
                    self.proxy_manager.report_proxy_result(current_proxy, False, response_time)
                
                self.failed_requests += 1
                
                # Handle failure
                if attempt < retry_attempts - 1:
                    self._handle_request_failure(attempt)
                else:
                    logging.error(f"All retry attempts failed for {url}")
                    return None
        
        return None
    
    def get_soup(self, url: str, **kwargs) -> Optional[BeautifulSoup]:
        """Get BeautifulSoup object with security"""
        response = self.make_request(url, **kwargs)
        if response:
            return BeautifulSoup(response.content, 'html.parser')
        return None
    
    def _should_renew_session(self) -> bool:
        """Check if session should be renewed"""
        current_time = time.time()
        
        # Check session duration
        if current_time - self.session_start_time > self.max_session_duration:
            return True
        
        # Check request count
        if self.requests_in_session >= self.max_requests_per_session:
            return True
        
        # Check failure rate
        if self.failed_requests >= self.max_failed_requests:
            return True
        
        # Check if profile should be rotated
        if self.anti_detection.should_rotate_profile():
            return True
        
        return False
    
    def _renew_session(self):
        """Renew session with new security settings"""
        logging.info("Renewing session for enhanced security")
        
        # Close current session
        self.session.close()
        
        # Create new session
        self.session = requests.Session()
        
        # Setup with new security settings
        self._setup_session()
        
        # Add extra delay after session renewal
        time.sleep(random.uniform(5, 15))
    
    def _is_bot_detected(self, response: requests.Response) -> bool:
        """Check if bot detection is triggered"""
        content = response.text.lower()
        
        # Common bot detection indicators
        bot_indicators = [
            'captcha',
            'robot',
            'automated',
            'blocked',
            'access denied',
            'cloudflare',
            'checking your browser',
            'please verify',
            'security check',
            'suspicious activity'
        ]
        
        return any(indicator in content for indicator in bot_indicators)
    
    def _handle_bot_detection(self):
        """Handle bot detection"""
        logging.warning("Bot detection handled - renewing session")
        
        # Force session renewal
        self._renew_session()
        
        # Add longer delay
        delay = random.uniform(30, 120)
        logging.info(f"Adding {delay:.1f}s delay after bot detection")
        time.sleep(delay)
    
    def _handle_rate_limit(self, response: requests.Response):
        """Handle rate limiting"""
        # Check for Retry-After header
        retry_after = response.headers.get('Retry-After')
        if retry_after:
            try:
                delay = int(retry_after)
                logging.info(f"Rate limited - waiting {delay}s as requested")
                time.sleep(delay)
                return
            except ValueError:
                pass
        
        # Default rate limit handling
        delay = random.uniform(60, 180)
        logging.info(f"Rate limited - waiting {delay:.1f}s")
        time.sleep(delay)
        
        # Consider switching proxy
        if self.config.get('enable_proxy_rotation', True):
            self._renew_session()
    
    def _handle_request_failure(self, attempt: int):
        """Handle request failure"""
        # Exponential backoff
        delay = min(self.config.get('base_delay', 2.0) * (2 ** attempt), self.config.get('max_delay', 10.0))
        delay += random.uniform(0, delay * 0.5)  # Add jitter
        
        logging.info(f"Request failed - waiting {delay:.2f}s before retry")
        time.sleep(delay)
        
        # Consider switching proxy after multiple failures
        if attempt >= 1 and self.config.get('enable_proxy_rotation', True):
            self._renew_session()
    
    def _get_current_proxy(self) -> Optional:
        """Get current proxy info"""
        # This would need to be implemented based on how proxy info is stored
        # For now, return None
        return None
    
    def get_security_stats(self) -> Dict:
        """Get security and performance statistics"""
        proxy_stats = self.proxy_manager.get_proxy_stats()
        detection_stats = self.anti_detection.get_request_stats()
        
        return {
            'session_info': {
                'session_age': time.time() - self.session_start_time,
                'requests_in_session': self.requests_in_session,
                'failed_requests': self.failed_requests
            },
            'proxy_stats': proxy_stats,
            'detection_stats': detection_stats
        }
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, 'session'):
            self.session.close()
