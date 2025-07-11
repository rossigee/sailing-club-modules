# Copyright 2024 Ross Golder (https://golder.org)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Bank Statements Endpoint',
    'version': '16.0.1.0.1',
    'author': 'Ross Golder',
    'website': 'https://golder.org/',
    'license': 'AGPL-3',
    'category': 'Accounting',
    'summary': 'Provides REST-like endpoints to expose details about the bank account statements.',
    'description': """
        This module allows us to present up-to-date details from our (publicly funded) club's bank book on the club's (static) public website. As up-to-date as can be expected given we have to manually drive to 'the bank' to update the bank book, and then drive home and manually input the new lines into Odoo.
    """,    
    'depends': [
        'account_statement_base',
        'maintenance',
        'account_asset',
    ],
    'data': [
        'views/account_journal_public_checkbox.xml',
        'views/statement_buttons.xml',
        'views/res_partner.xml',
        'views/maintenance_equipment_category_views.xml',
        'views/maintenance_equipment_views.xml',
        'views/ir_attachment_views.xml',
        'views/account_asset_views.xml',
        'views/public_website_menu.xml',
        'data/demo_data.xml',
    ],
    'installable': True,
}
