# Copyright 2009 Pexego Sistemas Informáticos. All Rights Reserved
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import date

from odoo import _, api, exceptions, fields, models

_logger = logging.getLogger(__name__)

# Los nombres temporales usan el mismo prefijo y un numero que no puede existir, de modo
# que cumplen el formato de la secuencia y la restriccion de unicidad no salta a mitad.
_TEMP_OFFSET = 10 ** 9


class WizardRenumber(models.TransientModel):
    _name = "wizard.renumber"
    _description = "Account renumber wizard"

    date_from = fields.Date(
        string="Starting date",
        required=True,
        default=lambda self: self._default_date_from(),
        help="Start renumbering in this date, inclusive.",
    )
    date_to = fields.Date(
        string="Finish date",
        required=True,
        default=lambda self: self._default_date_to(),
        help="Finish renumbering in this date, inclusive.",
    )
    journal_ids = fields.Many2many(
        comodel_name="account.journal",
        relation="account_journal_wzd_renumber_rel",
        column1="wizard_id",
        column2="journal_id",
        string="Journals",
        required=True,
        help="Journals to renumber",
    )
    number_next = fields.Integer(
        string="First Number",
        default=1,
        required=True,
        help="Journal sequences will start counting on this number",
    )

    @api.model
    def _default_date_from(self):
        """Day 1 of current year by default."""
        return date(self._default_date_to().year, 1, 1)

    @api.model
    def _default_date_to(self):
        """Today by default."""
        return fields.Date.context_today(self)

    def renumber(self):
        """Renumber all the posted moves on the given journal and periods.

        Igual que en v12, los asientos publicados se ordenan por fecha (y id) y se numeran
        sin huecos empezando en `number_next`; la numeracion se reinicia en cada secuencia
        (en 19: cada prefijo de diario/periodo, p. ej. cada anio o las rectificativas).

        :return dict: Window action to open the renumbered moves, to review them.
        """
        self.ensure_one()
        _logger.debug("Searching for account moves to renumber.")
        moves = self.env["account.move"].search(
            [
                ("journal_id", "in", self.journal_ids.ids),
                ("date", ">=", self.date_from),
                ("date", "<=", self.date_to),
                ("state", "=", "posted"),
                ("name", "not in", ("/", False)),
            ],
            order="date, id",
        )
        if not moves:
            raise exceptions.MissingError(_("No records found for your selection!"))
        secured = moves.filtered("inalterable_hash")
        if secured:
            raise exceptions.UserError(
                _(
                    "Some of the entries are protected by an inalterability hash "
                    "and cannot be renumbered: %s",
                    ", ".join(secured[:10].mapped("name")),
                )
            )

        _logger.debug("Renumbering %d account moves.", len(moves))
        # grupos de numeracion: (diario, prefijo) -> asientos en orden de fecha
        groups = {}
        for move in moves:
            groups.setdefault((move.journal_id.id, move.sequence_prefix), []).append(move)

        plan = []
        for (_journal_id, prefix), group in groups.items():
            # ancho del numero tal como lo usa el propio diario/periodo
            width = max(len(move.name) - len(prefix) for move in group)
            for counter, move in enumerate(group, start=self.number_next):
                plan.append((move, "%s%0*d" % (prefix, width, counter)))

        ctx = {"check_move_validity": False, "skip_account_move_synchronization": True}
        Move = self.env["account.move"].with_context(**ctx)
        # fase 1: nombres temporales (evita choques de unicidad entre numeraciones solapadas)
        for move, _new_name in plan:
            temp = "%s%0*d" % (
                move.sequence_prefix,
                len(move.name) - len(move.sequence_prefix) + 10,
                _TEMP_OFFSET + move.id,
            )
            Move.browse(move.id).write({"name": temp})
        # fase 2: nombres definitivos
        for move, new_name in plan:
            Move.browse(move.id).write({"name": new_name})

        _logger.debug("%d account moves renumbered.", len(moves))
        return {
            "type": "ir.actions.act_window",
            "name": _("Renumbered account moves"),
            "res_model": "account.move",
            "domain": [("id", "in", moves.ids)],
            "view_mode": "list,form",
            "context": self.env.context,
            "target": "current",
        }
