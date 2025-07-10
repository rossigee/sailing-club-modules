# -*- coding: utf-8 -*-
import time
import json
import functools
from collections import defaultdict
from datetime import datetime, timedelta
from odoo import http
from odoo.http import request

class RateLimiter:
    """Simple in-memory rate limiter for API endpoints"""
    
    def __init__(self):
        # Store request counts by IP address
        # Format: {ip: [(timestamp1, count1), (timestamp2, count2), ...]}
        self._requests = defaultdict(list)
        # Configuration
        self.requests_per_minute = 30  # Max requests per minute per IP
        self.requests_per_hour = 500   # Max requests per hour per IP
        self.cleanup_interval = 300    # Cleanup old entries every 5 minutes
        self.last_cleanup = time.time()
    
    def cleanup_old_entries(self):
        """Remove old entries to prevent memory growth"""
        current_time = time.time()
        if current_time - self.last_cleanup < self.cleanup_interval:
            return
            
        hour_ago = current_time - 3600
        for ip in list(self._requests.keys()):
            # Keep only entries from last hour
            self._requests[ip] = [
                (ts, count) for ts, count in self._requests[ip] 
                if ts > hour_ago
            ]
            # Remove IP if no recent requests
            if not self._requests[ip]:
                del self._requests[ip]
        
        self.last_cleanup = current_time
    
    def is_allowed(self, ip_address):
        """Check if request from IP address is allowed"""
        self.cleanup_old_entries()
        
        current_time = time.time()
        minute_ago = current_time - 60
        hour_ago = current_time - 3600
        
        # Get request history for this IP
        requests = self._requests[ip_address]
        
        # Count requests in last minute and hour
        minute_count = sum(
            count for ts, count in requests 
            if ts > minute_ago
        )
        hour_count = sum(
            count for ts, count in requests 
            if ts > hour_ago
        )
        
        # Check limits
        if minute_count >= self.requests_per_minute:
            return False, "Rate limit exceeded: too many requests per minute"
        if hour_count >= self.requests_per_hour:
            return False, "Rate limit exceeded: too many requests per hour"
        
        # Add this request
        if requests and requests[-1][0] == int(current_time):
            # Same second, increment count
            requests[-1] = (requests[-1][0], requests[-1][1] + 1)
        else:
            # New second
            requests.append((int(current_time), 1))
        
        return True, None

# Global rate limiter instance
rate_limiter = RateLimiter()

def rate_limit(requests_per_minute=30, requests_per_hour=500):
    """Decorator to add rate limiting to controller methods"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get client IP address
            ip_address = request.httprequest.environ.get('REMOTE_ADDR', 'unknown')
            
            # Check rate limit
            allowed, error_message = rate_limiter.is_allowed(ip_address)
            
            if not allowed:
                # Return 429 Too Many Requests
                data = {
                    "status": "error",
                    "error": error_message
                }
                response = http.Response(
                    json.dumps(data),
                    status=429,
                    headers=[
                        ('Content-Type', 'application/json'),
                        ('Retry-After', '60')  # Tell client to retry after 60 seconds
                    ]
                )
                return response
            
            # Call original function
            return func(*args, **kwargs)
        return wrapper
    return decorator

def get_client_ip():
    """Get real client IP, considering proxy headers"""
    # Check for proxy headers
    forwarded_for = request.httprequest.headers.get('X-Forwarded-For')
    if forwarded_for:
        # X-Forwarded-For can contain multiple IPs, take the first
        ip = forwarded_for.split(',')[0].strip()
    else:
        # Fall back to remote address
        ip = request.httprequest.environ.get('REMOTE_ADDR', 'unknown')
    return ip