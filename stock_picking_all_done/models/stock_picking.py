# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class Picking(models.Model):
    _inherit = "stock.picking"

    def action_all_as_done(self):

        #_logger.info("*" * 80)
        #_logger.info("action_all_as_done")

        if not self.move_ids and not self.move_line_ids and not self.move_ids_without_package:
            raise UserError(_('Please add some items to move.'))

        # 17.0: qty_done/reserved_uom_qty/quantity_done desaparecen; la cantidad es `quantity` y se marca `picked`
        if self.move_line_ids:
            for move_line in self.move_line_ids:
                move_line.picked = True

        if self.move_ids_without_package:
            for move in self.move_ids_without_package:
                move.quantity = move.product_uom_qty
                move.picked = True
