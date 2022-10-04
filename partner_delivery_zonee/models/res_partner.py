# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from lxml import etree


class ResPartner(models.Model):
    _inherit = 'res.partner'

    delivery_zone_ids = fields.One2many(
        string='Delivery Zones',
        comodel_name='delivery.zone.partner.line',
        inverse_name='partner_id',
    )

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        """The purpose of this is to write a context on "child_ids" field
         respecting other contexts on this field.
         There is a PR (https://github.com/odoo/odoo/pull/26607) to odoo for
         avoiding this. If merged, remove this method and add the attribute
         in the field.
         """
        res = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu,
        )
        if view_type == 'form':
            partner_xml = etree.XML(res['arch'])
            partner_fields = partner_xml.xpath("//field[@name='child_ids']")
            if partner_fields:
                partner_field = partner_fields[0]
                context = partner_field.attrib.get("context", "{}").replace(
                    "{", "{'default_delivery_zone_ids': delivery_zone_ids, ", 1,
                )
                partner_field.attrib['context'] = context
                res['arch'] = etree.tostring(partner_xml)
        return res
