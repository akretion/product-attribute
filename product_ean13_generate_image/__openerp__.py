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


{
    'name': 'Product EAN13 Generate Image',
    'version': '0.1',
    'category': 'TODO',
    'license': 'AGPL-3',
    'summary': 'Generate image of EAN13 barcode of products',
    'description': """
TODO

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion,Odoo Community Association (OCA)',
    'website': 'http://www.akretion.com',
    'depends': ['product'],
    'external_dependencies': {'python': ['barcode']},
    # sudo pip install pyBarcode (and NOT pip install barcode)
    # requires version >= 0.5.0
    'data': [
        'wizard/product_ean13_generate_image_view.xml',
    ],
    'installable': True,
}
