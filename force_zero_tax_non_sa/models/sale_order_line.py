
from odoo import models, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def create(self, vals):
        line = super().create(vals)
        if not self.env.context.get('skip_tax_fix'):
            line.with_context(skip_tax_fix=True)._set_tax_by_country()
        return line

    def write(self, vals):
        res = super().write(vals)
        if not self.env.context.get('skip_tax_fix'):
            self.with_context(skip_tax_fix=True)._set_tax_by_country()
        return res

    def _set_tax_by_country(self):
        # ضريبة صفرية للعملاء خارج السعودية
        zero_tax = self.env['account.tax'].search([
            ('amount', '=', 0),
            ('type_tax_use', '=', 'sale'),
            ('company_id', '=', self.company_id.id)
        ], limit=1)

        # ضريبة 15% للعملاء داخل السعودية
        sa_tax = self.env['account.tax'].search([
            ('amount', '=', 15),
            ('type_tax_use', '=', 'sale'),
            ('company_id', '=', self.company_id.id)
        ], limit=1)

        for line in self:
            partner = line.order_id.partner_shipping_id or line.order_id.partner_id
            if not partner.country_id:
                continue

            if partner.country_id.code == 'SA':
                # العميل من السعودية → 15%
                if sa_tax and line.tax_id != sa_tax:
                    line.write({'tax_id': [(6, 0, sa_tax.ids)]})
                elif not sa_tax:
                    line.write({'tax_id': False})
            else:
                # العميل من خارج السعودية → 0%
                if zero_tax and line.tax_id != zero_tax:
                    line.write({'tax_id': [(6, 0, zero_tax.ids)]})
                elif not zero_tax:
                    line.write({'tax_id': False})

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def write(self, vals):
        res = super().write(vals)
        # لو العميل اتغير نحدث الضريبة لكل الأسطر
        if 'partner_id' in vals or 'partner_shipping_id' in vals:
            for line in self.order_line:
                line.with_context(skip_tax_fix=True)._set_tax_by_country()
        return res