from odoo import api, exceptions, fields, models, _

class AccountInvoiceTax(models.Model):
    _inherit = "account.invoice.tax"


    real_amount_total = fields.Monetary(string="Real Amount Total")

    @api.depends('amount', 'amount_rounding', 'real_amount_total')
    def _compute_amount_total(self):
        for tax_line in self:
            if tax_line.real_amount_total:
                tax_line.amount_total = tax_line.real_amount_total
            else:
                tax_line.amount_total = tax_line.amount + tax_line.amount_rounding
