# -*- coding: utf-8 -*-
from odoo import http
from odoo.tools import date_utils

import json, base64
import werkzeug.datastructures

class BankStatements(http.Controller):
    # Included in 'odoo.http' from Odoo (15/16/17?)
    def _make_json_response(self, data, headers=None, cookies=None, status=200):
        headers = werkzeug.datastructures.Headers(headers)
        headers['Content-Length'] = len(data)
        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json; charset=utf-8'
        data = json.dumps(data, ensure_ascii=False, default=date_utils.json_default)
        return http.Response(data, status=status, headers=headers.to_wsgi_list())

    @http.route('/bank/balances', auth='public')
    def bank_balances(self):
        """
        Used to retrieve top-level summary view (just the balances of public journals).
        """
        try:
            # For each of the public journals, fetch the ending balance from the
            # latest statement
            total_balance = 0.0
            balances = []
            domain = [
                ('public_can_view', '=', True),
            ]
            journals = http.request.env['account.journal'].sudo().search(domain)
            for journal in journals:
                domain = [
                    ('journal_id', '=', journal.id),
                ]
                orderby = "date desc, id desc"
                bank_statement = http.request.env['account.bank.statement'].sudo().search(domain, order=orderby, limit=1).read([
                    'id',
                    'name',
                    'balance_end'
                ])
                if len(bank_statement) < 1:
                    continue
                statement = bank_statement[0]
                total_balance += statement['balance_end']
                balances.append({
                    "id": statement['id'],
                    "name": statement['name'],
                    "balance_end": statement['balance_end'],
                    "journal_id": journal.id,
                    "journal_name": journal.name,
                    "public_slug": journal.public_slug,
                })

            # Return JSON response with list of bank statements
            data = {
                "status": "ok",
                "total_balance": total_balance,
                "balances": balances,
            }
            return self._make_json_response(data, headers=None, cookies=None, status=200)
        # Catch all exceptions and log a meaningful error message
        except Exception as e:
            import logging
            logging.error(f"Error accessing bank balances: {str(e)}", exc_info=True)
            data = {
                "status": "error",
                "error": f"An unexpected error occurred: {str(e)}"
            }
            return self._make_json_response(data, headers=None, cookies=None, status=500)

    @http.route('/bank/statements', auth='public')
    def bank_statements(self):
        """
        Used to retrieve top-level summary view (just the balances of public journals).
        """
        try:
            # Fetch list of bank statements
            domain = [
                ('journal_id.public_can_view', '=', True)
            ]
            bank_statements = http.request.env['account.bank.statement'].sudo().search(domain)

            # Return JSON response with list of bank statements
            data = {
                "status": "ok",
                "bank_statements": bank_statements.read(["id", "name", "date", "balance_end"]),
            }
            return self._make_json_response(data, headers=None, cookies=None, status=200)
        # Catch all exceptions and log a meaningful error message
        except Exception as e:
            import logging
            logging.error(f"Error accessing bank statements: {str(e)}", exc_info=True)
            data = {
                "status": "error",
                "error": f"An unexpected error occurred: {str(e)}"
            }
            return self._make_json_response(data, headers=None, cookies=None, status=500)

    @http.route('/bank/statements/<public_slug>', auth='public')
    def bank_statement_by_id(self, public_slug):
        try:
            # Fetch single bank statement with name as 'yyyy-mm'
            domain = [
                ('journal_id.public_can_view', '=', True)
                ('journal_id.public_slug', '=', public_slug)
            ]  
            bank_statements = http.request.env['account.bank.statement'].sudo().search(domain, limit=1)
            if not bank_statements:
                data = {
                    "status": "not found",
                    "error": f"No bank statement found with id {id}"
                }
                return self._make_json_response(data, headers=None, cookies=None, status=404)
            bank_statement = bank_statements[0]

            # Gather statement lines
            domain = [
                ('statement_id', '=', bank_statement.id)
            ]
            raw_lines = http.request.env['account.bank.statement.line'].sudo().search(domain)
            lines = [
                {
                    "date": line.date,
                    "payment_ref": line.payment_ref,
                    "amount": line.amount
                } for line in raw_lines
            ]

            # Identify attachments for this statement
            base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            domain = [
                ('res_model', '=', 'account.bank.statement'),
                ('res_id', '=', bank_statement.id),
                ('mimetype', '=', 'image/jpeg')
            ]
            raw_attachments = http.request.env['ir.attachment'].sudo().search(domain)
            attachments = [
                {
                    'id': att['id'],
                    'description': att['description'],
                    'url': f"{base_url}/bank/statements/image/{att['id']}",
                } for att in raw_attachments
            ]

            # Present details of bank statement, including lines and a list of attachments
            data = {
                "status": "ok",
                "header": {
                    "id": bank_statement.id,
                    "name": bank_statement.name,
                    "date": bank_statement.date,
                    "balance_start": bank_statement.balance_start,
                    "balance_end": bank_statement.balance_end
                },
                "lines": lines,
                "attachments": attachments
            }
            return self._make_json_response(data, headers=None, cookies=None, status=200)
        # Catch all exceptions and log a meaningful error message
        except Exception as e:
            import logging
            logging.error(f"Error accessing bank statement: {str(e)}", exc_info=True)
            data = {
                "status": "error",
                "error": f"An unexpected error occurred: {str(e)}"
            }
            return self._make_json_response(data, headers=None, cookies=None, status=500)

    @http.route('/bank/statements/image/<int:att_id>', auth='public')
    def bank_statement_image_by_id(self, att_id):
        try:
            attachment = http.request.env['ir.attachment'].sudo().browse(att_id)
            if attachment.res_model != 'account.bank.statement':
                data = {
                    "status": "not found",
                    "error": f"No bank statement image found with id {att_id}"
                }
                return self._make_json_response(data, headers=None, cookies=None, status=404)
                data = {
                    "status": "not found",
                    "error": f"No bank statement attachment found with id {att_id}"
                }
                return self._make_json_response(data, headers=None, cookies=None, status=404)
            if attachment.mimetype != 'image/jpeg':
                data = {
                    "status": "not found",
                    "error": f"No image attachment found with id {att_id}"
                }
                return self._make_json_response(data, headers=None, cookies=None, status=404)
            statement = http.request.env['account.bank.statement'].sudo().browse(attachment.res_id).read([
                'id',
                'journal_id',
            ])
            journal = http.request.env['account.journal'].sudo().browse(statement.journal_id).read([
                'public_can_view'
            ])
            if len(journal) < 1:
                data = {
                    "status": "not found",
                    "error": f"No bank journal attachment found with id {att_id}"
                }
                return self._make_json_response(data, headers=None, cookies=None, status=404)
            if journal[0]['public_can_view'] == False:
                data = {
                    "status": "not found",
                    "error": f"Attachment does not belong to a bank statement for a public journal {att_id}"
                }
                return self._make_json_response(data, headers=None, cookies=None, status=404)
    
            rawdata = base64.b64decode(attachment.datas)
            headers = werkzeug.datastructures.Headers({
                'Content-Length': len(rawdata),
                'Content-Type': 'image/jpeg'
            })
            return http.Response(rawdata, headers=headers, status=200)

        # Catch all exceptions and log a meaningful error message
        except Exception as e:
            import logging
            logging.error(f"Error accessing bank statement image: {str(e)}", exc_info=True)
            data = {
                "status": "error",
                "error": f"An unexpected error occurred: {str(e)}"
            }
            return self._make_json_response(data, headers=None, cookies=None, status=500)
