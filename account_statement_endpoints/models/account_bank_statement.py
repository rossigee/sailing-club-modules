# Copyright 2023 Ross Golder (https://golder.org)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, api

class AccountBankStatement(models.Model):
    """
    Adds action to handle sorting of bank statements and recalculation of ending balance
    """
    _inherit = 'account.bank.statement'

    @api.model
    def _get_previous_statement_id(self):
        domain = [
            ('journal_id', '=', self.journal_id.id),
            ('date', '<', self.date),
        ]
        previous_statement = self.search(domain, order='date desc, id desc', limit=1)
        return previous_statement.id if previous_statement else False

    def action_bank_statement_sort_by_date(self):
        """
        Sorts statement lines by date.
        """

        # Sort tuples by date
        txs = [(line.date, line.id) for line in self.line_ids]
        txs.sort(key=lambda x: x[0])

        i = 1
        for (line_date, line_id) in txs:
            # Update sequence field for each statement line
            self.env['account.bank.statement.line'].browse(line_id).write({'sequence': i})
            i += 1

        return None

    def action_bank_statement_align_balances(self):
        """
        Set starting balance from previous statement and ending balance based on starting balance and transactions.
        """

        self.ensure_one()

        # Find ending balance from previous statement, or zero if none
        new_balance_start = 0.0
        previous_statement_id = self._get_previous_statement_id()
        if previous_statement_id:
            previous_statement = self.browse(previous_statement_id)
            new_balance_start = previous_statement.balance_end_real
        self.balance_start = new_balance_start

        # Set ending balance based on starting balance and transactions
        new_balance_end = self.balance_start
        for line in self.line_ids:
            new_balance_end += line.amount
        self.balance_end_real = new_balance_end

        return None

    @api.model
    def create(self, vals):
        """
        Applies sort when statement lines are saved.
        """

        record = super().create(vals)
        self.action_bank_statement_sort_by_date()
        return record

    @api.model
    def update(self, vals):
        """
        Applies sort when statement lines are saved.
        """

        record = super().update(vals)
        self.action_bank_statement_sort_by_date()
        return record
