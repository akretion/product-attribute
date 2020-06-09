# Copyright 2020 Akretion (https://www.akretion.com).
# @author Pierrick Brun <pierrick.brun@akretion.com>
# @author Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    list_price_per_quantity = fields.Monetary(
        string="Price per quantity",
        compute="_calc_list_price_per_quantity",
        help="List price per unit of measure.",
    )
    price_per_quantity_uom = fields.Many2one(
        "uom.uom",
        string="Price unit of measure",
        help="Express price in unit of measure",
    )

    def _prepare_price_for_price_per_quantity(self, product):
        return product.list_price

    def _prepare_price_per_quantity(self, product, price, price_per_quantity_uom):
        # we don't read price_per_quantity_uom on product
        # because in some cases, you can to calculate
        # price per weight and price per volume at the same time
        uom_categ_type = self._uom_lookup_by_categ().get(price_per_quantity_uom.category_id)

        if uom_categ_type == "weight":
            vals = {
                "price_per_unit": price,
                "quantity_per_unit": product.weight,
                "quantity_uom": product.weight_uom_id,
                "target_uom": price_per_quantity_uom,
            }
        elif uom_categ_type == "volume":
            vals = {
                "price_per_unit": price,
                "quantity_per_unit": product.volume,
                "quantity_uom": product.volume_uom_id,
                "target_uom": price_per_quantity_uom,
            }
        elif uom_categ_type == "unit":
            # ie price per egg:
            #  quantity_uom: dozen, target uom : unit
            vals = {
                "price_per_unit": price,
                "quantity_per_unit": 1,  # uom.factor is used in _compute_price
                "quantity_uom": product.uom_id,
                "target_uom": price_per_quantity_uom,
            }
        else:
            vals = False
        return vals

    def _calc_list_price_per_quantity(self):
        for product in self:
            vals = self._prepare_price_per_quantity(
                product,
                self._prepare_price_for_price_per_quantity(product),
                product.price_per_quantity_uom,
            )
            if vals:
                product.list_price_per_quantity = self._calc_price_per_uom(**vals)
            else:
                product.list_price_per_quantity = 0

    def _calc_price_per_uom(
        self, price_per_unit, quantity_per_unit, quantity_uom, target_uom
    ):
        """Calc a price for a given unit of measure.

        When the product is sell in unit, you may need
        to display a price per kg (or price/L for volumes).

        price_per_unit price for 1 unit (usually lst_price) (float)
        quantity_per_unit: product.weight or product.volume (float)
        quantity_uom: uom of quantity_per_unit (kg or m³ [uom.uom])
        target_uom: kg or l [uom.uom]
        """
        if not quantity_per_unit:
            return 0
        price_per_quantity = price_per_unit / quantity_per_unit
        return quantity_uom._compute_price(price_per_quantity, target_uom)

    def _uom_lookup_by_categ(self):
        """Helper."""
        return {
            self.env.ref("uom.product_uom_categ_kgm"): "weight",
            self.env.ref("uom.product_uom_categ_vol"): "volume",
            self.env.ref("uom.product_uom_categ_unit"): "unit",
        }


class ProductProduct(models.Model):
    _inherit = "product.product"

    lst_price_per_quantity = fields.Monetary(
        string="Price per quantity", compute="_calc_lst_price_per_quantity",
    )

    def _prepare_price_for_price_per_quantity(self, product):
        return product.lst_price

    def _calc_lst_price_per_quantity(self):
        tmpl = self.env["product.template"]
        prod_prod = self.env["product.product"]
        for product in self:
            vals = tmpl._prepare_price_per_quantity(
                product,
                prod_prod._prepare_price_for_price_per_quantity(product),
                product.price_per_quantity_uom,
            )
            if vals:
                product.lst_price_per_quantity = tmpl._calc_price_per_uom(**vals)
            else:
                product.lst_price_per_quantity = 0
