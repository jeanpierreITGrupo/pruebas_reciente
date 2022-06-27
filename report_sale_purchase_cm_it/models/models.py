# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class saleOrderContactChildIT(models.Model):
	_inherit = 'sale.order'

	contact_partner_childs = fields.Many2one('res.partner', 'Contacto cliente')
	tiempo_atencion = fields.Char('Tiempo de atención')
	totem_plastico = fields.Char('Tótem plástico * 1000 kg.')
	pedido_minimo = fields.Char('Pedido mínimo')

	@api.onchange('payment_term_id')
	def onchange_payment_term_id(self):
		plazos = self.env['account.payment.term'].search([])
		contado = False
		for plazo in plazos:
			cont = 0
			for line in plazo.line_ids:
				if line.days != 0 or line.days >0:
					cont += 1
			if cont == 0:
				contado = plazo            
		for sale in self:
			if sale.partner_id:
				if sale.partner_id.credit_limit <= 0 and sale.payment_term_id != contado:
					raise UserError('Lo sentimos, este cliente no tiene linea de credito, solo puede pagar al contado.')

	@api.onchange('partner_id')
	def _onchange_partner_id_contact(self):
		for sale in self:
			sale.contact_partner_childs = False

	

class saleOrderLineKgIT(models.Model):
	_inherit = 'sale.order.line'

	peso_x_kg_comp = fields.Float('Precio por kg', compute="_compute_peso_x_kg_comp")

	def _compute_peso_x_kg_comp(self):
		for record in self:
			if record.product_id.weight > 0 and record.price_unit >0 :
				record.peso_x_kg_comp = record.price_unit / record.product_id.weight
			else:
				record.peso_x_kg_comp = False