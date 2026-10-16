from odoo import api, models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    # Informes que Odoo 19 enlaza al menu Imprimir y que en la v12 de Casa del Hostelero no estaban
    # (v12 solo tenia: factura con pagos, factura bluetooth, 2 descuentos, asiento, recibo de pago,
    # pedido, pro-forma, albaran, preparacion y bluetooth). Se quita el enlace; el informe sigue existiendo.
    _LCH_HIDDEN_PRINT_ACTIONS = [
        "account.account_invoices_without_payment",
        "account.action_account_original_vendor_bill",
        "sale_pdf_quote_builder.action_report_saleorder_raw",
        "stock.action_report_picking_packages",
        "stock.return_label_report",
    ]

    @api.model
    def _lch_hide_print_actions(self):
        for xmlid in self._LCH_HIDDEN_PRINT_ACTIONS:
            report = self.env.ref(xmlid, raise_if_not_found=False)
            if report and report.binding_model_id:
                report.binding_model_id = False
