# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product EAN13 Generate Image module for Odoo
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
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


from openerp import models, fields, api, _
from openerp.exceptions import Warning
from StringIO import StringIO
from barcode.writer import ImageWriter
from barcode import generate
import base64


class ProductEan13GenerateImage(models.TransientModel):
    _name = 'product.ean13.generate.image'  # renommer sans le "product" ?
    _description = 'Generate EAN13 Image'

    def _default_ean13(self):
        active_id = self.env.context.get('active_id')
        if (
                self.env.context.get('active_model') == 'product.product' and
                active_id):
            product = self.env['product.product'].browse(active_id)
            return product.ean13
        else:
            return False

    ean13 = fields.Char(string='EAN13', readonly=True, default=_default_ean13)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ], readonly=True, default='draft')
    image = fields.Binary(string='Image File')
    filename = fields.Char(readonly=True)
    image_format = fields.Selection([
        ('png', 'PNG'),
        ('jpeg', 'JPEG'),
        ('svg', 'SVG'),
        ], string='Image Format', default='png', required=True)
    width = fields.Integer('Width', default=35)
    height = fields.Integer('Height', default=15)
    dpi = fields.Integer('DPI', default=300)
    with_text = fields.Boolean(string='With Text', default=True)

    @api.multi
    def generate_image(self):
        self.ensure_one()
        if not self.ean13:
            raise Warning(_('Missing EAN13'))
        # TODO : SVG
        myimagewriter = ImageWriter()
        myimagewriter.format = self.image_format
        myimagewriter.dpi = self.dpi
        writer_options = {
            # 'module_width': self.width,
            # 'module_height': self.height,
            # 'quiet_zone': 6.5,
            'font_size': self.with_text and 20 or 0,
            'text_distance': 5,
            'center_text': True,
        }
        vfile = StringIO()
        generate(
            'EAN13', self.ean13, writer=myimagewriter, output=vfile,
            writer_options=writer_options)
        self.write({
            'state': 'done',
            'image': base64.encodestring(vfile.getvalue()),
            'filename': u'%s.%s' % (self.ean13, self.image_format),
        })
        action = {
            'name': self._description,
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': self._name,
            'res_id': self.id,
            'target': 'new',
        }
        return action
