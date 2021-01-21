# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange("product_id")
    def _onchange_product_id_set_packaging(self):
        default_pack_id = self.env["product.packaging"].search(
            [("product_id", "=", self.product_id.id), ("is_default", "=", True)],
            limit=1,
        )
        self.product_packaging = default_pack_id
        self.product_uom =  default_pack_id.product_uom_id
        self.product_uom_qty = default_pack_id.qty
