"""
Adaptive Security System
Automatically adjusts security measures based on threat level and success rates
Implements circuit breaker pattern and machine learning-based adaptations
"""

import time
import json
import logging
import statistics
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import threading

class ThreatLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered

@dataclass
class SecurityMetrics:
    success_rate: float
    average_response_time: float
    bot_detections: int
    captcha_challenges: int
    rate_limits: int
    ip_bans: int
    proxy_failures: int
    timestamp: float

@dataclass
class AdaptiveConfig:
    min_delay: float
    max_delay: float
    proxy_rotation_frequency: int
    profile_rotation_frequency: int
    aggressive_mode: bool
    stealth_mode: bool
    threat_level: ThreatLevel

class CircuitBreaker:
    """Circuit breaker for handling cascading failures"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60, success_threshold: int = 3):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = 0
        self.state = CircuitState.CLOSED
        
        self.lock = threading.Lock()
        
    def call(self, func, *args, **kwargs):
        """Execute function through circuit breaker"""
        with self.lock:
            if self.state == CircuitState.OPEN:
                if time.time() - self.last_failure_time > self.recovery_timeout:
                    self.state = CircuitState.HALF_OPEN
                    self.success_count = 0
                    logging.info("Circuit breaker moving to HALF_OPEN state")
                else:
                    raise Exception("Circuit breaker is OPEN - rejecting request")
            
            try:
                result = func(*args, **kwargs)
                self._on_success()
                return result
            except Exception as e:
                self._on_failure()
                raise e
    
    def _on_success(self):
        """Handle successful request"""
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                logging.info("Circuit breaker moving to CLOSED state")
        else:
            self.failure_count = max(0, self.failure_count - 1)
    
    def _on_failure(self):
        """Handle failed request"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logging.warning(f"Circuit breaker moving to OPEN state after {self.failure_count} failures")

class AdaptiveSecurityManager:
    """Adaptive security system that learns and adjusts"""
    
    def __init__(self, config_file: str = "security/adaptive_config.json"):
        self.config_file = Path(config_file)
        self.metrics_history: List[SecurityMetrics] = []
        self.current_config = self._load_config()
        self.circuit_breaker = CircuitBreaker()
        
        # Adaptive parameters
        self.learning_window = 100  # Number of requests to analyze
        self.adaptation_threshold = 0.1  # Minimum change to trigger adaptation
        self.max_metrics_history = 1000
        
        # Threat detection
        self.threat_indicators = {
            ThreatLevel.LOW: {"bot_detection_rate": 0.05, "success_rate": 0.95},
            ThreatLevel.MEDIUM: {"bot_detection_rate": 0.15, "success_rate": 0.85},
            ThreatLevel.HIGH: {"bot_detection_rate": 0.30, "success_rate": 0.70},
            ThreatLevel.CRITICAL: {"bot_detection_rate": 0.50, "success_rate": 0.50}
        }
        
        self.lock = threading.Lock()
        logging.info("AdaptiveSecurityManager initialized")
    
    def _load_config(self) -> AdaptiveConfig:
        """Load adaptive configuration"""
        if not self.config_file.exists():
            return self._create_default_config()
        
        try:
            with open(self.config_file, 'r') as f:
                config_data = json.load(f)
            
            return AdaptiveConfig(
                min_delay=config_data.get('min_delay', 1.0),
                max_delay=config_data.get('max_delay', 10.0),
                proxy_rotation_frequency=config_data.get('proxy_rotation_frequency', 50),
                profile_rotation_frequency=config_data.get('profile_rotation_frequency', 30),
                aggressive_mode=config_data.get('aggressive_mode', False),
                stealth_mode=config_data.get('stealth_mode', True),
                threat_level=ThreatLevel(config_data.get('threat_level', 'low'))
            )
        except Exception as e:
            logging.error(f"Error loading adaptive config: {e}")
            return self._create_default_config()
    
    def _create_default_config(self) -> AdaptiveConfig:
        """Create default adaptive configuration"""
        config = AdaptiveConfig(
            min_delay=1.0,
            max_delay=10.0,
            proxy_rotation_frequency=50,
            profile_rotation_frequency=30,
            aggressive_mode=False,
            stealth_mode=True,
            threat_level=ThreatLevel.LOW
        )
        
        self._save_config(config)
        return config
    
    def _save_config(self, config: AdaptiveConfig):
        """Save adaptive configuration"""
        self.config_file.parent.mkdir(exist_ok=True)
        
        config_data = asdict(config)
        config_data['threat_level'] = config.threat_level.value
        
        with open(self.config_file, 'w') as f:
            json.dump(config_data, f, indent=2)
    
    def record_metrics(self, success: bool, response_time: float, bot_detected: bool = False,
                      captcha_challenge: bool = False, rate_limited: bool = False,
                      ip_banned: bool = False, proxy_failed: bool = False):
        """Record security metrics for analysis"""
        with self.lock:
            # Calculate current success rate
            recent_metrics = self.metrics_history[-self.learning_window:] if self.metrics_history else []
            if recent_metrics:
                success_rate = sum(1 for m in recent_metrics if m.success_rate > 0.5) / len(recent_metrics)
            else:
                success_rate = 1.0 if success else 0.0
            
            # Count recent events
            bot_detections = sum(1 for m in recent_metrics if m.bot_detections > 0)
            captcha_challenges_count = sum(1 for m in recent_metrics if m.captcha_challenges > 0)
            rate_limits_count = sum(1 for m in recent_metrics if m.rate_limits > 0)
            ip_bans_count = sum(1 for m in recent_metrics if m.ip_bans > 0)
            proxy_failures_count = sum(1 for m in recent_metrics if m.proxy_failures > 0)
            
            metrics = SecurityMetrics(
                success_rate=success_rate,
                average_response_time=response_time,
                bot_detections=1 if bot_detected else 0,
                captcha_challenges=1 if captcha_challenge else 0,
                rate_limits=1 if rate_limited else 0,
                ip_bans=1 if ip_banned else 0,
                proxy_failures=1 if proxy_failed else 0,
                timestamp=time.time()
            )
            
            self.metrics_history.append(metrics)
            
            # Keep history manageable
            if len(self.metrics_history) > self.max_metrics_history:
                self.metrics_history = self.metrics_history[-self.max_metrics_history//2:]
            
            # Trigger adaptation if needed
            if len(self.metrics_history) % 10 == 0:  # Check every 10 requests
                self._analyze_and_adapt()
    
    def _analyze_and_adapt(self):
        """Analyze metrics and adapt security configuration"""
        if len(self.metrics_history) < 10:
            return
        
        recent_metrics = self.metrics_history[-self.learning_window:]
        
        # Calculate key indicators
        success_rate = statistics.mean([m.success_rate for m in recent_metrics])
        bot_detection_rate = sum(m.bot_detections for m in recent_metrics) / len(recent_metrics)
        avg_response_time = statistics.mean([m.average_response_time for m in recent_metrics])
        
        # Determine threat level
        new_threat_level = self._assess_threat_level(success_rate, bot_detection_rate)
        
        # Adapt configuration if threat level changed
        if new_threat_level != self.current_config.threat_level:
            logging.info(f"Threat level changed from {self.current_config.threat_level.value} to {new_threat_level.value}")
            self._adapt_to_threat_level(new_threat_level)
        
        # Adaptive delay adjustment
        if success_rate < 0.8:
            # Increase delays if success rate is low
            new_min_delay = min(self.current_config.min_delay * 1.2, 5.0)
            new_max_delay = min(self.current_config.max_delay * 1.2, 20.0)
            
            if abs(new_min_delay - self.current_config.min_delay) > self.adaptation_threshold:
                self.current_config.min_delay = new_min_delay
                self.current_config.max_delay = new_max_delay
                logging.info(f"Adapted delays: min={new_min_delay:.2f}s, max={new_max_delay:.2f}s")
        
        elif success_rate > 0.95 and avg_response_time < 2.0:
            # Decrease delays if performing well
            new_min_delay = max(self.current_config.min_delay * 0.9, 0.5)
            new_max_delay = max(self.current_config.max_delay * 0.9, 2.0)
            
            if abs(new_min_delay - self.current_config.min_delay) > self.adaptation_threshold:
                self.current_config.min_delay = new_min_delay
                self.current_config.max_delay = new_max_delay
                logging.info(f"Optimized delays: min={new_min_delay:.2f}s, max={new_max_delay:.2f}s")
        
        # Adaptive rotation frequency
        if bot_detection_rate > 0.2:
            # Increase rotation frequency if bot detection is high
            self.current_config.proxy_rotation_frequency = max(
                self.current_config.proxy_rotation_frequency - 10, 10
            )
            self.current_config.profile_rotation_frequency = max(
                self.current_config.profile_rotation_frequency - 5, 5
            )
            logging.info("Increased rotation frequency due to high bot detection")
        
        # Save adapted configuration
        self._save_config(self.current_config)
    
    def _assess_threat_level(self, success_rate: float, bot_detection_rate: float) -> ThreatLevel:
        """Assess current threat level based on metrics"""
        if success_rate < 0.5 or bot_detection_rate > 0.5:
            return ThreatLevel.CRITICAL
        elif success_rate < 0.7 or bot_detection_rate > 0.3:
            return ThreatLevel.HIGH
        elif success_rate < 0.85 or bot_detection_rate > 0.15:
            return ThreatLevel.MEDIUM
        else:
            return ThreatLevel.LOW
    
    def _adapt_to_threat_level(self, threat_level: ThreatLevel):
        """Adapt configuration based on threat level"""
        self.current_config.threat_level = threat_level
        
        if threat_level == ThreatLevel.CRITICAL:
            self.current_config.aggressive_mode = False
            self.current_config.stealth_mode = True
            self.current_config.min_delay = 5.0
            self.current_config.max_delay = 30.0
            self.current_config.proxy_rotation_frequency = 5
            self.current_config.profile_rotation_frequency = 3
            
        elif threat_level == ThreatLevel.HIGH:
            self.current_config.aggressive_mode = False
            self.current_config.stealth_mode = True
            self.current_config.min_delay = 3.0
            self.current_config.max_delay = 15.0
            self.current_config.proxy_rotation_frequency = 10
            self.current_config.profile_rotation_frequency = 5
            
        elif threat_level == ThreatLevel.MEDIUM:
            self.current_config.stealth_mode = True
            self.current_config.min_delay = 2.0
            self.current_config.max_delay = 8.0
            self.current_config.proxy_rotation_frequency = 25
            self.current_config.profile_rotation_frequency = 15
            
        else:  # LOW
            self.current_config.min_delay = 1.0
            self.current_config.max_delay = 5.0
            self.current_config.proxy_rotation_frequency = 50
            self.current_config.profile_rotation_frequency = 30
        
        logging.info(f"Adapted configuration for {threat_level.value} threat level")
    
    def get_current_config(self) -> AdaptiveConfig:
        """Get current adaptive configuration"""
        return self.current_config
    
    def should_use_circuit_breaker(self) -> bool:
        """Check if circuit breaker should be used"""
        return self.current_config.threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]
    
    def execute_with_protection(self, func, *args, **kwargs):
        """Execute function with adaptive protection"""
        if self.should_use_circuit_breaker():
            return self.circuit_breaker.call(func, *args, **kwargs)
        else:
            return func(*args, **kwargs)
    
    def get_adaptive_delay(self) -> float:
        """Get adaptive delay based on current configuration"""
        import random
        base_delay = random.uniform(self.current_config.min_delay, self.current_config.max_delay)
        
        # Add threat-level specific adjustments
        if self.current_config.threat_level == ThreatLevel.CRITICAL:
            # Add extra random delay for critical threat
            base_delay += random.uniform(5, 15)
        elif self.current_config.threat_level == ThreatLevel.HIGH:
            base_delay += random.uniform(2, 8)
        
        return base_delay
    
    def should_rotate_proxy(self, request_count: int) -> bool:
        """Check if proxy should be rotated"""
        return request_count % self.current_config.proxy_rotation_frequency == 0
    
    def should_rotate_profile(self, request_count: int) -> bool:
        """Check if profile should be rotated"""
        return request_count % self.current_config.profile_rotation_frequency == 0
    
    def get_security_stats(self) -> Dict:
        """Get comprehensive security statistics"""
        if not self.metrics_history:
            return {"status": "no_data"}
        
        recent_metrics = self.metrics_history[-50:]  # Last 50 requests
        
        return {
            "current_threat_level": self.current_config.threat_level.value,
            "circuit_breaker_state": self.circuit_breaker.state.value,
            "total_requests": len(self.metrics_history),
            "recent_success_rate": statistics.mean([m.success_rate for m in recent_metrics]),
            "recent_avg_response_time": statistics.mean([m.average_response_time for m in recent_metrics]),
            "recent_bot_detections": sum(m.bot_detections for m in recent_metrics),
            "recent_captcha_challenges": sum(m.captcha_challenges for m in recent_metrics),
            "recent_rate_limits": sum(m.rate_limits for m in recent_metrics),
            "recent_ip_bans": sum(m.ip_bans for m in recent_metrics),
            "current_config": asdict(self.current_config),
            "adaptation_active": True
        }
    
    def reset_circuit_breaker(self):
        """Manually reset circuit breaker"""
        with self.circuit_breaker.lock:
            self.circuit_breaker.state = CircuitState.CLOSED
            self.circuit_breaker.failure_count = 0
            self.circuit_breaker.success_count = 0
            logging.info("Circuit breaker manually reset")
    
    def force_threat_level(self, threat_level: ThreatLevel):
        """Manually set threat level (for testing)"""
        logging.info(f"Manually setting threat level to {threat_level.value}")
        self._adapt_to_threat_level(threat_level)
