from odoo import models

class PosSession(models.Model):
    _inherit = 'pos.session'

    def get_closing_control_data(self):
        res = super().get_closing_control_data()
        has_group = self.env.user.has_group('pos_hide_closing_details.group_show_closing_details')
        
        # Backend Blind Count: Zero out sensitive data if no group
        if not has_group:
            if 'orders_details' in res:
                res['orders_details']['amount'] = 0.0
            if 'default_cash_details' in res:
                res['default_cash_details']['amount'] = 0.0
                res['default_cash_details']['opening'] = 0.0
                res['default_cash_details']['payment_amount'] = 0.0
            if 'non_cash_payment_methods' in res:
                for pm in res['non_cash_payment_methods']:
                    pm['amount'] = 0.0
            
        res['can_show_closing_details'] = has_group
        return res
