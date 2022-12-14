# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
class ResPartner(models.Model):
    _inherit = "res.partner"

    commercial_name = fields.Char(string='Commercial Name')

    admin_comment = fields.Text(string='Administrator Notes')
