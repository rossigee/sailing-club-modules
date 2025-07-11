from odoo import fields, models


class Digest(models.Model):
    _inherit = 'digest.digest'

    kpi_bksc_bank_statements = fields.Boolean('Bank Statements Summary')
    kpi_bksc_bank_statements_value = fields.Integer(compute='_compute_kpi_bksc_bank_statements_value')
    
    kpi_bksc_recent_transactions = fields.Boolean('Recent Transactions')
    kpi_bksc_recent_transactions_value = fields.Integer(compute='_compute_kpi_bksc_recent_transactions_value')
    
    kpi_bksc_account_balance = fields.Boolean('Account Balance Summary')
    kpi_bksc_account_balance_value = fields.Monetary(compute='_compute_kpi_bksc_account_balance_value')

    def _compute_kpi_bksc_bank_statements_value(self):
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            statements = self.env['account.bank.statement'].search([
                ('date', '>=', start),
                ('date', '<', end),
                ('company_id', '=', company.id)
            ])
            record.kpi_bksc_bank_statements_value = len(statements)

    def _compute_kpi_bksc_recent_transactions_value(self):
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            transactions = self.env['account.bank.statement.line'].search([
                ('date', '>=', start),
                ('date', '<', end),
                ('company_id', '=', company.id)
            ])
            record.kpi_bksc_recent_transactions_value = len(transactions)

    def _compute_kpi_bksc_account_balance_value(self):
        for record in self:
            company = record.company_id
            accounts = self.env['account.account'].search([
                ('account_type', '=', 'asset_cash'),
                ('company_id', '=', company.id)
            ])
            balance = sum(accounts.mapped('current_balance'))
            record.kpi_bksc_account_balance_value = balance

    def compute_kpis_actions(self, company, user):
        res = super().compute_kpis_actions(company, user)
        res['kpi_bksc_bank_statements'] = 'account.action_bank_statement_tree'
        res['kpi_bksc_recent_transactions'] = 'account.action_bank_statement_line'
        res['kpi_bksc_account_balance'] = 'account.action_account_form'
        return res