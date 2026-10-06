# 13.0: NO SE PORTA. Sobrescribia _compute_price de account.invoice.line (desaparece en 13); el calculo con 3 descuentos
# lo cubre account_invoice_triple_discount de OCA 13.0 sobre account.move.line. El modulo no tenia campos propios (sin datos).
# Copyright 2019 Manuel Calero Solis (http://www.xtendoo.es)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Account Invoice Triple Discount Fix',
    'version': "13.0.1.0.0",
    'category': 'Accounting & Finance',
    'author': 'Manuel Calero Solís',
    'license': 'AGPL-3',
    'summary': 'Manage triple discount on invoice lines',
    'depends': [
        'account_invoice_triple_discount',
    ],
    'installable': False,
}
