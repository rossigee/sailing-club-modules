# -*- coding: utf-8 -*-
from odoo import models, fields

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'
    
    public_display = fields.Boolean(
        string='Public Display',
        default=False,
        help='Check this box to allow this attachment to be displayed on the public website.'
    )