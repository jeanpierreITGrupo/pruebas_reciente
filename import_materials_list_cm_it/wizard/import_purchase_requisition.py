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
	_name = 'import.materials'

	document_file = fields.Binary(string='Excel')
	name_file = fields.Char(string='Nombre de Archivo')
	currency_id = fields.Many2one('res.currency', related='pricelist_id.currency_id')
	pricelist_id = fields.Many2one('product.pricelist','Lista de precios')

	def import_marterials(self):
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
				list_materials = self.env['mrp.bom']
				line = list(map(lambda row:isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value), sheet1.row(row_no)))
				if len(line) == 15:
					nro_list_materials = self.env['mrp.bom'].search([('code','=',line[0])])
					producto = self.env['product.template'].search([('default_code','=',line[2])])
					producto_name = self.env['product.template'].search([('name','=',line[1])])

					if nro_list_materials:
						print('REF SI',line[0])
						### YA EXISTE ACUERDO, NO SE CREA CABECERA ###
						# CREANDO LINEAS
						if line[6] != '' and line[7] != '' and line[8] != '' and line[10] != '':
							cabecera = list_materials.search([('code','=',line[0])])
							# CREANDO LINEAS COMPONENTE
							producto_id = self.env['product.template'].search([('default_code','=',line[7])])
							if not producto_id:
								raise UserError((u'En el componente, no existe el siguiente producto: "%s"') % (line[7]))
							product_uom_id = self.env['uom.uom'].search([('name','=',line[9])])
							if not product_uom_id:
								raise UserError((u'En el componente, no existe la siguiente Unidad de Medida: "%s"') % (line[9]))
							stage_id = self.env['stage.mrpline'].search([('name','=',line[10])])
							if not stage_id:
								raise UserError((u'En el componente, no existe la siguiente Etapa: "%s"') % (line[10]))
							line_componente = self.env['mrp.bom.line'].create({
								'bom_id': cabecera.id,
								'product_id':producto_id.id,
								'product_qty':line[8],
								'product_uom_id': product_uom_id.id,
								'stage_id': stage_id.id
							})
						if line[11] != '' and line[12] != '' and line[13] != '' and line[14] != '':
							# CREANDO LINEAS SUBPRODUCTO
							producto_id = self.env['product.template'].search([('default_code','=',line[12])])
							if not producto_id:
								raise UserError((u'En el subproducto, no existe el siguiente producto: "%s"') % (line[12]))
							product_uom_id = self.env['uom.uom'].search([('name','=',line[14])])
							if not product_uom_id:
								raise UserError((u'En el subproducto, no existe la siguiente Unidad de Medida: "%s"') % (line[14]))
							line_subproducto = self.env['mrp.bom.byproduct'].create({
								'bom_id': cabecera.id,
								'product_id':producto_id.id,
								'product_qty':line[13],
								'product_uom_id': product_uom_id.id
							})
					else:
						print('REF NO',line[0])
						### NO EXISTE ACUERDO, SE CREA CABECERA ###
						# CREACION DE CABECERA
						if not producto and not producto_name:							
							raise UserError((u'No se puede crear una lista sin producto principal. Producto: "%s"') % (line[1]))
						producto_search = False
						if producto:
							producto_search = producto
						else:
							producto_search = producto_name
						product_uom_cabe_id = self.env['uom.uom'].search([('name','=',line[4])])
						
						if not product_uom_cabe_id:
							raise UserError((u'No existe la siguiente Unidad de Medida: "%s"') % (line[4]))
						list_materials.create({
							'code': line[0],
							'product_tmpl_id':producto_search.id,
							'product_qty':line[3],
							'product_uom_id': product_uom_cabe_id.id,
							'type':line[5]
						})
						cabecera = list_materials.search([('code','=',line[0])])
						if line[6] != '' and line[7] != '' and line[8] != '' and line[10] != '':
							# CREANDO LINEAS COMPONENTE
							producto_id = self.env['product.template'].search([('default_code','=',line[7])])
							if not producto_id:
								raise UserError((u'En el componente, no existe el siguiente producto: "%s"') % (line[7]))
							product_uom_id = self.env['uom.uom'].search([('name','=',line[9])])
							if not product_uom_id:
								raise UserError((u'En el componente, no existe la siguiente Unidad de Medida: "%s"') % (line[9]))
							stage_id = self.env['stage.mrpline'].search([('name','=',line[10])])
							if not stage_id:
								raise UserError((u'En el componente, no existe la siguiente Etapa: "%s"') % (line[10]))
							line_componente = self.env['mrp.bom.line'].create({
								'bom_id': cabecera.id,
								'product_id':producto_id.id,
								'product_qty':line[8],
								'product_uom_id': product_uom_id.id,
								'stage_id': stage_id.id
							})
						if line[11] != '' and line[12] != '' and line[13] != '' and line[14] != '':
							# CREANDO LINEAS SUBPRODUCTO
							producto_id = self.env['product.template'].search([('default_code','=',line[12])])
							if not producto_id:
								raise UserError((u'En el subproducto, no existe el siguiente producto: "%s"') % (line[12]))
							product_uom_id = self.env['uom.uom'].search([('name','=',line[14])])
							if not product_uom_id:
								raise UserError((u'En el subproducto, no existe la siguiente Unidad de Medida: "%s"') % (line[14]))
							line_subproducto = self.env['mrp.bom.byproduct'].create({
								'bom_id': cabecera.id,
								'product_id':producto_id.id,
								'product_qty':line[13],
								'product_uom_id': product_uom_id.id
							})
						

				else:
					raise UserError(_("Una de las lineas excede de los 15 campos!"))

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
			 'url': '/web/binary/download_template_import_materials',
			 'target': 'new',
			 }


class mrpBomDigitsIT(models.Model):
	_inherit = 'mrp.bom.line'

	product_qty = fields.Float(digits=(12, 3))