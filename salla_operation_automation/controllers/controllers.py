# -*- coding: utf-8 -*-
# from odoo import http


# class SallaOperationAutomation(http.Controller):
#     @http.route('/salla_operation_automation/salla_operation_automation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/salla_operation_automation/salla_operation_automation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('salla_operation_automation.listing', {
#             'root': '/salla_operation_automation/salla_operation_automation',
#             'objects': http.request.env['salla_operation_automation.salla_operation_automation'].search([]),
#         })

#     @http.route('/salla_operation_automation/salla_operation_automation/objects/<model("salla_operation_automation.salla_operation_automation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('salla_operation_automation.object', {
#             'object': obj
#         })

