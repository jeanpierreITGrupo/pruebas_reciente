# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools import float_compare
import pytz
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
import urllib.parse
import requests
import json

class ResCurrency(models.Model):
	_inherit = "res.currency"
	
	@api.model
	def _action_sunat_exchange_rate(self):
		rate_obj = self.env['res.currency.rate']
		currency = self.env.ref('base.USD')
		rate_date = fields.Datetime.now().replace(tzinfo=pytz.UTC).astimezone(pytz.timezone(self.env.user.tz or 'UTC'))
		print(rate_date)
		url = 'https://itgrupo.net/api/webservice/currencyratetoday'
		params = {'UserName' : 'APIUserGOLDtc',
				  'Password': 'Api$pass&241G13nd4TC',
				  'Date': rate_date.strftime('%Y/%m/%d')}

		try:
			r = requests.post(url, params=params)
			arre = r.text.replace("'",'"')
			arr2 = json.loads(arre)

			if currency:
				rate_search = rate_obj.search([
							('name', '=', self.date),
							('currency_id', '=', currency.id),
							('company_id','=',self.env.company.id)
						],limit=1)

				if rate_search:
					rate_search.write({
						'rate': arr2['rate'],
						'sale_type': arr2['sale_type'],
						'purchase_type': arr2['purchase_type'],
					})
				else:
					rate_obj.create({
						'currency_id': currency.id,
						'rate': arr2['rate'],
						'name': self.date,
						'sale_type': arr2['sale_type'],
						'purchase_type': arr2['purchase_type'],
						'company_id': self.env.company.id
					})

				return self.env['popup.it'].get_message(u'SE ACTUALIZÓ CORRECTAMENTE EL TC PARA EL DIA %s'%(self.date.strftime('%Y/%m/%d')))
		
		except Exception as err:
			raise UserError(err)

		#####################################33
		url = 'https://api.apis.net.pe/v1/tipo-cambio-sunat'
		try:
			res_html = urllib.request.urlopen(url)
			html = BeautifulSoup(res_html, "lxml")
			p = html.find("p")
			arr2 = json.loads(p.text.strip())
			currency = self.env.ref('base.USD')
			if arr2:
				values = {
					'compra': float(arr2["compra"]),
					'venta': float(arr2["venta"]),
				}
				rate_date = fields.Datetime.now().replace(tzinfo=pytz.UTC).astimezone(pytz.timezone(self.env.user.tz or 'UTC'))
				currency_rate = self.env['res.currency.rate']
				for cmpny in self.env['res.company'].search([]):
					rate = currency_rate.search([
						('currency_id', '=', currency.id),
						('name', '=', rate_date.date()),
						('company_id','=',cmpny.id)
					], limit=1)
					if not rate:
						currency_rate.create({
							'currency_id': currency.id,
							'rate': 1.0 / values['venta'],
							'name': rate_date,
							'sale_type': values['venta'],
							'purchase_type': values['compra'],
							'company_id': cmpny.id,
						})
					else:
						rate.write({
							'rate': 1.0 / values['venta'],
							'sale_type': values['venta'],
							'purchase_type': values['compra'],
						})
		except urllib.error.HTTPError as e:
			print('Error: %s' % e)
		except urllib.error.URLError as a:
			print('Error: %s' % a)
			
class ResCurrencyRate(models.Model):
	_inherit = "res.currency.rate"

	@api.onchange('sale_type')
	def _update_currency(self):
		for i in self:
			if i.sale_type:
				i.rate = 1/i.sale_type