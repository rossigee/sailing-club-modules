# -*- coding: utf-8 -*-
from odoo import models, fields, api

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'
    
    public_display = fields.Boolean(
        string='Public Display',
        default=False,
        help='Check this box to display this equipment on the public website.'
    )
    
    condition = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor')
    ], string='Condition', default='good',
       help='Current condition of the equipment for public display.')
    
    availability = fields.Selection([
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired')
    ], string='Availability', default='available',
       help='Current availability status for public display.')
    
    rental_rate = fields.Float(
        string='Daily Rental Rate',
        help='Daily rental rate in local currency for public display.',
        digits=(10, 2)
    )
    
    year = fields.Integer(
        string='Year of Manufacture',
        help='Year the equipment was manufactured.'
    )
    
    manufacturer = fields.Char(
        string='Manufacturer',
        help='Equipment manufacturer name.'
    )
    
    model_name = fields.Char(
        string='Model',
        help='Equipment model designation.'
    )
    
    specifications = fields.Text(
        string='Technical Specifications',
        help='Technical specifications in JSON format or structured text for public display.'
    )
    
    public_description = fields.Text(
        string='Public Description',
        help='Description to display on the public website for this equipment.'
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
    
    specifications_en = fields.Text(
        string='Technical Specifications (English)',
        help='English technical specifications for public display.'
    )
    
    specifications_th = fields.Text(
        string='Technical Specifications (Thai)',
        help='Thai technical specifications for public display.'
    )
    
    # Asset integration fields
    asset_ids = fields.One2many(
        'account.asset',
        'equipment_id',
        string='Related Assets',
        help='Financial assets related to this equipment.'
    )
    
    purchase_value = fields.Float(
        string='Purchase Value',
        compute='_compute_asset_values',
        help='Original purchase value from related assets.'
    )
    
    current_value = fields.Float(
        string='Current Book Value',
        compute='_compute_asset_values',
        help='Current book value after depreciation from related assets.'
    )
    
    # Image attachments for public display
    public_image_ids = fields.One2many(
        'ir.attachment',
        'res_id',
        domain=[('res_model', '=', 'maintenance.equipment'), ('public_display', '=', True)],
        string='Public Images',
        help='Images to display on the public website.'
    )
    
    @api.depends('asset_ids.original_value', 'asset_ids.value_residual')
    def _compute_asset_values(self):
        """Compute purchase and current values from related assets."""
        for equipment in self:
            if equipment.asset_ids:
                equipment.purchase_value = sum(equipment.asset_ids.mapped('original_value'))
                equipment.current_value = sum(equipment.asset_ids.mapped('value_residual'))
            else:
                equipment.purchase_value = 0.0
                equipment.current_value = 0.0
    
    def get_public_images(self):
        """Get list of public image URLs for API responses."""
        public_images = []
        
        # Add main equipment image if exists
        if self.image_1920:
            public_images.append(f"/web/image/maintenance.equipment/{self.id}/image_1920")
        
        # Add additional public attachments
        for attachment in self.public_image_ids:
            public_images.append(f"/web/image/ir.attachment/{attachment.id}/datas")
        
        return public_images
    
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
    
    def get_localized_specifications(self, lang='en'):
        """Get the specifications in the specified language, falling back to main specifications."""
        specs_text = ''
        if lang == 'th' and self.specifications_th:
            specs_text = self.specifications_th
        elif lang == 'en' and self.specifications_en:
            specs_text = self.specifications_en
        else:
            specs_text = self.specifications or ''
        
        return self._parse_specifications(specs_text)
    
    def get_specifications_dict(self, lang='en'):
        """Parse specifications text into a dictionary for API responses."""
        return self.get_localized_specifications(lang)
    
    def _parse_specifications(self, specs_text):
        """Parse specifications text into a dictionary."""
        if not specs_text:
            return {}
        
        try:
            import json
            # Try to parse as JSON first
            return json.loads(specs_text)
        except (json.JSONDecodeError, ValueError):
            # If not JSON, treat as key-value pairs separated by newlines
            specs = {}
            for line in specs_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    specs[key.strip()] = value.strip()
            return specs