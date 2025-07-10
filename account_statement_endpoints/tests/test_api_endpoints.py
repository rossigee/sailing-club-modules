# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase, tagged
from odoo import fields
from datetime import datetime, timedelta
import json


@tagged('post_install', '-at_install')
class TestAPIEndpoints(TransactionCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # Create test data
        cls.currency = cls.env.ref('base.USD')
        
        # Create a test bank journal with public access
        cls.journal = cls.env['account.journal'].create({
            'name': 'Test Bank',
            'type': 'bank',
            'code': 'TBNK',
            'currency_id': cls.currency.id,
            'public_can_view': True,
            'public_slug': 'TEST',
        })
        
        # Create bank statements
        cls.statement1 = cls.env['account.bank.statement'].create({
            'name': 'TEST/2024/0001',
            'journal_id': cls.journal.id,
            'date': fields.Date.today() - timedelta(days=30),
            'balance_start': 1000.00,
            'balance_end_real': 1500.00,
        })
        
        cls.statement2 = cls.env['account.bank.statement'].create({
            'name': 'TEST/2024/0002',
            'journal_id': cls.journal.id,
            'date': fields.Date.today(),
            'balance_start': 1500.00,
            'balance_end_real': 2000.00,
        })
        
        # Create statement lines
        cls.env['account.bank.statement.line'].create({
            'statement_id': cls.statement1.id,
            'date': fields.Date.today() - timedelta(days=25),
            'payment_ref': 'Customer Payment',
            'amount': 500.00,
        })
        
        # Create team members
        cls.team_member1 = cls.env['res.partner'].create({
            'name': 'Test Instructor',
            'email': 'instructor@test.com',
            'phone': '+1234567890',
            'mobile': '+0987654321',
            'function': 'Sailing Instructor',
            'is_company': False,
            'is_team_member': True,
        })
        
        cls.team_member2 = cls.env['res.partner'].create({
            'name': 'Test Manager',
            'email': 'manager@test.com',
            'function': 'Club Manager',
            'is_company': False,
            'is_team_member': True,
        })
        
        # Create a non-team member
        cls.regular_partner = cls.env['res.partner'].create({
            'name': 'Regular Customer',
            'email': 'customer@test.com',
            'is_company': False,
            'is_team_member': False,
        })
        
        # Create test calendar event
        cls.event = cls.env['calendar.event'].create({
            'name': 'Test Sailing Event',
            'description': 'Test event description',
            'location': 'Test Marina',
            'start': datetime.now() + timedelta(days=7),
            'stop': datetime.now() + timedelta(days=7, hours=3),
            'allday': False,
            'class': 'public',
            'show_as': 'busy',
        })
        
    def test_bank_journals_endpoint(self):
        """Test /bank/journals endpoint"""
        controller = self.env['ir.http']._dispatch()
        
        # Simulate HTTP request
        with self.env.cr.savepoint():
            from odoo.addons.account_statement_endpoints.controllers.controllers import BankStatements
            ctrl = BankStatements()
            
            # Mock request
            from unittest.mock import Mock
            request = Mock()
            request.env = self.env
            import odoo.http
            odoo.http.request = request
            
            response = ctrl.bank_journals()
            data = json.loads(response.data)
            
            self.assertEqual(data['status'], 'ok')
            self.assertEqual(len(data['journals']), 1)
            self.assertEqual(data['journals'][0]['public_slug'], 'TEST')
            self.assertEqual(data['total_balance'], 2000.00)
            
    def test_bank_statements_list_endpoint(self):
        """Test /bank/statements/<slug> endpoint"""
        from odoo.addons.account_statement_endpoints.controllers.controllers import BankStatements
        ctrl = BankStatements()
        
        # Mock request
        from unittest.mock import Mock
        request = Mock()
        request.env = self.env
        import odoo.http
        odoo.http.request = request
        
        response = ctrl.bank_statements_list_view('TEST')
        data = json.loads(response.data)
        
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(len(data['statements']), 2)
        self.assertEqual(data['account']['name'], 'Test Bank')
        
    def test_bank_statement_detail_endpoint(self):
        """Test /bank/statements/<slug>/<id> endpoint"""
        from odoo.addons.account_statement_endpoints.controllers.controllers import BankStatements
        ctrl = BankStatements()
        
        # Mock request
        from unittest.mock import Mock
        request = Mock()
        request.env = self.env
        import odoo.http
        odoo.http.request = request
        
        response = ctrl.bank_statements_detail_view('TEST', str(self.statement1.id))
        data = json.loads(response.data)
        
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['header']['name'], 'TEST/2024/0001')
        self.assertEqual(len(data['lines']), 1)
        self.assertEqual(data['lines'][0]['amount'], 500.00)
        
    def test_team_members_endpoint(self):
        """Test /team/members endpoint"""
        from odoo.addons.account_statement_endpoints.controllers.controllers import BankStatements
        ctrl = BankStatements()
        
        # Mock request
        from unittest.mock import Mock
        request = Mock()
        request.env = self.env
        import odoo.http
        odoo.http.request = request
        
        response = ctrl.team_members()
        data = json.loads(response.data)
        
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['count'], 2)  # Only team members, not regular partner
        
        # Check team member data
        member_names = [m['name'] for m in data['members']]
        self.assertIn('Test Instructor', member_names)
        self.assertIn('Test Manager', member_names)
        self.assertNotIn('Regular Customer', member_names)
        
        # Check data structure
        instructor = next(m for m in data['members'] if m['name'] == 'Test Instructor')
        self.assertEqual(instructor['email'], 'instructor@test.com')
        self.assertEqual(instructor['function'], 'Sailing Instructor')
        self.assertTrue(instructor['image_url'])
        
    def test_calendar_events_endpoint(self):
        """Test /calendar/events endpoint"""
        from odoo.addons.account_statement_endpoints.controllers.controllers import BankStatements
        ctrl = BankStatements()
        
        # Mock request
        from unittest.mock import Mock
        request = Mock()
        request.env = self.env
        import odoo.http
        odoo.http.request = request
        
        # Test without filters
        response = ctrl.calendar_events()
        data = json.loads(response.data)
        
        self.assertEqual(data['status'], 'ok')
        self.assertGreaterEqual(data['count'], 1)
        
        # Test with date filters
        start_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        end_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        
        response = ctrl.calendar_events(start=start_date, end=end_date)
        data = json.loads(response.data)
        
        self.assertEqual(data['status'], 'ok')
        
        # Check event data
        if data['count'] > 0:
            event = data['events'][0]
            self.assertIn('name', event)
            self.assertIn('start', event)
            self.assertIn('stop', event)
            self.assertIn('class', event)
            
    def test_error_handling(self):
        """Test error responses"""
        from odoo.addons.account_statement_endpoints.controllers.controllers import BankStatements
        ctrl = BankStatements()
        
        # Mock request
        from unittest.mock import Mock
        request = Mock()
        request.env = self.env
        import odoo.http
        odoo.http.request = request
        
        # Test non-existent journal
        response = ctrl.bank_statements_list_view('NONEXISTENT')
        data = json.loads(response.data)
        
        self.assertEqual(data['status'], 'not found')
        self.assertIn('error', data)
        
        # Test non-existent statement
        response = ctrl.bank_statements_detail_view('TEST', '99999')
        data = json.loads(response.data)
        
        self.assertEqual(data['status'], 'not found')
        self.assertIn('error', data)
        
    def test_cors_headers(self):
        """Test CORS headers are properly set"""
        from odoo.addons.account_statement_endpoints.controllers.controllers import BankStatements
        ctrl = BankStatements()
        
        # Test _make_json_response includes CORS headers
        response = ctrl._make_json_response({'test': 'data'})
        
        headers_dict = dict(response.headers)
        self.assertEqual(headers_dict.get('Access-Control-Allow-Origin'), '*')
        self.assertEqual(headers_dict.get('Access-Control-Allow-Methods'), 'GET, POST, OPTIONS')
        self.assertEqual(headers_dict.get('Access-Control-Allow-Headers'), 'Content-Type, Authorization')
        
    def test_public_visibility_filter(self):
        """Test that only public journals are exposed"""
        # Create a private journal
        private_journal = self.env['account.journal'].create({
            'name': 'Private Bank',
            'type': 'bank',
            'code': 'PRVT',
            'currency_id': self.currency.id,
            'public_can_view': False,
            'public_slug': 'PRIVATE',
        })
        
        from odoo.addons.account_statement_endpoints.controllers.controllers import BankStatements
        ctrl = BankStatements()
        
        # Mock request
        from unittest.mock import Mock
        request = Mock()
        request.env = self.env
        import odoo.http
        odoo.http.request = request
        
        # Should not appear in journals list
        response = ctrl.bank_journals()
        data = json.loads(response.data)
        
        journal_slugs = [j['public_slug'] for j in data['journals']]
        self.assertNotIn('PRIVATE', journal_slugs)
        
        # Should return 404 when accessed directly
        response = ctrl.bank_statements_list_view('PRIVATE')
        data = json.loads(response.data)
        
        self.assertEqual(data['status'], 'not found')