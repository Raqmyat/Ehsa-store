from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # إخفاء الحقل الأصلي
    location_dest_id = fields.Many2one(store=False, readonly=True)

    # الحقل الجديد Many2many
    location_dest_ids = fields.Many2many(
        'stock.location',
        'stock_picking_location_dest_rel',
        'picking_id',
        'location_id',
        string='Destination Locations',
        domain="[('usage', '=', 'internal')]",
        required=True
    )

    @api.model
    def create(self, vals):
        # لو في location_dest_id، حوّله لـ location_dest_ids
        if 'location_dest_id' in vals and vals['location_dest_id']:
            if 'location_dest_ids' not in vals:
                vals['location_dest_ids'] = [(6, 0, [vals['location_dest_id']])]
        return super(StockPicking, self).create(vals)

    def write(self, vals):
        # لو في location_dest_id، حوّله لـ location_dest_ids
        if 'location_dest_id' in vals and vals['location_dest_id']:
            if 'location_dest_ids' not in vals:
                vals['location_dest_ids'] = [(6, 0, [vals['location_dest_id']])]
        return super(StockPicking, self).write(vals)

    @api.depends('location_dest_ids')
    def _compute_location_dest_id(self):
        """للتوافق مع الكود القديم - نرجع أول location"""
        for picking in self:
            picking.location_dest_id = picking.location_dest_ids[:1] if picking.location_dest_ids else False


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def create(self, vals):
        # التعامل مع الـ moves حسب الـ destinations المتعددة
        move = super(StockMove, self).create(vals)
        if move.picking_id and move.picking_id.location_dest_ids:
            # استخدام أول destination أو عمل logic خاص
            if not move.location_dest_id:
                move.location_dest_id = move.picking_id.location_dest_ids[0]
        return move