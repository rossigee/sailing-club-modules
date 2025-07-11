from odoo import models, api
import logging

_logger = logging.getLogger(__name__)


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    @api.model
    def _setup_demo_public_access(self):
        """Configure demo bank journals for public access"""
        try:
            # Find bank and cash journals
            bank_journals = self.search([('type', 'in', ['bank', 'cash'])], limit=3)
            
            for i, journal in enumerate(bank_journals):
                slug = ['BANK', 'SAVINGS', 'CASH'][i] if i < 3 else f'ACCOUNT-{i+1}'
                journal.write({
                    'public_can_view': True,
                    'public_slug': slug
                })
                _logger.info(f"Configured journal {journal.name} for public access with slug {slug}")
                
        except Exception as e:
            _logger.warning(f"Failed to setup demo bank journals: {e}")


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _setup_demo_team_members(self):
        """Configure demo team members"""
        try:
            # Find contacts (not companies) with emails
            contacts = self.search([
                ('is_company', '=', False),
                ('email', '!=', False),
                ('email', '!=', '')
            ], limit=5)
            
            for contact in contacts:
                contact.write({'is_team_member': True})
                _logger.info(f"Configured {contact.name} as team member")
                
        except Exception as e:
            _logger.warning(f"Failed to setup demo team members: {e}")


class MaintenanceEquipmentCategory(models.Model):
    _inherit = 'maintenance.equipment.category'

    @api.model
    def _setup_demo_equipment_categories(self):
        """Configure demo equipment categories for public display"""
        try:
            categories = self.search([], limit=3)
            
            for i, category in enumerate(categories):
                slug = category.name.lower().replace(' ', '-').replace('&', 'and')
                category.write({
                    'public_display': True,
                    'public_slug': slug,
                    'display_order': (i + 1) * 10
                })
                _logger.info(f"Configured category {category.name} for public display with slug {slug}")
                
        except Exception as e:
            _logger.warning(f"Failed to setup demo equipment categories: {e}")


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    @api.model
    def _setup_demo_equipment(self):
        """Configure demo equipment for public display"""
        try:
            # Find equipment in public categories
            public_categories = self.env['maintenance.equipment.category'].search([
                ('public_display', '=', True)
            ])
            
            if public_categories:
                equipment = self.search([
                    ('category_id', 'in', public_categories.ids)
                ], limit=10)
                
                for item in equipment:
                    item.write({'public_display': True})
                    _logger.info(f"Configured equipment {item.name} for public display")
                    
        except Exception as e:
            _logger.warning(f"Failed to setup demo equipment: {e}")


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    @api.model
    def _setup_demo_calendar_events(self):
        """Configure demo calendar events for public display"""
        try:
            # Find recent/upcoming events
            events = self.search([
                ('start', '>=', '2024-01-01'),
                ('start', '<=', '2025-12-31')
            ], limit=10)
            
            for event in events:
                event.write({'class': 'public'})
                _logger.info(f"Configured event {event.name} for public display")
                
        except Exception as e:
            _logger.warning(f"Failed to setup demo calendar events: {e}")