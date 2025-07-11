{
    'name': 'BKSC Digest Extensions',
    'version': '16.0.1.0.0',
    'category': 'Mail',
    'summary': 'Bangkok Sailing Club digest email sections',
    'description': """
        BKSC Digest Extensions
        ======================
        
        This module extends Odoo's digest functionality to include
        Bangkok Sailing Club specific content:
        
        * Bank statement summaries
        * Member activity reports
        * Upcoming events
        * Financial KPIs
        * Recent transactions
    """,
    'author': 'Bangkok Sailing Club',
    'website': 'https://www.bangkoksailingclub.com',
    'depends': [
        'digest',
        'account_statement_endpoints',
        'account',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/digest_data.xml',
        'views/digest_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}