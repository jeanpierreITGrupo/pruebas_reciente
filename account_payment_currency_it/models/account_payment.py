# -*- coding: utf-8 -*-

from odoo import api, models, fields, tools
from odoo.exceptions import UserError


class AccountPayment(models.Model):
	_inherit = "account.payment"

	def personalize_currency_rate(self):
		for pay in self:
			pay.move_id.write({'currency_rate': pay.type_change})
			pay.paired_internal_transfer_payment_id.move_id.write({'currency_rate': pay.type_change})
			pay.paired_internal_transfer_payment_id.write({'type_change': pay.type_change})
			pay.paired_internal_transfer_payment_id.write({'is_personalized_change': True})
			if not pay.destination_journal_id.currency_id:
				pay.paired_internal_transfer_payment_id.move_id.write({'currency_id': pay.company_id.currency_id.id})
			else:
				pay.paired_internal_transfer_payment_id.move_id.write({'currency_id': pay.destination_journal_id.currency_id.id})

			if pay.journal_id.currency_id or pay.destination_journal_id.currency_id:
				for line in (pay.move_id.line_ids+pay.paired_internal_transfer_payment_id.move_id.line_ids):
					line.write({'tc': pay.type_change})
					if line.currency_id.id == pay.company_id.currency_id.id:
						currency_id = pay.journal_id.currency_id or pay.destination_journal_id.currency_id
						if line.debit>0:
							self.env.cr.execute("UPDATE account_move_line SET amount_currency = %s, currency_id = %d WHERE id = %d" % (str(round(pay.amount/pay.type_change,2)),currency_id.id,line.id))
						if line.credit>0:
							self.env.cr.execute("UPDATE account_move_line SET amount_currency = %s, currency_id = %d WHERE id = %d" % (str(round(pay.amount/pay.type_change,2)*-1),currency_id.id,line.id))
				
				if pay.currency_id.id != pay.company_id.currency_id.id:
					self.env.cr.execute("UPDATE account_move_line SET debit = "+str(round(pay.amount*pay.type_change,2))+" WHERE amount_currency>0 and payment_id in (%d,%d)"%(pay.id,pay.paired_internal_transfer_payment_id.id))
					self.env.cr.execute("UPDATE account_move_line SET credit = "+str(round(pay.amount*pay.type_change,2))+" WHERE amount_currency<0 and payment_id in (%d,%d)"%(pay.id,pay.paired_internal_transfer_payment_id.id))
					self.env.cr.execute("UPDATE account_move_line SET balance = (coalesce(debit,0) - coalesce(credit,0)) WHERE payment_id in (%d,%d)"%(pay.id,pay.paired_internal_transfer_payment_id.id))