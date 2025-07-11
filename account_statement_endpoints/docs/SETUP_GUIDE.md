# BKSC Public API Setup Guide

This guide helps you get started with the Ban Krut Sailing Club Public API using Postman, cURL, or other HTTP clients.

## Quick Start

### 1. Postman Setup (Recommended)

**Step 1: Import Collection**
1. Download `BKSC_Public_API.postman_collection.json`
2. Open Postman → Import → Upload Files
3. Select the collection file
4. Click Import

**Step 2: Import Environment**
1. Download `BKSC_API.postman_environment.json` 
2. Postman → Environments → Import
3. Select the environment file
4. Click Import

**Step 3: Configure Environment**
1. Select "BKSC API Environment" in the environment dropdown
2. Modify variables as needed:
   - `base_url`: Production URL (default: `https://odoo.bksc.net`)
   - `lang`: Language preference (`en` or `th`)
   - Other test IDs and slugs as needed

**Step 4: Test the API**
1. Open any request from the collection
2. Click "Send" 
3. Check response and test results
4. All requests include automatic validation tests

### 2. Environment Variables Reference

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `base_url` | `https://odoo.bksc.net` | API base URL |
| `local_url` | `http://localhost:8080` | Local development URL |
| `lang` | `en` | Language (en\|th) |
| `account_slug` | `BANK` | Bank account slug |
| `statement_id` | `31` | Statement ID for testing |
| `category_slug` | `catamarans` | Equipment category |
| `equipment_id` | `15` | Equipment ID for testing |
| `event_start_date` | `2025-02-01` | Event filter start |
| `event_end_date` | `2025-02-28` | Event filter end |
| `event_limit` | `50` | Max events to return |

### 3. Alternative Setup Options

#### Using cURL

**Test basic connectivity:**
```bash
# Check API health
curl -X GET "https://odoo.bksc.net/bank/journals" \
  -H "Accept: application/json" \
  -v

# Test with parameters  
curl -X GET "https://odoo.bksc.net/calendar/events?lang=en&limit=10" \
  -H "Accept: application/json"
```

#### Using HTTPie

```bash
# Install HTTPie first: pip install httpie

# Get bank journals
http GET https://odoo.bksc.net/bank/journals

# Get events with filtering
http GET https://odoo.bksc.net/calendar/events start==2025-02-01 end==2025-02-28 lang==en

# Get equipment details
http GET https://odoo.bksc.net/equipment/15 lang==th
```

#### Using wget

```bash
# Simple GET request
wget -O bank_journals.json "https://odoo.bksc.net/bank/journals"

# With custom headers
wget --header="Accept: application/json" \
     -O events.json \
     "https://odoo.bksc.net/calendar/events?lang=en&limit=25"
```

## API Testing Scenarios

### Basic Connectivity Test

1. **Test API Access:**
   ```
   GET /bank/journals
   Expected: 200 OK with JSON response
   ```

2. **Test Rate Limiting:**
   - Make 35+ requests in 1 minute
   - Expected: 429 Too Many Requests after limit

3. **Test Error Handling:**
   ```
   GET /bank/statements/INVALID
   Expected: 404 Not Found
   ```

### Banking API Tests

```bash
# 1. Get all bank accounts
curl "https://odoo.bksc.net/bank/journals"

# 2. Get statements for BANK account  
curl "https://odoo.bksc.net/bank/statements/BANK"

# 3. Get detailed statement
curl "https://odoo.bksc.net/bank/statements/BANK/31"

# 4. Test invalid account
curl "https://odoo.bksc.net/bank/statements/NONEXISTENT"
```

### Calendar API Tests

```bash
# 1. Get all events
curl "https://odoo.bksc.net/calendar/events"

# 2. Get events with date filtering
curl "https://odoo.bksc.net/calendar/events?start=2025-02-01&end=2025-02-28"

# 3. Get limited events in Thai
curl "https://odoo.bksc.net/calendar/events?lang=th&limit=10"

# 4. Test invalid date format
curl "https://odoo.bksc.net/calendar/events?start=invalid-date"
```

### Equipment API Tests

```bash
# 1. Get all categories
curl "https://odoo.bksc.net/equipment/categories"

# 2. Get catamarans
curl "https://odoo.bksc.net/equipment/categories/catamarans"

# 3. Get equipment details
curl "https://odoo.bksc.net/equipment/15"

# 4. Test Thai localization
curl "https://odoo.bksc.net/equipment/categories?lang=th"
```

### Team API Tests

```bash
# 1. Get team members in English
curl "https://odoo.bksc.net/team/members?lang=en"

# 2. Get team members in Thai
curl "https://odoo.bksc.net/team/members?lang=th"
```

## Common Issues & Solutions

### Issue: Connection Refused
**Symptoms:** `curl: (7) Failed to connect`
**Solutions:**
- Check if the API server is running
- Verify the base URL is correct
- Check firewall/network settings
- Try the local URL if testing locally

### Issue: Rate Limit Exceeded
**Symptoms:** `429 Too Many Requests`
**Solutions:**
- Wait for rate limit to reset (check `X-RateLimit-Reset` header)
- Reduce request frequency
- Implement exponential backoff in your client

### Issue: Invalid JSON Response
**Symptoms:** Malformed or unexpected JSON
**Solutions:**
- Check `Accept: application/json` header is set
- Verify endpoint URL is correct
- Check API documentation for expected response format

### Issue: Missing Data
**Symptoms:** Empty arrays or null values
**Solutions:**
- Verify you're using correct IDs/slugs
- Check if data exists in the system
- Try different language parameters
- Check if you have permission to view the data

## Development Workflow

### 1. Explore the API
1. Start with `/bank/journals` to get familiar with response format
2. Use `/equipment/categories` to understand category structure  
3. Try different language parameters (`lang=en` vs `lang=th`)
4. Test error cases with invalid IDs

### 2. Integration Development
1. Use Postman collection for API exploration
2. Copy working cURL commands to your application
3. Implement error handling for 404, 429, 500 errors
4. Add rate limiting to your client code

### 3. Production Deployment
1. Update `base_url` to production endpoint
2. Implement proper error handling and retries
3. Monitor rate limiting headers
4. Set up health checks

## Advanced Configuration

### Custom Environment Setup

Create your own Postman environment for different deployment stages:

```json
{
  "name": "BKSC Development",
  "values": [
    {"key": "base_url", "value": "http://localhost:8069"},
    {"key": "lang", "value": "en"},
    {"key": "debug", "value": "true"}
  ]
}
```

### Bulk Testing Script

```bash
#!/bin/bash
BASE_URL="https://odoo.bksc.net"

echo "Testing BKSC API endpoints..."

# Test each major endpoint
endpoints=(
  "/bank/journals"
  "/bank/statements/BANK" 
  "/calendar/events?limit=5"
  "/team/members"
  "/equipment/categories"
  "/equipment/categories/catamarans"
  "/equipment/15"
)

for endpoint in "${endpoints[@]}"; do
  echo -n "Testing ${endpoint}... "
  status=$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}${endpoint}")
  if [ "$status" -eq 200 ]; then
    echo "✓ OK ($status)"
  else
    echo "✗ FAIL ($status)"
  fi
done
```

### Rate Limiting Test

```python
import requests
import time
from datetime import datetime

def test_rate_limiting():
    base_url = "https://odoo.bksc.net"
    endpoint = "/bank/journals"
    
    start_time = datetime.now()
    request_count = 0
    
    while request_count < 35:  # Exceed the 30/minute limit
        response = requests.get(f"{base_url}{endpoint}")
        request_count += 1
        
        if response.status_code == 429:
            print(f"Rate limited after {request_count} requests")
            print(f"Headers: {dict(response.headers)}")
            break
        elif response.status_code != 200:
            print(f"Unexpected status: {response.status_code}")
            break
        
        time.sleep(1)  # 1 second between requests
    
    duration = (datetime.now() - start_time).total_seconds()
    print(f"Test completed in {duration:.1f} seconds")

if __name__ == "__main__":
    test_rate_limiting()
```

## Support

For setup assistance:
- **Documentation**: `API_DOCUMENTATION.md`
- **Email**: info@bksc.net
- **Collection Issues**: Check that environment variables are set correctly
- **API Issues**: Verify endpoint URLs match the OpenAPI specification