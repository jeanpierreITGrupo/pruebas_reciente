# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class AccountPayment(models.Model):
	_inherit = 'account.payment'

	@api.onchange('date','currency_id')
	def _get_currency_rate(self):
		if not self.is_personalized_change:
			cu_rate = self.env['res.currency.rate'].search([('name','=',self.date),('company_id','=',self.company_id.id)],limit=1)
			if cu_rate:
				self.write({'type_change': cu_rate.sale_type})

class AccountPaymentRegister(models.TransientModel):
	_inherit = 'account.payment.register'

	@api.onchange('payment_date','currency_id')
	def _get_currency_rate(self):
		if not self.is_personalized_change:
			cu_rate = self.env['res.currency.rate'].search([('name','=',self.payment_date),('company_id','=',self.company_id.id)],limit=1)
			if cu_rate:
				self.type_change = cu_rate.sale_type