# Copyright  2018 Forest and Biomass Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.http import Controller, request, route
from odoo import api, fields, models, _

import logging


class PartnerDeliveryZoneWizard(models.TransientModel):
    _name = "partner.delivery.zone.wizard"
    _description = "Partner Delivery Zone Wizard"

    def _get_partner_delivery_zone(self):
        # Sin petición HTTP (shell, cron) no hay sesión; en 19 el default debe ser False, no 0
        if not request:
            return False
        return request.session.get('partner_delivery_zone_id') or False

    partner_delivery_zone = fields.Many2one(
        comodel_name='partner.delivery.zone',
        string='Partner Delivery Zone',
        default=_get_partner_delivery_zone,
    )

    def button_set_partner_delivery_zone(self):
        self.ensure_one()
        request.session['partner_delivery_zone_id'] = self.partner_delivery_zone.id

