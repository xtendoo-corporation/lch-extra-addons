# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    delivery_zone_ids = fields.One2many(
        string='Delivery Zones',
        comodel_name='delivery.zone.partner.line',
        inverse_name='partner_id',
    )

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        """Escribe un contexto en el campo "child_ids" respetando otros contextos del campo
        (17.0: fields_view_get desaparece, se usa _get_view; arch es un elemento lxml)."""
        arch, view = super()._get_view(view_id, view_type, **options)
        if view_type == 'form':
            for partner_field in arch.xpath("//field[@name='child_ids']"):
                context = partner_field.attrib.get("context", "{}").replace(
                    "{", "{'default_delivery_zone_ids': delivery_zone_ids, ", 1,
                )
                partner_field.attrib['context'] = context
        return arch, view
