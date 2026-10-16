
{
    'name': 'document_format_ch',
    'summary': """Formatos de documentos CH""",
    'version': "19.0.1.0.0",
    'description': """Formatos de documentos CH""",
    'author': 'Dani-Xtendoo',
    'company': 'Xtendoo',
    'website': 'http://www.xtendoo.com',
    'category': 'Extra Tools',
    'depends': [
        'base',
        'account',
        'account_edi_ubl_cii',
        'sale',
        'web',
        'stock',
        'purchase'
    ],
    'license': 'AGPL-3',
    'data': [
        #layout
        'views/layout/external_layout_clean.xml',
        #purchase / albarán de preparación (core con el estilo de v12)
        'views/purchase/report_purchase_core.xml',
        #sale
        'views/sale/report_saleorder_document.xml',
        'views/sale/report_saleorder_bluetooth.xml',
        #delivery
        'views/delivery/report_delivery_document.xml',
        'views/delivery/report_delivery_document_bluetooth.xml',
        #invoice
        'views/invoice/report_invoice_document.xml',
        'views/invoice/report_invoice_document_2_discounts.xml',
        'views/invoice/report_invoice_bluetooth.xml',
        #payment
        'views/payment/report_payment_receipt_bluetooth.xml',
        'views/payment/report_payment_receipt.xml',
        # ocultar del menu Imprimir lo que v12 no tenia
        'data/hide_print_actions.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,

}
