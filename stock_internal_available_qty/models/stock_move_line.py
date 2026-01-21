from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class StockMove(models.Model):
    _inherit = 'stock.move'

    source_qty_available = fields.Float(
        string="الكميه المتاحه فى الموقع المصدري",
        compute="_compute_available_qty",
        store=False
    )

    dest_qty_available = fields.Float(
        string="الكميه المتاحه فى الموقع الوجهة",
        compute="_compute_available_qty",
        store=False
    )
    @api.depends('product_id', 'location_id', 'location_dest_id')
    def _compute_available_qty(self):
        Quant = self.env['stock.quant']

        for move in self:
            move.source_qty_available = 0.0
            move.dest_qty_available = 0.0

            if not move.product_id:
                continue

            if move.location_id:
                move.source_qty_available = Quant._get_available_quantity(
                    move.product_id,
                    move.location_id
                )

            if move.location_dest_id:
                move.dest_qty_available = Quant._get_available_quantity(
                    move.product_id,
                    move.location_dest_id
                )




