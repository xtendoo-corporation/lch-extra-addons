# Migracion 12.0 -> 13.0: account.invoice se funde en account.move (OpenUpgrade deja account_move.old_invoice_id).
# La zona de reparto de cada factura se respaldo ANTES del salto en lch_legacy_invoice_zone
# (scripts/salto_13_pre.sql del proyecto de migracion) y aqui se copia a account_move.delivery_zone_id.
import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    if not openupgrade.table_exists(cr, "lch_legacy_invoice_zone"):
        _logger.warning("partner_delivery_zone: no hay respaldo lch_legacy_invoice_zone; nada que copiar")
        return
    if not openupgrade.column_exists(cr, "account_move", "old_invoice_id"):
        raise Exception("partner_delivery_zone: falta account_move.old_invoice_id (no se ejecuto la migracion de account)")
    openupgrade.logged_query(cr, """
        UPDATE account_move m
        SET delivery_zone_id = z.delivery_zone_id
        FROM lch_legacy_invoice_zone z
        WHERE m.old_invoice_id = z.invoice_id AND m.delivery_zone_id IS NULL
    """)
    cr.execute("SELECT count(*) FROM lch_legacy_invoice_zone")
    esperado = cr.fetchone()[0]
    cr.execute("""SELECT count(*) FROM lch_legacy_invoice_zone z
                  JOIN account_move m ON m.old_invoice_id = z.invoice_id
                  WHERE m.delivery_zone_id = z.delivery_zone_id""")
    copiado = cr.fetchone()[0]
    _logger.info("partner_delivery_zone: zonas de factura copiadas a account_move: %s de %s", copiado, esperado)
    if copiado != esperado:
        raise Exception("partner_delivery_zone: se copiaron %s zonas de %s: ABORTO para no perder datos"
                        % (copiado, esperado))
