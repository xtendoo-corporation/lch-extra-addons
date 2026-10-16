from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    # Claves de los elementos extra del menu Imprimir de facturas que se ocultan:
    # 'Export XML' (account_edi_ubl_cii) y 'Factura-e XML' (l10n_es_edi_facturae, si se instala)
    _LCH_HIDDEN_EXTRA_PRINT_KEYS = ("download_ubl", "download_xml_facturae")

    def get_extra_print_items(self):
        items = super().get_extra_print_items()
        return [i for i in items if i.get("key") not in self._LCH_HIDDEN_EXTRA_PRINT_KEYS]
