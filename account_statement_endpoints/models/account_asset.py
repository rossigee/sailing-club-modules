# -*- coding: utf-8 -*-
from odoo import models, fields

class AccountAsset(models.Model):
    _inherit = 'account.asset'
    
    equipment_id = fields.Many2one(
        'maintenance.equipment',
        string='Related Equipment',
        help='Link this asset to a maintenance equipment record for public display.'
    )