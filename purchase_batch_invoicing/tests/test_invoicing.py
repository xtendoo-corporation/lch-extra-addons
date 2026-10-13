# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests import Form, tagged
from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestPurchaseBatchInvoicing(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner2 = cls.env["res.partner"].create({"name": "Proveedor 2"})
        cls.product_a.purchase_method = "purchase"
        cls.orders = cls.env["purchase.order"]
        for partner, qty in (
            (cls.partner_a, 3),
            (cls.partner_a, 5),
            (cls.partner2, 7),
        ):
            po = cls.env["purchase.order"].create(
                {
                    "partner_id": partner.id,
                    "order_line": [
                        (0, 0, {"product_id": cls.product_a.id, "product_qty": qty, "price_unit": 10.0}),
                        (0, 0, {"product_id": cls.product_b.id, "product_qty": 0, "price_unit": 10.0}),
                    ],
                }
            )
            po.button_confirm()
            cls.orders |= po

    def _wizard(self, grouping, exclude=False):
        return self.env["purchase.batch_invoicing"].create(
            {
                "purchase_order_ids": [(6, 0, self.orders.ids)],
                "grouping": grouping,
                "exclude_zero_qty": exclude,
            }
        )

    def _run(self, wizard):
        return self.env["account.move"].search(wizard.action_batch_invoice()["domain"])

    def test_group_by_order(self):
        invoices = self._run(self._wizard("id"))
        self.assertEqual(len(invoices), 3)
        self.assertEqual(set(invoices.mapped("move_type")), {"in_invoice"})

    def test_group_by_vendor(self):
        invoices = self._run(self._wizard("partner_id"))
        self.assertEqual(len(invoices), 2)
        inv_a = invoices.filtered(lambda i: i.partner_id == self.partner_a)
        self.assertEqual(inv_a.amount_untaxed, (3 + 5) * 10.0)
        self.assertEqual(len(inv_a.invoice_line_ids.filtered("product_id")), 4)

    def test_exclude_zero_qty(self):
        invoices = self._run(self._wizard("partner_id", exclude=True))
        for inv in invoices:
            self.assertNotIn(self.product_b, inv.invoice_line_ids.product_id)

    def test_nothing_pending(self):
        self._run(self._wizard("id"))
        wizard = self.env["purchase.batch_invoicing"].create(
            {"purchase_order_ids": [(6, 0, self.orders.ids)], "grouping": "id"}
        )
        with self.assertRaises(UserError):
            wizard.action_batch_invoice()
