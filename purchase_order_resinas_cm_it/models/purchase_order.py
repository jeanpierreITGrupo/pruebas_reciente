# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class purchaseOrderApproveIT(models.Model):
    _inherit = 'purchase.requisition'

    num_import_requisiton = fields.Char('Nro de Acuerto Importado')
    def action_open(self):
        res = super(purchaseOrderApproveIT,self).action_open()
        if not self.env.user.has_group('purchase_order_resinas_cm_it.group_purchase_request'):
            raise UserError('Usted no se encuentra en el grupo de aprobadores.')
        return res

class purchaseOrderActionServerIT(models.Model):
    _inherit = 'purchase.order'

    def approve_purchase_orders(self):
        if not self.env.user.has_group('purchase.group_purchase_manager'):
            raise UserError('Lo sentimos, usted no tiene permisos de Administrador para realizar esta opeación.')
        cont = 0
        for purchase in self:
            if purchase.state in ['to approve']:
                purchase.button_approve()
                cont += 1
        if cont >= 1:
            return self.env['popup.it'].get_message((u'SE APROBO CON EXITO %s SOLICITUDES DE PRESUPUESTO.')% (cont) )
        else:
            return self.env['popup.it'].get_message(u'NO SE ACTUALIZO NINGUN REGISTRO.')

