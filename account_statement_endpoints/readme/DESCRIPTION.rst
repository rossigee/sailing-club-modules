This module provides REST API endpoints to expose bank statements, calendar events, and team member information for public consumption.

**Features:**

* Public REST API endpoints with CORS support for static website integration
* Bank journal overview with balance summaries
* Bank statement lists and detailed transaction views
* Statement attachment/image serving
* Calendar events with date filtering and attendee information
* Team member contact directory
* No authentication required for public data (configurable per journal/partner)

**Main Endpoints:**

* ``/bank/journals`` - List all public bank accounts with current balances
* ``/bank/statements/<slug>`` - List statements for a specific journal
* ``/bank/statements/<slug>/<id>`` - Detailed statement with transaction lines
* ``/calendar/events`` - Public calendar events with filtering options
* ``/team/members`` - Team member contact information

The module is designed for sailing clubs and similar organizations that need to provide financial transparency and event information to their members through a public website.