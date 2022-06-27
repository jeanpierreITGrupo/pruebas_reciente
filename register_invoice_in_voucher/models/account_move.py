# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AccountMove(models.Model):
	_inherit = 'account.move'
	
	def _post(self, soft=True):
		res = super(AccountMove,self)._post(soft=soft)
		for move in self:
			if move.move_type in ['out_invoice', 'in_invoice', 'out_refund', 'in_refund']:
				if move.move_type in ['out_invoice', 'out_refund'] and not move.ref:
					move.ref = move.name.split( )[1] if move.name[:2] in ('F ','N ') else move.name
				for line in move.line_ids:
					#if not line.is_advance_check:
					if not line.type_document_id:
						line.type_document_id = move.l10n_latam_document_type_id.id or None
					if not line.nro_comp:
						line.nro_comp = move.ref or None
		return res