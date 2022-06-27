# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class AccountMove(models.Model):
	_inherit = 'account.move'
	
	@api.depends('company_id', 'invoice_filter_type_domain')
	def _compute_suitable_journal_ids(self):
		for m in self:
			journal_type = m.invoice_filter_type_domain
			company_id = m.company_id.id or self.env.company.id
			if journal_type:
				domain = [('company_id', '=', company_id), ('type', '=', journal_type)]
			else:
				domain = [('company_id', '=', company_id)]
			m.suitable_journal_ids = self.env['account.journal'].search(domain)
	
	def _post(self, soft=True):
		for move in self:
			if move.move_type != 'entry':
				filtered_line = move.line_ids.filtered(lambda l: not l.display_type and l.debit==0 and l.credit==0 and l.amount_currency == 0 and not l.tax_tag_ids)
				filtered_line.unlink()
		to_post = super(AccountMove,self)._post(soft=soft)
		return to_post
	
	@api.model_create_multi
	def create(self, vals_list):
		rslt = super(AccountMove, self).create(vals_list)
		rslt.name = "/"
		return rslt