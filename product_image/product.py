# -*- coding: utf-8 -*-
###############################################################################
#
#   Module for OpenERP
#   Copyright (C) 2009  Sharoon Thomas, Open Labs Business solutions
#   Copyright (C) 2011-TODAY Akretion (http://www.akretion.com).
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

from openerp import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def _get_main_image(self):
        if self.image_ids:
            return self.image_ids[0]
        return None

    @api.one
    @api.depends('image_ids')
    def _get_images(self):
        self.image = False
        self.image_medium = False
        self.image_small = False
        image = self._get_main_image()
        if image:
            self.image = image.image
            self.image_medium = image.image_medium
            self.image_small = image.image_small

    image_ids = fields.One2many(
        'product.image',
        'product_id',
        string='Product Image',
        copy=False)
    image = fields.Binary(
        compute='_get_images',
        string="Main Image")
    image_medium = fields.Binary(
        compute='_get_images',
        string="Medium-sized image")
    image_small = fields.Binary(
        compute='_get_images',
        string="Small-sized image")
