# Copyright 2009 Pexego Sistemas Informáticos
# Copyright 2013-2018 Pedro Manuel Baeza
# Copyright 2013 Joaquin Gutierrez <http://www.gutierrezweb.es>
# Copyright 2016 Jairo Llopis
# Copyright 2017 David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Port a 19.0 de OCA/account-financial-tools 12.0 para LCH.
{
    "name": "Account Renumber Wizard",
    "version": "19.0.1.0.0",
    "author": "Pexego, Tecnativa, Xtendoo, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/account-financial-tools",
    "category": "Accounting/Accounting",
    "license": "AGPL-3",
    "depends": ["account"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/wizard_renumber_view.xml",
    ],
    "installable": True,
}
