
from odoo import models,fields, api
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    available_qty = fields.Float(
        string="Available Quantity",
        compute="_compute_available_qty",
        store=False
    )

    @api.depends('product_id', 'order_id.warehouse_id')
    def _compute_available_qty(self):
        for line in self:
            qty = 0.0
            if line.product_id and line.order_id.warehouse_id:
                warehouse = line.order_id.warehouse_id
                product = line.product_id.with_context(
                    warehouse=warehouse.id,
                    location=warehouse.lot_stock_id.id,  # 🔥 الفارق هنا
                    company_id=line.order_id.company_id.id,
                )
                qty = product.qty_available  # أو free_qty

            line.available_qty = qty

    @api.constrains('product_id', 'product_uom_qty', 'order_id.picking_type_id.warehouse_id')
    def _check_qty_available(self):
        for line in self:
            if line.product_id and line.product_uom_qty:
                if line.product_uom_qty > line.available_qty:
                    raise ValidationError(
                        f"لا يمكن اظافة هذا المنتج من هذا المخزن.\n"
                        f"الكميه المطلوبه ({line.product_uom_qty}) اكبر من الكميه المتاحه ({line.available_qty})."
                    )

    @api.onchange('product_id', 'product_uom_qty', 'order_id.picking_type_id.warehouse_id')
    def _onchange_check_qty(self):
        for line in self:
            if line.product_id and line.product_uom_qty:
                if line.product_uom_qty > line.available_qty:
                    return {
                        'warning': {
                            'title': "خطأ فى الكميه",
                            'message': "الكميه المطلوبه اكبر من الكميه المتاحه."
                        }
                    }
