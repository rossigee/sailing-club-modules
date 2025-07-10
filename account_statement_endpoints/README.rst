========================
Bank Statement Endpoints
========================

Overview
========

Module to hold all the extra functionality I need to manage bank statements for the clubs.

* Sort statement lines in date order on save.
* Re-calculate ending balance from start balance plus transactions.
* Endpoints to make the statement, lines and attachments publicly available.
* Calendar events endpoint for public event access.

Features
========

* Public REST API endpoints with CORS support
* Bank journals overview with balance summaries
* Bank statements list and detail views
* Statement attachment/image serving
* Calendar events with filtering
* No authentication required for public data

API Documentation
=================

See `API_DOCUMENTATION.md` for comprehensive endpoint documentation including:

* All available endpoints
* Request/response formats
* Query parameters
* Error handling
* Usage examples

Configuration
=============

To make journals publicly accessible:

1. Go to Accounting > Configuration > Journals
2. Edit the journal you want to make public
3. Check the "Public Can View" checkbox
4. Set a unique "Public Slug" (e.g., "BANK", "SAVINGS")

Requirements
============

* Odoo 14.0+ (tested on 15.0, 16.0, 17.0)
* account module
* calendar module


Credits
=======

Authors
~~~~~~~

* Ross Golder <ross@golder.org>
