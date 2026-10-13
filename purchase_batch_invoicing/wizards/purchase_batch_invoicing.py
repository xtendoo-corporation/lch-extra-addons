# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from logging import getLogger

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare

_logger = getLogger(__name__)


class PurchaseBatchInvoicing(models.TransientModel):
    _name = "purchase.batch_invoicing"
    _description = "Purchase Batch Invoicing"

    purchase_order_ids = fields.Many2many(
        comodel_name="purchase.order",
        string="Purchase orders",
        domain="[('invoice_status', '=', 'to invoice')]",
        required=True,
        readonly=True,
        default=lambda self: self._default_purchase_order_ids(),
    )
    grouping = fields.Selection(
        selection=[("id", "Purchase Order"), ("partner_id", "Vendor")],
        required=True,
        default="id",
        help="Make one invoice for each...",
    )
    exclude_zero_qty = fields.Boolean(help="Do not invoice lines with zero quantity.")

    @api.model
    def _default_purchase_order_ids(self):
        """Get purchase orders from active ids."""
        try:
            return (
                self.env["purchase.order"]
                .search(self._purchase_order_domain(self.env.context["active_ids"]))
                .ids
            )
        except KeyError:
            return False

    @api.model
    def _purchase_order_domain(self, ids=None):
        """Helper to filter current ids by those that are to invoice."""
        domain = [("invoice_status", "=", "to invoice")]
        if ids:
            domain += [("id", "in", ids)]
        pos = self.env["purchase.order"].search(domain)
        # Use only POs with less qty invoiced than the expected
        pos = pos.filtered(
            lambda order: any(
                line.qty_invoiced
                < (
                    line.qty_received
                    if line.product_id.purchase_method == "receive"
                    else line.product_qty
                )
                for line in order.order_line
                if not line.display_type
            )
        )
        if len(domain) > 1:
            domain[1] = ("id", "in", pos.ids)
        return domain

    def _prepare_batch_invoice_vals(self, partner):
        """Allow to override the invoice defaults by a third module.
        i.e.: set invoice type to in_refund"""
        return {"partner_id": partner.id, "move_type": "in_invoice"}

    def grouped_purchase_orders(self):
        """Purchase orders, applying current grouping.

        :return generator:
            Generator of grouped ``purchase.order`` recordsets.

            If :attr:`grouping` is ``id``, the generator will yield recordsets
            with 1 order each; if it is ``partner_id``, the yielded recordsets
            will contain all purchase orders from each vendor.
        """
        PurchaseOrder = self.env["purchase.order"]
        domain = self._purchase_order_domain(self.purchase_order_ids.ids)
        for group in self.mapped("purchase_order_ids.%s" % self.grouping):
            pos = PurchaseOrder.search(domain + [(self.grouping, "=", int(group))])
            if pos:
                yield pos

    def _prepare_group_invoice(self, pogroup):
        """Una factura de proveedor con las lineas de todos los pedidos del grupo.

        Mismo efecto que el `purchase_id = po` + `purchase_order_change()` de v12: cabecera
        del pedido (moneda, plazo de pago, posicion fiscal...) y sus lineas pendientes de
        facturar; con `exclude_zero_qty` se descartan las de cantidad 0.
        """
        partner = pogroup.mapped("partner_id")
        vals = dict(
            pogroup[0]
            .with_company(pogroup[0].company_id)
            .with_context(default_move_type="in_invoice")
            ._prepare_invoice(),
            **self._prepare_batch_invoice_vals(partner),
        )
        vals["invoice_line_ids"] = []
        vals["invoice_origin"] = ", ".join(pogroup.mapped("name"))
        sequence = 10
        precision = self.env["decimal.precision"].precision_get("Product Unit")
        for po in pogroup:
            pending_section = None
            for line in po.order_line:
                if line.display_type in ("line_section", "line_subsection"):
                    pending_section = line
                    continue
                if (
                    self.exclude_zero_qty
                    and not line.display_type
                    and not float_compare(line.qty_to_invoice, 0.0, precision_digits=precision)
                ):
                    continue
                if pending_section:
                    section_vals = pending_section._prepare_account_move_line()
                    section_vals["sequence"] = sequence
                    vals["invoice_line_ids"].append((0, 0, section_vals))
                    sequence += 1
                    pending_section = None
                line_vals = line._prepare_account_move_line()
                line_vals["sequence"] = sequence
                vals["invoice_line_ids"].append((0, 0, line_vals))
                sequence += 1
        return vals

    def action_batch_invoice(self):
        """Generate invoices for all selected purchase orders.

        :return dict: Window action to see the generated invoices.
        """
        invoices = self.env["account.move"]
        Move = self.env["account.move"].with_context(default_move_type="in_invoice")
        for pogroup in self.grouped_purchase_orders():
            invoices |= Move.with_company(pogroup[0].company_id).create(
                self._prepare_group_invoice(pogroup)
            )
        if not invoices:
            raise UserError(_("No ready-to-invoice purchase orders selected."))
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "name": _("Generated Invoices"),
            "views": [[False, "list"], [False, "form"]],
            "domain": [["id", "in", invoices.ids]],
        }

    @api.model
    def cron_invoice_all_pending(self, grouping="partner_id"):
        """Invoice all pending purchase orders."""
        _logger.info("Starting to invoice all pending purchase orders.")
        wizard = self.create(
            {
                "purchase_order_ids": [
                    (6, False, self.env["purchase.order"].search(self._purchase_order_domain()).ids)
                ],
                "grouping": grouping,
            }
        )
        try:
            result = wizard.action_batch_invoice()
            _logger.info("Finished invoicing all pending purchase orders.")
            _logger.debug("Result: %r", result)
        except UserError as error:
            _logger.info(error.args[0])
            _logger.debug("Traceback:", exc_info=True)
