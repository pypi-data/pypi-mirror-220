# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class MixinProductLineAccount(models.AbstractModel):
    _name = "mixin.product_line_account"
    _description = "Product Line Mixin - With Accounting"
    _inherit = [
        "mixin.product_line_price",
    ]

    tax_ids = fields.Many2many(
        string="Tax(es)",
        comodel_name="account.tax",
    )

    @api.depends(
        "quantity",
        "price_unit",
        "tax_ids",
        "currency_id",
    )
    def _compute_total(self):
        for record in self:
            subtotal = tax = total = 0.0
            taxes = record.tax_ids.compute_all(
                record.price_unit,
                record.currency_id,
                record.quantity,
                product=record.product_id,
                partner=False,
            )
            tax = sum(t.get("amount", 0.0) for t in taxes.get("taxes", []))
            total = taxes["total_included"]
            subtotal = taxes["total_excluded"]
            record.price_subtotal = subtotal
            record.price_tax = tax
            record.price_total = total

    price_subtotal = fields.Monetary(
        compute="_compute_total",
        store=True,
    )
    price_tax = fields.Monetary(
        string="Tax",
        compute="_compute_total",
        currency_field="currency_id",
        store=True,
    )
    price_total = fields.Monetary(
        string="Total",
        compute="_compute_total",
        currency_field="currency_id",
        store=True,
    )

    @api.depends(
        "product_id",
    )
    def _compute_allowed_usage_ids(self):
        Usage = self.env["product.usage_type"]
        for record in self:
            result = []
            if record.product_id:
                criteria = record._get_usage_domain()
                result = Usage.search(criteria).ids
            record.allowed_usage_ids = result

    allowed_usage_ids = fields.Many2many(
        string="Allowed Usages",
        comodel_name="product.usage_type",
        compute="_compute_allowed_usage_ids",
        compute_sudo=True,
    )
    usage_id = fields.Many2one(
        string="Usage",
        comodel_name="product.usage_type",
        ondelete="restrict",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
        required=True,
        ondelete="restrict",
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        required=False,
        ondelete="restrict",
    )

    def _get_usage_domain(self):
        self.ensure_one()
        return []

    @api.onchange(
        "usage_id",
        "product_id",
    )
    def onchange_account_id(self):
        self.account_id = False
        if self.product_id and self.usage_id:
            self.account_id = self.product_id._get_product_account(
                usage_code=self.usage_id.code
            )

    @api.onchange(
        "usage_id",
        "product_id",
    )
    def onchange_tax_ids(self):
        self.tax_ids = False
        if self.product_id and self.usage_id:
            self.tax_ids = [
                (6, 0, self.product_id._get_product_tax(usage_code=self.usage_id.code))
            ]
