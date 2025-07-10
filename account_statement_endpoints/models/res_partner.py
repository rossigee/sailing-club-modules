# -*- coding: utf-8 -*-
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    is_team_member = fields.Boolean(
        string='Is Team Member',
        default=False,
        help='Check this box to mark this contact as a team member who should appear in public team listings.'
    )