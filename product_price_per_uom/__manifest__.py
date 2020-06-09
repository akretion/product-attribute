# Copyright 2020 Akretion (https://www.akretion.com).
{
    "name": "Product Price Per UoM",
    "summary": "Calculate a price for a given UoM",
    "version": "12.0.1.0.0",
    "category": "Product",
    "development_status": "Beta",
    "author": "Akretion, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "maintainers": ["hparfr"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["product", "product_logistics_uom",],
    "data": ["views/product.xml"],
}
