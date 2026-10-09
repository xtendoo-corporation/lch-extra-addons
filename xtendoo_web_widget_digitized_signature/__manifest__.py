# Copyright 2004-2010 OpenERP SA (<http://www.openerp.com>)
# Copyright 2011-2015 Serpent Consulting Services Pvt. Ltd.
# Copyright 2017 Tecnativa - Vicent Cubells
# Copyright 2019 Open Source Integrators
# Copyright 2020 Xtendoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Xtendoo Web Widget Digitized Signature',
    'version': "15.0.1.0.0",
    'author': 'Xtendoo, '
              'Serpent Consulting Services Pvt. Ltd., '
              'Agile Business Group, '
              'Tecnativa, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/web',
    'license': 'AGPL-3',
    'category': 'Web',
    'depends': [
        'web',
        'mail',
        'stock',
    ],
    'data': [
        'views/res_users_view.xml',
        'views/stock_picking_view.xml',
    ],
    # 15.0: bundles en el manifest. Como en v12 (donde la ruta del <script> era erronea) solo se carga el qweb; el JS duplica web_digital_sign.
    'assets': {
        'web.assets_qweb': ['xtendoo_web_widget_digitized_signature/static/src/xml/digital_sign.xml'],
    },
    'installable': True,
    'development_status': 'Production/Stable',
    'maintainers': [
        'mgosai',
        'javier lagares',
        'manuel calero'
    ],
}
