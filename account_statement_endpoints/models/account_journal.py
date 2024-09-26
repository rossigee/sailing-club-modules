# Copyright 2024 Ross Golder (https://golder.org)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, api, fields

class AccountJournalInherit(models.Model):
    """
    Adds 'public' field to specify which journals can be queried publicly (i.e. public clubs, charities, funds).
    """
    _inherit = 'account.journal'

    public_can_view = fields.Boolean(string="Publicly viewable")
    public_slug = fields.Char(string="ID/slug for this journal")
