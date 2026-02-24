from odoo import models, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        if 'qty_available' not in fields:
            fields.append('qty_available')
        if 'free_qty' not in fields:
            fields.append('free_qty')
        return fields

    def _load_pos_data(self, data):
        """
        Injects warehouse into context for stock field computation.
        """
        config_id = data['pos.config']['data'][0]['id']
        config = self.env['pos.config'].browse(config_id)
        warehouse_id = config.picking_type_id.warehouse_id.id
        
        self = self.with_context(
            warehouse_id=warehouse_id,
            warehouse=warehouse_id,
        )
        
        return super()._load_pos_data(data)
