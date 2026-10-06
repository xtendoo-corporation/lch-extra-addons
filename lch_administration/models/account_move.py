# -- coding: utf-8 --


from odoo import api, models, fields
from odoo.exceptions import ValidationError
import logging

INVOICE_TYPES = ('out_invoice', 'out_refund', 'in_invoice', 'in_refund',
                 'out_receipt', 'in_receipt')


class AccountMove(models.Model):
    # 13.0: account.invoice se funde en account.move (los asientos y pagos tambien pasan por aqui)
    _inherit = ["account.move", "administrator.mixin.rule"]
    _name = 'account.move'

    @api.model
    def default_get(self, default_fields):
        """Si el contexto trae el dato 'active_model' y ese model es 'sale_order' eso quiere decir
        que viene de un pedido por tanto lo dejamos pasar.
        Solo se restringe la creacion de FACTURAS: los asientos (pagos, extractos...) no se tocan.
        """
        if (self._context.get('default_type') in INVOICE_TYPES
                and not self.env["res.users"].has_group("lch_administration.administration_group")):
            active_model = ""
            if self._context.get('params'):
                if self._context.get('params').get('model'):
                    active_model = self._context.get('params').get('model')
            if self._context.get('search_default_my_quotation'):
                active_model = "sale.order"
            if self._context.get('active_model'):
                active_model = self._context.get('active_model')
            if active_model != "sale.order":
                raise ValidationError(("No tiene permisos para crear facturas directas"))
        return super(AccountMove, self).default_get(default_fields)

    def button_cancel(self):
        # 12.0: action_invoice_cancel. Solo se restringe cancelar FACTURAS, no los asientos de pagos
        if any(move.type in INVOICE_TYPES for move in self) and not self.env.user.administration:
            raise ValidationError(("No tiene permisos para cancelar facturas"))
        return super(AccountMove, self).button_cancel()
