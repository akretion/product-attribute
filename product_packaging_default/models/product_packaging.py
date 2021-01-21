# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    is_default = fields.Boolean(
        string="Is default packaging",
        help="If selected, the packaging field in the product's Sale Order lines "
        "will be filled by default with this packaging.",
        readonly=True,
    )

    # The action button solution was prefered than an onchange method in order to avoid
    # having 2 packaging marked as default for the same product even in edit mode.
    def action_set_is_default(self):
        self.ensure_one()
        other_pack_ids = self.env["product.packaging"].search(
            [("product_id", "=", self.product_id.id), ("id", "!=", self.id)]
        )
        other_pack_ids.write({"is_default": False})
        self.is_default = True
