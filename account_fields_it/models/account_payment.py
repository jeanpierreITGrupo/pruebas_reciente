# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class AccountPayment(models.Model):
	_inherit = 'account.payment'

	cash_flow_id = fields.Many2one('account.cash.flow',string='Flujo de Caja')
	catalog_payment_id = fields.Many2one('einvoice.catalog.payment',string='Medio de Pago')
	type_doc_cash_id = fields.Many2one('l10n_latam.document.type',string='Tipo Documento Caja')
	cash_nro_comp = fields.Char(string='Nro. de Op. Caja',size=42)
	type_document_id = fields.Many2one('l10n_latam.document.type',string='Tipo Documento')
	nro_comp = fields.Char(string='Nro. Comprobante')
	is_personalized_change = fields.Boolean(string='T.C. Personalizado',default=False)
	type_change = fields.Float(string='Tipo de Cambio',digits=(12,4),default=1)
	manual_batch_payment_id = fields.Many2one('account.batch.payment',string='Lote de Pago')
class AccountPaymentRegister(models.TransientModel):
	_inherit = 'account.payment.register'

	cash_flow_id = fields.Many2one('account.cash.flow',string='Flujo de Caja')
	catalog_payment_id = fields.Many2one('einvoice.catalog.payment',string='Medio de Pago')
	type_doc_cash_id = fields.Many2one('l10n_latam.document.type',string='Tipo Documento Caja')
	cash_nro_comp = fields.Char(string='Nro. de Op. Caja',size=42)
	type_document_id = fields.Many2one('l10n_latam.document.type',string='Tipo Documento')
	nro_comp = fields.Char(string='Nro. Comprobante')
	is_personalized_change = fields.Boolean(string='T.C. Personalizado',default=False)
	type_change = fields.Float(string='Tipo de Cambio',digits=(12,4),default=1)
	manual_batch_payment_id = fields.Many2one('account.batch.payment',string='Lote de Pago')

	#@api.depends('line_ids')
	#def _compute_type_document_id(self):
	#	for wizard in self:
	#		l10n_latam_document_type_id = wizard.line_ids.move_id.mapped('l10n_latam_document_type_id')
	#		wizard.type_document_id = l10n_latam_document_type_id if len(l10n_latam_document_type_id) == 1 else None

	#@api.depends('line_ids')
	#def _compute_nro_comp(self):
	#	for wizard in self:
	#		move_id = wizard.line_ids.mapped('move_id')
	#		wizard.nro_comp = move_id.ref if len(move_id) == 1 else None