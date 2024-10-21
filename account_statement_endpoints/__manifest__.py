# Copyright 2024 Ross Golder (https://golder.org)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Bank Statements Endpoint',
    'version': '14.0.1.0.4',
    'author': 'Ross Golder',
    'website': 'https://golder.org/',
    'license': 'AGPL-3',
    'category': 'Accounting',
    'summary': 'Provides REST-like endpoints to expose details about the bank account statements.',
    'description': """
        This module allows us to present up-to-date details from our (publicly funded) club's bank book on the club's (static) public website. As up-to-date as can be expected given we have to manually drive to 'the bank' to update the bank book, and then drive home and manually input the new lines into Odoo. F**k banks with no APIs (and poor secops)."
    """,    
    'depends': [
        'account',
    ],
    'data': [
        'views/account_journal_public_checkbox.xml',
        'views/statement_buttons.xml',
    ],
    'installable': True,
}
