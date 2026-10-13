# Port a 19.0 de OCA/account-payment 12.0 (Eficent) para LCH: mismo comportamiento que la v12 de origen.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Account Payment Show Invoice",
    "summary": "Extends the tree view of payments to show the paid invoices "
               "related to the payments using the vendor reference by default",
    "version": "19.0.1.0.0",
    "category": "Accounting/Payment",
    "author": "Eficent, Xtendoo, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/account-payment",
    "license": "AGPL-3",
    "depends": ["account"],
    "data": ["views/account_payment_view.xml"],
    "installable": True,
}
