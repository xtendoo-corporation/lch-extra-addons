# Migracion 12.0 -> 13.0: en Odoo 12 los Binary se guardan en COLUMNA (bytea con el texto base64);
# en Odoo 13 el valor por defecto es attachment=True (ir.attachment con res_field). Las firmas se respaldaron
# ANTES del salto en lch_legacy_sig_* (scripts/salto_13_pre.sql) y aqui se convierten en adjuntos.
# account.invoice se funde en account.move: se mapea con account_move.old_invoice_id.
import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

FIELD = "digital_signature"


def _create_attachments(env, model, rows, label):
    """rows: [(res_id, base64_bytes)]. No duplica los que ya tienen adjunto."""
    cr = env.cr
    cr.execute(
        "SELECT res_id FROM ir_attachment WHERE res_model = %s AND res_field = %s",
        (model, FIELD))
    existentes = {r[0] for r in cr.fetchall()}
    Attachment = env["ir.attachment"].sudo()
    creados = 0
    for res_id, data in rows:
        if res_id in existentes or not data:
            continue
        Attachment.create({
            "name": FIELD,
            "type": "binary",
            "res_model": model,
            "res_field": FIELD,
            "res_id": res_id,
            "datas": bytes(data),   # ya es base64 (texto) tal como lo guardaba la columna de Odoo 12
        })
        creados += 1
    cr.execute(
        "SELECT count(DISTINCT res_id) FROM ir_attachment WHERE res_model = %s AND res_field = %s",
        (model, FIELD))
    total = cr.fetchone()[0]
    _logger.info("web_digital_sign: %s: %s adjuntos creados, %s en total", label, creados, total)
    return total


def _check(label, total, esperado):
    if total < esperado:
        raise Exception("web_digital_sign: %s tiene %s firmas de %s esperadas: ABORTO para no perder datos"
                        % (label, total, esperado))


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    if not openupgrade.table_exists(cr, "lch_legacy_sig_invoice"):
        _logger.warning("web_digital_sign: sin respaldo lch_legacy_sig_*; nada que convertir")
        return
    # 1) facturas -> account.move (via old_invoice_id)
    cr.execute("SELECT count(*) FROM lch_legacy_sig_invoice")
    esperado = cr.fetchone()[0]
    cr.execute("""SELECT m.id, s.digital_signature FROM lch_legacy_sig_invoice s
                  JOIN account_move m ON m.old_invoice_id = s.invoice_id""")
    total = _create_attachments(env, "account.move", cr.fetchall(), "account.move")
    _check("account.move", total, esperado)
    # 2) resto de modelos: el id se conserva
    for model, table in (("sale.order", "lch_legacy_sig_sale_order"),
                         ("res.users", "lch_legacy_sig_res_users"),
                         ("stock.picking", "lch_legacy_sig_stock_picking")):
        cr.execute("SELECT count(*) FROM %s" % table)
        esperado = cr.fetchone()[0]
        cr.execute("SELECT rec_id, digital_signature FROM %s" % table)
        total = _create_attachments(env, model, cr.fetchall(), model)
        _check(model, total, esperado)
