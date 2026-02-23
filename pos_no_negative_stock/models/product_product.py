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

    def _load_product_with_domain(self, domain, config_id, load_archived=False):
        config = self.env['pos.config'].browse(config_id)
        context = {
            **self.env.context,
            'display_default_code': False,
            'active_test': not load_archived,
            'bin_size': True,
            'warehouse_id': config.warehouse_id.id,
            'is_storable': True,
        }
        return self.with_context(context).search_read(
            domain,
            self._load_pos_data_fields(config_id),
            order='sequence,default_code,name',
            load=False)
