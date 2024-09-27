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

    def _get_attachments(self, res_id):
        # Identify attachments for this statement
        domain = [
            ('res_model', '=', 'account.bank.statement'),
            ('res_id', '=', res_id),
            ('mimetype', '=', 'image/jpeg')
        ]
        raw_attachments = http.request.env['ir.attachment'].sudo().search(domain)
        if len(raw_attachments) < 1:
            return []

        # Return the metadata as an array of objects
        base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return [
            {
                'id': att['id'],
                'description': att['description'],
                'url': f"{base_url}/bank/statements/image/{att['id']}",
            } for att in raw_attachments
        ]

    @http.route('/bank/journals', auth='public')
    def bank_journals(self):
        """
        Used to retrieve top-level summary view, which is a list of journals and
        a summary of their last statement's balance. Public slugs are supplied so
        client can link to a view of a particular journal.
        """

        try:
            # For each of the public journals, fetch the ending balance from the
            # latest statement
            total_balance = 0.0
            domain = [
                ('public_can_view', '=', True),
            ]
            journals_data = []
            journals = http.request.env['account.journal'].sudo().search(domain)
            for journal in journals:
                # Find latest statement for this journal
                domain = [
                    ('journal_id', '=', journal.id),
                ]
                orderby = "date desc, id desc"
                bank_statements = http.request.env['account.bank.statement'].sudo().search(domain, order=orderby, limit=1).read([
                    'id',
                    'name',
                    "date",
                    'balance_end'
                ])
                if len(bank_statements) < 1:
                    continue

                # Summarise findings for this journal
                journals_data.append({
                    "id": journal.id,
                    "name": journal.name,
                    "public_slug": journal.public_slug,
                    "latest_statement": bank_statements[0]
                })

                total_balance += bank_statements[0]['balance_end']

            # Return JSON response with list of bank statements
            data = {
                "status": "ok",
                "total_balance": total_balance,
                "journals": journals_data,
            }
            return self._make_json_response(data, headers=None, cookies=None, status=200)

        # Catch all exceptions and log a meaningful error message
        except Exception as e:
            import logging
            logging.error(f"Error accessing bank journals: {str(e)}", exc_info=True)
            data = {
                "status": "error",
                "error": f"An unexpected error occurred: {str(e)}"
            }
            return self._make_json_response(data, headers=None, cookies=None, status=500)

    @http.route('/bank/statements/<book>', auth='public')
    def bank_statements_list_view(self, book):
        try:
            domain = [
                ('journal_id.public_can_view', '=', True),
                ('journal_id.public_slug', '=', book),
            ]
            orderby = "date desc, id desc"
            bank_statements = http.request.env['account.bank.statement'].sudo().search(domain, order=orderby)
            if not bank_statements:
                data = {
                    "status": "not found",
                    "error": f"No bank statements found for journal with public slug '{book}'"
                }
                return self._make_json_response(data, headers=None, cookies=None, status=404)

            bank_statements_data = []
            for bank_statement in bank_statements:
                attachments = self._get_attachments(bank_statement.id)

                bank_statements_data.append({
                    'id': bank_statement.id,
                    'name': bank_statement.name,
                    'date': bank_statement.date,
                    'balance_end': bank_statement.balance_end,
                    'attachments': attachments
                })

            data = {
                "status": "ok",
                "statements": bank_statements_data
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

    @http.route('/bank/statements/<book>/<page>', auth='public')
    def bank_statements_detail_view(self, book, page):
        try:
            domain = [
                ('journal_id.public_can_view', '=', True),
                ('journal_id.public_slug', '=', book),
                ('id', '=', page),
            ]
            orderby = "date desc, id desc"
            bank_statements = http.request.env['account.bank.statement'].sudo().search(domain, order=orderby, limit=1)
            if not bank_statements:
                data = {
                    "status": "not found",
                    "error": f"No bank statements found for journal with public slug '{book}'"
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

            # Attachments
            attachments = self._get_attachments(bank_statement.id)

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
            # Identify requested attachment
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

            # Check it belongs to a public statement
            journal = http.request.env['account.bank.statement'].sudo().browse(attachment.res_id).journal_id
            if not journal.public_can_view:
                data = {
                    "status": "not found",
                    "error": f"Image {att_id} does not belongs to a public journal statement"
                }
                return self._make_json_response(data, headers=None, cookies=None, status=404)

            # Encode it for consumption
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
