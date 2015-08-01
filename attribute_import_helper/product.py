# coding: utf-8
##############################################################################
#
#    Author: Sébastien BEAU
#    Copyright 2015 Akretion
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api
from collections import defaultdict


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def set_attribute_vals(self, vals):
        # if 'categ_id' not in vals:
        #     vals['categ_id'] = 1
        # if 'product_variant_ids' not in vals:
        #     return True
        # res = defaultdict(list)
        # value_obj = self.env['product.attribute.value']
        # for variant in vals['product_variant_ids']:
        #     if variant[2]['attribute_value_ids']:
        #         for value in value_obj.browse(
        #                 variant[2]['attribute_value_ids'][0][2]):
        #             if value.id not in res[value.attribute_id.id]:
        #                 res[value.attribute_id.id].append(value.id)
        # lines = []
        # for attr_id, value_ids in res.items():
        #     lines.append([0, 0, ({
        #         'attribute_id': attr_id,
        #         'value_ids': [(6, 0, value_ids)],
        #         })])
        # vals['attribute_line_ids'] = lines
        return True

    @api.model
    def create(self, vals):
        self.set_attribute_vals(vals)
        res = super(ProductTemplate, self).create(vals)
        return res

    @api.multi
    def write(self, vals):
        add_xml = False
        if 'attribute_line_ids' in vals or vals.get('active'):
            add_xml = True
        # Update attribute vals if template already exist
        if self._context.get('install_mode') \
                and vals.get('attribute_line_ids'):
            for tmpl in self:
                new_attr = []
                for key, _, attr_vals in vals['attribute_line_ids']:
                    exist = False
                    for attr in tmpl.attribute_line_ids:
                        if attr.attribute_id.id == attr_vals['attribute_id']:
                            attr.write({'value_ids': attr_vals['value_ids']})
                            exist = True
                            break
                    if not exist:
                        new_attr.append((0, 0, attr_vals))
                vals['attribute_line_ids'] = new_attr
                super(ProductTemplate, tmpl).write(vals)
        else:
            super(ProductTemplate, self).write(vals)
        if add_xml:
            self.product_variant_ids.add_xml_id()
        return True


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def _generate_product_xml_id(self):
        self.ensure_one()

        def get_id(record):
            xml_id = record.get_external_id()[record.id].split('.')
            if len(xml_id) == 2:
                return xml_id[1]
        tmpl_xmlid = get_id(self.product_tmpl_id)
        # only imported data should have xmlid
        if tmpl_xmlid:
            xml_id = ['variant', tmpl_xmlid]
            for value in self.attribute_value_ids:
                xml_id.append(get_id(value))
            return '_'.join(xml_id)
        return True

    @api.one
    def add_xml_id(self):
        xml_id = self.get_external_id()[self.id]
        if self.product_tmpl_id.get_external_id() and not xml_id:
            self.env['ir.model.data'].create({
                'name': self._generate_product_xml_id(),
                'model': 'product.product',
                'module': '',
                'res_id': self.id,
                'noupdate': False,
                })
