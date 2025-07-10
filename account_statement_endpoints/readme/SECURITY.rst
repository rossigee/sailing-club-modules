# Security Considerations for Account Statement Endpoints

This document outlines security considerations and recommendations for the public API endpoints.

## Current Security Measures

1. **Access Control**: Only data explicitly marked as public is accessible:
   - Bank journals must have `public_can_view = True`
   - Calendar events must have `class = 'public'`
   - Partners must have `is_team_member = True`
   - Statement images are validated to belong to public journals

2. **SQL Injection Protection**: All database queries use Odoo's ORM with proper parameterization

3. **Path Traversal Protection**: All parameters are validated through Odoo's routing system

## Security Recommendations

### 1. Rate Limiting (IMPLEMENTED)

**Risk**: DoS attacks, resource exhaustion, bandwidth consumption

**Current Implementation**: 
- **Module Level**: Basic in-memory rate limiting with configurable limits per endpoint
- **Proxy Level**: Nginx configuration example provided in `nginx-rate-limit.conf`

**Defense in Depth Strategy**:
1. **Primary Defense (Nginx)**: Blocks requests at network edge
   - See `nginx-rate-limit.conf` for complete configuration
   - Different limits for different endpoint types
   - IP whitelisting support
   
2. **Secondary Defense (Module)**: Application-level rate limiting
   - Per-endpoint customizable limits
   - Returns 429 status with Retry-After header
   - In-memory storage with automatic cleanup

**Current Limits**:
- Standard endpoints: 30 req/min, 500 req/hour
- Detail views: 20 req/min, 300 req/hour  
- Image endpoints: 60 req/min, 1000 req/hour

**Monitoring**: 
- Nginx: Use `/req_status` endpoint
- Module: Check Odoo logs for rate limit warnings

### 2. Response Size Limits (MEDIUM PRIORITY)

**Risk**: Large responses can overwhelm clients and consume bandwidth

**Current Issues**:
- `/bank/statements/<slug>` returns all statements without pagination
- `/calendar/events` limit parameter has no upper bound
- No limits on the number of attachments returned

**Recommendations**:
```python
# Add to controllers.py
MAX_STATEMENTS_PER_REQUEST = 100
MAX_EVENTS_PER_REQUEST = 100
MAX_ATTACHMENTS_PER_STATEMENT = 10

# In bank_statements_list_view:
bank_statements = http.request.env['account.bank.statement'].sudo().search(
    domain, order=orderby, limit=MAX_STATEMENTS_PER_REQUEST
)

# In calendar_events:
limit = min(int(kwargs.get('limit', 50)), MAX_EVENTS_PER_REQUEST)
```

### 3. Error Message Sanitization (MEDIUM PRIORITY)

**Risk**: Detailed error messages can reveal system internals

**Current Issue**: Exception details are exposed to users

**Recommendation**:
```python
except Exception as e:
    import logging
    logging.error(f"Error accessing bank journals: {str(e)}", exc_info=True)
    data = {
        "status": "error",
        "error": "An error occurred while processing your request"
    }
    return self._make_json_response(data, headers=None, cookies=None, status=500)
```

### 4. CORS Configuration (LOW PRIORITY)

**Risk**: Any website can access the API

**Current State**: `Access-Control-Allow-Origin: *`

**Recommendation**: If you know which domains will access the API, configure specific origins:
```python
ALLOWED_ORIGINS = ['https://www.bksc.net', 'https://bksc.net']
origin = http.request.httprequest.headers.get('Origin')
if origin in ALLOWED_ORIGINS:
    headers['Access-Control-Allow-Origin'] = origin
else:
    headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS[0]
```

### 5. Caching Headers (LOW PRIORITY)

**Recommendation**: Add cache headers to reduce load:
```python
headers['Cache-Control'] = 'public, max-age=300'  # 5 minutes
headers['Vary'] = 'Accept-Encoding'
```

### 6. Input Validation (IMPLEMENTED)

**Status**: ✅ Properly implemented through Odoo's routing and ORM

### 7. Authentication (BY DESIGN)

**Status**: ✅ Public access is intentional for transparency

## Implementation Priority

1. **Completed**: ✅ Rate limiting implemented at both module and proxy levels
2. **High**: Add response size limits and pagination
3. **Medium**: Sanitize error messages
4. **Low**: Configure CORS and caching if needed

## Using the Implementations

### Nginx Rate Limiting
1. Copy `nginx-rate-limit.conf` to your nginx configuration directory
2. Include it in your server configuration or adapt it to your setup
3. Reload nginx: `nginx -s reload`
4. Monitor with: `curl http://127.0.0.1:8080/req_status`

### Module Rate Limiting
The module-level rate limiting is automatically active. To customize:
- Edit limits in `controllers.py` decorators
- Modify global limits in `rate_limit.py` RateLimiter class
- Monitor by checking Odoo logs for 429 responses

## Monitoring Recommendations

1. Log all API access with source IPs
2. Monitor for unusual request patterns
3. Set up alerts for high request rates
4. Track response times and sizes
5. Regular security audits of exposed data

## Testing Checklist

- [ ] Test rate limiting effectiveness
- [ ] Verify large dataset handling
- [ ] Confirm error messages don't leak information
- [ ] Validate CORS behavior
- [ ] Check caching headers
- [ ] Load test endpoints
- [ ] Security scan with OWASP ZAP or similar