To install this module:

1. Place the module in your Odoo addons path
2. Update the module list (Apps > Update Apps List)
3. Search for "Bank Statements Endpoint" and click Install

**Dependencies:**

* ``account_statement_base`` module must be installed first
* Requires Odoo 14.0 or later (tested on 15.0, 16.0, 17.0)

**Post-Installation:**

1. Configure bank journals for public access:
   
   * Go to Accounting > Configuration > Journals
   * Edit the journals you want to make public
   * Check "Public Can View"
   * Set a unique "Public Slug" (e.g., "BANK", "SAVINGS")

2. Mark team members:
   
   * Go to Contacts
   * Edit team member contacts
   * Check "Is Team Member" to include them in the public API

3. Ensure calendar events are marked as public:
   
   * Only events with visibility set to "Public" will be exposed

**CORS Configuration:**

The module automatically adds CORS headers to all endpoints. If you need to restrict origins, modify the controller methods to check against a whitelist.