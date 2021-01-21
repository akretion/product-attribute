# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Default Product Packaging",
    "summary": """
        Define default product packaging to be used in sale.order.line""",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "Akretion,Odoo Community Association (OCA)",
    "website": "http://akretion.com",
    "depends": ["product", "stock", "sale"],
    "data": ["views/product_packaging.xml"],
}
