# -*- coding: utf-8 -*-

import time
from datetime import datetime
import tempfile
import binascii
import xlrd
import openpyxl

from datetime import date, datetime
from odoo.exceptions import Warning, UserError
from odoo.osv import osv
from odoo import models, fields, exceptions, api, _
import logging
_logger = logging.getLogger(__name__)
import io
try:
	import csv
except ImportError:
	_logger.debug('Cannot `import csv`.')
try:
	import xlwt
except ImportError:
	_logger.debug('Cannot `import xlwt`.')
try:
	import cStringIO
except ImportError:
	_logger.debug('Cannot `import cStringIO`.')
try:
	import base64
except ImportError:
	_logger.debug('Cannot `import base64`.')

class ImportPurchaseRequisition(models.TransientModel):
	_name = 'import.purchase.requisition'

	document_file = fields.Binary(string='Excel')
	name_file = fields.Char(string='Nombre de Archivo')
	currency_id = fields.Many2one('res.currency', related='pricelist_id.currency_id')
	pricelist_id = fields.Many2one('product.pricelist','Lista de precios')

	def import_requisition(self):
		if not self.document_file:
			raise UserError('Tiene que cargar un archivo.')
		try:
			fp = tempfile.NamedTemporaryFile(delete= False,suffix=".xlsx")
			fp.write(binascii.a2b_base64(self.document_file))
			fp.seek(0)
			workbook = xlrd.open_workbook(fp.name)
			sheet1 = workbook.sheet_by_index(0)
			move_ids = []
		except:
			raise UserError(_("Archivo invalido!"))

		for row_no in range(sheet1.nrows):
			if row_no < 1:
				continue
			else:
				requisition_line = self.env['purchase.requisition.line']
				requisition = self.env['purchase.requisition']
				line = list(map(lambda row:isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value), sheet1.row(row_no)))
				if len(line) == 11:

					nro_acuerdo = self.env['purchase.requisition'].search([('num_import_requisiton','=',line[0])])
					moneda = self.env['res.currency'].search([('name','=',line[10])])
					cuenta = self.env['account.analytic.account'].search([('name','=',line[9])])
					print(222,line[10])
					if not moneda:
						raise UserError('Una de las lineas no tiene moneda. Agréguela por favor!')
					if nro_acuerdo:
						### YA EXISTE ACUERDO, NO SE CREA CABECERA ###
						# CREANDO LINEAS
						producto_id = self.env['product.template'].search([('default_code','=',line[5])])
						if not producto_id:
							raise UserError((u'No existe el siguiente producto: "%s"') % (line[5]))
						# date_string10=None
						# if line[10] != '':
						# 	a10 = int(float(line[10]))
						# 	a10_as_datetime = datetime(*xlrd.xldate_as_tuple(a10, workbook.datemode))
						# 	date_string10 = a10_as_datetime.date().strftime('%Y-%m-%d')
						linea = self.env['purchase.requisition.line'].create({
							'requisition_id': nro_acuerdo.id,
							'product_id':producto_id.id,
							'product_description_variants':line[6],
							'product_qty':line[7],
							# 'qty_ordered':line[9],
							# 'schedule_date':date_string10,
							'price_unit':line[8],
							'account_analytic_id':cuenta.id
						})
						# nro_acuerdo.update({'line_ids':(4,0, linea.id)})
					else:
						### NO EXISTE ACUERDO, SE CREA CABECERA ###
						# CREACION DE CABECERA
						partner_id = self.env['res.partner'].search([('name','=',line[1])])
						if line[1] != '':							
							if not partner_id:
								raise UserError((u'No existe el cliente: "%s"') % (line[1]))
						date_string2=None
						date_string3=None
						date_string4=None
						if line[2] != '':
							a2 = int(float(line[2]))
							a2_as_datetime = datetime(*xlrd.xldate_as_tuple(a2, workbook.datemode))
							date_string2 = a2_as_datetime.date().strftime('%Y-%m-%d')
						if line[3] != '':
							a3 = int(float(line[3]))
							a3_as_datetime = datetime(*xlrd.xldate_as_tuple(a3, workbook.datemode))
							date_string3 = a3_as_datetime.date().strftime('%Y-%m-%d')
						if line[4] != '':
							a4 = int(float(line[4]))
							a4_as_datetime = datetime(*xlrd.xldate_as_tuple(a4, workbook.datemode))
							date_string4 = a4_as_datetime.date().strftime('%Y-%m-%d')
						requisition.create({
							'vendor_id':partner_id.id,
							'date_end':date_string2,
							'ordering_date':date_string3,
							'schedule_date':date_string4,
							# 'origin':line[5],
							'num_import_requisiton':line[0],
							'currency_id': moneda.id
						})
						cabecera = requisition.search([('num_import_requisiton','=',line[0])])
						# CREANDO LINEAS
						# date_string10=None
						# if line[10] != '':
						# 	a10 = int(float(line[10]))
						# 	a10_as_datetime = datetime(*xlrd.xldate_as_tuple(a10, workbook.datemode))
						# 	date_string10 = a10_as_datetime.date().strftime('%Y-%m-%d')
						producto_id = self.env['product.template'].search([('default_code','=',line[5])])
						if not producto_id:
							raise UserError((u'No existe el siguiente producto: "%s"') % (line[5]))
						line2 = self.env['purchase.requisition.line'].create({
							'requisition_id': cabecera.id,
							'product_id':producto_id.id,
							'product_description_variants':line[6],
							'product_qty':line[7],
							# 'qty_ordered':line[9],
							# 'schedule_date':date_string10,
							'price_unit':line[8],
							'account_analytic_id':cuenta.id
						})
						# cabecera.update({
						# 	'line_ids': (4,0, line2.id)
						# })

				else:
					raise UserError(_("Una de las lineas excede de los 10 campos!"))

		return self.env['popup.it'].get_message(u'SE ACTUALIZO CON EXITO LOS REQUERIMIENTOS DE COMPRA.')

	def find_product(self, ref):
		product_obj = self.env['product.template']
		product_search = product_obj.search([('default_code', '=', str(ref))],limit=1)
		if product_search:
			return product_search
		else:
			# just try with 0 before
			product_search = product_obj.search([('default_code', '=', '0'+str(ref))],limit=1)
			if product_search:
				return product_search
			else:
				# just try with 00 before
				product_search = product_obj.search([('default_code', '=', '00'+str(ref))],limit=1)
				if product_search:
					return product_search
				else:
					raise UserError((u'Código de producto no encontrado "%s"') % ref)

	def find_currency(self, moneda):
		currency_obj = self.env['res.currency']
		currency_search = currency_obj.search([('name', '=', moneda)],limit=1)
		if currency_search:
			return currency_search
		else:
			raise UserError((u'La moneda indicada no se ha encontrado'))


	def download_template(self):
		return {
			 'type' : 'ir.actions.act_url',
			 'url': '/web/binary/download_template_import_requisition',
			 'target': 'new',
			 }
