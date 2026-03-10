from odoo import models, fields, api

class PosSession(models.Model):
    _inherit = 'pos.session'

    balance_status = fields.Char(string='الحالة', compute='_compute_balance_status', store=True)

    @api.depends('cash_register_balance_end', 'cash_register_balance_end_real')
    def _compute_balance_status(self):
        for session in self:
            if session.cash_register_balance_end == session.cash_register_balance_end_real:
                session.balance_status = 'متوازن'
            else:
                session.balance_status = 'غير متوازن'
