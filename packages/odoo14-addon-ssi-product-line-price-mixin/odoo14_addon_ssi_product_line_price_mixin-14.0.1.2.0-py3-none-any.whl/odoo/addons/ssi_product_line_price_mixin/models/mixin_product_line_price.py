# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class MixinProductLinePrice(models.AbstractModel):
    _name = "mixin.product_line_price"
    _description = "Product Line Mixin - With Price"
    _inherit = [
        "mixin.product_line",
    ]

    @api.model
    def _default_currency_id(self):
        return self.env.company.currency_id.id

    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        required=True,
        default=lambda self: self._default_currency_id(),
    )

    @api.depends(
        "currency_id",
    )
    def _compute_allowed_pricelist_ids(self):
        Pricelist = self.env["product.pricelist"]
        for record in self:
            result = []
            if record.currency_id:
                criteria = record._get_pricelist_domain()
                result = Pricelist.search(criteria).ids
            record.allowed_pricelist_ids = result

    allowed_pricelist_ids = fields.Many2many(
        string="Allowed Pricelists",
        comodel_name="product.pricelist",
        compute="_compute_allowed_pricelist_ids",
        compute_sudo=True,
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
    )
    price_unit = fields.Monetary(
        string="Price Unit",
        currency_field="currency_id",
        required=True,
        default=0.0,
    )

    @api.depends(
        "price_unit",
        "uom_quantity",
    )
    def _compute_price(self):
        for record in self:
            record.price_subtotal = record.price_unit * record.uom_quantity

    price_subtotal = fields.Monetary(
        string="Price Subtotal",
        currency_field="currency_id",
        compute="_compute_price",
        store=True,
    )

    @api.onchange(
        "allowed_pricelist_ids",
        "currency_id",
    )
    def onchange_pricelist_id(self):
        self.pricelist_id = False
        if self.allowed_pricelist_ids:
            self.pricelist_id = self.allowed_pricelist_ids[0]._origin.id

    def _get_pricelist_domain(self):
        self.ensure_one()
        return [
            ("currency_id", "=", self.currency_id.id),
        ]

    @api.onchange(
        "product_id",
        "uom_quantity",
        "uom_id",
        "pricelist_id",
    )
    def onchange_price_unit(self):
        if self.product_id and self.pricelist_id:
            product_context = dict(
                self.env.context, uom=self.uom_id and self.uom_id.id or False
            )
            final_price, rule_id = self.pricelist_id.with_context(
                product_context
            ).get_product_price_rule(self.product_id, self.uom_quantity or 1.0, False)
            self.price_unit = final_price
