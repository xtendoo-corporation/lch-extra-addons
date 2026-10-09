
from odoo import _, models, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

    def action_back_to_draft(self):
        if self.filtered(lambda m: m.state == 'done'):
            self.write({'state': 'draft'})
            self.write({'quantity': 0, 'picked': False})  # 17.0: quantity_done -> quantity + picked
        self._action_confirm()
        self._action_assign()




class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_back_to_draft(self):
        moves = self.mapped('move_ids')
        moves.action_back_to_draft()


