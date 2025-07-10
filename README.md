# Sailing Club Odoo Modules

This repository contains Odoo modules developed for sailing clubs and similar organizations.

## Available Modules

### account_statement_endpoints

REST API endpoints for exposing bank statements, calendar events, and team member information for public consumption. Designed for integration with static websites to provide financial transparency and event information.

**Features:**
- Public bank statement access with configurable visibility
- Calendar event API with filtering
- Team member directory
- CORS support for static site integration

## Installation

1. Clone this repository into your Odoo addons path:
   ```bash
   cd /path/to/odoo/addons
   git clone https://github.com/yourusername/sailing-club-modules.git
   ```

2. Update the addons list in Odoo
3. Install the desired modules through the Apps menu

## Requirements

- Odoo 14.0+ (tested on 15.0, 16.0, 17.0)
- Dependencies vary by module (see individual module README files)

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Follow OCA coding guidelines
4. Submit a pull request

## License

These modules are licensed under AGPL-3.0. See individual module manifests for details.

## Support

For issues and feature requests, please use the GitHub issue tracker.

## Author

Ross Golder <ross@golder.org>