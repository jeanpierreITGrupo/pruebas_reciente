# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class AccountJournal(models.Model):
	_inherit = 'account.journal'

	register_sunat = fields.Selection([('1','Compras'),
								('2','Ventas'),
								('3','Honorarios'),
								('4','Retenciones'),
								('5','Percepciones'),
								('6','No Deducibles')],string='Registro Sunat')
	sequence_id_it = fields.Many2one('ir.sequence', string='Secuencia del Asiento', copy=False)
	voucher_edit = fields.Boolean(string=u'Editar Número Asiento', default=False)
	check_surrender = fields.Boolean(string=u'Se usa para Rendiciones',default=False)