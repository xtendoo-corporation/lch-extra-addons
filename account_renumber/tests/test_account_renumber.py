# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import exceptions
from odoo.tests import tagged
from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestAccountRenumber(AccountTestInvoicingCommon):
    def _invoice(self, date):
        inv = self.init_invoice("out_invoice", products=[self.product_a], invoice_date=date)
        inv.action_post()
        return inv

    def test_renumber_by_date_without_gaps(self):
        # se crean en orden distinto al de la fecha y con un hueco (se borra uno)
        i3 = self._invoice("2024-03-01")
        i1 = self._invoice("2024-01-01")
        i2 = self._invoice("2024-02-01")
        journal = i1.journal_id
        wizard = self.env["wizard.renumber"].create(
            {
                "date_from": "2024-01-01",
                "date_to": "2024-12-31",
                "journal_ids": [(6, 0, journal.ids)],
                "number_next": 1,
            }
        )
        action = wizard.renumber()
        self.assertEqual(set(action["domain"][0][2]), set((i1 | i2 | i3).ids))
        # misma longitud de numero y numeracion correlativa por fecha
        nums = [m.sequence_number for m in (i1, i2, i3)]
        self.assertEqual(nums, [1, 2, 3])
        self.assertEqual(len({len(m.name) for m in (i1, i2, i3)}), 1)
        self.assertEqual(i1.name[: -len(str(1))], i1.sequence_prefix + "0" * (len(i1.name) - len(i1.sequence_prefix) - 1))

    def test_renumber_start_number_and_empty(self):
        i1 = self._invoice("2024-05-01")
        wizard = self.env["wizard.renumber"].create(
            {"date_from": "2024-05-01", "date_to": "2024-05-31", "journal_ids": [(6, 0, i1.journal_id.ids)], "number_next": 50}
        )
        wizard.renumber()
        self.assertEqual(i1.sequence_number, 50)
        wizard.date_from = wizard.date_to = "2000-01-01"
        with self.assertRaises(exceptions.MissingError):
            wizard.renumber()
