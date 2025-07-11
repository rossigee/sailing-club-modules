from odoo import api, fields, models
from datetime import datetime, timedelta
from markupsafe import Markup


class DigestBKSC(models.Model):
    _name = 'digest.bksc'
    _description = 'BKSC Digest Content Provider'

    @api.model
    def get_bank_statement_summary(self, digest):
        """Generate bank statement summary for digest"""
        start, end, company = digest._get_kpi_compute_parameters()
        
        statements = self.env['account.bank.statement'].search([
            ('date', '>=', start),
            ('date', '<', end),
            ('company_id', '=', company.id)
        ], order='date desc', limit=5)
        
        if not statements:
            return False
            
        html = """
        <div style="margin: 16px 0;">
            <h3 style="color: #875A7B; font-weight: 600;">Recent Bank Statements</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background-color: #f8f9fa;">
                        <th style="padding: 8px; text-align: left;">Date</th>
                        <th style="padding: 8px; text-align: left;">Journal</th>
                        <th style="padding: 8px; text-align: right;">Balance</th>
                        <th style="padding: 8px; text-align: right;">Transactions</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for statement in statements:
            html += f"""
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid #dee2e6;">{statement.date}</td>
                        <td style="padding: 8px; border-bottom: 1px solid #dee2e6;">{statement.journal_id.name}</td>
                        <td style="padding: 8px; text-align: right; border-bottom: 1px solid #dee2e6;">
                            {statement.balance_end_real:,.2f} {statement.currency_id.symbol}
                        </td>
                        <td style="padding: 8px; text-align: right; border-bottom: 1px solid #dee2e6;">
                            {len(statement.line_ids)}
                        </td>
                    </tr>
            """
            
        html += """
                </tbody>
            </table>
        </div>
        """
        
        return Markup(html)

    @api.model
    def get_recent_transactions(self, digest):
        """Generate recent transactions summary for digest"""
        start, end, company = digest._get_kpi_compute_parameters()
        
        transactions = self.env['account.bank.statement.line'].search([
            ('date', '>=', start),
            ('date', '<', end),
            ('company_id', '=', company.id),
            ('amount', '!=', 0)
        ], order='date desc, id desc', limit=10)
        
        if not transactions:
            return False
            
        html = """
        <div style="margin: 16px 0;">
            <h3 style="color: #875A7B; font-weight: 600;">Recent Transactions</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background-color: #f8f9fa;">
                        <th style="padding: 8px; text-align: left;">Date</th>
                        <th style="padding: 8px; text-align: left;">Description</th>
                        <th style="padding: 8px; text-align: right;">Amount</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for transaction in transactions:
            amount_style = "color: #28a745;" if transaction.amount > 0 else "color: #dc3545;"
            html += f"""
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid #dee2e6;">{transaction.date}</td>
                        <td style="padding: 8px; border-bottom: 1px solid #dee2e6;">{transaction.payment_ref or transaction.name or 'N/A'}</td>
                        <td style="padding: 8px; text-align: right; border-bottom: 1px solid #dee2e6; {amount_style}">
                            {transaction.amount:,.2f} {transaction.currency_id.symbol}
                        </td>
                    </tr>
            """
            
        html += """
                </tbody>
            </table>
        </div>
        """
        
        return Markup(html)

    @api.model
    def get_account_summary(self, digest):
        """Generate account balance summary for digest"""
        company = digest.company_id
        
        # Get cash accounts
        cash_accounts = self.env['account.account'].search([
            ('account_type', '=', 'asset_cash'),
            ('company_id', '=', company.id)
        ])
        
        # Get bank accounts
        bank_accounts = self.env['account.account'].search([
            ('account_type', '=', 'asset_bank'),
            ('company_id', '=', company.id)
        ])
        
        if not cash_accounts and not bank_accounts:
            return False
            
        html = """
        <div style="margin: 16px 0;">
            <h3 style="color: #875A7B; font-weight: 600;">Account Balances</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background-color: #f8f9fa;">
                        <th style="padding: 8px; text-align: left;">Account</th>
                        <th style="padding: 8px; text-align: left;">Type</th>
                        <th style="padding: 8px; text-align: right;">Balance</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        total_balance = 0.0
        currency = company.currency_id
        
        for account in cash_accounts:
            balance = account.current_balance
            total_balance += balance
            html += f"""
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid #dee2e6;">{account.name}</td>
                        <td style="padding: 8px; border-bottom: 1px solid #dee2e6;">Cash</td>
                        <td style="padding: 8px; text-align: right; border-bottom: 1px solid #dee2e6;">
                            {balance:,.2f} {currency.symbol}
                        </td>
                    </tr>
            """
            
        for account in bank_accounts:
            balance = account.current_balance
            total_balance += balance
            html += f"""
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid #dee2e6;">{account.name}</td>
                        <td style="padding: 8px; border-bottom: 1px solid #dee2e6;">Bank</td>
                        <td style="padding: 8px; text-align: right; border-bottom: 1px solid #dee2e6;">
                            {balance:,.2f} {currency.symbol}
                        </td>
                    </tr>
            """
            
        html += f"""
                    <tr style="font-weight: bold; background-color: #f8f9fa;">
                        <td style="padding: 8px;" colspan="2">Total</td>
                        <td style="padding: 8px; text-align: right;">
                            {total_balance:,.2f} {currency.symbol}
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        """
        
        return Markup(html)