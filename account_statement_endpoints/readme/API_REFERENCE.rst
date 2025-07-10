# Bank Statement Endpoints API Documentation

This module provides public REST API endpoints for accessing bank statements, journals, calendar events, and team member information.

## Usage Guides

For detailed implementation examples and best practices, see:
- [Bank Statements API Usage Guide](readme/bank-statements-api.md)
- [Calendar Events API Usage Guide](readme/calendar-events-api.md)
- [Team Members API Usage Guide](readme/team-members-api.md)

## Base URL
```
https://odoo.bksc.net
```

## Authentication
All endpoints use `auth='public'` - no authentication required.

## CORS Support
All endpoints support CORS with:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, POST, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type, Authorization`

## Endpoints

### 1. Get Bank Journals
```
GET /bank/journals
```

Returns a list of all public bank journals with their latest statement balances.

**Response:**
```json
{
  "status": "ok",
  "total_balance": 1234567.89,
  "journals": [
    {
      "id": 1,
      "name": "Bank Account",
      "public_slug": "BANK",
      "latest_statement": {
        "id": 31,
        "name": "BANK/2024/0031",
        "date": "2024-01-31",
        "balance_end": 1234567.89
      }
    }
  ]
}
```

### 2. Get Bank Statements List
```
GET /bank/statements/<journal_slug>
```

Returns all statements for a specific journal.

**Parameters:**
- `journal_slug`: The public slug of the journal (e.g., "BANK")

**Response:**
```json
{
  "status": "ok",
  "account": {
    "name": "Bank Account",
    "number": "1234567890",
    "bankname": "Example Bank",
    "branch": "Bangkok"
  },
  "statements": [
    {
      "id": 31,
      "name": "BANK/2024/0031",
      "date": "2024-01-31",
      "balance_end": 1234567.89,
      "attachments": [
        {
          "id": 123,
          "description": "Statement scan",
          "url": "https://odoo.bksc.net/bank/statements/image/123"
        }
      ]
    }
  ]
}
```

### 3. Get Bank Statement Detail
```
GET /bank/statements/<journal_slug>/<statement_id>
```

Returns detailed information about a specific bank statement including all transaction lines.

**Parameters:**
- `journal_slug`: The public slug of the journal (e.g., "BANK")
- `statement_id`: The ID of the statement (e.g., 31)

**Response:**
```json
{
  "status": "ok",
  "header": {
    "id": 31,
    "name": "BANK/2024/0031",
    "date": "2024-01-31",
    "balance_start": 1000000.00,
    "balance_end": 1234567.89
  },
  "lines": [
    {
      "date": "2024-01-15",
      "payment_ref": "Transfer from member",
      "amount": 5000.00
    },
    {
      "date": "2024-01-20",
      "payment_ref": "Equipment purchase",
      "amount": -2500.00
    }
  ],
  "attachments": [
    {
      "id": 123,
      "description": "Statement scan",
      "url": "https://odoo.bksc.net/bank/statements/image/123"
    }
  ]
}
```

### 4. Get Statement Attachment Image
```
GET /bank/statements/image/<attachment_id>
```

Returns the actual image file for a statement attachment.

**Parameters:**
- `attachment_id`: The ID of the attachment

**Response:**
- Content-Type: `image/jpeg`
- Binary image data

### 5. Get Team Members
```
GET /team/members
```

Returns public team member contact information.

**Response:**
```json
{
  "status": "ok",
  "count": 2,
  "members": [
    {
      "id": 14,
      "name": "Ross Golder",
      "email": "ross@example.com",
      "phone": "+66 123 456 789",
      "mobile": "+66 987 654 321",
      "function": "Sailing Instructor",
      "image_url": "/web/image/res.partner/14/image_1920",
      "website": "https://example.com"
    },
    {
      "id": 15,
      "name": "Chai Example",
      "email": "chai@example.com",
      "phone": "+66 111 222 333",
      "mobile": "+66 444 555 666",
      "function": "Club Manager",
      "image_url": "/web/image/res.partner/15/image_1920"
    }
  ]
}
```

**Note:** Currently uses hardcoded partner IDs (14, 15). In production, you should:
- Add a boolean field `is_team_member` to res.partner, or
- Use partner categories/tags to identify team members

### 6. Get Calendar Events
```
GET /calendar/events
```

Returns public calendar events.

**Query Parameters:**
- `start` or `start_date`: Filter events starting after this date (ISO format)
- `end` or `end_date`: Filter events starting before this date (ISO format)
- `limit`: Maximum number of events to return (default: 50)

**Response:**
```json
{
  "status": "ok",
  "count": 3,
  "events": [
    {
      "id": 1,
      "name": "Weekly Sailing Training",
      "description": "Regular training session",
      "location": "Ban Krut Marina",
      "start": "2024-07-12T09:00:00",
      "stop": "2024-07-12T12:00:00",
      "duration": 3.0,
      "allday": false,
      "state": "open",
      "class": "public",
      "show_as": "busy",
      "user_id": 2,
      "attendees": [
        {
          "id": 101,
          "partner_id": 45,
          "name": "John Sailor",
          "email": "john@example.com",
          "state": "accepted"
        }
      ],
      "categories": [
        {
          "id": 1,
          "name": "Training"
        }
      ],
      "recurrency": false,
      "rrule": ""
    }
  ]
}
```

## Error Responses

All endpoints return consistent error responses:

### 404 Not Found
```json
{
  "status": "not found",
  "error": "No public journal found with slug 'INVALID'"
}
```

### 500 Server Error
```json
{
  "status": "error",
  "error": "An unexpected error occurred: [error details]"
}
```

## Model Requirements

For these endpoints to work, the following Odoo models need specific fields:

### account.journal
- `public_can_view`: Boolean field to mark journals as publicly accessible
- `public_slug`: Char field for URL-friendly identifier

### account.bank.statement
- Standard Odoo fields (name, date, balance_start, balance_end, etc.)
- Related to journal with `public_can_view = True`

### account.bank.statement.line
- Standard Odoo fields (date, payment_ref, amount, etc.)

### calendar.event
- Standard Odoo calendar fields
- Only events with `class = 'public'` are returned

## Usage Example (JavaScript)

```javascript
// Fetch all bank journals
const response = await fetch('https://odoo.bksc.net/bank/journals');
const data = await response.json();

// Fetch statements for a specific journal
const statements = await fetch('https://odoo.bksc.net/bank/statements/BANK');
const statementsData = await statements.json();

// Fetch statement details with transactions
const detail = await fetch('https://odoo.bksc.net/bank/statements/BANK/31');
const detailData = await detail.json();

// Fetch calendar events for July 2024
const events = await fetch('https://odoo.bksc.net/calendar/events?start=2024-07-01&end=2024-07-31');
const eventsData = await events.json();
```

## Security Notes

1. Only journals with `public_can_view = True` are accessible
2. Only calendar events with `class = 'public'` are returned
3. Attachment images are only accessible if they belong to a public journal statement
4. No sensitive data (passwords, internal notes, etc.) is exposed
5. Consider implementing rate limiting to prevent abuse