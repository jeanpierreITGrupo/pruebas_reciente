# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import *
from odoo.exceptions import UserError
import base64

from io import BytesIO
import re
import uuid

class AccountBookHonoraryWizard(models.TransientModel):
	_name = 'account.book.honorary.wizard'
	_description = 'Account Book Honorary Wizard'

	name = fields.Char()
	company_id = fields.Many2one('res.company',string=u'Compañia',required=True, default=lambda self: self.env.company,readonly=True)
	fiscal_year_id = fields.Many2one('account.fiscal.year',string=u'Ejercicio',required=True)
	date_from = fields.Date(string=u'Fecha Inicial',required=True)
	date_to = fields.Date(string=u'Fecha Final',required=True)
	type_show =  fields.Selection([('pantalla','Pantalla'),('excel','Excel')],string=u'Mostrar en',default='pantalla')
	type_date =  fields.Selection([('date','Fecha Contable'),('invoice_date_due','Fecha de Vencimiento')],string=u'Mostrar en base a', required=True, default='date')

	@api.onchange('company_id')
	def get_fiscal_year(self):
		if self.company_id:
			today = fields.Date.context_today(self)
			fiscal_year = self.env['account.fiscal.year'].search([('name','=',str(today.year))],limit=1)
			if fiscal_year:
				self.fiscal_year_id = fiscal_year.id
				self.date_from = fiscal_year.date_from
				self.date_to = fiscal_year.date_to

	def get_report(self):
		
		if self.type_show == 'pantalla':
			self.env.cr.execute("""CREATE OR REPLACE view account_book_honorary_view as (SELECT row_number() OVER () AS id, T.* FROM ("""+self._get_sql(self.date_from,self.date_to,self.company_id.id,self.type_date)+""")T)""")

			return {
				'name': 'Libro de Honorarios',
				'type': 'ir.actions.act_window',
				'res_model': 'account.book.honorary.view',
				'view_mode': 'tree',
				'view_type': 'form',
			}

		if self.type_show == 'excel':
			return self.get_excel()

	def get_excel(self):
		import io
		from xlsxwriter.workbook import Workbook

		ReportBase = self.env['report.base']
		direccion = self.env['account.main.parameter'].search([('company_id','=',self.company_id.id)],limit=1).dir_create_file

		if not direccion:
			raise UserError(u'No existe un Directorio Exportadores configurado en Parametros Principales de Contabilidad para su Compañía')

		workbook = Workbook(direccion +'Libros_de_Honorarios.xlsx')
		workbook, formats = ReportBase.get_formats(workbook)

		import importlib
		import sys
		importlib.reload(sys)

		##########LIBROS DE HONORARIOS############
		worksheet = workbook.add_worksheet("LIBROS DE HONORARIOS")
		worksheet.set_tab_color('blue')
		
		worksheet = ReportBase.get_headers(worksheet,self.get_header(),0,0,formats['boldbord'])
		self.env.cr.execute(self._get_sql(self.date_from,self.date_to,self.company_id.id,self.type_date))
		res = self.env.cr.dictfetchall()
		x=1

		renta = retencion = neto_p = 0

		for line in res:
			worksheet.write(x,0,line['periodo'] if line['periodo'] else '',formats['especial1'])
			worksheet.write(x,1,line['libro'] if line['libro'] else '',formats['especial1'])
			worksheet.write(x,2,line['voucher'] if line['voucher'] else '',formats['especial1'])
			worksheet.write(x,3,line['fecha_e'] if line['fecha_e'] else '',formats['dateformat'])
			worksheet.write(x,4,line['fecha_p'] if line['fecha_p'] else '',formats['dateformat'])
			worksheet.write(x,5,line['td'] if line['td'] else '',formats['especial1'])
			worksheet.write(x,6,line['serie'] if line['serie'] else '',formats['especial1'])
			worksheet.write(x,7,line['numero'] if line['numero'] else '',formats['especial1'])
			worksheet.write(x,8,line['tdp'] if line['tdp'] else '',formats['especial1'])
			worksheet.write(x,9,line['docp'] if line['docp'] else '',formats['especial1'])
			worksheet.write(x,10,line['apellido_p'] if line['apellido_p'] else '',formats['especial1'])
			worksheet.write(x,11,line['apellido_m'] if line['apellido_m'] else '',formats['especial1'])
			worksheet.write(x,12,line['namep'] if line['namep'] else '',formats['especial1'])
			worksheet.write(x,13,line['divisa'] if line['divisa'] else '',formats['especial1'])
			worksheet.write(x,14,line['tipo_c'] if line['tipo_c'] else '0.0000',formats['numbercuatro'])
			worksheet.write(x,15,line['renta'] if line['renta'] else '0.00',formats['numberdos'])
			worksheet.write(x,16,line['retencion'] if line['retencion'] else '0.00',formats['numberdos'])
			worksheet.write(x,17,line['neto_p'] if line['neto_p'] else '0.00',formats['numberdos'])
			worksheet.write(x,18,line['periodo_p'] if line['periodo_p'] else '',formats['especial1'])
			worksheet.write(x,19,line['is_not_home'] if line['is_not_home'] else '',formats['especial1'])
			renta += line['renta'] if line['renta'] else 0
			retencion += line['retencion'] if line['retencion'] else 0
			neto_p += line['neto_p'] if line['neto_p'] else 0
			x += 1
		
		worksheet.write(x,15,renta,formats['numbertotal'])
		worksheet.write(x,16,retencion,formats['numbertotal'])
		worksheet.write(x,17,neto_p,formats['numbertotal'])

		widths = [9,7,11,9,9,4,5,10,4,11,10,10,15,5,7,12,12,12,9,15]
		worksheet = ReportBase.resize_cells(worksheet,widths)
		workbook.close()

		f = open(direccion +'Libros_de_Honorarios.xlsx', 'rb')

		return self.env['popup.it'].get_file('RH%s.xlsx'%(self.company_id.partner_id.vat),base64.encodestring(b''.join(f.readlines())))
	
	def get_header(self):
		HEADERS = ['PERIODO','LIBRO','VOUCHER','FECHA E','FECHA P','TD','SERIE','NUMERO','TDP','RUC','AP. PATERNO',
				   'AP. MATERNO','NOMBRES','DIVISA','TC','RENTA','RETENCION','NETO P','PERIODO P','NO DOMICILIADO']
		return HEADERS

	def _get_sql(self,x_date_ini,x_date_end,x_company_id,x_date_type):

		sql = """select
			tt.periodo::character varying,
			tt.libro,
			tt.voucher,
			tt.fecha_e,
			tt.fecha_p,
			tt.td,
			tt.serie,
			tt.numero,
			tt.tdp,
			tt.docp,
			tt.apellido_p,
			tt.apellido_m,
			tt.namep,
			tt.divisa,
			tt.tipo_c,
			tt.renta,
			tt.retencion,
			tt.neto_p,
			tt.periodo_p,
			tt.is_not_home
			from get_recxhon_1_1('%s','%s',%d,'%s') tt
		""" % (x_date_ini.strftime('%Y/%m/%d'),x_date_end.strftime('%Y/%m/%d'),x_company_id,x_date_type)
		return sql

	def domain_dates(self):
		if self.date_from:
			if self.fiscal_year_id.date_from.year != self.date_from.year:
				raise UserError("La fecha inicial no esta en el rango del Año Fiscal escogido (Ejercicio).")
		if self.date_to:
			if self.fiscal_year_id.date_from.year != self.date_to.year:
				raise UserError("La fecha final no esta en el rango del Año Fiscal escogido (Ejercicio).")
		if self.date_from and self.date_to:
			if self.date_to < self.date_from:
				raise UserError("La fecha final no puede ser menor a la fecha inicial.")