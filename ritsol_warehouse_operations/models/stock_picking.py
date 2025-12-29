from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    location_dest_ids = fields.Many2many(
        'stock.location',
        'stock_picking_location_dest_rel',
        'picking_id',
        'location_id',
        string='Destination Locations',
        domain="[('usage', '=', 'internal')]"
    )

    @api.model
    def create(self, vals):
        # نقل القيمة من location_dest_id إلى location_dest_ids
        if 'location_dest_id' in vals and vals.get('location_dest_id'):
            if 'location_dest_ids' not in vals or not vals.get('location_dest_ids'):
                vals['location_dest_ids'] = [(6, 0, [vals['location_dest_id']])]
        return super(StockPicking, self).create(vals)

    def write(self, vals):
        # نقل القيمة من location_dest_id إلى location_dest_ids
        if 'location_dest_id' in vals and vals.get('location_dest_id'):
            if 'location_dest_ids' not in vals:
                vals['location_dest_ids'] = [(6, 0, [vals['location_dest_id']])]
        return super(StockPicking, self).write(vals)

    def button_validate(self):
        """Override للـ validation"""
        for picking in self:
            if picking.location_dest_ids:
                # تحديث الحقل الأصلي بأول location
                picking.sudo().write({
                    'location_dest_id': picking.location_dest_ids[0].id
                })
                # تحديث كل الـ moves
                for move in picking.move_ids:
                    move.location_dest_id = picking.location_dest_ids[0].id

        return super(StockPicking, self).button_validate()