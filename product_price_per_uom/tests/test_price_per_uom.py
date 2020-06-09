# Copyright 2020 Akretion (http://www.akretion.com).
# @author Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common
from odoo.tools import float_compare


class TestProductPericePerUom(common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.precision = self.env['decimal.precision'].precision_get('Stock')
        self.product = self.env.ref('product.product_product_6')
        self.uom_unit = self.env.ref('uom.product_uom_unit')
        self.uom_kgm = self.env.ref('uom.product_uom_kgm')
        self.uom_gram = self.env.ref('uom.product_uom_gram')

    def test_unit(self):
        self.product.weight_uom_id = self.uom_kgm
        self.product.price_per_quantity_uom = self.uom_unit
        self.assertEqual(
            self.product.list_price_per_quantity,
            self.product.list_price)

    def test_kg(self):
        self.product.weight_uom_id = self.uom_kgm
        self.product.price_per_quantity_uom = self.uom_kgm
        self.assertEqual(
            float_compare(
                self.product.list_price_per_quantity,
                self.product.list_price / self.product.weight,
                precision_digits=self.precision
            ), 0)

    def test_g(self):
        self.product.weight_uom_id = self.uom_kgm
        self.product.price_per_quantity_uom = self.uom_gram
        self.assertEqual(
            float_compare(
                self.product.list_price_per_quantity,
                self.product.list_price / (self.product.weight * 1000),
                precision_digits=self.precision
            ), 0)

    def test_g_g(self):
        self.product.weight_uom_id = self.uom_gram
        self.product.price_per_quantity_uom = self.uom_gram
        self.assertEqual(
            float_compare(
                self.product.list_price_per_quantity,
                self.product.list_price / (self.product.weight),
                precision_digits=self.precision
            ), 0)

    def test_g_kg(self):
        self.product.weight_uom_id = self.uom_gram
        self.product.price_per_quantity_uom = self.uom_kgm
        self.assertEqual(
            float_compare(
                self.product.list_price_per_quantity,
                self.product.list_price / (self.product.weight / 1000),
                precision_digits=self.precision
            ), 0)
