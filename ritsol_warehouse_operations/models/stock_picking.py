from odoo import models, fields, api
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    location_dest_ids = fields.Many2many(
        'stock.location',
        'stock_picking_multi_dest_rel',
        'picking_id',
        'location_id',
        string='Destination Locations',
        domain=[('usage', '=', 'internal')],
    )

    def button_validate(self):
        """
        Create one stock.move per destination location
        """
        for picking in self:
            if picking.location_dest_ids:
                moves = picking.move_ids_without_package
                if not moves:
                    continue

                dest_count = len(picking.location_dest_ids)
                if dest_count == 0:
                    continue

                # create new moves
                for location in picking.location_dest_ids:
                    for move in moves:
                        self.env['stock.move'].create({
                            'name': move.name,
                            'product_id': move.product_id.id,
                            'product_uom': move.product_uom.id,
                            'product_uom_qty': move.product_uom_qty / dest_count,
                            'location_id': move.location_id.id,
                            'location_dest_id': location.id,
                            'picking_id': picking.id,
                        })

                # remove original moves
                moves.unlink()

        return super().button_validate()
