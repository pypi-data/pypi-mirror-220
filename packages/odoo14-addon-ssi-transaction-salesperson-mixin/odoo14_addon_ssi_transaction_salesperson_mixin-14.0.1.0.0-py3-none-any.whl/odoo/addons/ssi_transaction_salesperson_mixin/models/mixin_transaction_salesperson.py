# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MixinTransactionSalesperson(models.AbstractModel):
    _name = "mixin.transaction_salesperson"
    _inherit = [
        "mixin.transaction",
        "mixin.salesperson",
    ]
    _description = "Transaction + Salesperson Mixin"

    sale_team_id = fields.Many2one(
        required=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    salesperson_id = fields.Many2one(
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
