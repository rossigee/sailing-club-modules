# Ban Krut Sailing Club Public API Documentation

## Overview

The BKSC Public API provides read-only access to public information about the sailing club including banking data, calendar events, team members, and equipment inventory. The API is designed for website integration and requires no authentication for public endpoints.

## Base URL

**Production:** `https://odoo.bksc.net`  
**Development:** `http://localhost:8080` (mock server)

## Features

- 🏦 **Banking**: Account summaries and detailed statements
- 📅 **Calendar**: Public events with filtering capabilities  
- 👥 **Team**: Member contact information
- ⛵ **Equipment**: Categories and detailed equipment listings
- 🌐 **Multi-language**: English/Thai localization support
- 🚦 **Rate Limiting**: Built-in API protection
- 📖 **OpenAPI**: Complete specification available

## Rate Limiting

| Endpoint Type | Rate Limit | Hourly Limit |
|---------------|------------|--------------|
| Standard endpoints | 30 requests/minute | 500 requests/hour |
| Detail views | 20 requests/minute | 300 requests/hour |
| Images | 60 requests/minute | 1000 requests/hour |

Rate limit headers are included in responses:
- `X-RateLimit-Limit`: Requests allowed per period
- `X-RateLimit-Remaining`: Requests remaining in current period
- `X-RateLimit-Reset`: Time when the rate limit resets

## Localization

Most endpoints support the `lang` parameter for localized content:
- `lang=en` - English (default)
- `lang=th` - Thai

## API Endpoints

### Banking API

#### GET `/bank/journals`
Get bank account summaries with latest statement balances.

**Response:**
```json
{
  "status": "ok",
  "total_balance": 125750.50,
  "journals": [
    {
      "id": 1,
      "name": "Bank Account - Krungsri",
      "public_slug": "BANK",
      "latest_statement": {
        "id": 31,
        "name": "BANK/2025/001",
        "date": "2025-01-15",
        "balance_end": 85250.50,
        "attachments": [...]
      }
    }
  ]
}
```

#### GET `/bank/statements/{slug}`
Get bank statements for a specific account by public slug.

**Parameters:**
- `slug` (path): Account slug (e.g., 'BANK', 'SAVINGS')

**Example:** `/bank/statements/BANK`

#### GET `/bank/statements/{slug}/{id}`
Get detailed bank statement with transaction lines.

**Parameters:**
- `slug` (path): Account slug
- `id` (path): Statement ID

**Example:** `/bank/statements/BANK/31`

### Calendar API

#### GET `/calendar/events`
Get public calendar events with optional filtering.

**Parameters:**
- `start` (query): Start date filter (YYYY-MM-DD)
- `end` (query): End date filter (YYYY-MM-DD)  
- `limit` (query): Max events (1-100, default 50)
- `lang` (query): Language (en|th, default en)

**Example:** `/calendar/events?start=2025-02-01&end=2025-02-28&lang=en`

**Response:**
```json
{
  "status": "ok",
  "count": 2,
  "events": [
    {
      "id": 15,
      "name": "Sailing Regatta 2025",
      "description": "Annual sailing competition",
      "location": "BKSC Marina",
      "start": "2025-02-15T09:00:00+07:00",
      "stop": "2025-02-15T17:00:00+07:00",
      "duration": 8.0,
      "allday": false,
      "state": "open",
      "class": "public",
      "attendees": [...],
      "categories": [...]
    }
  ]
}
```

### Team API

#### GET `/team/members`
Get contact information for publicly listed team members.

**Parameters:**
- `lang` (query): Language (en|th, default en)

**Response:**
```json
{
  "status": "ok",
  "count": 3,
  "members": [
    {
      "id": 1,
      "name": "Captain Mike Thompson",
      "email": "captain@bksc.net",
      "phone": "+66-32-123-456",
      "mobile": "+66-89-123-4567",
      "function": "Sailing Instructor & Commodore",
      "image_url": "/team/images/1",
      "website": "https://bksc.net/team/mike"
    }
  ]
}
```

### Equipment API

#### GET `/equipment/categories`
Get equipment categories with counts.

**Parameters:**
- `lang` (query): Language (en|th, default en)

**Response:**
```json
{
  "status": "ok",
  "categories": [
    {
      "id": 1,
      "name": "Catamarans",
      "slug": "catamarans",
      "description": "Multi-hull sailing boats",
      "equipment_count": 8,
      "image_url": "/equipment/categories/images/1"
    }
  ]
}
```

#### GET `/equipment/categories/{slug}`
Get equipment items in a specific category.

**Parameters:**
- `slug` (path): Category slug (e.g., 'catamarans', 'dinghys')
- `lang` (query): Language (en|th, default en)

**Example:** `/equipment/categories/catamarans?lang=en`

#### GET `/equipment/{id}`
Get detailed equipment information.

**Parameters:**
- `id` (path): Equipment ID
- `lang` (query): Language (en|th, default en)

**Example:** `/equipment/15?lang=en`

**Response includes:**
- Basic equipment details
- Condition and availability
- Rental rates
- Technical specifications
- Image gallery
- Financial values (purchase/current value)

## Getting Started

### 1. Using Postman

1. **Import Collection:**
   - Download: `BKSC_Public_API.postman_collection.json`
   - Import into Postman
   - Collection includes pre-configured requests and examples

2. **Set Environment Variables:**
   ```
   base_url: https://odoo.bksc.net
   lang: en
   account_slug: BANK
   statement_id: 31
   category_slug: catamarans
   equipment_id: 15
   ```

3. **Run Requests:**
   - No authentication required
   - All requests include automatic tests
   - Response examples provided

### 2. Using cURL

**Get bank journals:**
```bash
curl -X GET "https://odoo.bksc.net/bank/journals" \
  -H "Accept: application/json"
```

**Get calendar events (filtered):**
```bash
curl -X GET "https://odoo.bksc.net/calendar/events?start=2025-02-01&end=2025-02-28&lang=en" \
  -H "Accept: application/json"
```

**Get equipment details:**
```bash
curl -X GET "https://odoo.bksc.net/equipment/15?lang=en" \
  -H "Accept: application/json"
```

### 3. Using JavaScript/Fetch

```javascript
// Get bank account summaries
async function getBankJournals() {
  const response = await fetch('https://odoo.bksc.net/bank/journals', {
    headers: {
      'Accept': 'application/json'
    }
  });
  const data = await response.json();
  return data;
}

// Get equipment categories
async function getEquipmentCategories(lang = 'en') {
  const response = await fetch(`https://odoo.bksc.net/equipment/categories?lang=${lang}`, {
    headers: {
      'Accept': 'application/json'
    }
  });
  const data = await response.json();
  return data;
}

// Get calendar events with filtering
async function getEvents(start, end, lang = 'en') {
  const url = new URL('https://odoo.bksc.net/calendar/events');
  url.searchParams.set('lang', lang);
  if (start) url.searchParams.set('start', start);
  if (end) url.searchParams.set('end', end);
  
  const response = await fetch(url, {
    headers: {
      'Accept': 'application/json'
    }
  });
  const data = await response.json();
  return data;
}
```

### 4. Using Python/Requests

```python
import requests
from datetime import datetime

BASE_URL = "https://odoo.bksc.net"

def get_bank_journals():
    """Get bank account summaries"""
    response = requests.get(f"{BASE_URL}/bank/journals")
    response.raise_for_status()
    return response.json()

def get_equipment_by_category(slug, lang='en'):
    """Get equipment in a specific category"""
    params = {'lang': lang}
    response = requests.get(f"{BASE_URL}/equipment/categories/{slug}", params=params)
    response.raise_for_status()
    return response.json()

def get_events(start_date=None, end_date=None, lang='en', limit=50):
    """Get calendar events with optional filtering"""
    params = {'lang': lang, 'limit': limit}
    if start_date:
        params['start'] = start_date.strftime('%Y-%m-%d')
    if end_date:
        params['end'] = end_date.strftime('%Y-%m-%d')
    
    response = requests.get(f"{BASE_URL}/calendar/events", params=params)
    response.raise_for_status()
    return response.json()

# Example usage
if __name__ == "__main__":
    # Get all bank accounts
    journals = get_bank_journals()
    print(f"Total balance: ฿{journals['total_balance']:,.2f}")
    
    # Get catamarans in English
    catamarans = get_equipment_by_category('catamarans', 'en')
    print(f"Found {len(catamarans['equipment'])} catamarans")
    
    # Get this month's events
    from datetime import date
    start = date(2025, 2, 1)
    end = date(2025, 2, 28)
    events = get_events(start, end)
    print(f"Found {events['count']} events in February")
```

## Error Handling

### Standard Error Response
```json
{
  "status": "error",
  "error": "Descriptive error message"
}
```

### HTTP Status Codes
- `200 OK`: Successful request
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### Common Error Scenarios

**Rate Limit Exceeded:**
```json
{
  "status": "error",
  "error": "Rate limit exceeded. Please wait before making more requests."
}
```

**Resource Not Found:**
```json
{
  "status": "not found",
  "error": "Account with slug 'INVALID' not found"
}
```

**Invalid Parameters:**
```json
{
  "status": "error",
  "error": "Invalid date format. Use YYYY-MM-DD."
}
```

## CORS Support

The API includes Cross-Origin Resource Sharing (CORS) headers for web browser access:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type, Accept`

## Data Formats

### Dates
- ISO 8601 format: `YYYY-MM-DD` for dates
- ISO 8601 format: `YYYY-MM-DDTHH:MM:SS+TZ` for timestamps
- Example: `2025-02-15T09:00:00+07:00`

### Currency
- Thai Baht (THB) as decimal numbers
- Example: `2500.00` represents ฿2,500.00

### Images
- Image URLs are relative to the base URL
- Example: `/equipment/images/15/main.jpg`
- Access via: `https://odoo.bksc.net/equipment/images/15/main.jpg`

## Security Considerations

- **No Authentication Required**: All endpoints are public
- **Rate Limiting**: Prevents API abuse
- **Read-Only**: All endpoints are GET requests only
- **Input Validation**: Parameters are validated server-side
- **HTTPS Only**: Production API requires HTTPS

## Support

For API support or questions:
- **Email**: info@bksc.net
- **Website**: https://bksc.net
- **Issues**: Report bugs or request features via the project repository

## OpenAPI Specification

Complete API specification is available at:
`/static/description/api_specification.yaml`

Import this file into tools like:
- Swagger UI
- Postman
- Insomnia
- OpenAPI Generator

## Changelog

### Version 1.1.0
- Added equipment management endpoints
- Enhanced rate limiting
- Multi-language support for all endpoints
- Improved error handling
- Added CORS support

### Version 1.0.0
- Initial release with banking and calendar APIs
- Basic rate limiting
- OpenAPI specification