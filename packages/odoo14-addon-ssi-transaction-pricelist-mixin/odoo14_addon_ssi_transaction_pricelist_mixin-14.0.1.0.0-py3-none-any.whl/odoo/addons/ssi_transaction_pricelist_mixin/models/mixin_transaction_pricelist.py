# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MixinTransactionPricelist(models.AbstractModel):
    _name = "mixin.transaction_pricelist"
    _inherit = [
        "mixin.transaction",
        "mixin.pricelist",
    ]
    _description = "Transaction + Pricelist Mixin"

    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
