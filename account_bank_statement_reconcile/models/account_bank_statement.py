# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountBankStatementLine(models.Model):
	_inherit = 'account.bank.statement.line'

	@api.model
	def _prepare_counterpart_move_line_vals(self, counterpart_vals, move_line=None):
		data = super(AccountBankStatementLine,self)._prepare_counterpart_move_line_vals(counterpart_vals=counterpart_vals,move_line=move_line)
		if move_line:
			data['nro_comp'] = move_line.nro_comp
			data['type_document_id'] = move_line.type_document_id.id
		return data
	
	@api.model
	def _prepare_liquidity_move_line_vals(self):
		data = super(AccountBankStatementLine,self)._prepare_liquidity_move_line_vals()
		data['nro_comp'] = self.ref
		data['type_document_id'] = self.type_document_id.id
		return data
	
	@api.model_create_multi
	def create(self, vals_list):
		st_lines = super(AccountBankStatementLine,self).create(vals_list)
		for st_line in st_lines:
			st_line.move_id.write({'glosa':st_line.payment_ref})
			st_line.move_id.write({'td_payment_id':st_line.catalog_payment_id.id})
		return st_lines
	
	def _synchronize_to_moves(self, changed_fields):
		res = super(AccountBankStatementLine,self)._synchronize_to_moves(changed_fields = changed_fields)
		if self._context.get('skip_account_move_synchronization'):
			return
		if not any(field_name in changed_fields for field_name in (
			 'payment_ref','catalog_payment_id','type_document_id'
		)):
			return
		for st_line in self.with_context(skip_account_move_synchronization=True):
			st_line.move_id.write({
				'td_payment_id': st_line.catalog_payment_id.id or None,
				'glosa': st_line.payment_ref,
				'l10n_latam_document_type_id': st_line.type_document_id.id or None
			})
		return res

class AccountBankStatement(models.Model):
	_inherit = 'account.bank.statement'

	def button_post(self):
		self.write({'balance_end_real': self.balance_end})
		res = super(AccountBankStatement,self).button_post()
		return res