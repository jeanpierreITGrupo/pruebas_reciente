# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import content_disposition
import base64
import os, os.path
import csv
from os import listdir
import sys

class Download_xls_requisition(http.Controller):
	
	@http.route('/web/binary/download_template_import_requisition', type='http', auth="public")
	def download_template_import_requisition(self, **kw):

		invoice_xls = request.env['ir.attachment'].sudo().search([('name','=','requisition_template.xlsx')])
		filecontent = invoice_xls.datas
		filename = 'Formato de Requerimientos de Compra.xlsx'
		filecontent = base64.b64decode(filecontent)
			

		return request.make_response(filecontent,
			[('Content-Type', 'application/octet-stream'),
			('Content-Disposition', content_disposition(filename))])