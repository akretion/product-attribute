# -*- coding: utf-8 -*-
# © 2014-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ProductTemplate(models.Model):
    """Reference core image fields to multi-image variants.

    It is needed to use v7 api here because core model fields use the ``multi``
    attribute, that has no equivalent in v8, and it needs to be disabled or
    bad things will happen. For more reference, see
    https://github.com/odoo/odoo/issues/10799
    """
    _name = 'product.template'
    _inherit = [_name, "storage.image.owner.compatibility"]

    image = fields.Binary(
        related='image_main',
        store=False
    )
    image_medium = fields.Binary(
        related='image_main_medium',
        store=False
    )
    image_small = fields.Binary(
        related='image_main_small',
        store=False
    )
