Changelog
=========

16.0.1.1.0 (unreleased)
-----------------------

**Features**

* Add team members endpoint at ``/team/members``
* Add ``is_team_member`` field to ``res.partner`` model
* Add CORS support to all endpoints
* Add calendar events endpoint at ``/calendar/events``

**Improvements**

* Add comprehensive API documentation
* Add usage guides for React, Vue.js, and vanilla JavaScript
* Add unit tests for all endpoints
* Improve error handling and response consistency

**Fixes**

* Fix CORS preflight request handling
* Fix date serialization in JSON responses

16.0.1.0.1 (2024-01-01)
-----------------------

**Features**

* Initial release
* Bank journals endpoint at ``/bank/journals``
* Bank statements list endpoint at ``/bank/statements/<slug>``
* Bank statement detail endpoint at ``/bank/statements/<slug>/<id>``
* Statement attachment serving at ``/bank/statements/image/<id>``
* Configurable public visibility per journal