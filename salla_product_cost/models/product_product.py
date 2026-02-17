# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    x_salla_cost = fields.Float(
        string='Salla Cost',
        digits='Product Price',
        help='Cost price that syncs with Standard Price. Always visible and editable.',
        tracking=True,
    )

    @api.model
    def create(self, vals):
        # عند الإنشاء، لو في x_salla_cost نحط قيمته في standard_price
        if 'x_salla_cost' in vals and vals.get('x_salla_cost'):
            vals['standard_price'] = vals['x_salla_cost']
        # لو في standard_price ومفيش x_salla_cost، ناخد قيمة standard_price
        elif 'standard_price' in vals and 'x_salla_cost' not in vals:
            vals['x_salla_cost'] = vals.get('standard_price', 0.0)
        return super(ProductProduct, self).create(vals)

    def write(self, vals):
        # لو المستخدم عدل x_salla_cost، نحدث standard_price
        if 'x_salla_cost' in vals:
            vals['standard_price'] = vals['x_salla_cost']
        # لو المستخدم عدل standard_price من مكان تاني، نحدث x_salla_cost
        elif 'standard_price' in vals and 'x_salla_cost' not in vals:
            vals['x_salla_cost'] = vals['standard_price']
        return super(ProductProduct, self).write(vals)

    @api.onchange('x_salla_cost')
    def _onchange_x_salla_cost(self):
        """عند تغيير Salla Cost، نحدث Standard Price مباشرة"""
        if self.x_salla_cost:
            self.standard_price = self.x_salla_cost

    @api.onchange('standard_price')
    def _onchange_standard_price(self):
        """عند تغيير Standard Price، نحدث Salla Cost مباشرة"""
        if self.standard_price and not self.x_salla_cost:
            self.x_salla_cost = self.standard_price
