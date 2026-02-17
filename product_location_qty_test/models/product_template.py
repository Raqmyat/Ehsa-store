from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    qty_main_stock = fields.Float(
        string='رئيسي/Stock',
        compute='_compute_location_qty',
        store=False
    )
    qty_roshdy_stock = fields.Float(
        string='رشدية/Stock',
        compute='_compute_location_qty',
        store=False
    )
    qty_ghasany_stock = fields.Float(
        string='غساني/Stock',
        compute='_compute_location_qty',
        store=False
    )
    qty_nozha_stock = fields.Float(
        string='نزهة/Stock',
        compute='_compute_location_qty',
        store=False
    )

    def _compute_location_qty(self):
        Quant = self.env['stock.quant']
        locations = {
            'qty_main_stock': 'رئيسي/Stock',
            'qty_roshdy_stock': 'رشدية/Stock',
            'qty_ghasany_stock': 'غساني/Stock',
            'qty_nozha_stock': 'نزهة/Stock',
        }

        for product in self:
            for field_name, location_name in locations.items():
                qty = 0.0
                location = self.env['stock.location'].search(
                    [('complete_name', '=', location_name)],
                    limit=1
                )
                if location:
                    quants = Quant.search([
                        ('product_id.product_tmpl_id', '=', product.id),
                        ('location_id', '=', location.id),
                    ])
                    qty = sum(quants.mapped('quantity'))

                product[field_name] = qty
