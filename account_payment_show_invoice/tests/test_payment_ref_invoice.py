# Copyright 2017 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import tagged
from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestPaymentRefInvoice(AccountTestInvoicingCommon):
    def _bill(self, ref):
        bill = self.init_invoice(
            "in_invoice", products=[self.product_a], invoice_date="2025-01-10"
        )
        bill.ref = ref
        bill.action_post()
        return bill

    def test_payment_ref_invoice(self):
        # 2 facturas de proveedor, 1 pago: referencias ordenadas y separadas por coma
        bill1 = self._bill("REF-B")
        bill2 = self._bill("REF-A")
        wizard = (
            self.env["account.payment.register"]
            .with_context(active_model="account.move", active_ids=(bill1 | bill2).ids)
            .create({"group_payment": True})
        )
        payment = wizard._create_payments()
        self.assertEqual(payment.invoice_vendor_references, "REF-A, REF-B")
        # sin referencia de proveedor se usa el numero
        bill3 = self._bill(False)
        wizard = (
            self.env["account.payment.register"]
            .with_context(active_model="account.move", active_ids=bill3.ids)
            .create({})
        )
        self.assertEqual(wizard._create_payments().invoice_vendor_references, bill3.name)
