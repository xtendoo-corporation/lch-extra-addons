# -- coding: utf-8 --


from odoo import api, models, fields
from odoo.exceptions import ValidationError
import logging


class AccountMoveLine(models.Model):
    # 13.0: account.invoice.line se funde en account.move.line
    _inherit = ["account.move.line", "administrator.mixin.rule"]
    _name = 'account.move.line'
