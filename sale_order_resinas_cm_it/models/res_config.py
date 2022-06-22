# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class res_company(models.Model):
	_inherit = 'res.company'

	tipo_credito = fields.Selection([('soles','PEN'),('dolares','USD')],'Tipo de Crédito')

class resConfigSettingsModificationsIT(models.TransientModel):
    _inherit = 'res.config.settings'

    tipo_credito = fields.Selection([('soles','PEN'),('dolares','USD')],'Tipo de Crédito',related="company_id.tipo_credito",readonly=False)

# class resPartnerModificationsIT(models.Model):
#     _inherit = 'res.partner'

#     def _get_default_tipo_credito(self):
#         res = self.env['res.config.settings'].search([], limit=1)
#         return res.tipo_credito

#     tipo_credito = fields.Selection([('soles','PEN'),('dolares','USD')],'Tipo de Crédito',default=_get_default_tipo_credito)
#     switch_modifica_credito = fields.Boolean('Puede modificar créditos', compute='_compute_switch_modifica_credito', default=True)
#     linea_credito = fields.Float('Linea de crédito')

    # def _compute_switch_modifica_credito(self):
    #     if self.env.user.has_group('sale_order_resinas_cm_it.group_partner_modify_credit'):
    #         self.switch_modifica_credito = True
    #     else:
    #         self.switch_modifica_credito = False

    # @api.model
    # def create(self,vals):
    #     res = super(resPartnerModificationsIT,self).create(vals)
    #     credito_default = self._get_default_tipo_credito()
    #     if 'tipo_credito' in vals and vals['tipo_credito'] != credito_default and not self.env.user.has_group('sale_order_resinas_cm_it.group_partner_modify_credit'):
    #         raise UserError('Lo sentimos, usted no puede modificar el Tipo de Crédito por defecto.')
    #     if 'linea_credito' in vals and vals['linea_credito'] != credito_default and not self.env.user.has_group('sale_order_resinas_cm_it.group_partner_modify_credit'):
    #         raise UserError('Lo sentimos, usted no puede modificar la Linea de Crédito.')
    #     return res
            

    
    

