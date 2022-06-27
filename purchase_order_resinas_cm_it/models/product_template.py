# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


# class productTemplateModificationsIT(models.Model):
#     _inherit = 'product.template'

#     @api.model
#     def create(self,vals):        
#         if not self.env.user.has_group('purchase_order_resinas_cm_it.group_product_template'):
#             raise UserError('Lo sentimos, usted no puede crear ni editar productos.')
#         res = super(productTemplateModificationsIT,self).create(vals)
#         return res

#     def write(self,vals):        
#         if not self.env.user.has_group('purchase_order_resinas_cm_it.group_product_template'):
#             raise UserError('Lo sentimos, usted no puede crear ni editar productos.')
#         res = super(productTemplateModificationsIT,self).write(vals)
#         return res

#     def unlink(self):
#         if not self.env.user.has_group('purchase_order_resinas_cm_it.group_product_template'):
#             raise UserError('Lo sentimos, usted no puede crear, editar ni eliminar productos.')
#         res = super(productTemplateModificationsIT,self).unlink()        
#         return res

    
