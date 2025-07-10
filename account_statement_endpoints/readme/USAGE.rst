The module provides REST API endpoints that can be consumed by any client application (website, mobile app, etc.).

Quick Start Example
-------------------

Here's a simple example using JavaScript to display bank account balances:

.. code-block:: javascript

   // Fetch and display bank accounts
   fetch('https://odoo.yourdomain.com/bank/journals')
     .then(response => response.json())
     .then(data => {
       console.log(`Total Balance: ${data.total_balance}`);
       data.journals.forEach(journal => {
         console.log(`${journal.name}: ${journal.latest_statement.balance_end}`);
       });
     });

Endpoints Overview
------------------

1. **Bank Journals** - ``GET /bank/journals``
   
   Returns all public bank accounts with current balances

2. **Bank Statements** - ``GET /bank/statements/<slug>``
   
   Returns all statements for a specific journal

3. **Statement Detail** - ``GET /bank/statements/<slug>/<id>``
   
   Returns detailed transaction lines for a statement

4. **Team Members** - ``GET /team/members``
   
   Returns contact information for team members

5. **Calendar Events** - ``GET /calendar/events?start=YYYY-MM-DD&end=YYYY-MM-DD``
   
   Returns public events with optional date filtering

Frontend Integration
--------------------

The API is designed for integration with static websites. Common use cases:

* **Financial Transparency Page**: Display real-time account balances
* **Statement Archive**: Browse historical bank statements
* **Team Directory**: Show instructor/staff contact information
* **Event Calendar**: Display upcoming club activities

For detailed implementation examples in React, Vue.js, and vanilla JavaScript, see:

* `Bank Statements Implementation Guide <BANK_STATEMENTS_GUIDE.html>`_
* `Calendar Events Implementation Guide <CALENDAR_EVENTS_GUIDE.html>`_
* `Team Members Implementation Guide <TEAM_MEMBERS_GUIDE.html>`_

Error Handling
--------------

All endpoints return consistent error responses:

.. code-block:: json

   {
     "status": "error",
     "error": "Description of the error"
   }

Common status codes:

* ``200`` - Success
* ``404`` - Resource not found (e.g., invalid journal slug)
* ``500`` - Server error

Best Practices
--------------

1. **Cache responses** client-side to reduce server load
2. **Handle errors gracefully** with user-friendly messages
3. **Use loading states** while fetching data
4. **Implement retry logic** for network failures
5. **Respect rate limits** if implemented