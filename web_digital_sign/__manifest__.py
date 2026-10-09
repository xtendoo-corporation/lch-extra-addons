# See LICENSE file for full copyright and licensing details.

{
    'name': 'Xtendoo Web Digital Signature',
    'version': "15.0.1.0.0",
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
    # 15.0: los bundles se declaran aqui (ya no se hereda web.assets_backend desde XML ni existe la clave 'qweb')
    'assets': {
        'web.assets_backend': ['web_digital_sign/static/src/js/digital_sign.js'],
        'web.assets_qweb': ['web_digital_sign/static/src/xml/digital_sign.xml'],
    },
    'installable': True,
    'auto_install': False,
}
