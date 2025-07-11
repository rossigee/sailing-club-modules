# BKSC Public API Documentation & Examples

Complete documentation and examples for the Ban Krut Sailing Club Public API.

## 📁 Contents

| File | Description |
|------|-------------|
| `API_DOCUMENTATION.md` | **Complete API reference** with endpoints, parameters, responses, and code examples |
| `SETUP_GUIDE.md` | **Quick start guide** for Postman, cURL, and other HTTP clients |
| `BKSC_Public_API.postman_collection.json` | **Postman collection** with all endpoints and example responses |
| `BKSC_API.postman_environment.json` | **Postman environment** with pre-configured variables |

## 🚀 Quick Start

### Option 1: Use Postman (Recommended)
1. Import `BKSC_Public_API.postman_collection.json` into Postman
2. Import `BKSC_API.postman_environment.json` as environment
3. Select the environment and start testing endpoints
4. All requests include automatic validation tests

### Option 2: Use cURL
```bash
# Get bank account summaries
curl "https://odoo.bksc.net/bank/journals"

# Get calendar events
curl "https://odoo.bksc.net/calendar/events?lang=en&limit=10"

# Get equipment categories  
curl "https://odoo.bksc.net/equipment/categories?lang=en"
```

### Option 3: Use Hoppscotch
1. Import the OpenAPI specification: `../static/description/api_specification.yaml`
2. Or manually configure requests using the documentation

## 📊 API Overview

### Endpoints Available

| Category | Endpoints | Features |
|----------|-----------|----------|
| **Banking** | 3 endpoints | Account summaries, statements, transaction details |
| **Calendar** | 1 endpoint | Public events with date filtering |
| **Team** | 1 endpoint | Member contact information |
| **Equipment** | 3 endpoints | Categories, listings, detailed specifications |

### Key Features
- ✅ **No Authentication Required** - All endpoints are public
- ✅ **Rate Limited** - 30-60 requests/minute depending on endpoint
- ✅ **Multi-language** - English/Thai localization support
- ✅ **CORS Enabled** - Ready for web browser integration
- ✅ **OpenAPI Spec** - Complete specification available
- ✅ **Comprehensive Examples** - Postman collection with tests

## 🌐 Base URLs

- **Production**: `https://odoo.bksc.net`
- **Development**: `http://localhost:8080` (mock server)

## 📚 Documentation Structure

### 1. API_DOCUMENTATION.md
Complete API reference including:
- Endpoint descriptions and parameters
- Request/response examples
- Error handling
- Rate limiting details
- Code examples in multiple languages (JavaScript, Python, cURL)
- Security considerations

### 2. SETUP_GUIDE.md  
Step-by-step setup instructions for:
- Postman configuration
- Environment variable setup
- Testing scenarios
- Common troubleshooting
- Development workflow

### 3. Postman Collection
Ready-to-use collection with:
- All API endpoints pre-configured
- Example responses for each endpoint
- Automatic test scripts
- Environment variable integration
- Rate limiting validation

### 4. Environment Configuration
Pre-configured variables for:
- Base URLs (production/development)
- Language preferences
- Test data IDs and slugs
- Date ranges for filtering

## 🎯 Example Usage Scenarios

### Website Integration
```javascript
// Get equipment categories for navigation menu
const categories = await fetch('https://odoo.bksc.net/equipment/categories?lang=en')
  .then(r => r.json());

// Display on website
categories.categories.forEach(cat => {
  console.log(`${cat.name}: ${cat.equipment_count} items`);
});
```

### Financial Dashboard
```python
import requests

# Get current financial status
response = requests.get('https://odoo.bksc.net/bank/journals')
data = response.json()

print(f"Total Balance: ฿{data['total_balance']:,.2f}")
for account in data['journals']:
    latest = account['latest_statement']
    print(f"{account['name']}: ฿{latest['balance_end']:,.2f}")
```

### Event Calendar
```bash
# Get this month's events for calendar widget
curl "https://odoo.bksc.net/calendar/events?start=2025-01-01&end=2025-01-31&lang=en" \
  | jq '.events[] | {name, start, location}'
```

## 🔧 Development Tools

### Supported Tools
- **Postman** - Import collection and environment files
- **Hoppscotch** - Import OpenAPI specification
- **Insomnia** - Import OpenAPI specification  
- **Swagger UI** - Load OpenAPI specification
- **cURL** - Use provided examples
- **HTTPie** - Clean command-line interface
- **Any HTTP client** - Standard REST API

### Testing & Validation
- All endpoints return consistent JSON responses
- Built-in rate limiting with proper headers
- Comprehensive error handling with meaningful messages
- CORS enabled for browser testing
- Response validation included in Postman tests

## 📞 Support

- **Email**: info@bksc.net
- **Website**: https://bksc.net
- **API Issues**: Check setup guide troubleshooting section
- **Feature Requests**: Contact via email

## 📈 API Versions

- **Current Version**: 1.1.0
- **OpenAPI Spec**: 3.0.3
- **Backward Compatibility**: Maintained for all 1.x versions

## 🔄 Updates & Changelog

The API is actively maintained. Check `API_DOCUMENTATION.md` for the latest changelog and version information.

---

*This documentation is part of the BKSC sailing club management system. For internal administrative access, contact the club management.*