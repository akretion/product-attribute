# Copyright 2021 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_compare


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    def _compute_tax_incl(self, price):
        """Returns `price` with added self's taxes"""
        self.ensure_one()
        res_tax = self.product_tax_ids.compute_all(price, currency=self.currency_id)
        return res_tax["total_included"]

    product_tax_ids = fields.Many2many(
        string="Product taxes",
        comodel_name="account.tax",
        compute="_compute_product_tax_ids",
        help="Product (or Variant) taxes",
    )

    fixed_price_tax = fields.Float(
        "Fixed Price incl. tax",
        digits=dp.get_precision("Product Price"),
        compute="_compute_fixed_price_tax",
        inverse="_inverse_fixed_price_tax",
        readonly=False,
        help="Price calculated from 'Fixed Price excl. tax' and 'Product taxes'.\n"
        "If this price is set manually, you need to save the record to allow the "
        "'Fixed Price excl. tax' value calculation.",
    )

    display_fixed_price_tax = fields.Boolean(
        string="Display Fixed Price incl. tax", default=False
    )

    @api.onchange("compute_price")
    def _onchange_compute_price_set_display_fixed_price_tax(self):
        if self.compute_price != "fixed_price":
            self.display_fixed_price_tax = False

    @api.depends("product_id", "product_tmpl_id")
    def _compute_product_tax_ids(self):
        for item in self:
            prod_id = item.product_id or item.product_tmpl_id
            item.product_tax_ids = prod_id.taxes_id if prod_id else [(5, 0, 0)]

    @api.depends("fixed_price", "product_tax_ids")
    def _compute_fixed_price_tax(self):
        for item in self:
            if item.product_tax_ids:
                item.fixed_price_tax = item._compute_tax_incl(item.fixed_price)
            else:
                item.fixed_price_tax = item.fixed_price

    def _inverse_fixed_price_tax(self):
        for item in self:
            rounding = item.currency_id.rounding
            starting_price_excl = item.fixed_price_tax - rounding
            
            if item.product_tax_ids and starting_price_excl > 0:
                price_excl = starting_price_excl
                price_incl = item._compute_tax_incl(price_excl)
                while (
                    float_compare(
                        price_incl, item.fixed_price_tax, precision_rounding=rounding,
                    )
                    != 0
                ):
                    price_excl -= rounding
                    price_incl = item._compute_tax_incl(price_excl)

                item.fixed_price = price_excl
            else:
                item.fixed_price = item.fixed_price_tax
