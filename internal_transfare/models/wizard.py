from odoo import models, fields, api
from odoo.exceptions import UserError


class MultiLocationTransferWizard(models.TransientModel):
    _name = 'multi.location.transfer.wizard'
    _description = 'Multi Location Internal Transfer'

    product_id = fields.Many2one(
        'product.product',
        required=True
    )

    source_location_id = fields.Many2one(
        'stock.location',
        domain=[('usage', '=', 'internal')],
        required=True
    )

    source_qty_available = fields.Float(
        string="Source Available Qty",
        compute="_compute_source_qty",
        readonly=True
    )

    line_ids = fields.One2many(
        'multi.location.transfer.line',
        'wizard_id',
        string='Destination Lines',
        required=True
    )

    @api.depends('product_id', 'source_location_id')
    def _compute_source_qty(self):
        for wizard in self:
            if wizard.product_id and wizard.source_location_id:
                wizard.source_qty_available = wizard.product_id.with_context(
                    location=wizard.source_location_id.id
                ).qty_available
            else:
                wizard.source_qty_available = 0.0

    def action_confirm(self):
        self.ensure_one()

        if not self.line_ids:
            raise UserError("Please add at least one destination location.")

        picking_type = self.env['stock.picking.type'].search(
            [('code', '=', 'internal')], limit=1
        )

        if not picking_type:
            raise UserError("Internal transfer picking type not found.")

        total_qty = sum(self.line_ids.mapped('quantity'))
        if total_qty <= 0:
            raise UserError("Total quantity must be greater than zero.")

        if total_qty > self.source_qty_available:
            raise UserError("Not enough quantity in source location.")

        picking = self.env['stock.picking'].create({
            'picking_type_id': picking_type.id,
            'location_id': self.source_location_id.id,
            'location_dest_id': self.line_ids[0].destination_location_id.id,
        })

        for line in self.line_ids:
            if line.quantity <= 0:
                continue

            self.env['stock.move'].create({
                'name': self.product_id.display_name,
                'product_id': self.product_id.id,
                'product_uom': self.product_id.uom_id.id,
                'product_uom_qty': line.quantity,
                'location_id': self.source_location_id.id,
                'location_dest_id': line.destination_location_id.id,
                'picking_id': picking.id,
            })

        picking.action_confirm()
        picking.action_assign()

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'view_mode': 'form',
            'res_id': picking.id,
        }


class MultiLocationTransferLine(models.TransientModel):
    _name = 'multi.location.transfer.line'
    _description = 'Multi Location Transfer Line'

    wizard_id = fields.Many2one(
        'multi.location.transfer.wizard',
        required=True,
        ondelete='cascade'
    )

    destination_location_id = fields.Many2one(
        'stock.location',
        domain=[('usage', '=', 'internal')],
        required=True
    )

    quantity = fields.Float(required=True)

    destination_qty_available = fields.Float(
        string="Available Qty",
        compute="_compute_destination_qty",
        readonly=True
    )

    @api.depends('wizard_id.product_id', 'destination_location_id')
    def _compute_destination_qty(self):
        for line in self:
            if line.wizard_id.product_id and line.destination_location_id:
                line.destination_qty_available = line.wizard_id.product_id.with_context(
                    location=line.destination_location_id.id
                ).qty_available
            else:
                line.destination_qty_available = 0.0
