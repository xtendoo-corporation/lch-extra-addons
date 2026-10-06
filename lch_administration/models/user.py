# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Users(models.Model):
    _inherit = "res.users"

    administration = fields.Boolean(
        string='Administración',
        default="False"
        )
