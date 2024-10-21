from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged

from werkzeug.test import Client
from odoo.service.wsgi_server import application

import logging
_logger = logging.getLogger(__name__)

@tagged('post_install', '-at_install')
class BankStatementsEndpointTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(BankStatementsEndpointTestCase, cls).setUpClass()

        # Create data for each test. Doing it in setUpClass instead of setUp or each test case reduces testing time and code duplication.
        cls.properties = cls.env['account.journal'].create([
            # Create a Bank Journal
            {
                'name': 'Bank Journal',
                'type': 'bank',
                'public_can_view': True,
                'public_slug': 'bank',
            },

            # Create a Cash Journal
            {
                'name': 'Cash Journal',
                'type': 'cash',
                'public_can_view': True,
                'public_slug': 'cash',
            },

            # Create another journal
            {
                'name': 'Off-balance Journal',
                'type': 'off_balance',
                'public_can_view': False,
            }
        ])

    @tagged('sailing', 'post_install')
    def test_bank_statements_endpoint(self):
        """Test that the statements endpoint only returns journals marked public."""

        # Test an 'http.route'...
        c = Client(application)
        r = c.get("/bank/statements")
        _logger.info(r.status_code)
        self.assertEqual(r.status_code, 201)
        _logger.info(r.data.decode('utf-8'))
