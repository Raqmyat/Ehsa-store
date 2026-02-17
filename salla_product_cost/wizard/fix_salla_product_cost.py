# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError


class FixSallaProductCost(models.TransientModel):
    _name = 'fix.salla.product.cost'
    _description = 'Fix Salla Product Cost Wizard'

    product_count = fields.Integer(string='Products to Fix', readonly=True)
    default_cost = fields.Float(
        string='Default Cost for Empty Products',
        default=0.0,
        help='القيمة الافتراضية للتكلفة للمنتجات اللي مفيهاش تكلفة'
    )

    @api.model
    def default_get(self, fields_list):
        res = super(FixSallaProductCost, self).default_get(fields_list)
        # عد المنتجات اللي محتاجة إصلاح
        products = self.env['product.template'].search([
            ('x_salla_cost', '=', 0.0),
        ])
        res['product_count'] = len(products)
        return res

    def action_fix_products(self):
        """إصلاح كل المنتجات اللي فيها مشكلة"""
        self.ensure_one()
        
        # جيب كل المنتجات اللي x_salla_cost فاضي أو صفر
        products = self.env['product.template'].search([
            ('x_salla_cost', '=', 0.0),
        ])
        
        fixed_count = 0
        error_count = 0
        
        for product in products:
            try:
                # حاول تاخد القيمة من standard_price
                if product.standard_price and isinstance(product.standard_price, (int, float)):
                    # لو standard_price رقم صحيح، خده
                    product.write({
                        'x_salla_cost': product.standard_price,
                    })
                    fixed_count += 1
                else:
                    # لو standard_price فيه مشكلة، حط القيمة الافتراضية
                    product.write({
                        'x_salla_cost': self.default_cost,
                        'standard_price': self.default_cost,
                    })
                    fixed_count += 1
            except Exception as e:
                error_count += 1
                continue
        
        # رسالة نجاح
        message = f'✅ تم إصلاح {fixed_count} منتج بنجاح!'
        if error_count > 0:
            message += f'\n⚠️ فشل إصلاح {error_count} منتج'
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'نجح الإصلاح!',
                'message': message,
                'type': 'success',
                'sticky': False,
            }
        }

    def action_fix_variants(self):
        """إصلاح كل الـ variants اللي فيها مشكلة"""
        self.ensure_one()
        
        # جيب كل الـ variants اللي x_salla_cost فاضي أو صفر
        variants = self.env['product.product'].search([
            ('x_salla_cost', '=', 0.0),
        ])
        
        fixed_count = 0
        error_count = 0
        
        for variant in variants:
            try:
                # حاول تاخد القيمة من standard_price
                if variant.standard_price and isinstance(variant.standard_price, (int, float)):
                    # لو standard_price رقم صحيح، خده
                    variant.write({
                        'x_salla_cost': variant.standard_price,
                    })
                    fixed_count += 1
                else:
                    # لو standard_price فيه مشكلة، حط القيمة الافتراضية
                    variant.write({
                        'x_salla_cost': self.default_cost,
                        'standard_price': self.default_cost,
                    })
                    fixed_count += 1
            except Exception as e:
                error_count += 1
                continue
        
        # رسالة نجاح
        message = f'✅ تم إصلاح {fixed_count} variant بنجاح!'
        if error_count > 0:
            message += f'\n⚠️ فشل إصلاح {error_count} variant'
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'نجح الإصلاح!',
                'message': message,
                'type': 'success',
                'sticky': False,
            }
        }
