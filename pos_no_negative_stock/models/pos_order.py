from odoo import models, _
from odoo.exceptions import UserError


class PosOrder(models.Model):
    _inherit = 'pos.order'

    @classmethod
    def create_from_ui(cls, orders, draft=False):
        for order in orders:
            for line in order.get('data', {}).get('lines', []):
                line_data = line[2]
                product_id = line_data['product_id']
                qty = line_data['qty']

                product = cls.env['product.product'].browse(product_id)

                if product.type == 'product':
                    # free_qty is available in Odoo 18 via stock.quant
                    if product.free_qty < qty:
                        raise UserError(_(
                            "%s has not enough stock.", product.display_name
                        ))

        return super().create_from_ui(orders, draft)
