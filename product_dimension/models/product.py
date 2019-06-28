# Copyright 2015 ADHOC SA  (http://www.adhoc.com.ar)
# Copyright 2015-2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, api


class ProductVolumeMixin(models.AbstractModel):
    _name = 'product.volume.mixin'
    _description = 'Product Volume Mixin'

    def create(self, vals_list):
        # recompute volume when dimensions are created from import because
        # onchange won't have any effect on this case.
        if self.env.context.get('import_file'):
            dimension_fields = [
                'length', 'height', 'width', 'dimensional_uom_id'
            ]
            for vals in vals_list:
                if (all([vals.get(key) for key in dimension_fields]) and
                        'volume' not in vals):
                    dimensional_uom = self.env['uom.uom'].browse(
                        vals['dimensional_uom_id'])
                    volume = self.env['product.template']._calc_volume(
                        vals['length'], vals['height'], vals['width'],
                        dimensional_uom)
                    vals['volume'] = volume
        return super().create(vals_list)

    def write(self, vals):
        # recompute volume when dimensions are updated from import because
        # onchange won't have any effect on this case.
        # write from import can only update 1 product at a time?
        if (self.env.context.get('import_file') and 'volume' not in vals and
                len(self) == 1):
            dimension_fields = [
                'length', 'height', 'width', 'dimensional_uom_id'
            ]
            if any([key in dimension_fields for key in vals.keys()]):
                length = 'length' in vals and vals['length'] or self.length
                height = 'height' in vals and vals['height'] or self.height
                width = 'width' in vals and vals['width'] or self.width
                dimensional_uom = ('dimensional_uom_id' in vals and
                                   self.env['uom.uom'].browse(
                                       vals['dimensional_uom_id']) or
                                   self.dimensional_uom_id)
                volume = self.env['product.template']._calc_volume(
                    length, height, width, dimensional_uom)
                vals['volume'] = volume
        return super().write(vals)


class Product(models.Model):
    _name = 'product.product'
    _inherit = ['product.product', 'product.volume.mixin']

    @api.onchange('length', 'height', 'width', 'dimensional_uom_id')
    def onchange_calculate_volume(self):
        self.volume = self.env['product.template']._calc_volume(
            self.length, self.height, self.width, self.dimensional_uom_id)

    @api.model
    def _get_dimension_uom_domain(self):
        return [
            ('category_id', '=', self.env.ref('uom.uom_categ_length').id)
        ]

    length = fields.Float()
    height = fields.Float()
    width = fields.Float()
    dimensional_uom_id = fields.Many2one(
        'uom.uom',
        'Dimensional UoM',
        domain=lambda self: self._get_dimension_uom_domain(),
        help='UoM for length, height, width')


class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = ['product.template', 'product.volume.mixin']

    @api.model
    def _calc_volume(self, length, height, width, uom_id):
        volume = 0
        if length and height and width and uom_id:
            length_m = self.convert_to_meters(length, uom_id)
            height_m = self.convert_to_meters(height, uom_id)
            width_m = self.convert_to_meters(width, uom_id)
            volume = length_m * height_m * width_m

        return volume

    @api.onchange('length', 'height', 'width', 'dimensional_uom_id')
    def onchange_calculate_volume(self):
        self.volume = self._calc_volume(
            self.length, self.height, self.width, self.dimensional_uom_id)

    def convert_to_meters(self, measure, dimensional_uom):
        uom_meters = self.env.ref('uom.product_uom_meter')

        return dimensional_uom._compute_quantity(
            qty=measure,
            to_unit=uom_meters,
            round=False,
        )

    length = fields.Float(related='product_variant_ids.length', readonly=False)
    height = fields.Float(related='product_variant_ids.height', readonly=False)
    width = fields.Float(related='product_variant_ids.width', readonly=False)
    dimensional_uom_id = fields.Many2one(
        'uom.uom',
        'Dimensional UoM', related='product_variant_ids.dimensional_uom_id',
        help='UoM for length, height, width', readonly=False)
