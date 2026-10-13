# Copyright 2017 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    invoice_vendor_references = fields.Char(
        string="Ref Invoices",
        compute="_compute_invoice_vendor_references",
    )

    def _compute_invoice_vendor_references(self):
        # v12: sorted(reference or number) de las facturas del pago.
        # v19: ref (referencia del proveedor) o name (numero).
        for payment in self:
            invoices = (
                payment.invoice_ids
                | payment.reconciled_invoice_ids
                | payment.reconciled_bill_ids
            )
            refs = sorted(invoice.ref or invoice.name or "" for invoice in invoices)
            payment.invoice_vendor_references = ", ".join(refs)
