from odoo import models

class PosSession(models.Model):
    _inherit = 'pos.session'

    def get_closing_control_data(self):
        res = super().get_closing_control_data()
        res['can_show_closing_details'] = self.env.user.has_group('pos_hide_closing_details.group_show_closing_details')
        return res
