# See LICENSE file for full copyright and licensing details.

{
    'name': 'Xtendoo Web Digital Signature',
    'version': "18.0.1.0.0",
    'author': 'Xtendoo',
    'maintainer': 'Javier Lagares',
    'complexity': 'easy',
    'depends': ['web'],
    "license": "AGPL-3",
    'category': 'Tools',
    'description': '''
     This module provides the functionality to store digital signature
     Example can be seen into the User's form view where we have
        added a test field under signature.
    ''',
    'summary': '''
        Touch screen enable so user can add signature with touch devices.
        Digital signature can be very usefull for documents.
    ''',
    'images': ['static/description/Digital_Signature.jpg'],
    'depends': ['sale'],
    'data': [
        'views/users_view.xml',
        'views/sale_view.xml',
        'views/stock_picking_view.xml',
        'views/account_move_view.xml'],
    'website': 'http://www.serpentcs.com',
    # 17.0: sin JS propio; widget="signature" es nativo (el widget legacy odoo.define ya no existe en 17)
    'installable': True,
    'auto_install': False,
}
