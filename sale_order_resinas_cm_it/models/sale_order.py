# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class saleOrderModificationsIT(models.Model):
	_inherit = 'sale.order'

	commitment_date = fields.Datetime(track_visibility="onchange")
	state = fields.Selection([
		('draft', 'Quotation'),
		('sent', 'Quotation Sent'),
		('to approve', 'Por aprobar'),
		('sale', 'Sales Order'),
		('done', 'Locked'),
		('cancel', 'Cancelled'),
		])
	margin_error = fields.Boolean('Cotizacion no cumple margen', compute="_margin_error")
	sale_line_cero_error = fields.Boolean('Productos con costo cero', compute="_sale_line_cero_error")
	margin_sale_compute = fields.Char('Margen configurado', compute='_compute_margin_sale')
	edit_margin_group = fields.Char('Edicion de costo en lineas', compute='_compute_margin_sale_2')
	

	def _compute_edit_margin_group(self):
		for sale in self:
			if self.user_has_groups('sale_order_resinas_cm_it.group_sale_line_edit_costo'):
				sale.edit_margin_group = 'True'
			else:
				sale.edit_margin_group = False
			print('cabecera funciona')

	def _compute_margin_sale(self):
		margin = self.env['margin.sale'].search([])
		for sale in self:
			if self.user_has_groups('sale_order_resinas_cm_it.group_sale_line_edit_costo'):
				sale.edit_margin_group = 'True'
			else:
				sale.edit_margin_group = False
			if margin:
				sale.margin_sale_compute = '(márgen establecido: ' + str(margin[0].margin) + '%)'
			else:
				sale.margin_sale_compute =  False
			print('siempre', sale.edit_margin_group) 

	def _compute_margin_sale_2(self):
		margin = self.env['margin.sale'].search([])
		for sale in self:
			if margin:
				sale.edit_margin_group = '(márgen establecido: ' + str(margin[0].margin) + '%)'
			else:
				sale.edit_margin_group =  False
			print('siempre2') 


	def _sale_line_cero_error(self):
		for sale in self:
			nro_incumple = 0
			if sale.order_line:
				for linea in sale.order_line:
					if linea.product_id.standard_price <= 0:
						nro_incumple += 1
			if nro_incumple > 0:
				sale.sale_line_cero_error = True
			else:
				sale.sale_line_cero_error = False

	def _margin_error(self):
		for sale in self:
			margen_establecido = self.env['margin.sale'].search([])
			# sale._compute_margin()
			if margen_establecido  and sale.margin_percent*100 <= margen_establecido[0].margin:
				sale.margin_error = True
			else:
				sale.margin_error = False

	def action_confirm(self):
		res = super(saleOrderModificationsIT, self).action_confirm()
		if not self.commitment_date:
			raise UserError('El campo Fecha de entrega, es obligatorio.')
		return res

	def action_confirm_to_approve(self):
		if not self.commitment_date:
			raise UserError('El campo Fecha de entrega, es obligatorio.')
		if self.sale_line_cero_error or self.margin_error:
			if self.env.user.has_group('sale_order_resinas_cm_it.group_sale_order_approve'):
				self.action_confirm()
			else:
				self.state = 'to approve'
		else:
			self.action_confirm()

	def action_approve(self):
		self.action_confirm()

	def action_disapprove(self):
		self.state = 'draft'

class marginSaleIT(models.Model):
	_name = 'margin.sale'

	name = fields.Char('Nombre')
	margin = fields.Float('Margen establecido %')

class saleOrderLineEditCostoIT(models.Model):  
	_inherit = 'sale.order.line'

	edit_margin_group = fields.Boolean('Edicion de costo en lineas', compute="_compute_edit_margin_group")


	@api.depends('order_id')
	def _compute_edit_margin_group(self):
		for sale in self:
			if self.user_has_groups('sale_order_resinas_cm_it.group_sale_line_edit_costo'):
				sale.edit_margin_group = True
			else:
				sale.edit_margin_group = False
			print('linea funciona', sale.edit_margin_group)