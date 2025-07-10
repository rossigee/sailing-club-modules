Configuration
=============

Bank Journals
-------------

To make bank statements publicly accessible:

1. Navigate to **Accounting > Configuration > Journals**
2. Select the bank journal you want to expose
3. In the journal form, you'll see two new fields:
   
   * **Public Can View**: Check this box to make the journal publicly accessible
   * **Public Slug**: Enter a URL-friendly identifier (e.g., "BANK", "SAVINGS", "CHECKING")
     
     - Must be unique across all journals
     - Use only letters, numbers, and hyphens
     - This will be used in the API URLs: ``/bank/statements/BANK``

Team Members
------------

To add contacts to the public team directory:

1. Navigate to **Contacts**
2. Select or create the contact for your team member
3. In the contact form:
   
   * Ensure **Is a Company** is unchecked
   * Check **Is Team Member** to include them in the API
   * Fill in relevant fields:
     
     - Name (required)
     - Job Position (recommended)
     - Email (optional but recommended)
     - Phone/Mobile (optional)
     - Website (optional)
     - Photo (optional - will be served via API)

Calendar Events
---------------

Calendar events are automatically exposed if they meet these criteria:

* Event visibility is set to **Public**
* Event is active
* Event falls within the requested date range (if filtering is applied)

Security Considerations
-----------------------

1. **Data Exposure**: Only data explicitly marked as public is exposed
2. **Rate Limiting**: Not included by default - implement reverse proxy rate limiting
3. **CORS**: Enabled for all origins by default - restrict if needed
4. **No Authentication**: These are public endpoints - do not store sensitive data

API Base URL
------------

The API will be available at your Odoo instance URL, for example:

* Development: ``http://localhost:8069``
* Production: ``https://odoo.yourdomain.com``

Testing the API
---------------

After configuration, test the endpoints:

.. code-block:: bash

   # List all public journals
   curl https://odoo.yourdomain.com/bank/journals
   
   # Get statements for a journal
   curl https://odoo.yourdomain.com/bank/statements/BANK
   
   # Get team members
   curl https://odoo.yourdomain.com/team/members
   
   # Get calendar events
   curl https://odoo.yourdomain.com/calendar/events