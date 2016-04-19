# -*- coding: utf-8 -*-
###############################################################################
#
#   Copyright (C) 2015 Akretion (http://www.akretion.com). All Rights Reserved
#   @author Abdessamad HILALI <abdessamad.hilali@akretion.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################


from openerp.tools.safe_eval import safe_eval
from openerp import fields, models, api, _
from openerp.exceptions import Warning


class ProductTemplate(models.Model):
    _inherit = "product.template"

    base_code = fields.Char(
        'Base Code',
        help="this field is used like a base to automatically create "
             "Internal Reference (default_code)")
    base_code_template = fields.Char(
        'Base Code Template',
        help="This field is used like a code base to automatically create "
             "Internal Reference (default_code)",
        default="''.join([o.attribute_id.code or '', o.code or ''])")
    auto_default_code = fields.Boolean(
        'Auto Generate Reference', default=True)


class ProductProduct(models.Model):
    _inherit = "product.product"

    manual_default_code = fields.Char(
        help="This is an invisible field used to store default_code value"
    )
    default_code = fields.Char(
        compute="_compute_default_code",
        inverse="_set_manual_default_code", store=True)

    @api.multi
    def _get_default_code(self):
        """ this method used to create a list of code elements  """
        self.ensure_one()
        result = self.base_code or ''
        for o in self.attribute_value_ids:
            try:
                result += (safe_eval(self.base_code_template, {'o': o}))
            except AttributeError:
                raise Warning(_('Bad expression'),
                              _("One of your expressions contains "
                                "a non existing attribute: %s"
                                ))
        return result

    def _set_manual_default_code(self):
        self.manual_default_code = self.default_code

    @api.depends('auto_default_code',
                 'attribute_value_ids.attribute_id.code',
                 'attribute_value_ids.code',
                 'product_tmpl_id.base_code',
                 'product_tmpl_id.base_code_template'
                 )
    def _compute_default_code(self):
        for product in self:
            if product.auto_default_code:
                product.default_code = product._get_default_code()
            else:
                product.default_code = product.manual_default_code
