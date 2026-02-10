from odoo import models, api, _
from odoo.exceptions import UserError, ValidationError


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_id')
    def _onchange_product_no_duplicate(self):
        if not self.product_id or not self.order_id:
            return

        products = self.order_id.order_line.filtered(
            lambda l: l.product_id and l != self
        ).mapped('product_id.id')

        if self.product_id.id in products:
            raise UserError(_(
                "هذا المنتج مضاف بالفعل في نفس أمر الشراء ولا يمكن تكراره."
            ))

    @api.constrains('product_id', 'order_id')
    def _check_duplicate_product(self):
        for line in self:
            if not line.product_id or not line.order_id:
                continue

            duplicate = self.search([
                ('id', '!=', line.id),
                ('order_id', '=', line.order_id.id),
                ('product_id', '=', line.product_id.id),
            ], limit=1)

            if duplicate:
                raise ValidationError(_(
                    "لا يمكن إضافة نفس المنتج أكثر من مرة في نفس أمر الشراء."
                ))
