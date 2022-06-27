# -*- coding: utf-8 -*-
# from odoo import http


# class ModuloStandarIt(http.Controller):
#     @http.route('/modulo_standar_it/modulo_standar_it/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/modulo_standar_it/modulo_standar_it/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('modulo_standar_it.listing', {
#             'root': '/modulo_standar_it/modulo_standar_it',
#             'objects': http.request.env['modulo_standar_it.modulo_standar_it'].search([]),
#         })

#     @http.route('/modulo_standar_it/modulo_standar_it/objects/<model("modulo_standar_it.modulo_standar_it"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('modulo_standar_it.object', {
#             'object': obj
#         })
