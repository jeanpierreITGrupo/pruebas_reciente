# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import content_disposition
import base64
import os, os.path
import csv
from os import listdir
import sys

class Download_xls_requisition_materials(http.Controller):
	
	@http.route('/web/binary/download_template_import_materials', type='http', auth="public")
	def download_template_import_materials(self, **kw):

		materials_xls = request.env['ir.attachment'].sudo().search([('name','=','materials_template.xlsx')])
		filecontent = materials_xls.datas
		filename = 'Formato de Lista de Materiales.xls'
		filecontent = base64.b64decode(filecontent)
			

		return request.make_response(filecontent,
			[('Content-Type', 'application/octet-stream'),
			('Content-Disposition', content_disposition(filename))])