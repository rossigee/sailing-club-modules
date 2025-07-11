# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.misc import slugify

class MaintenanceEquipmentCategory(models.Model):
    _inherit = 'maintenance.equipment.category'
    
    public_display = fields.Boolean(
        string='Public Display',
        default=False,
        help='Check this box to display this equipment category on the public website.'
    )
    
    public_slug = fields.Char(
        string='Public Slug',
        help='URL-friendly identifier for this category. Auto-generated from name if empty.',
        index=True
    )
    
    public_description = fields.Text(
        string='Public Description',
        help='Description to display on the public website for this equipment category.'
    )
    
    # Multilingual fields for public display
    public_description_en = fields.Text(
        string='Public Description (English)',
        help='English description to display on the public website.'
    )
    
    public_description_th = fields.Text(
        string='Public Description (Thai)',
        help='Thai description to display on the public website.'
    )
    
    display_name_en = fields.Char(
        string='Display Name (English)',
        help='English name to display on the public website. If empty, uses the main name.'
    )
    
    display_name_th = fields.Char(
        string='Display Name (Thai)', 
        help='Thai name to display on the public website. If empty, uses the main name.'
    )
    
    display_order = fields.Integer(
        string='Display Order',
        default=10,
        help='Order in which this category appears on the public website (lower numbers first).'
    )
    
    image = fields.Binary(
        string='Category Image',
        help='Image to display for this equipment category on the public website.'
    )
    
    equipment_count = fields.Integer(
        string='Public Equipment Count',
        compute='_compute_equipment_count',
        help='Number of publicly visible equipment items in this category.'
    )
    
    @api.depends('equipment_ids.public_display')
    def _compute_equipment_count(self):
        """Compute the number of publicly visible equipment items in this category."""
        for category in self:
            category.equipment_count = len(category.equipment_ids.filtered('public_display'))
    
    @api.model
    def create(self, vals):
        """Auto-generate public_slug from name if not provided."""
        if vals.get('name') and not vals.get('public_slug'):
            vals['public_slug'] = slugify(vals['name'])
        return super().create(vals)
    
    def write(self, vals):
        """Auto-generate public_slug from name if name changes and slug is empty."""
        if vals.get('name'):
            for record in self:
                if not record.public_slug:
                    vals['public_slug'] = slugify(vals['name'])
        return super().write(vals)
    
    @api.constrains('public_slug')
    def _check_unique_public_slug(self):
        """Ensure public slugs are unique among publicly displayed categories."""
        for category in self.filtered('public_display'):
            if category.public_slug:
                duplicate = self.search([
                    ('public_slug', '=', category.public_slug),
                    ('public_display', '=', True),
                    ('id', '!=', category.id)
                ])
                if duplicate:
                    raise ValueError(f"Public slug '{category.public_slug}' already exists for another publicly displayed category.")
    
    def get_localized_name(self, lang='en'):
        """Get the display name in the specified language, falling back to main name."""
        if lang == 'th' and self.display_name_th:
            return self.display_name_th
        elif lang == 'en' and self.display_name_en:
            return self.display_name_en
        else:
            return self.name
    
    def get_localized_description(self, lang='en'):
        """Get the description in the specified language, falling back to main description."""
        if lang == 'th' and self.public_description_th:
            return self.public_description_th
        elif lang == 'en' and self.public_description_en:
            return self.public_description_en
        else:
            return self.public_description or ''