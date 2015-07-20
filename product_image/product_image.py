# -*- coding: utf-8 -*-
###############################################################################
#
#   Module for OpenERP
#   Copyright (C) 2009  Sharoon Thomas, Open Labs Business solutions
#   Copyright (C) 2014 Akretion (http://www.akretion.com).
#   @author Sébastien BEAU <sebastien.beau@akretion.com>
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

from openerp import fields, models, api, tools
import os


class ProductImage(models.Model):
    "Products Image"
    _name = "product.image"
    _order='sequence,name'

    @api.one
    @api.depends('image')
    def _get_image_sizes(self):
        self.image_medium = False
        self.image_small = False
        if self.image:
            try:
                vals = tools.image_get_resized_images(
                    self.image, avoid_resize_medium=True)
                self.image_small = vals['image_small']
                self.image_medium = vals['image_medium']
            except:
                pass

    sequence = fields.Integer('Sequence')
    name = fields.Char('Image Title')
    file_name = fields.Char('File name', required=True)
    description = fields.Text('Description')
    image = fields.Binary('Image')
    image_medium = fields.Binary(
       compute='_get_image_sizes',
       string='Medium Image',
       )
    image_small = fields.Binary(
       compute='_get_image_sizes',
       string='Small Image',
       )
    product_id = fields.Many2one('product.template', 'Product')

    @api.onchange('file_name')
    def onchange_file_name(self):
        if not self.name and self.file_name:
            name, extension = os.path.splitext(self.file_name)
            for mapping in [('_', ' '), ('.', ' ')]:
                name = name.replace(mapping[0], mapping[1])
            self.name = name

    @api.model
    def create(self, vals):
        if not 'sequence' in vals:
            cr.execute("""SELECT max(sequence)
                FROM product_image
                WHERE product_id = %s""",
                (vals['product_id'],))
            max_sequence = cr.fetchone()[0]
            if max_sequence is not None:
                vals['sequence'] = max_sequence + 1
            else:
                vals['sequence'] = 0
        return super(ProductImage, self).create(vals)
