# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields, _
from dateutil.relativedelta import relativedelta
from odoo.tools import float_is_zero

class ReportAccountAgedPartner(models.AbstractModel):
	_inherit = "account.aged.partner"

	def _format_id_line(self, res, value_dict, options):
		res['name'] = value_dict['move_ref']
		res['title_hover'] = value_dict['move_ref']
		res['caret_options'] = 'account.payment' if value_dict.get('payment_id') else 'account.move'
		for col in res['columns']:
			if col.get('no_format') == 0:
				col['name'] = ''
		res['columns'][-1]['name'] = ''