# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class MixinPricelist(models.AbstractModel):
    _name = "mixin.pricelist"
    _description = "Pricelist Mixin"

    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
    )

    @api.depends(
        "currency_id",
    )
    def _compute_allowed_pricelist_ids(self):
        Pricelist = self.env["product.pricelist"]
        for record in self:
            result = False
            if record.currency_id:
                criteria = [
                    ("currency_id", "=", record.currency_id.id),
                ]
                result = Pricelist.search(criteria).ids
            record.allowed_pricelist_ids = result

    allowed_pricelist_ids = fields.Many2many(
        string="Allowed Pricelists",
        comodel_name="product.pricelist",
        compute="_compute_allowed_pricelist_ids",
        store=False,
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
    )

    @api.onchange(
        "currency_id",
    )
    def onchange_pricelist_id(self):
        self.pricelist_id = False
