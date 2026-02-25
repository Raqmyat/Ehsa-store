from odoo import models

class PosSession(models.Model):
    _inherit = 'pos.session'

    def get_closing_control_data(self):
        res = super().get_closing_control_data()
        has_group = self.env.user.has_group('pos_hide_closing_details.group_show_closing_details')
        res['can_show_closing_details'] = has_group
        return res
