from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.constrains('product_id', 'picking_id')
    def _check_duplicate_product_in_picking(self):
        for move in self:
            if not move.product_id or not move.picking_id:
                continue

            duplicates = self.search([
                ('id', '!=', move.id),
                ('picking_id', '=', move.picking_id.id),
                ('product_id', '=', move.product_id.id),
                ('state', '!=', 'cancel'),
            ], limit=1)

            if duplicates:
                raise ValidationError((
                    "لا يمكن إضافة نفس المنتج أكثر من مرة في نفس التحويل.\n"
                    "المنتج: %s"
                ) % move.product_id.display_name)

    @api.onchange('product_id')
    def _onchange_product_no_duplicate(self):
        if not self.product_id or not self.picking_id:
            return

        # المنتجات الموجودة بالفعل في السطور الأخرى
        existing_products = self.picking_id.move_ids_without_package.filtered(
            lambda m: m.product_id and m != self
        ).mapped('product_id.id')

        # لو المنتج المختار موجود قبل كده
        if self.product_id.id in existing_products:
            raise UserError((
                "هذا المنتج مضاف بالفعل في نفس التحويل ولا يمكن تكراره."
            ))
