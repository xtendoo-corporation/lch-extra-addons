# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Port a 19.0 de OCA/account-invoicing 12.0 para LCH.
{
    "name": "Purchase Batch Invoicing",
    "summary": "Make invoices for all ready purchase orders",
    "version": "19.0.1.0.0",
    "category": "Inventory/Purchase",
    "website": "https://www.github.com/OCA/account-invoicing",
    "author": "Tecnativa, Xtendoo, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["purchase"],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_cron_data.xml",
        "wizards/purchase_batch_invoicing_view.xml",
        "views/purchase_order_view.xml",
    ],
    "installable": True,
}
