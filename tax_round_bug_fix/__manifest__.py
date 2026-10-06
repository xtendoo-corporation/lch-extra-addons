# 13.0: NO SE PORTA. Parcheaba account.invoice.tax (desaparece en 13: los impuestos son apuntes de account.move.line).
# Sus 615 valores real_amount_total se conservan en la tabla lch_legacy_invoice_tax (ver scripts/salto_13_pre.sql del proyecto de migracion).

{
    'name': 'Tax round bug fix',
    'summary': """Tax round bug fix""",
    'version': "13.0.1.0.0",
    'description': """Tax round bug fix""",
    'author': 'Dani-Xtendoo',
    'company': 'Xtendoo',
    'website': 'http://www.xtendoo.com',
    'category': 'Extra Tools',
    'depends': [
        'account'
    ],
    'license': 'AGPL-3',
    'data': [
        'views/account_invoice_form.xml'
    ],
    'demo': [],
    'installable': False,
    'auto_install': False,

}
